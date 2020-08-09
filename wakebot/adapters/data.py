from typing import Union
from ..entities.reserve import Reserve


class BaseDataAdapter:
    """A base class for a data adapters"""

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        return NotImplementedError

    def get_data_by_keys(self, **kwargs) -> any:
        """Get a set of data from storage by a keys

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)

        Returns:
            A iterator object of given data
        """
        return NotImplementedError

    def append_data(self, **kwargs):
        """Append new data to storage

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)
        """
        return NotImplementedError

    def update_data(self, **kwargs):
        """Append new data to storage

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)
        """
        return NotImplementedError

    def remove_data_by_keys(self, **kwargs):
        """Remove data from storage by a keys

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)

        Returns:
            A iterator object of given data
        """
        return NotImplementedError


class MemoryDataAdapter(BaseDataAdapter):
    """A memory data adapter

    An adapter store a data in a memory allocated dictionary

    Attributes:
        storage:
            A dictionary of a stored data
    """
    __storage: dict

    def __init__(self):
        self.__storage = {}

    @property
    def storage(self):
        return self.__storage

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        return self.__storage.copy()

    def get_data_by_keys(self, key: str):
        """Get a set of data  from storage by a keys

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)

        Returns:
            A object of given data
        """
        try:
            data = self.__storage[key]
        except KeyError:
            data = None

        return data

    def append_data(self, key: str, data):
        """Append new data to storage

        Args:
            key:
                A string or integer key value
            data:
                A dictionary of a data to append to storage
        """
        self.__storage[key] = data

    def update_data(self, key: str, data):
        """Append new data to storage

        Args:
            key:
                A string or integer key value
            data:
                A dictionary of a data to append to storage
        """
        self.__storage[key] = data

    def remove_data_by_keys(self, key: str):
        """Remove data from storage by a keys

        Args:
            key:
                A string or integer key value

        Returns:
            A iterator object of given data
        """
        del self.__storage[key]


class ReserveDataAdapter:
    """A base wakeboard reservation adapter class"""

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        return NotImplementedError

    def get_data_by_keys(self, id: int) -> Union[Reserve, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of wake reservation

        Returns:
            A iterator object of given data
        """
        return NotImplementedError

    def get_active_reserves(self) -> iter:
        """Get an active wakeboard reservations from storage

        Returns:
            A iterator object of given data
        """
        raise NotImplementedError

    def get_concurrent_reserves(self, reserve: Reserve) -> iter:
        """Get an concurrent reservations from storage

        Returns:
            A iterator object of given data
        """
        raise NotImplementedError

    def get_concurrent_count(self, reserve: Reserve) -> int:
        """Get an concurrent reservations from storage

        Returns:
            A iterator object of given data
        """
        raise NotImplementedError

    def append_data(self, reserve: Reserve) -> Reserve:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        return NotImplementedError

    def update_data(self, reserve: Reserve):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        return NotImplementedError

    def remove_data_by_keys(self, id: int):
        """Remove data from storage by a keys

        Args:
            id:
                An identifier of wake reservation

        Returns:
            A iterator object of given data
        """
        return NotImplementedError
