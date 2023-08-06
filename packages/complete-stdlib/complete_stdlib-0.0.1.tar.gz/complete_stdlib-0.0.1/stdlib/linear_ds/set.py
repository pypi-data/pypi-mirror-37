from abc import ABC, abstractmethod
from collections import Iterable
from stdlib.abstracts.iterator import Iterator


class Set(ABC, Iterable):
    @abstractmethod
    def __sizeof__(self) -> int:
        ...

    @abstractmethod
    def __empty__(self) -> bool:
        ...

    @abstractmethod
    def __contains__(self, item) -> bool:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator:
        ...

    @abstractmethod
    def to_array(self):
        ...

    @abstractmethod
    def add(self, e) -> bool:
        ...

    @abstractmethod
    def remove(self, o) -> bool:
        ...

    @abstractmethod
    def contains_all(self, c) -> bool:
        ...

    @abstractmethod
    def add_all(self, c) -> bool:
        ...

    @abstractmethod
    def retain_all(self, c) -> bool:
        ...

    @abstractmethod
    def remove_all(self, c) -> bool:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...
