import os
import csv
import json
import zipfile
import argparse
import shutil
import math
from tqdm import tqdm
import numpy as np
import pandas as pd

def uid_to_yx(uid):
    id = int(uid) - 1 # 1 to 0 base
    chip = id // 64
    id = id % 64 # shift position
    x = id // 8
    y = id % 8
    if x % 2:
        # odd column, reverse y
        y = 7 - y
    return chip, y, x

def make_uid_path(root, sn, uid, subdir=''):
    chip, y, x = uid_to_yx(uid)
    dest = os.path.join(
        root, 
        '{}_{}'.format(sn, chip), 
        '{}_{}'.format(y, x), 
        subdir)
    os.makedirs(dest, exist_ok=True)
    return dest

def run(root, zips):
    ext = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    tmp = os.path.join(root, 'tmp')
    for src in tqdm(zips):
        sn = None
        n = 0
        with zipfile.ZipFile(src, 'r') as zf:
            # extract first
            for f in tqdm(zf.infolist(), desc='Extract'):
                zf.extract(f, tmp)

            # transform to correct path
            csvfile = ''
            for f in tqdm(zf.namelist(), desc='Transform'):
                src = os.path.join(tmp, f)
                # only move image files
                if f.endswith(ext):
                    # image file
                    if not sn:
                        sn = f.split(os.sep)[0]
                    assert sn == f.split(os.sep)[0]
                    uid = os.path.splitext(os.path.basename(f))[0].split('_')[0]
                    n = max(n, int(uid))
                    dest = make_uid_path(root, sn, uid, 'images')
                    shutil.move(src, dest)
                elif f.endswith('labels.csv'):
                    csvfile = src
                else:
                    # other files, ignore for now
                    pass

            # load metadata
            _n = math.ceil(n / 64) * 64 # align to 8x8 grid
            grid = np.zeros(_n, dtype=int).reshape(-1, 8, 8)
            if os.path.exists(csvfile):
                df = pd.read_csv(csvfile, usecols=['fov_index','x','y','class'])
                df.dropna(subset=['class'], inplace=True) # filter out NaN label rows
                for uid in tqdm(range(1, n+1), desc='Load'):
                    chip, y, x = uid_to_yx(uid)
                    dest = make_uid_path(root, sn, uid)
                    centroid = df.loc[df['fov_index'] == uid].filter(items=['y','x','class']).values.tolist()
                    grid[chip, y, x] = len(centroid)
                    if len(centroid):
                        with open(os.path.join(dest, 'meta.json'), 'w') as f:
                            json.dump({'centroid': centroid}, f)
            else:
                print('Warning: no label files')
            for i, chip in enumerate(grid):
                fp = os.path.join(root, '{}_{}'.format(sn, i), 'meta.json')
                with open(fp, 'w') as f:
                    json.dump({'grid': chip.tolist()}, f)

            # clean up tmp
            shutil.rmtree(tmp)

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='etl_zip'
    )
    parser.add_argument('zipfile', nargs='+', type=str, help='zip filepath')
    parser.add_argument('--dest', type=str, help='subfolder to extract')
    parser.set_defaults(dest='test')
    args = parser.parse_args(args)

    dataset_path = 'data'
    root = os.path.join(dataset_path, args.dest)
    assert os.path.exists(dataset_path)
    assert os.path.exists(root)
    run(root, args.zipfile)
