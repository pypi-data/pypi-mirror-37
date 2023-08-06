import numpy as np
from PIL import Image
import os
import csv
import time
import unittest
import json

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
    from skimage.measure import find_contours
    import warnings
    warnings.filterwarnings('ignore')
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

def image_picker(root, path, mode='DAPI'):
    '''
    Image picker rule:
        DAPI mode :=
            #1: <- single file
            #2: <- filename w/ '_UV' or 'DAPI'
            #3: <- first file
        RGB mode :=
            #1: <- filename w/ 'RGB' substring
            #2: <- R: '_Blue-Red', '_Green', or '_Red'
                   G: '_Blue'
                   B: '_UV' or 'DAPI'
            #3: <- secondary file
            #4: <- first file
        EpCAM mode :=
            #1: <- '_Blue-Red', '_Green', '_Red', or 'EpCAM'
        CD45 mode :=
            #1: <- G: '_Blue', or 'CD45'
    '''
    ext = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    path = os.path.join(root, path, 'images')
    if not os.path.exists(path):
        return None
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
            return None
        if isinstance(fn, list):
            return [os.path.join(path, f) for f in fn]
        return os.path.join(path, fn)
    rule = {
        'DAPI' : ['_UV.', 'DAPI'],
        'EpCAM': ['_Blue-Red.', '_Green.', '_Red.', 'EpCAM'],
        'CD45':  ['_Blue.', 'CD45'],
    }
    if mode == 'DAPI':
        return _r(_isin(rule[mode], files[0]))
    elif mode == 'RGB':
        fn = _isin(['RGB'])
        if fn:
            return _r(fn)
        r, g, b = _isin(rule['EpCAM']), _isin(rule['CD45']), _isin(rule['DAPI'])
        if r is not None and g is not None and b is not None:
            return _r([r, g, b])
        return _r(files[len(files) > 1])
    else:
        return _r(_isin(rule[mode]))

def approximate_polygon(coords, tolerance):
    """Approximate a polygonal chain with the specified tolerance.
    It is based on the Douglas-Peucker algorithm.
    Note that the approximated polygon is always within the convex hull of the
    original polygon.
    Parameters
    ----------
    coords : (N, 2) array
        Coordinate array.
    tolerance : float
        Maximum distance from original points of polygon to approximated
        polygonal chain. If tolerance is 0, the original coordinate array
        is returned.
    Returns
    -------
    coords : (M, 2) array
        Approximated polygonal chain where M <= N.
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
    """
    if tolerance <= 0:
        return coords

    chain = np.zeros(coords.shape[0], 'bool')
    # pre-allocate distance array for all points
    dists = np.zeros(coords.shape[0])
    chain[0] = True
    chain[-1] = True
    pos_stack = [(0, chain.shape[0] - 1)]
    end_of_chain = False

    while not end_of_chain:
        start, end = pos_stack.pop()
        # determine properties of current line segment
        r0, c0 = coords[start, :]
        r1, c1 = coords[end, :]
        dr = r1 - r0
        dc = c1 - c0
        segment_angle = - np.arctan2(dr, dc)
        segment_dist = c0 * np.sin(segment_angle) + r0 * np.cos(segment_angle)

        # select points in-between line segment
        segment_coords = coords[start + 1:end, :]
        segment_dists = dists[start + 1:end]

        # check whether to take perpendicular or euclidean distance with
        # inner product of vectors

        # vectors from points -> start and end
        dr0 = segment_coords[:, 0] - r0
        dc0 = segment_coords[:, 1] - c0
        dr1 = segment_coords[:, 0] - r1
        dc1 = segment_coords[:, 1] - c1
        # vectors points -> start and end projected on start -> end vector
        projected_lengths0 = dr0 * dr + dc0 * dc
        projected_lengths1 = - dr1 * dr - dc1 * dc
        perp = np.logical_and(projected_lengths0 > 0,
                              projected_lengths1 > 0)
        eucl = np.logical_not(perp)
        segment_dists[perp] = np.abs(
            segment_coords[perp, 0] * np.cos(segment_angle)
            + segment_coords[perp, 1] * np.sin(segment_angle)
            - segment_dist
        )
        segment_dists[eucl] = np.minimum(
            # distance to start point
            np.sqrt(dc0[eucl] ** 2 + dr0[eucl] ** 2),
            # distance to end point
            np.sqrt(dc1[eucl] ** 2 + dr1[eucl] ** 2)
        )

        if np.any(segment_dists > tolerance):
            # select point with maximum distance to line
            new_end = start + np.argmax(segment_dists) + 1
            pos_stack.append((new_end, end))
            pos_stack.append((start, new_end))
            chain[new_end] = True

        if len(pos_stack) == 0:
            end_of_chain = True

    return coords[chain, :]

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
