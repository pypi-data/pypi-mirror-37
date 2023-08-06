import numpy as np
from PIL import Image
import os
import csv
import time
import unittest
import json
from skimage import img_as_ubyte
from skimage.measure import find_contours, approximate_polygon
from skimage.exposure import equalize_adapthist
import warnings
warnings.filterwarnings('ignore')
from .config import config

def timeit(method):
    ''' as decorator ''' 
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

def timef(method, *args, **kw):
    ''' as helper function '''
    ts = time.time()
    result = method(*args, **kw)
    te = time.time()
    print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
    return result

def rle_encode(x):
    '''
    x: numpy array of shape (height, width), 1 - mask, 0 - background
    Returns run length as list
    '''
    dots = np.where(x.T.flatten()==1)[0] # .T sets Fortran order down-then-right
    run_lengths = []
    prev = -2
    for b in dots:
        if (b>prev+1): run_lengths.extend((b+1, 0))
        run_lengths[-1] += 1
        prev = b
    return ' '.join([str(i) for i in run_lengths])

def rle_decode(mask_rle, shape, fill=True):
    '''
    mask_rle: run-length as string formated (start length)
    shape: (height,width) of array to return 
    Returns numpy array, 1 - mask, 0 - background
    '''
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=bool) #np.uint8)
    for lo, hi in zip(starts, ends):
        if fill:
            img[lo:hi] = 1
        else:
            img[lo] = img[hi-1] = 1
    return img.reshape(shape, order='F')

def rle_contour(mask_rle, shape):
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths - 1
    pix = set()
    for p in np.append(starts, ends):
        y = p % shape[0]
        x = p // shape[0]
        pix.add((y, x))
    return pix

def save_rle(input_path):
    mask_path = os.path.join(input_path, 'masks')
    if not os.path.exists(mask_path):
        return
    masks = [f for f in os.listdir(mask_path) if f.endswith('.png')]
    masks.sort()
    mask_csv = os.path.join(input_path, 'mask.csv')
    with open(mask_csv, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['ImageId', 'EncodedPixels'])
        for m in masks:
            img = Image.open(os.path.join(mask_path, m))
            # = np.array(img.getdata(), dtype=np.uint8).reshape(img.size[::-1])
            x = np.asarray(img, dtype=bool)
            #x = x // 255
            rle = rle_encode(x)
            writer.writerow([os.path.splitext(m)[0], rle])

def load_rle_contour(input_path, shape, centroid=None):
    return [c for m, c in iter_contour(input_path, shape, centroid)]

def iter_contour(input_path, shape, centroid=None):
    mask_csv = os.path.join(input_path, 'mask.csv')
    if not os.path.exists(mask_csv):
        save_rle(input_path)
    if not os.path.exists(mask_csv):
        return
    with open(mask_csv) as fp:
        reader = csv.reader(fp)
        next(reader) # skip header
        for row in reader:
            m, rle = row
            p = rle_contour(rle, shape)
            if len(p) == 0:
                continue
            c = np.array(list(polygon_sort(p)))
            y, x = np.mean(c, axis=0, dtype=int) # center of polygon
            dist = 0
            if centroid is not None:
                centroid = np.asarray(centroid)
                dist = np.sqrt((centroid[:, 0] - y)**2 + (centroid[:, 1] - x)**2)
            if np.any(dist <= 150):
                yield m, c
            else:
                continue

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    mask = dist_from_center <= radius
    return mask

def centroid_mask(shape, centroid):
    if centroid is None:
        return np.full(shape, True)
    mask = np.full(shape, False)
    h, w = shape
    for c in centroid:
        c = c[::-1] # reverse order
        m = create_circular_mask(h, w, c, 150) # limit scope
        mask = np.logical_or(mask, m)
    return mask

def skimage_contour(input_path):
    masks = [f for f in os.listdir(input_path) if f.endswith('.png')]
    masks.sort()
    for m in masks:
        img = Image.open(os.path.join(input_path, m))
        x = np.asarray(img, dtype=bool)
        contour = find_contours(x, 0.9)[0]

