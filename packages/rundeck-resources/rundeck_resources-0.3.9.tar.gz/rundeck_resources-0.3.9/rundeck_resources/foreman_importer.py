import logging
import requests
import requests_oauthlib

from .cache import Cache
from .interfaces import ResourcesImporter
from .common import get_section


class ForemanImporter(ResourcesImporter):
    """
    A Foreman node information importer
    """

    def __init__(self, title: str, config: dict, cache: Cache) -> None:
        """
        Initialize the *ForemanImporter* plugin.

        :param title: The title provided by the configuration section.
        :param config: The configuration provided by `config.read_config`.
        :param cache: The cache system instance.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cache = cache
        self.title = title
        self.section = get_section('ForemanImporter', title)
        self.config = config[self.section]

    def get_foreman_inventory(self) -> dict:
        """
        Method to get the foreman inventory information.

        :returns: The foreman inventory information.
        """
        pass

    def call_foreman(self):
        pass

    def import_resources(self):
        pass

    @staticmethod
    def get_foreman_protocol(ssl_cert_path: str = None) -> str:
        if ssl_cert_path:
            return 'https'
        return 'http'

    @staticmethod
    def get_foreman_inventory_url(host: str,
                                  ssl_cert_path: str = None) -> str:
        protocol = ForemanImporter.get_foreman_protocol(ssl_cert_path)
        return "{}://{}/api/v2/hosts".format(
            protocol, host)

    @staticmethod
    def get_foreman_node_facts_url(host: str, server_id: str,
                                   ssl_cert_path: str = None) -> str:
        protocol = ForemanImporter.get_foreman_protocol(ssl_cert_path)
        return "{}://{}/api/v2/hosts/{}/facts".format(
            protocol, host, server_id)

    @staticmethod
    def get_oauth1(consumer_key: str,
                   consumer_secret: str) -> requests_oauthlib.OAUth1:
        return requests_oauthlib.OAUth1(
            client_key=consumer_key, client_secret=consumer_secret)

    @staticmethod
    def check_status(response: requests.Response,
                     status_code: int = 200) -> bool:
        if response.status_code == status_code:
            return True
        return False

    @staticmethod
    def create_session(oauth1: str, ssl_cert_path: str = None) \
            -> requests.session:
        session = requests.session()
        session.auth(oauth1)
        session.verify(ssl_cert_path)
        return session
