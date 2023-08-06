from abc import ABC, abstractmethod


class Iterable(ABC):
    @abstractmethod
    def __iter__(self):
        ...
