""" video module of dozy. """
import glob
import os

import cv2

import image


def extract(video_path, frm_save_dir, prefix='', pattern='%06d.jpg'):
    """ Extract frames of a video and save them
    Args:
        video_path (str) : path of a video
        frm_save_dir (str) : where to save the frames
        prefix (str) : prefix of name for saving frames, default: ''
        pattern (str): format of frame names, default: '%06d.jpg'
    Returns:

    """
    cap = cv2.VideoCapture(video_path)
    idx = 0
    while True:
        _, img = cap.read(0)
        if img is None:
            print('All frames have been saved.')
            break

        img_save_name = prefix + pattern % idx
        img_save_path = os.path.join(frm_save_dir, img_save_name)
        image.save(img_save_path, img)
        idx += 1

    cap.release()


def merge(frm_dir, video_save_path, fps=25, filter_pattern='*.*', h=None, w=None):
    """ Combine frames to a video file
    Args:
        frm_dir (str): directory where to find images to make the video
        video_save_path (str) : where to save the created video
        fps (int) : fps (Frames Per Second), default: 25
        filter_pattern (str) : format to find the targe image in frm_dir,
            default: '*.*'
        h (int) : height of created video. if None, use default height of first frame
        w (int) : width of created video. if None, use default width of first frame
    Return:

    """

    img_pattern = os.path.join(frm_dir, filter_pattern)
    img_paths = sorted(glob.glob(img_pattern))
    h_init, w_init = cv2.imread(img_paths[0]).shape[:2]
    h = h_init if h is None else h
    w = w_init if w is None else w
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(video_save_path, fourcc, fps, (w, h))
    for img_path in img_paths:
        frame = image.load(img_path)
        writer.write(frame)
    print('All images have been written to the video.')

    writer.release()


def record(video_save_path, fps=25, h=480, w=640):
    """ record a realtime video using a camera
    Args:
        video_save_path (str) : where to save the video
        fps (int) : how many frames per second, default: 25
        h (int) : height of saved video, default: 480
        w (int) : width of saved video, default: 640
    Returns:

    """
    cap = cv2.VideoCapture(0)
    video_name_extension = os.path.splitext(video_save_path)[-1]
    fourcc_pattern = "XVID" if video_name_extension == '.avi' else "MP4V"
    fourcc = cv2.VideoWriter_fourcc(*fourcc_pattern)
    writer = cv2.VideoWriter(video_save_path, fourcc, fps, (w, h))

    while cap.isOpened():
        ret, frm = cap.read()
        if ret:
            cv2.imshow('frame', frm)
            k = cv2.waitKey(1)
            if k & 0xFF == ord('q'):
                break
            else:
                writer.write(frm)
        else:
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()


def play(video_path):
    """ Play a video
    Args:
        video_path (str) : the path of the video to play
    Returns:

    """
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frm = cap.read(0)
        if ret:
            cv2.imshow('frame', frm)
            k = cv2.waitKey(1)
            if k & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
