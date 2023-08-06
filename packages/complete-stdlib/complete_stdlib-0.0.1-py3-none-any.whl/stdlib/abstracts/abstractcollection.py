from abc import abstractmethod
from stdlib.abstracts.iterator import Iterator
import typing

from stdlib.abstracts.collection import Collection


class AbstractCollection(Collection):
    """
    An abstract implementation of the abstracted Collection class
    """
    @abstractmethod
    def __iter__(self) -> Iterator:
        ...

    @abstractmethod
    def __sizeof__(self) -> int:
        ...

    def empty(self) -> bool:
        return self.__sizeof__() == 0

    def __contains__(self, item: typing.Generic) -> bool:
        it = self.__iter__()
        if item is None:
            while it.__has_next__():
                try:
                    if it.__next__() is None:
                        return True
                except StopIteration:
                    break
        else:
            while it.__has_next__():
                try:
                    if item.__eq__(it.__next__()):
                        return True
                except StopIteration:
                    break

        return False

    def to_array(self) -> typing.List[typing.Generic]:
        raise NotImplementedError
        # r = [object for i in range(self.__sizeof__())]
        # it = self.__iter__()
        # for i in range(len(r)):

    def add(self, e: typing.Generic) -> bool:
        raise NotImplementedError

    def remove(self, o: typing.Generic) -> bool:
        it = self.__iter__()
        if o is None:
            while it.__has_next__():
                try:
                    if it.__next__() is None:
                        it.__remove__()
                        return True
                except StopIteration:
                    break
        else:
            while it.__has_next__():
                try:
                    if o.__eq__(it.__next__()):
                        it.__remove__()
                        return True
                except StopIteration:
                    break
        return False

    def contains_all(self, c: typing.List) -> bool:
        for e in c:
            if not self.__contains__(e):
                return False

        return True

    def add_all(self, c: typing.List) -> bool:
        modified = False
        for e in c:
            if self.add(e):
                modified = True

        return modified

    def clear(self):
        pass

    # def remove_all(self, c: List):
    #     modified = False
