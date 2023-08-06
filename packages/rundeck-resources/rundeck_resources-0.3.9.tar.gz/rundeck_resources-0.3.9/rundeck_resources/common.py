import os
import logging

# Setup logging
logger = logging.getLogger(__name__)


def normalize_path(path: str) -> str:
    """
    Method to expand and return an absolute
    path from a normal path.

    :param path: The path to normalize.
    :returns: The absolute path.
    """
    logger.debug("Normalizing path: %s", path)
    exp_path = os.path.expanduser(path)
    abs_path = os.path.abspath(exp_path)
    logger.debug("Normalized path: %s", abs_path)
    return abs_path


def check_file(path: str) -> str:
    """
    Method to normalize the path of a file and
    check if the file exists and is a file.

    :param path: The file path to check.
    :returns: The absolute path of a file.
    :raises: FileNotFoundError
    """
    logger.debug("Checking file: %s", path)
    file_path = normalize_path(path)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        logger.error("File '%s' not found, raising exception", file_path)
        raise FileNotFoundError
    logger.debug("File '%s' found, returning path", file_path)
    return file_path


def get_section(plugin: str, title: str) -> str:
    """
    Construct the configuration section

    :param plugin: The plugin name.
    :param title: The title seperated by `:` in the configuration file.
    :returns: The configuration section to pull from the configuration
                file.
    """
    return ':'.join([plugin, title])
