# -*- coding: utf-8 -*-

class BaseDataAdapter:
    """A base class for a data adapters"""

    def get_data(self):
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        return NotImplementedError

    def get_data_by_keys(self, **kwargs) -> iter:
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

    def remove_data_by_keys(self, **kwargs) -> iter:
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

    def __init__(self):
        self.__storage = {}

    @property
    def storage(self):
        return self.__storage

    def get_data(self):
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        return self.__storage.copy()

    def get_data_by_keys(self, key) -> iter:
        """Get a set of data  from storage by a keys

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)

        Returns:
            A iterator object of given data
        """
        try:
            data = self.__storage[key]
        except KeyError:
            data = None

        return data

    def append_data(self, key, data):
        """Append new data to storage

        Args:
            key:
                A string or integer key value
            data:
                A dictionary of a data to append to storage
        """
        self.__storage[key] = data

    def update_data(self, key, data):
        """Append new data to storage

        Args:
            key:
                A string or integer key value
            data:
                A dictionary of a data to append to storage
        """
        self.__storage[key] = data

    def remove_data_by_keys(self, key):
        """Remove data from storage by a keys

        Args:
            **kwargs:
                A custom set of arguments (defined by child class)

        Returns:
            A iterator object of given data
        """
        del self.__storage[key]