def cv2_contour(input_path):
    import cv2
    masks = [f for f in os.listdir(input_path) if f.endswith('.png')]
    masks.sort()
    for m in masks:
        img = cv2.imread(os.path.join(input_path, m), cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(img,127,255,0)
        _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

def polygon_sort(corners):
    n = len(corners)
    cx = float(sum(x for x, y in corners)) / n
    cy = float(sum(y for x, y in corners)) / n
    cornersWithAngles = []
    for x, y in corners:
        an = (np.arctan2(y - cy, x - cx) + 2.0 * np.pi) % (2.0 * np.pi)
        cornersWithAngles.append((x, y, an))
    cornersWithAngles.sort(key = lambda tup: tup[2])
    return map(lambda p: (p[0], p[1]), cornersWithAngles)

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

def clahe(x):
    '''
    return PIL image or numpy array
    '''
    is_pil = isinstance(x, Image.Image)
    if is_pil:
        x = np.asarray(x, dtype=np.uint8)
    x = equalize_adapthist(x, clip_limit=0.05)
    x = img_as_ubyte(x)
    if is_pil:
        x = Image.fromarray(x)
    return x

def save_contour(input_path, shape):
    mask_path = os.path.join(input_path, 'masks')
    mask_csv = os.path.join(input_path, 'mask.csv')
    contour_csv = os.path.join(input_path, 'contour.json')
    if not os.path.exists(mask_csv) and not os.path.exists(mask_path):
        return
    if not os.path.exists(mask_csv):
        save_rle(input_path)
    with open(mask_csv) as fp:
        reader = csv.reader(fp)
        next(reader) # skip header
        contours = {}
        for row in reader:
            m, rle = row
            p = rle_contour(rle, shape)
            c = np.array(list(polygon_sort(p)))
            c = approximate_polygon(c, 0.02)
            contours[m] = c.tolist()
    with open(contour_csv, 'w') as fp:
        json.dump(contours, fp)

def iter_contour_v2(input_path, shape, centroid=None):
    contour_csv = os.path.join(input_path, 'contour.json')
    if not os.path.exists(contour_csv):
        save_contour(input_path, shape)
    with open(contour_csv) as f:
        contours = json.load(f)
    for m in contours:
        c = contours[m]
        y, x = np.mean(c, axis=0, dtype=int) # center of polygon
        dist = 0
        if centroid is not None:
            centroid = np.asarray(centroid)
            dist = np.sqrt((centroid[:, 0] - y)**2 + (centroid[:, 1] - x)**2)
        if np.any(dist <= 150):
            yield m, c
        else:
            continue

class FunctionTest(unittest.TestCase):
    def test_rle_convert(self):
        def random_test():
            data = np.random.randint(0,2,(100,100))
            seq = rle_encode(data)
            data_ = rle_decode(seq, data.shape)
            np.testing.assert_allclose(data, data_)
        random_test()

    def test_polygon_sort(self):
        a = np.array([
            [0, 1, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        c = [(2, 2), (1, 3), (0, 2), (0, 1), (1, 1), (2, 1)]
        b = list(polygon_sort(list(zip(*np.nonzero(a)))))
        np.testing.assert_allclose(b, c)

class BenchmarkTest(unittest.TestCase):
    def test(self):
        uid = '2018-01-30/1_3'
        input_path = 'data/nina/{}'.format(uid)
        image_path = 'data/nina/{}/images/1_3_DAPI.png'.format(uid, uid)
        centroid = [[6, 1459], [617, 364], [634, 2040], [767, 1411], [1804, 589], [1893, 523], [2109, 1967]]
        img = Image.open(image_path)
        shape = img.size[::-1]
        print('Image shape is', shape)
        #timef(save_rle, mask_path)
        timef(save_contour, input_path, shape)
        timef(load_rle_contour, input_path, shape, centroid)
        #timef(cv2_contour, mask_path)
        #timef(skimage_contour, mask_path)

if __name__ == '__main__':
    unittest.main()
