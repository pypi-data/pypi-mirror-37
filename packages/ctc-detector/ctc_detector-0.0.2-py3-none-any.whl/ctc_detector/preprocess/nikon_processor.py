import numpy as np
import math
import os
import csv
import json
import argparse
import re
from multiprocessing import Pool
from functools import partial
from skimage.io import imread, imsave
from tqdm import tqdm
from xlsx2csv import Xlsx2csv


"""
Input Directory Layout
.
└── group_1
     ├── sample_1
     │   ├── sample_1 (labels).csv
     │   ├── sample_1 (3 points).csv
     │   └── images
     │       ├──sample_1 (R).tif
     │       ├──sample_1 (G).tif
     │       └──sample_1 (B).tif
     ├── sample_2
     ├── sample_3
     └── ...


Output Directory Layout
.
└── group_1
    ├── sample_1
    │   ├── meta.json
    │   ├── 0_0 (e.g. grid index)
    │   │   ├── images
    │   │   │   ├── 0_0_DAPI.png
    │   │   │   ├── 0_0_EpCAM.png
    │   │   │   ├── 0_0_CD45.png
    │   │   │   └── 0_0_RGB.png
    │   │   └── meta.json
    │   ├── 0_1
    │   └── ...
    ├── sample_2
    ├── sample_3
    └── ...
"""

PRE_PROCESSING_WORKER_LIMIT = 10
BACKGROUND_INTENSITY = 255


def _round_int(number):
    return int(round(number))

def _str2int(text):
    return _round_int(float(text))

def _str2dec(text, digits=3):
    return round(float(text), digits)

