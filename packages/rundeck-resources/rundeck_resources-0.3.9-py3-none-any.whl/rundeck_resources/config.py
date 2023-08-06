import logging
import configparser
from .common import check_file

# Setup logging
logger = logging.getLogger(__name__)


def read_config(path: str) -> dict:
    """
    Method to read the init configuration file.

    :param path: The path to the init configuration file.
    :returns: The content of the configuration file.
    """
    logger.debug("Reading configuration file")
    config_path = check_file(path)
    logger.debug("Parsing configuration file content")
    config = configparser.ConfigParser()
    config.read(config_path)
    configuration = {}
    logger.debug("Converting configuration into a dictionary")
    for section in config.sections():
        configuration[section] = {}
        for key, val in config.items(section):
            configuration[section][key] = val
    logger.debug("Returning configuration dictionary")
    return configuration
