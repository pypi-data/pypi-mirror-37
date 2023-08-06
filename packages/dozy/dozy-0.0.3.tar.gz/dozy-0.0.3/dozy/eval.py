""" Functions of evaluation for images and videos."""
import glob
import os

import numpy as np

from . import utils
from . import image


def _seg_hist(pred, gt, num_class=2):
    """ create hist.
    Args:
        pred (np.ndarray): Predicted image, has value in range[0, 255] (no
            binarization yet.)
        gt (np.ndarray): Ground truth image, has value in range[0, 255] (no
            binarization yet.)
        num_class (int, optional): How many classes in each image. Default: 2
    Returns:
        np.ndarray: The bind of predicted image and ground truth image
    """
    pred = (pred > 100).astype('uint8')
    gt = (gt > 100).astype('uint8')

    k = (gt >= 0) & (gt < num_class)
    return np.bincount(num_class * gt[k].astype(int) + pred[k].astype(int),
                       minlength=num_class ** 2).reshape(num_class, num_class)


def _seg_score(hist):
    """ calculate mean IoU.
    Args:
        hist (np.ndarray): Get from method _seg_hist
    Returns:
        iu (np.ndarray): IoU array
        acc (np.ndarray): Contains value for each pred and gt pair
        mean_iou (np.ndarray): Mean IoU on all pred and gt pairs.
    """
    acc = np.diag(hist).sum() / hist.sum()
    iou = np.diag(hist) / (hist.sum(1) + hist.sum(0) - np.diag(hist))
    mean_iou = np.nanmean(iou)
    return iou, acc, mean_iou


def iu(pred, gt, num_class=2):
    """ calculate Mean IoU for groundtruth image and predicted image.
    Args:
        pred (np.ndarray): Predicted result image, shape [h, w]
        gt (np.ndarray): Groud truth image, shape [h, w]
        num_class (int, optional): How many classes in each image. Default: 2
    Returns:
        float: IoU value of pred image and gt image
    """
    hist = _seg_hist(pred, gt, num_class=num_class)
    _, _, iou = _seg_score(hist)
    return iou


def miu(pred_dir, gt_dir, pred_ptn="*.mask.png", gt_ptn="*.png", num_class=2):
    """ calculate Mean IoU for images in groundtruth dir and predicted dir.
    Args:
        pred_dir (str): Where to find predicted images
        gt_dir (str): Where to find ground truth images
        pred_ptn (str, optional): The pattern for finding predicted image in a
            dir. Default: `*.mask.png`
        gt_ptn (str, optional): The pattern for finding gt image in a dir.
            Default: `*.png`
        num_class (int, optional): How many classes in each image. Default: 2
    Returns:
        float: Mean IoU for all predicted and ground truth image pairs
    """
    utils.complaint_dir_absence(pred_dir)
    utils.complaint_dir_absence(gt_dir)

    pred_filter_ptn = os.path.join(pred_dir, pred_ptn)
    gt_filter_ptn = os.path.join(gt_dir, gt_ptn)

    pred_img_paths = sorted(glob.glob(pred_filter_ptn))
    gt_img_paths = sorted(glob.glob(gt_filter_ptn))

    assert len(pred_img_paths) == len(gt_img_paths), \
        'nums of pred images and gt images must be equal'

    hist = np.zeros((num_class, num_class))
    for (pred_img_path, gt_img_path) in zip(pred_img_paths, gt_img_paths):
        cur_pred = image.load(pred_img_path)
        cur_gt = image.load(gt_img_path)
        hist += _seg_hist(cur_pred, cur_gt, num_class=num_class)

    _, _, mean_iou = _seg_score(hist)
    return mean_iou
