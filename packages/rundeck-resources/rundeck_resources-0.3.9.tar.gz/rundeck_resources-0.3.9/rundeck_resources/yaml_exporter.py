import yaml
import logging
from .interfaces import ResourcesExporter
from .common import normalize_path, get_section


class YAMLExporter(ResourcesExporter):
    """
    The YAML rundeck exporter class
    """

    def __init__(self, title: str, config: dict = {}) -> None:
        """
        Initialize the *YAMLExporter plugin.

        :param title: The title provided by the configuration section.
        :param config: The configuration provided by `config.read_config`.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.title = title
        self.section = get_section('YAMLExporter', title)
        self.config = config.get(self.section, None)

    def export_resources(self, dictionary: dict) -> None:
        """
        Method to save nodes' information into a rundeck
        nodes resources `YAML` file.

        :param dictionary: Rundeck formatted nodes information.
        """
        self.logger.info("Exporting Rundeck resources in YAML format")
        self.logger.debug("Getting resources export path")
        yaml_file = YAMLExporter.export_path(self.config)
        if yaml_file:
            self.logger.debug("Export path found, normalizing path")
            abs_path = normalize_path(yaml_file)
            self.logger.debug("Saving Rundeck YAML resources file")
            with open(abs_path, 'w+') as yfile:
                yaml.dump(dictionary,
                          stream=yfile,
                          explicit_start=True,
                          default_flow_style=False)
        else:
            self.logger.debug("Export path not found, dumping data to stdout")
            print(yaml.dump(dictionary,
                            explicit_start=True,
                            default_flow_style=False))

    @staticmethod
    def export_path(config: dict) -> str:
        """
        Method to get the rundeck export file in absolute
        path format.

        :param config: The `Rundeck` section of the configuration.
        :returns: The file path of rundeck resources to export to.
        """
        return config.get('export_path', '') if config else ''
