from abc import ABC, abstractmethod
from typing import Generic

from stdlib.stdlib.collections import Collections


class Comparator(ABC):
    @abstractmethod
    def compare(self, o1: Generic, o2: Generic) -> int:
        ...

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __reversed__(self):
        return Collections.reverse(self)
