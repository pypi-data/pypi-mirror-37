import numpy as np
import math
import os
import csv
import json
import argparse
import re
from skimage.io import imread
from multiprocessing import Pool
from tqdm import tqdm

PRE_PROCESSING_WORKER_LIMIT = 10

# modified from https://www.kaggle.com/paulorzp/run-length-encode-and-decode
# note: the rle encoding is in vertical direction per Kaggle competition rule 
def rle_decode(mask_id, mask_rle, shape):
    h, w = shape
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(h * w, dtype=np.uint16)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = mask_id
    return img.reshape((w, h)).T

def read_metadata(path):
    fp = os.path.join(path, 'meta.json')
    if not os.path.exists(fp):
        return {}
    with open(fp) as f:
        data = json.load(f)
        return data

def write_metadata(path, data):
    fp = os.path.join(path, 'meta.json')
    with open(fp, 'w') as f:
        json.dump(data, f)

def get_nucleus_array(csv_path, shape):
    with open(csv_path) as f:
        reader = csv.reader(f)
        next(reader) #skip header
        nucleus = np.zeros(shape, dtype=np.uint16)
        for mask_id, rle in reader:
            match = re.search(r'mask_([0-9]+)', mask_id)
            mask_id = match[1]
            obj = rle_decode(mask_id, rle, shape)
            nucleus = np.maximum(nucleus, obj)    
    return nucleus

def parallel_processing_with_progress(func, data):
    with Pool(PRE_PROCESSING_WORKER_LIMIT) as p:
        with tqdm(total=len(data)) as pbar:
            for result in tqdm(p.imap_unordered(func, data)):
                yield result
                pbar.update()

def match_nuclei(sample_dir):
    grids = next(os.walk(sample_dir))[1]  # immediate child directories
    grid_dirs = [os.path.join(sample_dir, idx) for idx in grids]
    for _ in parallel_processing_with_progress(match_grid_nuclei, grid_dirs): pass


def match_grid_nuclei(grid_dir):
    grid_id = os.path.basename(os.path.normpath(grid_dir)) # retrieve the last part of grid_dir
    img = imread(os.path.join(grid_dir, 'images', f'{grid_id}_DAPI.png'))
    h, w = img.shape
    metadata = read_metadata(grid_dir)
    if metadata:
        centroids = metadata['centroid'] if metadata else None
        nucleus = get_nucleus_array(os.path.join(grid_dir, 'mask.csv'), (h, w))
        # reconstruct all nucleus rles in a numpy array, label with individual mask_id
        target_mask = np.zeros((h, w)).astype(np.bool)
        for y, x in centroids:
            target_mask[y][x] = True
        result = np.where((nucleus > 0) & target_mask, nucleus, 0)
        rows, cols = np.nonzero(result)
        match_ids = result[rows, cols]
    
        mask_ids = ['ctc']
        for i in match_ids:
            mask_ids.append(f'mask_{i}')
        if len(mask_ids) > 1:
            metadata['ctc'] = mask_ids
            write_metadata(grid_dir, metadata)

def entry_wrapper(input_dir):
    if not os.path.exists(input_dir):
        raise IOError(f'{input_dir} not exist!')

    samples = [os.path.join(input_dir, s) for s in os.listdir(input_dir)
              if os.path.isdir(os.path.join(input_dir, s))]
    print(f'Starting process input directory: {input_dir}')
    for sample in samples:
        print(f'Processing sample directory: {sample}')
        match_nuclei(sample)
    print('Completed!')

def run(args=None):
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    required.add_argument('--input_dir', type=str, help='root directory of examples, which contain cropped images & metadata', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['input_dir'])

if __name__ == '__main__':
    run()