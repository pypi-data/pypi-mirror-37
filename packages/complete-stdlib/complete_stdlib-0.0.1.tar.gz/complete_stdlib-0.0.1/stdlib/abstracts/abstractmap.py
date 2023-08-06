from abc import ABC, abstractmethod
from typing import Generic, Collection

from stdlib.linear_ds.set import Set
from stdlib.abstracts.map import Map
from stdlib.abstracts.map import Entry


# NOT FINISHED
class AbstractMap(Map, ABC):
    """
    An abstract implementation of the abstracted Map class
    """
    def __sizeof__(self) -> int:
        return self.entry_set().__sizeof__()

    def __empty__(self):
        return self.__sizeof__() == 0

    def contains_value(self, value: Generic) -> bool:
        i = self.entry_set().__iter__()
        if value is None:
            while not StopIteration:
                e = i.__next__()
                if e.get_value() is None:
                    return True
        else:
            while not StopIteration:
                e = i.__next__()
                if value.__eq__(e.get_value()):
                    return True

        return False

    def contains_key(self, key: Generic) -> bool:
        i = self.entry_set().__iter__()
        if key is None:
            while True:
                try:
                    e = i.__next__()
                    if e.get_key() is None:
                        return True
                except StopIteration:
                    break
        else:
            while True:
                try:
                    e = i.__next__()
                    if key.__eq__(e.get_key):
                        return True
                except StopIteration:
                    break

        return False

    def get(self, key: Generic) -> None:
        i = self.entry_set().__iter__()
        if key is None:
            while True:
                try:
                    e = i.__next__()
                    if e.get_key() is None:
                        return e.get_value()
                except StopIteration:
                    break
        else:
            while True:
                try:
                    e = i.__next__()
                    if key.__eq__(e.get_key()):
                        return e.get_value()
                except StopIteration:
                    break

        return None

    def put(self, key: Generic, value: Generic) -> Generic or None:
        raise NotImplementedError

    def remove(self, key: Generic, value=None) -> Generic or None:
        i = self.entry_set()
        correct_entry = None
        if key is None:
            # has_next = True
            while correct_entry is None: #  and has_next:
                try:
                    e = i.__iter__().__next__()
                    if e.get_key() is None:
                        correct_entry = e
                except StopIteration:
                    break
                    # has_next = False
        else:
            # has_next = True
            while correct_entry is None: #  and has_next:
                try:
                    e = i.__iter__().__next__()
                    if key.__eq__(e.get_key()):
                        correct_entry = e
                except StopIteration:
                    break

        old_value = None
        if correct_entry is not None:
            old_value = correct_entry.get_value()
            i.remove(e)

        return old_value

    def put_all(self, map):
        raise NotImplementedError

    def clear(self) -> None:
        self.entry_set().clear()

    keyset = None
    values = Collection

    def __eq__(self, other: Generic) -> bool:
        if other == self:
            return True

        if not isinstance(other, Map):
            return False

        m = other
        if m.__sizeof__() != self.__sizeof__():
            return False

        try:
            i = self.entry_set().__iter__()
            while i.__has_next__():
                e = i.__next__()
                key = e.get_key()
                value = e.get_value()
                if value is None:
                    if not (m.get(key) is None and m.contains_key(key)):
                        return False
                else:
                    if not value.__eq__(m.get(key)):
                        return False

        except (None, BaseException):
            return False

        return True

    def __hash__(self):
        h = 0
        i = self.entry_set().__iter__()
        while i.__has_next__():
            h += i.__next__().__hash__()

        return h

    def __str__(self):
        i = self.entry_set().__iter__()
        if not i.__has_next__():
            return '{}'

        sb = '{'
        while True:
            e = i.__next__()
            key = e.get_key()
            value = e.get_value()
            sb += '(this Map)' if key == self else key
            sb += '='
            sb += '(this Map)' if value == self else value
            if not i.__has_next__():
                sb += '}'
                return sb

            sb += ', '

    def equals(self, o1: object, o2: object) -> bool:
        return o2 is None if o1 is None else o1.__eq__(o2)

    @abstractmethod
    def entry_set(self) -> Set:
        ...


class SimpleEntry(Entry):
    def __init__(self):
        pass
# class KeySet(AbstractSet):
#     def __iter__(self):
#         i =
#
#     def __sizeof__(self):
#         AbstractMap.__new__(self).__sizeof__()
#
#     def empty(self):
#         AbstractMap.__new__(KeySet).em
#
#     def clear(self):
#         AbstractMap.__new__(self).clear1
