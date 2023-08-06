from abc import ABCMeta, abstractmethod


class ResourcesImporter(metaclass=ABCMeta):
    """
    ResourcesImporter interface definition
    """

    @abstractmethod
    def import_resources(self) -> dict:
        """
        This method is expected to export the
        data into a rundeck data structure that
        can be easily saved

        :returns: Resources data.
        """
        pass


class ResourcesExporter(metaclass=ABCMeta):
    """
    ResourcesExporter interface definition
    """

    @abstractmethod
    def export_resources(self, resources: dict) -> None:
        """
        This method is expected to save the data
        into a rundeck resources formatted file.

        :param resources: The resources to save into the resources file.
        """
        pass
