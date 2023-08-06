class ConfigError(Exception):
    """
    Custom `ConfigError` exception.
    We raise this exception when a configuration error
    is encountered.
    """

    def __init__(self, message: str = None) -> None:
        super().__init__(message)


class NoResourcesFound(Exception):
    """
    Custom `NoResourcesFound` exception.
    We raise this exception when no resources have been
    returned from the importers.
    """

    def __init__(self, message: str = None) -> None:
        super().__init__(message)


class CacheNotFound(Exception):
    """
    Custom `CacheNotFound` exception.
    We raise this exception when no plugin cache have been
    found.
    """

    def __init__(self, message: str = None) -> None:
        super().__init__(message)