#copy from scipy/misc/pilutil.py
def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    if data.dtype == np.uint8:
        return data
    if high > 255:
        raise ValueError("`high` should be less than or equal to 255.")
    if low < 0:
        raise ValueError("`low` should be greater than or equal to 0.")
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")
    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()
    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1
    scale = float(high - low) / cscale
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype(np.uint8)

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = [int(w / 2), int(h / 2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    return mask

# in pixel unit
def read_tiff_centroids(filename):
    if not os.path.exists(filename):
        xlsx = f'{os.path.splitext(filename)[0]}.xlsx'
        if not os.path.exists(xlsx):
            raise IOError(f'labels file {filename} NOT found!')
        else:
            Xlsx2csv(xlsx, outputencoding='utf-8').convert(filename)

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        centroids = [(_str2int(r['CentreXpx']), _str2int(r['CentreYpx']))
                     for r in reader if r and r['CentreXpx'] and r['CentreYpx']]
        return centroids


# in pixel unit
def read_tiff_3points(filename):
    if not os.path.exists(filename):
        xlsx = f'{os.path.splitext(filename)[0]}.xlsx'
        if not os.path.exists(xlsx):
            raise IOError(f'3 points file {filename} NOT found!')
        else:
            Xlsx2csv(xlsx, outputencoding='utf-8').convert(filename)

    with open(filename, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # rewind
        reader = csv.reader(csvfile, delimiter=',')
        if has_header:
            next(reader)  # skip header row
        points = [complex(_str2int(r[0]), _str2int(r[1])) for r in reader if r and r[0] and r[1]]
    return points[:3]


# in complex coordinates
def define_circle(p1, p2, p3):
    w = p3 - p1
    w /= p2 - p1
    c = (p1 - p2) * (w - abs(w)**2) / 2j / w.imag - p1
    (x, y), radius = (_round_int(-c.real), _round_int(-c.imag)), _round_int(abs(c + p1))
    # print('(x%+.3f)^2+(y%+.3f)^2 = %.3f^2' % (c.real, c.imag, abs(c+p1)))
    return (x, y), radius


def get_tiff_images(image_dir):
    ext = ['tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    files = [f for f in os.listdir(image_dir) if f.endswith(ext)]
    if not files:
        raise IOError('No TIFF image files found!')

    for i, f in enumerate(files):
        frame = imread(os.path.join(image_dir, f))
        if i == 0:
            h, w = frame.shape
            infr_image = r_img = g_img = b_img = np.zeros((h, w), dtype=np.uint8)

        fbase = os.path.splitext(f)[0] # drop postfix extension name
        match = re.search(r'[A-Za-z0-9 -]* \(([RrGgBb])\)', fbase)
        ch_name = match[1] if match else None
        if ch_name in ['B', 'b']: # Blue Channel
            # 'normalization' process to have better nuclei inference
            infr_image = np.around(np.multiply(frame, 255./65535)).astype(np.uint8)
            # 'bytescale' process to have better visualization for human eyes
            b_img = bytescale(frame)
        elif ch_name in ['G', 'g']: # Green Channel
            g_img = bytescale(frame)
        elif ch_name in ['R', 'r']: # Red Channel
            r_img = bytescale(frame)
        else:
            print(f'Ignoring unrecognized channel file {f}')

    rgb_image = np.stack([r_img, g_img, b_img], axis=2)
    return infr_image, r_img, g_img, rgb_image

# Parallelism refer to
# (1) https://stackoverflow.com/questions/7894791/use-numpy-array-in-shared-memory-for-multiprocessing
# (2) https://research.wmz.ninja/articles/2018/03/on-sharing-large-arrays-when-using-pythons-multiprocessing.html
# Used for
#   forking off ad-hoc child processes that each handle a snapshot of the parent process and then terminate, where
#   each child process does some costly computation on one slice of a matrix present in parent memory

# hold the implicitly mem-shared data (READ-ONLY)
infr_array = r_array = g_array = rgb_array = None

# grids in (y, x) order
def process_sample(sample_dir, grids, output_dir):
    global infr_array, r_array, g_array, rgb_array

    sample_id = os.path.basename(os.path.normpath(sample_dir)) # retrieve the last part of sample_dir
    centroid_file = os.path.join(sample_dir, f'{sample_id} (labels).csv')
    roi_file = os.path.join(sample_dir, f'{sample_id} (3 points).csv')

    # mask out area outside of region of interest
    tiff_centroids = read_tiff_centroids(centroid_file)
    tiff_roi_center, tiff_roi_radius = define_circle(*read_tiff_3points(roi_file))
    infr_image, r_image, g_image, rgb_image = get_tiff_images(os.path.join(sample_dir, 'images'))
    h, w = infr_image.shape
    roi_mask = create_circular_mask(h, w, center=tiff_roi_center, radius=tiff_roi_radius)
    infr_image[~roi_mask] = 0 # better for inference
    for img in [r_image, g_image, rgb_image]:
        img[~roi_mask] = BACKGROUND_INTENSITY
    infr_array, r_array, g_array, rgb_array = infr_image, r_image, g_image, rgb_image

    crop_height, crop_width = math.ceil(h / grids[0]), math.ceil(w / grids[1])
    rows_y, cols_x = math.ceil(h / crop_height), math.ceil(w / crop_width)
    stats = np.zeros((rows_y, cols_x), dtype=np.uint8)
    fovs = []
    for j in range(rows_y):
        for i in range(cols_x):
            fov_path = os.path.join(output_dir, sample_id, f'{j}_{i}')
            fovs.append((i, j, crop_width, crop_height, fov_path))

    for result in parallel_processing_with_progress(partial(collect_fov_job, centroids=tiff_centroids), fovs):
        idx_i, idx_j, count = result
        if count > 0:
            stats[idx_j][idx_i] = count

    stats_file = os.path.join(output_dir, sample_id, 'meta.json')
    with open(stats_file, "w") as f:
        json.dump({"grid" : stats.tolist()}, f)


def parallel_processing_with_progress(func, data):
    with Pool(PRE_PROCESSING_WORKER_LIMIT) as p:
        with tqdm(total=len(data)) as pbar:
            for result in tqdm(p.imap_unordered(func, data)):
                yield result
                pbar.update()

def collect_fov_job(region, centroids):
    i, j, w, h, fov_dir = region
    x, y = i * w, j * h
    rgb_img = rgb_array[y : y + h, x : x + w, :]
    infr_img = infr_array[y : y + h, x : x + w]
    r_img = r_array[y : y + h, x : x + w]
    g_img = g_array[y : y + h, x : x + w]
    if np.max(infr_img) > np.min(infr_img):
        img_dir = os.path.join(fov_dir, 'images')
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        imsave(os.path.join(img_dir, f'{j}_{i}_RGB.png'), rgb_img)
        imsave(os.path.join(img_dir, f'{j}_{i}_DAPI.png'), infr_img)
        imsave(os.path.join(img_dir, f'{j}_{i}_EpCAM.png'), r_img)
        imsave(os.path.join(img_dir, f'{j}_{i}_CD45.png'), g_img)
        targets = [[cy - y, cx - x] for cx, cy in centroids
                    if x <= cx < x + w and
                       y <= cy < y + h] # in [y, x] order
        if targets:
            meta_file = os.path.join(fov_dir, 'meta.json')
            with open(meta_file, "w") as f:
                json.dump({"centroid": targets}, f)
            return [i, j, len(targets)]
        else:
            return [i, j, 0]
    else:
        return [i, j, 0]


def entry_wrapper(input_dir, grids, output_dir):
    if not os.path.exists(input_dir):
        raise IOError(f'{input_dir} not exist!')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if grids is None:
        grids = (8, 8)

    samples = [os.path.join(input_dir, s) for s in os.listdir(input_dir)
              if os.path.isdir(os.path.join(input_dir, s))]
    print(f'Starting process input directory: {input_dir}')
    for sample in samples:
        print(f'Processing sample directory: {sample}')
        process_sample(sample, grids, output_dir)
    print('Completed!')


def run(args=None):
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('--input_dir', type=str, help='input directory of nikon tiff and labels', required=True)
    required.add_argument('--grids', nargs='+', type=int, help='specifiy partitioning grids, vertical first, horizontal second', required=False)
    required.add_argument('--output_dir', type=str, help='output directory of inference and viewer images', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['input_dir'], args['grids'], args['output_dir'])

if __name__ == '__main__':
    run()