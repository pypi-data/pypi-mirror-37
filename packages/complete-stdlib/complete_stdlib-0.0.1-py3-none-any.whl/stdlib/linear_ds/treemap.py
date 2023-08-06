from typing import Generic

from stdlib.abstracts.abstractmap import AbstractMap
from stdlib.abstracts.comparable import Comparable
from stdlib.abstracts.comparator import Comparator
from stdlib.abstracts.map import Map
from stdlib.abstracts.navigablemap import NavigableMap
from stdlib.stdexceptions import NonePointerException
from stdlib.abstracts.sortedmap import SortedMap


class TreeMap(AbstractMap, NavigableMap):
    def __init__(self, comparator: Comparator = None, m: Map = None, sm: SortedMap = None):
        self.comparator = None
        self._size = 0
        self._root = None
        self._mod_count = 0

        if comparator:
            self.comparator = comparator

        elif m:
            self.comparator = None
            self.put_all(m)

        elif sm:
            self.comparator = sm.comparator()
            try:
                self.__build_from_sorted(sm.__sizeof__(), sm.entry_set().__iter__(), None, None)
            except IOError as e:
                print(e)

    def __sizeof__(self) -> int:
        return self._size

    def contains_key(self, key: Generic) -> bool:
        return self.get_entry(key) is not None

    def contains_value(self, value: Generic) -> bool:
        e = self.get_first_entry()
        while e is not None:
            if self.val_equals(value, e.value):
                return True

            e = self.__successor(e)
        return False

    def get(self, key: Generic) -> Generic:
        p = self.get_entry(key)
        return None if p is None else p.value

    # Whatever type key is needs to have the Comparable as a part of it
    def put(self, key, value):
        t = self._root
        if t is None:
            self.compare(key, key)
            self._root = Entry(key, value, None)
            self._size = 1
            self._mod_count += 1
            return None

        cmp = 0
        parent = None
        cpr = self.__com

    def compare(self, k1: Comparable, k2) -> int:
        return k1.compare_to(k2) if self.comparator is None else self.comparator.compare(k1, k2)

    def first_key(self) -> Generic:
        return self.key(self.get_first_entry())

    def last_key(self) -> Generic:
        return self.key(self.get_last_entry())

    def put_all(self, map: Map) -> None:
        map_size = map.__sizeof__()
        if self._size == 0 and map_size != 0 and isinstance(map, SortedMap):
            c = map.comparator()
            if c == self.comparator or (c is not None and c.__eq__(self.comparator)):
                self._mod_count += 1
                try:
                    self.__build_from_sorted(map_size, map.entry_set().__iter__(), None, None)
                except (IOError, BlockingIOError) as e:
                    pass

                return
        AbstractMap.put_all(map)

    def get_entry(self, key: Comparable) -> Map.Entry:
        if self.comparator is not None:
            return self.get_entry_using_comparator(key)

        if key is None:
            raise NonePointerException

        k = key
        p = self._root
        # while p is not None:
        #     cmp = k.compare_to()

    def get_first_entry(self) -> Generic:
        pass

    def __build_from_sorted(self, a, b, c, d):
        pass

    def get_entry_using_comparator(self, key: Comparable) -> Map.Entry:
        pass

    def __successor(self, e) -> bool:
        pass

    def val_equals(self, this, that) -> bool:
        pass