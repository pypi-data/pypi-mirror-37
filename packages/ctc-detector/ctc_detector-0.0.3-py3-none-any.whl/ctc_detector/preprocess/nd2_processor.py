from nd2reader import ND2Reader
import numpy as np
import math
import os
import csv
import json
import argparse
from skimage.io import imread, imsave
from tqdm import tqdm



RADIUS = 7650
BACKGROUND_INTENSITY = 255

CENTROID_X_COLUMN = 13
CENTROID_Y_COLUMN = 14

def _round_int(number):
    return int(round(number))

def _str2int(text):
    return _round_int(float(text))

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

def read_raw_centroids(filename):
    with open(filename, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # rewind
        reader = csv.reader(csvfile, delimiter=',')
        if has_header:
            next(reader)  # skip header row
        # After experimented, the actual coordinates is confirmed to be (x, -y) instead of (x, y) in csv file
        centroids = [(_str2int(r[CENTROID_X_COLUMN]), -_str2int(r[CENTROID_Y_COLUMN]))
                     for r in reader if r[CENTROID_X_COLUMN] and r[CENTROID_Y_COLUMN]]
        return centroids

def read_raw_3points(filename):
    with open(filename, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # rewind
        reader = csv.reader(csvfile, delimiter=',')
        if has_header:
            next(reader)  # skip header row
        points = []
        for _ in range(3):
            row = next(reader)
            x, y = _str2int(row[CENTROID_X_COLUMN]), -_str2int(row[CENTROID_Y_COLUMN])
            points.append(complex(x, y))
        return points

# in complex coordinates
def define_circle(p1, p2, p3):
    w = p3 - p1
    w /= p2 - p1
    c = (p1 - p2) * (w - abs(w)**2) / 2j / w.imag - p1
    (x, y), radius = (_round_int(-c.real), _round_int(-c.imag)), _round_int(abs(c + p1))
    # print('(x%+.3f)^2+(y%+.3f)^2 = %.3f^2' % (c.real, c.imag, abs(c+p1)))
    return (x, y), radius

# centroid: (x, y) ; circle: ((x, y), radius)
def txf_nd2_centroids(raw_centroids, raw_circle, nd2_circle):
    ratio = nd2_circle[1] / raw_circle[1]
    # x_axis direction same in two coordinates, y_axis direction is opposite in two coordinates
    nd2_centroids = [ (_round_int(nd2_circle[0][0] + (c[0] - raw_circle[0][0]) * ratio),
                       _round_int(nd2_circle[0][1] - (c[1] - raw_circle[0][1]) * ratio)) for c in raw_centroids ]
    return nd2_centroids

def get_nd2_centroids(metafile_prefix, nd2_image):
    centroid_filename = f'{metafile_prefix} (Binary)-2.csv'
    anchor_filename = f'{metafile_prefix} (3-points).csv'
    h, w = nd2_image.metadata['height'], nd2_image.metadata['width']
    raw_circle = define_circle(*read_raw_3points(anchor_filename))
    nd2_circle = ((w // 2, h // 2), RADIUS)
    raw_centroids = read_raw_centroids(centroid_filename)
    nd2_centroids = txf_nd2_centroids(raw_centroids, raw_circle, nd2_circle)
    return nd2_centroids

def get_roi_images(nd2_image):
    h, w = nd2_image.metadata['height'], nd2_image.metadata['width']
    channels = len(nd2_image.metadata['channels'])
    roi_mask = create_circular_mask(h, w, radius=RADIUS)
    infr_image = r_img = g_img = b_img = np.zeros((h, w), dtype=np.uint8)
    r_img[~roi_mask] = BACKGROUND_INTENSITY
    for ch in range(channels):
        frame = nd2_image.get_frame_2D(c=ch)
        ch_name = nd2_image.metadata['channels'][ch]
        if ch_name == 'Penta-B':
            # process to have better nuclei inference
            infr_image = np.around(np.multiply(frame, 255./65535)).astype(np.uint8)
            infr_image[~roi_mask] = 0
            # process to have better visualization for human eyes
            b_img = bytescale(frame)
            b_img[~roi_mask] = BACKGROUND_INTENSITY
        elif ch_name == 'Penta-G':
            g_img = bytescale(frame)
            g_img[~roi_mask] = BACKGROUND_INTENSITY
        elif ch_name == 'Penta-R':
            r_img = bytescale(frame)
            r_img[~roi_mask] = BACKGROUND_INTENSITY
        else:
            raise ValueError('Unrecognized channels')

    view_image = np.stack([r_img, g_img, b_img], axis=2)
    return infr_image, view_image

# grids in (y, x) order
def process_nd2(nd2_file, grids, output_dir):
    fbase = os.path.splitext(nd2_file)[0] # drop postfix extension name
    with ND2Reader(nd2_file) as images:
        h, w = images.metadata['height'], images.metadata['width']
        nd2_centroids = get_nd2_centroids(fbase, images)
        infr_image, view_image = get_roi_images(images)

        crop_height, crop_width = h // grids[0], w // grids[1]
        rows_y, cols_x = math.ceil(h / crop_height), math.ceil(w / crop_width)
        fbase = os.path.basename(fbase) # drop prefix dir
        stats = np.zeros((rows_y, cols_x), dtype=np.uint8)
        for j in tqdm(range(rows_y)):
            for i in range(cols_x):
                cur_x, cur_y = i * crop_width, j * crop_height
                crop_view_img = view_image[cur_y : cur_y + crop_height, cur_x : cur_x + crop_width, :]
                crop_infr_img = infr_image[cur_y : cur_y + crop_height, cur_x : cur_x + crop_width]
                if np.max(crop_infr_img) > np.min(crop_infr_img):
                    file_idx = f'{j}_{i}'
                    # save rgb image & meta file for viewer
                    file_dir = os.path.join(output_dir, fbase, file_idx, 'images')
                    if not os.path.exists(file_dir):
                        os.makedirs(file_dir)
                    imsave(os.path.join(file_dir, f'{file_idx}_RGB.png'), crop_view_img)
                    targets = [[c[1] - cur_y, c[0] - cur_x] for c in nd2_centroids
                               if cur_x <= c[0] < cur_x + crop_width and
                                  cur_y <= c[1] < cur_y + crop_height] # in [y, x] order
                    if targets:
                        stats[j][i] = len(targets)
                        meta_file = os.path.join(output_dir, fbase, file_idx, 'meta.json')
                        with open(meta_file, "w") as f:
                            json.dump({"centroid": targets}, f)

                    # save B channel image for inference & viewer
                    imsave(os.path.join(file_dir, f'{file_idx}_DAPI.png'), crop_infr_img)

        stats_file = os.path.join(output_dir, fbase, 'meta.json')
        with open(stats_file, "w") as f:
            json.dump({"grid" : stats.tolist()}, f)


def entry_wrapper(nd2_path, grids, output_dir):
    if not os.path.exists(nd2_path):
        print(nd2_path + ' not exist')
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if grids is None:
        grids = (8, 8)
    print('Starting process ', nd2_path)
    process_nd2(nd2_path, grids, output_dir)
    print('Completed!')


def run(args=None):
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required named arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('--nd2_path', type=str, help='nd2 filepath', required=True)
    required.add_argument('--grids', nargs='+', type=int, help='specifiy partitioning grids, vertical first, horizontal second', required=False)
    required.add_argument('--output_dir', type=str, help='output directory of inference and viewer images', required=True)
    args = vars(parser.parse_args(args))
    entry_wrapper(args['nd2_path'], args['grids'], args['output_dir'])

if __name__ == '__main__':
    run()
