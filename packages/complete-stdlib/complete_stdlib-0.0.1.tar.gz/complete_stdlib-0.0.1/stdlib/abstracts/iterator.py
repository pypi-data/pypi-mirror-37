from abc import ABC, abstractmethod


class Iterator(ABC):
    @abstractmethod
    def __has_next__(self) -> bool:
        ...

    @abstractmethod
    def __next__(self):
        ...

    @abstractmethod
    def __remove__(self):
        ...
