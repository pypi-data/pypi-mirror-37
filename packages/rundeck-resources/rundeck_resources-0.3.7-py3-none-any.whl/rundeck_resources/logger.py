import os
import yaml
import logging.config
from .common import check_file


def setup_logging(default_path: str = None,
                  default_level: int = logging.ERROR,
                  env_key: str = 'LOG_CFG') -> None:
    """
    Method that sets the logging system up.

    :param default_path: The path to the logger configuration.
    :param default_level: The default logging level (DEFAULT: ERROR)
    :param env_key: The environment variable specifying the path to the
                    configuration file.
    """
    value = os.getenv(env_key, None)
    path = None
    if default_path:
        try:
            path = check_file(default_path)
        except FileNotFoundError:
            path = None
    if value:
        try:
            path = check_file(value)
        except FileNotFoundError:
            path = None

    if path:
        with open(path, mode='r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        _format = '%(asctime)s - %(levelname)s - %(filename)s:' \
            '%(name)s.%(funcName)s:%(lineno)d - %(message)s'
        logging.basicConfig(level=default_level, format=_format)
