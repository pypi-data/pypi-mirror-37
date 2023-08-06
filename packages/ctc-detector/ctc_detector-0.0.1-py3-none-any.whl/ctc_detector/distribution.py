import os
import glob
import re
import shutil
import tempfile
import itertools
import unittest
from copy import copy
from collections import defaultdict
import numpy as np
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import RandomSampler, SubsetRandomSampler, WeightedRandomSampler
from .config import config

_anchor_ = 'images'

class DistributionPolicyDataset(Dataset):
    def __init__(self, root, policy=None):
        self.root = root
        self.samples = self.__getall__(root)
        self.policy = policy if policy else config['dataset'].get('distribution_policy')

    def __getall__(self, root):
        samples = []
        # traverse root folder
        for s in glob.iglob(os.path.join(root, '**', _anchor_), recursive=True):
            # remove prefix and suffix
            s = re.sub(r'{}/|/{}$'.format(root, _anchor_), '', s)
            samples.append(s)
        samples.sort()
        return samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

    def split(self):
        ''' return CV split dataset object '''
        cv_ratio = config['dataset'].getfloat('cv_ratio')
        cv_seed = config['dataset'].getint('cv_seed')
        train, valid = [], []
        def keyfunc(s):
            s = s.split('/')
            return '' if len(s) == 1 else s[0]
        for k, v in itertools.groupby(self.samples, key=keyfunc):
            tr, cv = train_test_split(list(v), test_size=cv_ratio, random_state=cv_seed)
            train += tr
            valid += cv
        train_dataset = copy(self)
        valid_dataset = copy(self)
        train_dataset.samples = train
        valid_dataset.samples = valid
        valid_dataset.policy = 'Once' # CV samples always hit once
        return train_dataset, valid_dataset

    def sampler(self):
        ''' return sampler to control distribution '''
        if self.policy == 'Once':
            return RandomSampler(self)

        elif self.policy == 'Over':
            index = []
            for i, s in enumerate(self.samples):
                s = s.split('/')
                g = '' if len(s) == 1 else s[0]
                m = re.match(r'.*\.x(\d+)$', g)
                if m:
                    c = int(m.group(1))
                    index += [i] * c
                else:
                    index.append(i)
            return SubsetRandomSampler(index)

        elif self.policy == 'Amen':
            # count groups
            count = defaultdict(int)
            for s in self.samples:
                s = s.split('/')
                g = '' if len(s) == 1 else s[0]
                count[g] += 1
            # get weight for each samples
            weight = []
            for s in self.samples:
                s = s.split('/')
                g = '' if len(s) == 1 else s[0]
                weight.append( 1. / count[g] )
            # oversample amount to balance distribution
            c = list(count.values())
            ratio = np.max(c) / np.mean(c)
            num_samples = int( len(self.samples) * ratio )
            return WeightedRandomSampler(weight, num_samples)

        elif self.policy == 'Even':
            # count groups
            count = defaultdict(int)
            for s in self.samples:
                s = s.split('/')
                g = '' if len(s) == 1 else s[0]
                count[g] += 1
            # get weight for each samples
            weight = []
            for s in self.samples:
                s = s.split('/')
                g = '' if len(s) == 1 else s[0]
                w = 1. / count[g]
                m = re.match(r'.*\.x(\d+)$', g)
                if m:
                    w *= int(m.group(1))
                weight.append(w)
            num_samples = len(self.samples)
            return WeightedRandomSampler(weight, num_samples)

        else:
            raise TypeError('unknown policy: ' + policy)

