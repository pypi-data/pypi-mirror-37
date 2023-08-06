from abc import abstractmethod
from typing import Generic

from stdlib.abstracts.collection import Collection
from stdlib.abstracts.comparator import Comparator
from stdlib.abstracts.map import Map
from stdlib.linear_ds.set import Set


class SortedMap(Map):
    @abstractmethod
    def comparator(self) -> Comparator:
        ...

    @abstractmethod
    def __compare__(self):
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

    @abstractmethod
    def first_key(self) -> Generic:
        ...

    @abstractmethod
    def last_key(self) -> Generic:
        ...

    @abstractmethod
    def key_set(self) -> Set:
        ...

    @abstractmethod
    def values(self) -> Collection:
        ...

    @abstractmethod
    def entry_set(self) -> Set:
        ...
