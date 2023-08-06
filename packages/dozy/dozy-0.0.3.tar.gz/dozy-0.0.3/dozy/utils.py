""" Save useful utilities for dozy at here. """
import os


def check_file_exists(file_path, create=False):
    """ Check if a file exists. if `create` is True, create it when didn't exist
    Args:
        file_path (str): file path
        create (bool, optional): if file doesn't exist, whether to create it
    Returns:
        Return True if the file exists, otherwise False

    """
    if os.path.exists(file_path):
        return True
    if create:
        os.mknod(file_path)
    return False


def check_dir_exists(dir_path, create=False):
    """ Check if a dir exists. If `create` is True, create it when didn't exist
    Args:
        dir_path (str): path of a directory
        create (bool, optional), if the dir doesn't exist, whether to create it
    Returns:
        Return True if the dir exists, otherwise False
    """
    if os.path.exists(dir_path):
        return True
    if create:
        os.makedirs(dir_path)
    return False


def complaint_absence(path):
    """ Throw out an error when a file or a directory doesn't exist
    Args:
        path (str): path of a file or a directory
    Returns:

    """
    if not os.path.exists(path):
        raise FileNotFoundError('{} doesn\'t exist'.format(path))


def complaint_file_absence(path):
    """ Throw out an error if the path doesn't exist or is not a file
    Args:
        path (str): path to verify whether is a file
    Returns:

    """
    complaint_absence(path)
    if not os.path.isfile(path):
        raise Exception('{} is not a file, please check again'.format(path))


def complaint_dir_absence(path):
    """ Throw out an error if the path doesn't exist or is not a dir
    Args:
        path (str): path to verify whether is a dir
    Returns:

    """
    complaint_absence(path)
    if not os.path.isdir(path):
        raise Exception('{} is not a dir, please check again'.format(path))
