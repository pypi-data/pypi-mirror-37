""" image module of dozy. """
import os

import cv2
import numpy as np


def save(save_path, img):
    """ Save an image.
    Args:
        save_path (str): where to save the image. must have extension.
        img (np.ndarray): an image has shape [h, w, c] or [h, w]

    Returns:
        return True if save successfully else False
    """
    assert isinstance(save_path, str), 'save_path must be a str'

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
    assert os.path.exists(img_path), 'img_path doesn\'t exist'

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
    img1 (np.ndarray) : first image to combine
    img2 (np.ndarray) : second image to combine
    axis (int, optional) : which axis to combine images. 0 for vertically, 1
        for horizon. default: 0
    Returns:
        np.ndarray
    """
    res = np.concatenate((img1, img2), axis=axis)
    return res


def resize(img, h, w):
    """ Resize img to target shape [h, w]
    Args:
        img (np.ndarray) : image to resize
        h (int) : height of target image
        w (int) : width of target image
    Returns:
        np.ndarray with shape [h, w] or [h, w, 3]
    """

    assert isinstance(h, int), 'h must be an int'
    assert isinstance(w, int), 'w must be an int'
    assert h > 0, 'h must be larger than 0'
    assert w > 0, 'h must be larger than 0'

    return cv2.resize(img, (w, h))
