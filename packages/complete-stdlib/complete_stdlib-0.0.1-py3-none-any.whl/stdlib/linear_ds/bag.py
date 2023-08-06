from stdlib.abstracts.iterator import Iterator


class Bag(object):
    class Node(object):
        def __init__(self):
            self.item = None
            self.next = type(self)

    class ListIterator(Iterator):
        def __has_next__(self) -> bool:
            return type(self.__current.next).__name__ == 'Node'

        def __remove__(self):
            return NotImplementedError

        def __init__(self, first):
            self.__current = first

        def __next__(self):
            if not self.__has_next__():
                raise StopIteration

            item = self.__current.item
            self.__current = self.__current.next
            return item

    def __init__(self):
        self.__first = self.Node()
        self.__n = 0

    def __iter__(self):
        return self.ListIterator(self.__first)

    def __empty__(self):
        return self.__first is None

    def __sizeof__(self):
        return self.__n

    def add(self, item):
        old_first = self.__first
        self.__first = self.Node()
        self.__first.item = item
        self.__first.next = old_first
        self.__n += 1


def main():
    bag = Bag()
    bag.add(1)
    bag.add(3)
    bag.add(5)
    for i in bag:
        print(i)


if __name__ == '__main__':
    main()
