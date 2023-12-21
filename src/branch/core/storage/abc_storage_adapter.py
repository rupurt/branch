from abc import ABC, abstractmethod
from result import Result


class ABCStorageAdapter(ABC):
    """
    Abstract class for management of persistent storage
    """

    @abstractmethod
    def put(self, key: str, content: bytes) -> Result[None, type[NotImplementedError]]:
        """
        Write binary `contents` for the given `key`
        """
        pass

    @abstractmethod
    def get(
        self, key: str
    ) -> Result[bytes, type[FileNotFoundError] | type[NotImplementedError]]:
        """
        Retrieve binary `contents` for the given `key`
        """
        pass

    @abstractmethod
    def glob(self, pattern: str) -> Result[list[str], type[NotImplementedError]]:
        """
        Returns a list of paths relative to the adapter `location`
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> Result[bool, type[NotImplementedError]]:
        """
        Deletes the item at the given key
        """
        pass