class DistributionPolicyTest(unittest.TestCase):
    # syntax: { 'subfolder name' : # samples }
    data = {'group': 4, 'group.x1': 5, 'group.x2': 2, 'group.x5': 1}

    def setUp(self):
        # prepare temp folder as root in each test case
        self.root = tempfile.mkdtemp()
        for k in DistributionPolicyTest.data:
            for i in range(DistributionPolicyTest.data[k]):
                path = os.path.join(self.root, k, "%03d" % i, _anchor_)
                os.makedirs(path)
    
    def tearDown(self):
        shutil.rmtree(self.root)

    def test_once(self):
        ds = DistributionPolicyDataset(self.root, 'Once')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertGreater(len(visit), 0)
        self.assertEqual(len(visit), len(ds))
        self.assertEqual(len(np.unique(visit)), len(ds))

    def test_over(self):
        ds = DistributionPolicyDataset(self.root, 'Over')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertGreater(len(visit), 0)
        self.assertEqual(len(visit), 4 + 5 + 2*2 + 5*1 )
        self.assertEqual(len(np.unique(visit)), len(ds))

    def test_amen(self):
        ds = DistributionPolicyDataset(self.root, 'Amen')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertGreater(len(visit), 0)
        self.assertEqual(len(visit), 5*4 )
        # count groups
        count = defaultdict(int)
        for s in visit:
            g = s.split('/')[0]
            count[g] += 1
        c = list(count.values())
        self.assertEqual( np.mean(c), 5.0 )

    def test_even(self):
        ds = DistributionPolicyDataset(self.root, 'Even')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertGreater(len(visit), 0)
        self.assertEqual(len(visit), len(ds) )
        # count groups
        count = defaultdict(int)
        for s in visit:
            g = s.split('/')[0]
            count[g] += 1
        c = list(count.values())
        self.assertGreaterEqual( np.mean(c), len(ds) / np.mean([4, 5, 2*2, 5*1]) )

    def test_split(self):
        ds = DistributionPolicyDataset(self.root, 'Once')
        tr, cv = ds.split()
        self.assertGreater(len(ds), 0)
        self.assertGreater(len(tr), 0)
        self.assertGreater(len(cv), 0)
        self.assertEqual(len(tr) + len(cv), len(ds))

class SimpleDatasetTest(unittest.TestCase):
    def setUp(self):
        # prepare temp folder as root in each test case
        self.root = tempfile.mkdtemp()
        for i in range(20):
            path = os.path.join(self.root, "%03d" % i, _anchor_)
            os.makedirs(path)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_once(self):
        ds = DistributionPolicyDataset(self.root, 'Once')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertGreater(len(visit), 0)
        self.assertEqual(len(visit), len(ds))
        self.assertEqual(len(np.unique(visit)), len(ds))

    def test_over(self):
        ds = DistributionPolicyDataset(self.root, 'Over')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertGreater(len(visit), 0)
        self.assertEqual(len(visit), len(ds))
        self.assertEqual(len(np.unique(visit)), len(ds))

    def test_split(self):
        ds = DistributionPolicyDataset(self.root, 'Once')
        tr, cv = ds.split()
        self.assertGreater(len(ds), 0)
        self.assertEqual(len(tr) + len(cv), len(ds))
        self.assertEqual(len(tr), len(ds) * 0.9) 
        self.assertEqual(len(cv), len(ds) * 0.1)

class EmptyDatasetTest(unittest.TestCase):
    def test_invalid_folder(self):
        ds = DistributionPolicyDataset('/tmp/no_such_folder', 'Once')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertEqual(len(visit), 0)

    def test_empty_folder(self):
        root = tempfile.mkdtemp()
        ds = DistributionPolicyDataset(root, 'Once')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertEqual(len(visit), 0)
        shutil.rmtree(root)

    def test_noanchor_folder(self):
        root = tempfile.mkdtemp()
        for i in range(3):
            path = os.path.join(root, "%03d" % i)
            os.makedirs(path)
        ds = DistributionPolicyDataset(root, 'Once')
        loader = DataLoader(ds, batch_size = 5, sampler = ds.sampler())
        visit = []
        for x in loader:
            visit += x
        self.assertEqual(len(visit), 0)
        shutil.rmtree(root)

if __name__ == '__main__':
    unittest.main()
