from abc import abstractmethod
from typing import Generic

from stdlib.abstracts.map import Map
from stdlib.abstracts.sortedmap import SortedMap


class NavigableMap(SortedMap):
    @abstractmethod
    def lower_entry(self, key: Generic) -> Map.Entry or Generic:
        ...

    @abstractmethod
    def floor_entry(self, key: Generic) -> Map.Entry or Generic:
        ...

    @abstractmethod
    def ceiling_entry(self, key: Generic) -> Map.Entry or Generic:
        ...

    @abstractmethod
    def higher_key(self, key: Generic) -> Map.Entry or Generic:
        ...

    @abstractmethod
    def first_entry(self) -> Map.Entry:
        ...

    @abstractmethod
    def last_entry(self) -> Map.Entry:
        ...

    @abstractmethod
    def poll_first_entry(self) -> Map.Entry:
        ...

    @abstractmethod
    def poll_last_entry(self) -> Map.Entry:
        ...

    @abstractmethod
    def descending_map(self):
        ...

    @abstractmethod
    def navigable_key_set(self):
        ...

    @abstractmethod
    def descending_key_set(self):
        ...

    @abstractmethod
    def sub_map_nav(self, from_key: Generic, from_inclusive: bool, to_key: Generic, to_inclusive: bool):
        ...

    @abstractmethod
    def head_map_nav(self, to_key: Generic, inclusive: bool):
        ...

    @abstractmethod
    def tail_map_nav(self, from_key: Generic, inclusive: bool):
        ...

    @abstractmethod
    def sub_map(self, from_key: Generic, to_key: Generic):
        ...

    @abstractmethod
    def head_map(self, to_key: Generic):
        ...

    @abstractmethod
    def tail_map(self, from_key: Generic):
        ...
