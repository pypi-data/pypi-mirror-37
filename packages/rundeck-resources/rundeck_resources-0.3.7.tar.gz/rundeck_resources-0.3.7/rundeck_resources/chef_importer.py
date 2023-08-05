import logging
from chef import ChefAPI, Search

from .cache import Cache
from .interfaces import ResourcesImporter
from .common import check_file, get_section
from .errors import CacheNotFound


class ChefImporter(ResourcesImporter):
    """
    A Chef node information importer
    """

    def __init__(self, title: str, config: dict, cache: Cache) -> None:
        """
        Initialize the *ChefImporter* plugin.

        :param title: The title provided by the configuration section.
        :param config: The configuration provided by `config.read_config`.
        :param cache: The cache system instance.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cache = cache
        self.title = title
        self.section = get_section('ChefImporter', title)
        self.config = config[self.section]

    def get_chef_nodes(self) -> dict:
        """
        Method to get the chef nodes information.

        :returns: The chef nodes information.
        """
        self.logger.debug("Importing Chef resources")
        self.logger.debug("Expanding certificate paths")
        try:
            config = ChefImporter.expand_paths(self.config)
        except FileNotFoundError:
            self.logger.error(
                "Configuration file was not found, skipping this run "
                "and returning no data")
            return {}
        self.logger.debug("Querying Chef server API")
        chef_nodes = ChefImporter.call_chef(config)
        return chef_nodes

    @staticmethod
    def call_chef(config: dict) -> dict:
        """
        Method to query the chef server.

        :param config: The chef configuration.
        :returns: The chef nodes information.
        """
        with ChefAPI(config['url'],
                     config['user_cert_path'],
                     config['user'],
                     version=config.get('version', '0.10.8'),
                     ssl_verify=config.get('ssl_cert_path', False)):
            return Search('node', 'Node Name:*')

    @staticmethod
    def expand_paths(config: dict) -> dict:
        """
        Method to expand file paths for the user certificate
        and the chef ssl certificate.

        :param config: The chef configuration.
        :returns: The chef configuration with expanded paths.
        """
        config['user_cert_path'] = ChefImporter.expand_user_cert_path(
            config['user_cert_path'])
        config['ssl_cert_path'] = ChefImporter.expand_ssl_cert_path(
            config.get('ssl_cert_path', None))
        return config

    @staticmethod
    def expand_user_cert_path(user_cert_path: str) -> str:
        """
        Method to return expanded and checked `user_cert_path`.

        :param user_cert_path: The user certificate path.
        :returns: The check expanded user certificate path.
        """
        return check_file(user_cert_path)

    @staticmethod
    def expand_ssl_cert_path(ssl_cert_path: str) -> str:
        """
        Method to return expanded and checked `ssl_cert_path`.

        :param user_cert_path: The chef server SSL certificate path.
        :returns: The check expanded chef server SSL certificate path.
        """
        try:
            return check_file(ssl_cert_path)
        except FileNotFoundError:
            return ''

    def import_resources(self) -> dict:
        """
        Method to format chef resources into rundeck resources.

        :returns: Rundeck formatted nodes resources.
        """
        self.logger.info("Importing Rundeck resources from Chef plugin")
        chef_nodes = self.get_chef_nodes()
        nodes = {}
        self.logger.debug("Parsing Chef resources")
        try:
            for node in chef_nodes:
                try:
                    _node = {}
                    _node[node['name']] = {}
                    _node[node['name']]['hostname'] = node['automatic']['fqdn']
                    _node[node['name']]['nodename'] = \
                        node['automatic']['hostname']
                    _node[node['name']]['environment'] = \
                        node['chef_environment']
                    _node[node['name']]['osName'] = \
                        node['automatic']['platform']
                    _node[node['name']]['osFamily'] = \
                        node['automatic']['platform_family']
                    _node[node['name']]['osVersion'] = \
                        node['automatic']['platform_version']
                    _node[node['name']]['osArch'] = \
                        node['automatic']['kernel']['machine']
                    _node[node['name']]['recipes'] = \
                        ','.join(node['automatic']['recipes'])
                    _node[node['name']]['roles'] = \
                        ','.join(node['automatic']['roles'])
                    _node[node['name']]['tags'] = \
                        ','.join(node['automatic']['recipes'] +
                        node['automatic']['roles'])
                    _node[node['name']]['chef_tags'] = \
                        ','.join(node['normal']['tags'])
                    _description = \
                        node['automatic']['lsb'].get('description',
                                                     None)
                    if _description:
                        _node[node['name']]['description'] = \
                            _description
                    _username = self.config.get('rundeck_user_login', None)
                    if _username:
                        _node[node['name']]['username'] = _username
                except KeyError as e:
                    self.logger.warning("KeyError encountered with node '%s':"
                                        " %s",
                                        node['automatic']['hostname'], e)
                    continue
                nodes.update(_node)
            self.cache.cache(self.section, nodes)
        except AttributeError as e:
            self.logger.error("ChefAPI encountered an issues: %s", e)
            self.logger.warning("Retrieving data from cache")
            try:
                nodes.update(self.cache.uncache(self.section))
            except CacheNotFound as e:
                self.logger.warning(e)
                return nodes
        self.logger.debug("Returning Rundeck resources from Chef plugin")
        return nodes
