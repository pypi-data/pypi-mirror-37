from abc import abstractmethod, ABC


class Comparable(ABC):
    """
    Abstract interface for comparing objects. Similar to javas Comparable interface
    """
    @abstractmethod
    def compare_to(self, other) -> int:
        ...
