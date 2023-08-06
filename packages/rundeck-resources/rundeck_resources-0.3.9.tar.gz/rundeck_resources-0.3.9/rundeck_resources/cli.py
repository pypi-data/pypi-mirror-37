#!/usr/bin/env python3
import sys
import argparse
import logging
from .config import read_config
from .plugins import load_plugins
from .logger import setup_logging
from .cache import Cache
from .errors import ConfigError
from .errors import NoResourcesFound

from . import __version__

# Setup logging
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main method.
    """
    parser = argument_parse()
    args = parser.parse_args()
    verbosity_level = verbosity(args.verbose)
    setup_logging(args.logger, verbosity_level)
    logger.info("Reading the rundeck-resources configuration")
    config = read_config(args.config)
    logger.info("Initializing cache system")
    cache = Cache(config, args.no_cache)
    logger.info("Loading importer plugins")
    try:
        import_plugins = load_importers(config)
    except ConfigError as e:
        logger.critical("Importers error: %s", e)
        sys.exit(1)
    logger.info("Loading exporter plugins")
    try:
        export_plugins = load_exporters(config)
    except ConfigError as e:
        logger.critical("Exporters error: %s", e)
        sys.exit(1)

    logger.info("Initializing input interfaces")
    logger.debug("Input plugins: %s", import_plugins)
    import_interfaces = initialize_import_interfaces(
        config, import_plugins, cache)
    logger.info("Initializing output interfaces")
    logger.debug("Output plugins: %s", export_plugins)
    export_interfaces = initialize_export_interfaces(
        config, export_plugins)

    logger.info("Importing nodes resources from input plugins")
    logger.debug("Input interfaces: %s", import_interfaces)
    try:
        resources = import_resources(import_interfaces)
    except NoResourcesFound as e:
        logger.error("Import error: %s", e)
        logger.warning("No resources file written")
        sys.exit(0)
    logger.info("Exporting nodes resources using output plugins")
    logger.debug("Output interfaces: %s", export_interfaces)
    export_resources(export_interfaces, resources)
    logger.info("Rundeck Resources successfully completed")


def load_importers(config):
    """
    Method to load the `Importers` plugins configured in the configuration
    file.

    :param config: The configuration file content.
    :returns: The `Importers` plugins, loaded.
    """
    return load_plugins(config, 'Importers')


def load_exporters(config):
    """
    Method to load the `Exporters` plugins configured in the configuration
    file.

    :param config: The configuration file content.
    :returns: The `Exporters` plugins, loaded.
    """
    return load_plugins(config, 'Exporters')


def initialize_import_interfaces(config: dict, plugins: dict,
                                 cache: Cache) -> list:
    """
    Method to initialize the interfaces with the configuration.

    :param config: The configuration file content.
    :param plugins: The list of loaded plugins.
    :param cache: The cache system instance.
    :returns: The list of loaded plugins initialized.
    """
    interfaces = []
    for interface in plugins.values():
        interfaces.append(
            interface['plugin'](interface['title'],
                                config, cache))
    return interfaces


def initialize_export_interfaces(config: dict, plugins: dict) -> list:
    """
    Method to initialize the interfaces with the configuration.

    :param config: The configuration file content.
    :param plugins: The list of loaded plugins.
    :returns: The list of loaded plugins initialized.
    """
    interfaces = []
    for interface in plugins.values():
        interfaces.append(
            interface['plugin'](interface['title'],
                                config))
    return interfaces


def import_resources(interfaces: list) -> dict:
    """
    Method to get all resources from the *input* interfaces.

    :param interfaces: The list of initialized input interfaces.
    :returns: The resources returned by the input interfaces.
    """
    resources = {}
    for interface in interfaces:
        resources.update(interface.import_resources())
    if not resources:
        raise NoResourcesFound("No resources found")
    return resources


def export_resources(interfaces: list, resources: dict) -> None:
    """
    Method to export the resources using the *output* interfaces.

    :param interfaces: The list of initialized output interfaces.
    :param resources: The resources provided by the input interfaces.
    """
    for interface in interfaces:
        interface.export_resources(resources)


def argument_parse() -> argparse.ArgumentParser:
    """
    Method to extract the arguments from the command line.

    :returns: The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Generates rundeck resources "
                    "file from different API sources.")

    parser.add_argument(
        'config', type=str,
        help='Configuration file.')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Verbosity level to use.')
    parser.add_argument(
        '-l', '--logger', type=str,
        help='The logger YAML configuration file.')
    parser.add_argument(
        '--no-cache', action='store_true',
        help='Do not use cache.')
    parser.add_argument(
        '-V', '--version', action='version',
        version='%(prog)s {}'.format(__version__),
        help='Prints version.')
    return parser


def verbosity(verbose: int):
    """
    Method to set the verbosity.

    :param verbose: The verbosity set by user.
    :returns: The verbosity level.
    """
    if verbose == 0:
        return logging.ERROR
    elif verbose == 1:
        return logging.WARNING
    elif verbose == 2:
        return logging.INFO
    elif verbose > 2:
        return logging.DEBUG
