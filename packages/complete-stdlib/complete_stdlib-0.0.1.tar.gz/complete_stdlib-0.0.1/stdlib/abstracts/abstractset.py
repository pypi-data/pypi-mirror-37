from stdlib.abstracts.abstractcollection import AbstractCollection
from stdlib.abstracts.collection import Collection
from stdlib.linear_ds.set import Set


class AbstractSet(AbstractCollection, Set):
    """
    An abstract implementation of the abstracted Set class
    """
    def __eq__(self, other) -> bool:
        if other == self:
            return True

        if not isinstance(other, Set):
            return False
        c = other
        if c.__sizeof__() != self.__sizeof__():
            return False

        try:
            return self.contains_all(c)
        except None:
            return False

    def __hash__(self) -> int:
        h = 0
        i = self.__iter__()
        while i.__has_next__():
            obj = i.__next__()
            if obj is not None:
                h += obj.__hash__()

        return h

    def remove_all(self, c: Collection) -> bool:
        if c is None:
            return False

        modified = False
        if self.__sizeof__() > c.__sizeof__():
            i = c.__iter__()
            while i.__has_next__():
                modified |= self.remove(i.__next__())

        else:
            i = self.__iter__()
            while i.__has_next__():
                if c.__contains__(i.__next__()):
                    i.__remove__()
                    modified = True

        return modified
