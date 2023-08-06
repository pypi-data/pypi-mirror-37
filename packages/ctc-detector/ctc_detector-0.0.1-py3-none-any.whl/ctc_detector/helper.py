import os
import json
import numpy as np
import pandas as pd


def image_picker(root, path, channel='DAPI', failback=None):
    ext = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    path = os.path.join(root, path, 'images')
    if not os.path.exists(path):
        return
    files = [f for f in os.listdir(path) if f.endswith(ext)]
    files.sort()
    def _isin(sub, default=None):
        assert isinstance(sub, list)
        for fn in files:
            if any(s in fn for s in sub):
                return fn
        return default
    def _r(fn):
        if not fn:
            return
        if isinstance(fn, list):
            return [os.path.join(path, f) for f in fn]
        return os.path.join(path, fn)
    rule = json.loads(config.get('channels', channel))
    assert isinstance(rule, list)
    if isinstance(rule[0], list):
        # nested rule
        fn = []
        for x in rule:
            fn.append(_isin(x))
        if not fn.count(None):
            return _r(fn)
    else:
        fn = _isin(rule)
        if fn is not None:
            return _r(fn)
    # no matched filename, check failback
    if isinstance(failback, str):
        return image_picker(root, path, failback)
    elif isinstance(failback, int):
        return _r(files[failback])
    return


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


def get_nuclei_array(cav_path, json_path, shape):
    df = pd.read_csv(csv_path, index_col=0, names=['ImageId', 'EncodedPixels'], delimiter=',', skiprows=1)
    try:
        with open(json_path) as f:
            data = json.load(f)
    except EnvironmentError:
        data = {}
    mask_ids = data.get('ctc', [])
    mask_ids[:] = [x for x in mask_ids if x != 'ctc'] #TODO: current artifacts, to be removed later
    nuclei = np.zeros(shape, dtype=np.uint16)
    for i, mask in enumerate(mask_ids):
        print(i+1, mask)
        rle = df.loc[mask, 'EncodedPixels']
        print(rle)
        obj = rle_decode(1+1, rle, shape) # 1-based label
        nuclei = np.maximum(nuclei, obj)
    return nuclei     