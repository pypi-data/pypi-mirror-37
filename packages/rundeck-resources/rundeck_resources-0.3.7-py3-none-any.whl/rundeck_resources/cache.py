import os
import glob
import json
import logging
import tempfile

from .errors import CacheNotFound


class Cache:
    """
    A cache module the plugins can take advantage of in case the APIs
    do not return data or the server is down.
    """

    def __init__(self, config: dict, no_cache: bool) -> None:
        """
        Initialize the *Cache* system for `rundeck_resources`.

        :param config: The configuration provided by `config.read_config`.
        :param no_cache: Configure whether to use the cache or not.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.separator = '-'
        self.no_cache = no_cache
        self.cache_config = {} if no_cache else self.load_cache(config)

    def load_cache(self, config: dict) -> dict:
        """
        Method to search for all configured plugins cache files

        :param config: the configuration provided by `config.read_config`.
        :returns: The cache configuration that includes paths to all plugin
                  cache files.
        """
        self.logger.info("Loading cache configuration")
        tempdir = tempfile.gettempdir()
        self.logger.debug("The tempdir is '%s'", tempdir)
        rundeck_tempdir = glob.glob('{}/rundeck_resources*'
                                    .format(tempdir))
        cache = {}
        if rundeck_tempdir:
            self.logger.debug(
                "Cache directory found, searching for plugins cache files")
            cache = self._load_plugin_cache(rundeck_tempdir[0],
                                            config)
        else:
            self.logger.debug("No cache directory found")
            cache = self._create_cache_tempdir(config)
        return cache

    @staticmethod
    def translate_to_filename(plugin_name: str) -> str:
        """
        Static method to translate the plugin name to a standard prefix
        that could be used in a standard matter in the *Cache* class.

        :param plugin_name: The plugin to translate the name for.
        :returns: The translated plugin name.
        """
        return plugin_name.replace(':', '_').lower()

    def _create_cache_tempdir(self, config: dict) -> dict:
        """
        Private method to create the *rundeck-resources* cache directory.

        *NOTE*: This will initialize all configured plugins cache file paths.

        :param config: The dictionary provided by `config.read_config`.
        :returns: The cache configuration that includes the path to the
                  *rundeck-resources* cache directory.
        """
        self.logger.info("Creating cache directory")
        cache = {}
        cache['rundeck_resources_tempdir'] = \
            tempfile.mkdtemp(prefix='rundeck_resources{}'
                             .format(self.separator))
        self.logger.debug("Initializing an empty list of plugin cache paths")
        for plugin in config:
            cache[plugin] = ''
        return cache

    def _load_plugin_cache(self, rundeck_tempdir: str, config: dict) -> dict:
        """
        Private method that will search for all configured plugins cache files.

        :param rundeck_tempdir: The *rundeck-resources* cache directory.
        :param config: The configuration provided by `config.read_config`.
        :returns: The cache configuration with all plugins cache file paths.
        """
        self.logger.info("Searching for plugin cache files")
        cache = {}
        cache['rundeck_resources_tempdir'] = rundeck_tempdir
        rundeck_cache_files = glob.glob('{}/*'.format(rundeck_tempdir))
        for plugin in config.keys():
            cache_file_prefix = Cache.translate_to_filename(plugin)
            for plugin_cache_file in rundeck_cache_files:
                plugin_cache_filename = plugin_cache_file.split('/')[-1]
                if plugin_cache_filename.startswith(cache_file_prefix):
                    cache[plugin] = plugin_cache_file
                    self.logger.debug("Plugin '%s' cache file located at '%s'",
                                      plugin, plugin_cache_file)
                    break
            else:
                cache[plugin] = ''
                self.logger.debug("Plugin '%s' cache file not found",
                                  plugin)
        return cache

    def invalidate(self, plugin: str) -> None:
        """
        Method to invalidate a plugin cache file.

        :param plugin: The plugin name to invalidate the cache file for.
        """
        self.logger.info("Invalidating cache for plugin '%s'",
                         plugin)
        plugin_tempfile = self.cache_config.get(plugin, '')
        if plugin_tempfile:
            self.logger.debug("Plugin '%s' cache was found at '%s' attempting"
                              " to remove", plugin, plugin_tempfile)
            try:
                os.remove(plugin_tempfile)
            except FileNotFoundError as e:
                self.logger.error("Failed to remove '%s': %s",
                                  plugin_tempfile, e)
                pass
        self.cache_config[plugin] = ''

    def cache(self, plugin: str, resources: dict) -> None:
        """
        Method to cache plugin data.

        :param plugin: The plugin name to cache data for.
        :param resources: The resources data to cache.
        """
        if self.no_cache:
            self.logger.info("The cache is disabled, no caching to perform.")
        else:
            self.logger.info("Caching data for plugin '%s'", plugin)
            cache_tempdir = self.cache_config.get('rundeck_resources_tempdir')
            plugin_name_prefix = '{}{}'.format(
                Cache.translate_to_filename(plugin), self.separator)
            self.logger.debug("Creating new cache file for plugin '%s'",
                              plugin)
            fd, new_tempfile = tempfile.mkstemp(prefix=plugin_name_prefix,
                                                dir=cache_tempdir)
            self.logger.debug("Saving resources data for plugin '%s'"
                              " in new cache file", plugin)
            with open(new_tempfile, 'w') as f:
                f.write(json.dumps(resources))
            os.close(fd)
            self.invalidate(plugin)
            self.logger.debug("Updating '%s' plugin cache path with"
                              " the new cache file", plugin)
            self.cache_config[plugin] = new_tempfile

    def uncache(self, plugin: str) -> dict:
        """
        Method to read cached data for a specific plugin.

        :param plugin: The plugin to read cached data for.
        :raises: CacheNotFound
        """
        if self.no_cache:
            self.logger.info("The cache is disabled, returning an empty"
                             " dictionary")
            return {}
        self.logger.info("Retrieving cached data for plugin '%s'", plugin)
        plugin_tempfile = self.cache_config.get(plugin, '')
        if not plugin_tempfile:
            self.logger.warning("No cached data for plugin '%s' was found"
                                ", raising error", plugin)
            raise CacheNotFound("No cache found for plugin '{}'"
                                .format(plugin))

        self.logger.debug("Cached data for plugin '%s' found"
                          " and is being returned", plugin)
        with open(plugin_tempfile, 'r') as f:
            return json.loads(f.read())
