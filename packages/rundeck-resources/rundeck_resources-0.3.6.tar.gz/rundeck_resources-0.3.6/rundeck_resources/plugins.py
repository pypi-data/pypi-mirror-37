import logging
import pkg_resources
from .errors import ConfigError

# Setup logging
logger = logging.getLogger(__name__)


def load_plugins(config: dict, resource_types: str) -> dict:
    """
    Method to load plugins defined in the *entry_point*
    by *resource_type*.

    :param config: The configuration file content.
    :param resource_types: The resource type to load (Input, Output).
    :returns: The plugins loaded.
    """
    logger.debug("Loading plugins configured to be used")
    raised_error = Exception()
    entry_points = get_plugins(resource_types)
    plugins = {}
    for section in config:
        _section = section.split(":")
        try:
            if _section[0] in entry_points:
                plugins.update({_section[0]: {
                    'plugin': entry_points[_section[0]].load(),
                    'title': _section[1]
                }})
        except IndexError as e:
            raised_error = e

        if isinstance(raised_error, IndexError):
            raise ConfigError("No plugin title found, in section '{}'."
                              " Configuration sections need to be in"
                              " the format 'PluginName:Title'"
                              .format(section))
    return plugins


def get_plugins(resource_types: str) -> dict:
    """
    Method to get the plugins defined in the *entry_point*.

    :param resource_types: The resource type to get (Input, Output).
    :returns: The entry points by name.
    """
    logger.debug("Importing plugins from list available")
    entry_points = {}
    for entry_point in pkg_resources.iter_entry_points(resource_types):
        entry_points.update({entry_point.name: entry_point})
    return entry_points
