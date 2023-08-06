from abc import ABC, abstractmethod
from stdlib.abstracts.iterable import Iterable
from stdlib.abstracts.iterator import Iterator
import typing


class Collection(ABC, Iterable):
    """
    Abstract / Base class for a collection.
    """
    @abstractmethod
    def __sizeof__(self) -> int:
        ...

    @abstractmethod
    def __empty__(self) -> bool:
        ...

    @abstractmethod
    def __contains__(self, item: typing.Generic) -> bool:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator:
        ...

    @abstractmethod
    def to_array(self) -> typing.List[typing.Generic]:
        ...

    @abstractmethod
    def add(self, e: typing.Generic) -> bool:
        ...

    @abstractmethod
    def remove(self, o: typing.Generic) -> bool:
        ...

    @abstractmethod
    def contains_all(self, c: typing.List) -> bool:
        ...

    @abstractmethod
    def add_all(self, c: typing.List) -> bool:
        ...

    @abstractmethod
    def remove_all(self, c: typing.List) -> bool:
        ...

    @abstractmethod
    def __eq__(self, other: typing.Generic) -> bool:
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...
