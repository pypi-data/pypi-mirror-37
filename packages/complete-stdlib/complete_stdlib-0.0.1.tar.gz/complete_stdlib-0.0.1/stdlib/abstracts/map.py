from abc import ABC, abstractmethod
import typing

from stdlib.abstracts.abstractset import AbstractSet
from stdlib.abstracts.comparator import Comparator


class Map(ABC, object):
    @abstractmethod
    def __sizeof__(self) -> int:
        ...

    @abstractmethod
    def __empty__(self) -> bool:
        ...

    @abstractmethod
    def contains_key(self, key: typing.Generic) -> bool:
        ...

    @abstractmethod
    def contains_value(self, value: typing.Generic) -> bool:
        ...

    @abstractmethod
    def get(self, key: typing.Generic) -> typing.Generic or None:
        """
        If this map contains a mapping from a key to a value, then this method returns value otherwise returns None
        :param key: key whose associated value is to be returned
        :return: the value which the specified key is mapped to, or None if this map contains no mapping for the key
        """
        ...

    @abstractmethod
    def put(self, key: typing.Generic, value: typing.Generic) -> typing.Generic or None:
        """
        Associates the specified value with the specified key in this map
        :param key: key to which the value is to be associated
        :param value: value to be associated with the specified key
        :raise NotImplementedError: if the put operation isn't supported by this map
        :raise IndexError: if some property of the specified key or value prevents it from being stored in this map
        :return: the previous value associated key, or None if there was no mapping for key.
        """
        ...

    @abstractmethod
    def remove(self, key, value=None):
        """
        Removed the mapping for a key from this map if it's present
        :param value: value expected to be associated with the specified key
        :param key: key whose mapping is to ber removed from the map
        :raise NotImplementedError: if the remove operation is not supported by this map
        :return:
        """
        if value:
            cur_value = self.get(key)
            if not cur_value.__eq__(value) or (cur_value is None and not self.contains_key(key)):
                return False

            self.remove(key)
            return True

    @abstractmethod
    def replace(self, key, value):
        cur_value = self.get(key)
        if cur_value is not None or self.contains_key(key):
            cur_value = self.put(key, value)

        return cur_value

    @abstractmethod
    def put_all(self, map) -> None:
        """
        Copies all the mappings from the specified map to this map
        :param map: mappings to be stored in this map
        :return: None
        """
        ...

    @abstractmethod
    def replace_all(self, func):
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @abstractmethod
    def key_set(self) -> set:
        ...

    @abstractmethod
    def values(self):
        ...

    @abstractmethod
    def entry_set(self) -> AbstractSet:
        ...

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __hash__(self):
        ...

    @abstractmethod
    def get_or_default(self, key, default_value):
        v = self.get(key)
        return v if (v is not None) or self.contains_key(key) else default_value

    # @abstractmethod
    # def __iter__(self):
    #     ...

    # @abstractmethod
    # def __has_next__(self) -> bool:
    #     ...

    # @abstractmethod
    # def replace_all(self, func):
    #     ...
    #
    # def replace(self, key, old_value, new_value):
    #     ...


class Entry(ABC):
    @abstractmethod
    def get_key(self):
        ...

    @abstractmethod
    def get_value(self):
        ...

    def set_value(self, value):
        ...

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __hash__(self):
        ...

    @abstractmethod
    def comparing_by_key(self, cmp: Comparator = None) -> Comparator:
        if not cmp:
            return lambda c1, c2: c1.get_key().compare_to(c2.get_key())
        else:
            return lambda c1, c2: cmp.compare(c1.get_key, c2.get_key)

    @abstractmethod
    def comparing_by_value(self, cmp: Comparator = None) -> Comparator:
        if not cmp:
            return lambda c1, c2: c1.get_value().compare_to(c2.get_value())
        else:
            return lambda c1, c2: cmp.compare(c1.get_value(), c2.get_value())