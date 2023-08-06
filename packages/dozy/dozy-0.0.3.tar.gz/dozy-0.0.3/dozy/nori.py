""" Functions about nori is placed at here. """
import pickle

import cv2
import nori2 as nori
import numpy as np


def get_img(nori_id, img_key='img', is_color=True):
    """ Obtain an image in a given nori_id by key.
    Args:
        nori_id (str): nori id
        img_key (str): key for img. default: 'img'
        is_color (bool): if the wanted image is RGB image, default: True
    Returns:
        An image with type np.ndarray

    """
    fetcher = nori.Fetcher()
    raw = pickle.loads(fetcher.get(nori_id))
    flag = cv2.IMREAD_COLOR if is_color else cv2.IMREAD_GRAYSCALE
    img_raw = cv2.imdecode(np.fromstring(raw[img_key], np.uint8), flag)
    assert img_raw is not None, \
        'img_raw is None, please check the nori_id exists: ' + nori_id
    return img_raw


def get_mask(nori_id, h, w, img_key='mask', is_color=False):
    """ Obtain an image in a given nori_id by key.
    Args:
        nori_id (str): nori id
        h (int): height of mask
        w (int): width of mask
        img_key (str): key for img. default: 'mask'
        is_color (bool): if the wanted image is RGB image, default: False
    Returns:
        An image with type np.ndarray

    """
    fetcher = nori.Fetcher()
    raw = pickle.loads(fetcher.get(nori_id))
    flag = cv2.IMREAD_COLOR if is_color else cv2.IMREAD_GRAYSCALE
    try:
        img_raw = np.frombuffer(raw[img_key], np.uint8).reshape(h, w)
    except ValueError:
        img_raw = cv2.imdecode(np.frombuffer(raw[img_key], np.uint8), flag)
    assert img_raw is not None, \
        'img_raw is None, please check the nori_id exists: ' + nori_id
    return img_raw
