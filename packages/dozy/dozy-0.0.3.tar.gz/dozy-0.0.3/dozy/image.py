""" image module of dozy. """
import glob
import os

import cv2
import numpy as np

from . import utils


def save(save_path, img):
    """ Save an image.
    Args:
        save_path (str): where to save the image. must have extension.
        img (np.ndarray): an image has shape [h, w, c] or [h, w]

    Returns:
        return True if save successfully else False
    """
    assert isinstance(save_path, str), 'save_path must be a str'
    utils.complaint_dir_absence(os.path.dirname(save_path))

    res = cv2.imwrite(save_path, img)

    if res is None:
        print('Image saving failed. Please check whethe the save_path exists!')
        return False
    return True


def load(img_path):
    """ Load an image from a given path
    Args:
        img_path (str): where to load the image . must have extension.
    Return:
        An image has type np.ndarray
    """
    assert isinstance(img_path, str), 'img_path must be a str'
    utils.complaint_file_absence(img_path)

    img = cv2.imread(img_path)
    return img


def show(img, show_name='img', delay=0):
    """ Show an image
    Args:
        img (np.ndarray): an image has shape [h, w, c] or [h, w]
        show_name (str): the name of the show window, default: 'img'
        delay (int): how many milliseconds to wait the window then close.
            0 means forever util key pressed. default: 0
    Returns:
        No
    """
    assert isinstance(img, np.ndarray), 'img must be a np.ndarray'

    cv2.imshow(show_name, img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()


def crop(img, x0=None, y0=None, x1=None, y1=None):
    """Crop img[y0:y1, x0:x1] from img and return this part.

    Args:
        img (numpy.ndarray): an RGB or grayscale image. For RGB image,  shape
        is [h, w, c]. for grayscale image, shape is [h, w]
        y0 (int): top y coordinates of target part of img to crop
        y1 (int): bottom y coordinates of target part of img to crop
        x0 (int): left x coordinates of target part of img to crop
        x1 (int): right x coordinates of target part of img to crop


    Returns:
        img[y0:y1, x0:x1].
    Raises:
    ValueError: if value of coordinates < 0
    """

    h, w = img.shape[:2]
    y0 = 0 if y0 is None else y0
    y1 = h if y1 is None else y1
    x0 = 0 if x0 is None else x0
    x1 = w if x1 is None else x1

    assert isinstance(img, np.ndarray), 'img is not a np.ndarray'
    assert img.ndim in [2, 3], 'img must be RGB image or grayscale image'
    assert isinstance(y0, int), 'y0 is not a int'
    assert isinstance(y1, int), 'y1 is not a int'
    assert isinstance(x0, int), 'x0 is not a int'
    assert isinstance(x1, int), 'x1 is not a int'

    if y0 < 0:
        raise ValueError('y0 is < 0')
    if y1 < 0:
        raise ValueError('y1 is < 0')
    if x0 < 0:
        raise ValueError('x0 is < 0')
    if x1 < 0:
        raise ValueError('x1 is < 0')

    return img[y0:y1, x0:x1]


def combine(img1, img2, axis=0):
    """ Combine two images img1 and img2 to one image horizionly or vertically
    Args:
    img1 (np.ndarray): first image to combine
    img2 (np.ndarray): second image to combine
    axis (int, optional): which axis to combine images. 0 for vertically, 1
        for horizon. default: 0
    Returns:
        np.ndarray
    """
    res = np.concatenate((img1, img2), axis=axis)
    return res


def resize(img, h, w):
    """ Resize img to target shape [h, w]
    Args:
        img (np.ndarray): image to resize
        h (int): height of target image
        w (int): width of target image
    Returns:
        np.ndarray with shape [h, w] or [h, w, 3]
    """

    assert isinstance(h, int), 'h must be an int'
    assert isinstance(w, int), 'w must be an int'
    assert h > 0, 'h must be larger than 0'
    assert w > 0, 'h must be larger than 0'

    return cv2.resize(img, (w, h))


def show_pair(img1, img2, show_name="img_pair", delay=0):
    """ Show two images in a row
    Args:
        img1 (np.ndarray): First image to show.
        img2 (np.ndarray): Second image to show.
        show_name (str, optional): name for the window to show image. Default:
            'img_pair'
        delay (int): how many milliseconds to wait the window then close.
            0 means forever util key pressed. default: 0
    """
    img_combine = combine(img1, img2, axis=1)
    show(img_combine, show_name=show_name, delay=delay)


def show_pair_folder(dir1, dir2, dir1_ptn="*.*", dir2_ptn="*.*"):
    """ Show images in two folder to compare them easily.
    Args:
        dir1 (str): path of first directory
        dir2 (str): path of second directory
        dir1_ptn(str, optional): pattern for filtering image in dir1. Default:
            '*.*'
        dir2_ptn(str, optional): pattern for filtering image in dir2. Default:
            '*.*'
    """
    utils.complaint_dir_absence(dir1)
    utils.complaint_dir_absence(dir2)

    dir1_full_pth = os.path.join(dir1, dir1_ptn)
    dir2_full_pth = os.path.join(dir2, dir2_ptn)
    imgs_path1 = sorted(glob.glob(dir1_full_pth))
    imgs_path2 = sorted(glob.glob(dir2_full_pth))
    assert len(imgs_path1) == len(imgs_path2), 'images in two dir must be equal'

    def update(imgs_path1, imgs_path2, idx):
        """ Update shown images. """
        img1 = load(imgs_path1[idx])
        img2 = load(imgs_path2[idx])
        img_comb = combine(img1, img2, axis=1)
        cv2.imshow('img_comb', img_comb)

    idx = 0
    update(imgs_path1, imgs_path2, idx)
    while True:
        ch = cv2.waitKeyEx()
        if ch & 0xFF == ord('q'):
            break
        if ch == 65361 or ch == 65362 or ch == ord('h') or ch == ord('k'):
            idx = max(0, idx-1)
            update(imgs_path1, imgs_path2, idx)
            idx -= 1
        elif ch == 65363 or ch == 65364 or ch == ord('l') or ch == ord('j'):
            idx = min(idx, len(imgs_path1))
            update(imgs_path1, imgs_path2, idx)
            idx += 1
        else:
            print(ch)

    cv2.destroyAllWindows()
