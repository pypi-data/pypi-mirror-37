from typing import Iterable

from stdlib.linear_ds.queue import Queue


class RedBlackBST(object):
    class __Node(object):
        def __init__(self, key, val, color, size):
            self.key = key
            self.val = val
            self.color = color
            self.size = size
            self.left = None
            self.right = None

    def __init__(self):
        self.__RED = True
        self.__BLACK = False
        self.root = None

    def __is_red(self, x: type(__Node)) -> bool:
        if x is None:
            return False
        return x.color == self.__RED

    def __size(self, x: __Node) -> int:
        if x is None:
            return 0
        return x.size

    def __sizeof__(self) -> int:
        return self.__size(self.root)

    def __empty__(self):
        return self.root.__sizeof__ == 0

    def get(self, key: object):
        if key is None:
            raise ValueError('argument to get() is None')
        return self.__get(self.root, key)

    def __get(self, x: type(__Node), key: object):
        while x is not None:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x.val

        return None

    def __contains__(self, key: object) -> bool:
        return self.get(key) is not None

    def put(self, key: object, val: object):
        if key is None:
            raise ValueError("first argument to put() is None")
        if val is None:
            self.delete(key)
            return

        self.root = self.__put(self.root, key, val)
        self.root.color = self.__BLACK

    def __put(self, h: type(__Node), key: object, val: object) -> type(__Node):
        if h is None:
            return self.__Node(key, val, self.__RED, 1)

        if key < h.key:
            h.left = self.__put(h.left, key, val)
        elif key > h.key:
            h.right = self.__put(h.right, key, val)
        else:
            h.val = val

        if self.__is_red(h.right) and not self.__is_red(h.left):
            h = self.__rotate_left(h)
        if self.__is_red(h.left) and self.__is_red(h.left.left):
            h = self.__rotate_right(h)
        if self.__is_red(h.left) and self.__is_red(h.right):
            self.__flip_colors(h)
        h.size = self.__size(h.left) + self.__size(h.right) + 1

        return h

    def delete_min(self):
        if self.__empty__():
            raise IndexError("BST underflow")

        if not self.__is_red(self.root.left) and not self.__is_red(self.root.right):
            self.root.color = self.__RED

        self.root = self.__delete_min(self.root)
        if not self.__empty__():
            self.root.color = self.__BLACK

    def __delete_min(self, h: type(__Node)):
        if h.left is None:
            return None

        if not self.__is_red(h.left) and not self.__is_red(h.left.left):
            h = self.__move_red_left(h)

        h.left = self.__delete_min(h.left)
        return self.__balance(h)

    def delete_max(self):
        if self.__empty__():
            raise IndexError("BST underflow")

        if not self.__is_red(self.root.left) and not self.__is_red(self.root.right):
            self.root.color = self.__RED

        self.root = self.__delete_max(self.root)
        if not self.__empty__():
            self.root.color = self.__BLACK

    def __delete_max(self, h: type(__Node)) -> type(__Node):
        if self.__is_red(h.left):
            h = self.__rotate_right(h)

        if h.right is None:
            return None

        if not self.__is_red(h.right) and not self.__is_red(h.right.left):
            h = self.__move_red_right(h)

        h.right = self.__delete_max(h.right)
        return self.__balance(h)

    def delete(self, key: object):
        if key is None:
            raise ValueError('argument to delete() is None')

        if not self.__contains__(key):
            return

        if not self.__is_red(self.root.left) and not self.__is_red(self.root.right):
            self.root.color = self.__RED

        self.root = self.__delete(self.root, key)
        if not self.__empty__():
            self.root.color = self.__BLACK

    def __delete(self, h: type(__Node), key: object) -> type(__Node):
        if key < h.key:
            if not self.__is_red(h.left) and not self.__is_red(h.left.left):
                h = self.__move_red_left(h)
            h.left = self.__delete(h.left, key)

        else:
            if self.__is_red(h.left):
                h = self.__rotate_right(h)
            if key == h.key and h.right is None:
                return None
            if not self.__is_red(h.right) and not self.__is_red(h.right.left):
                h = self.__move_red_right(h)
            if key == h.key:
                x = self.__min(h.right)
                h.key = x.key
                h.val = x.val
                h.right = self.__delete_min(h.right)

            else:
                h.right = self.__delete(h.right, key)

        return self.__balance(h)

    """
    ***     Red-Black tree helpers      ***
    """

    def __rotate_right(self, h: type(__Node)) -> type(__Node):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = x.right.color
        x.right.color = self.__RED
        x.__sizeof__ = h.__sizeof__
        h.__sizeof__ = self.__size(h.left) + self.__size(h.right) + 1
        return x

    def __rotate_left(self, h: type(__Node)) -> type(__Node):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = x.left.color
        x.left.color = self.__RED
        x.__sizeof__ = h.__sizeof__
        h.__sizeof__ = self.__size(h.left) + self.__size(h.right) + 1
        return x

    def __flip_colors(self, h: type(__Node)):
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    def __move_red_left(self, h: type(__Node)) -> type(__Node):
        self.__flip_colors(h)
        if self.__is_red(h.right.left):
            h.right = self.__rotate_right(h.right)
            h = self.__rotate_left(h)
            self.__flip_colors(h)

        return h

    def __move_red_right(self, h: type(__Node)) -> type(__Node):
        self.__flip_colors(h)
        if self.__is_red(h.left.left):
            h = self.__rotate_right(h)
            self.__flip_colors(h)

        return h

    def __balance(self, h: type(__Node)) -> type(__Node):
        if self.__is_red(h.right):
            h = self.__rotate_left(h)
        if self.__is_red(h.left) and self.__is_red(h.left.left):
            h = self.__rotate_right(h)
        if self.__is_red(h.left) and self.__is_red(h.right):
            self.__flip_colors(h)

        h.size = self.__size(h.left) + self.__size(h.right) + 1
        return h

    def height(self) -> int:
        return self.__height(self.root)

    def __height(self, x: type(__Node)) -> int:
        if x is None:
            return -1

        return 1 + max(self.__height(x.left), self.__height(x.right))

    def min(self) -> object:
        if self.__empty__():
            raise IndexError("calls min() with empty dictionary")
        return self.__min(self.root).key

    def __min(self, x: type(__Node)) -> type(__Node):
        if x.left is None:
            return x
        else:
            return self.__min(x.left)

    def max(self) -> object:
        if self.__empty__():
            raise IndexError("calls max() with empty dictionary")

        return self.__max(self.root).key

    def __max(self, x: type(__Node)) -> type(__Node):
        if x.right is None:
            return x
        else:
            return self.__max(x.right)

    def floor(self, key: object) -> object:
        if key is None:
            raise ValueError("argument to floor() is None")

        if self.__empty__():
            raise IndexError('calls floor() with empty dictionary')

        x = self.__floor(self.root, key)
        if x is None:
            return None
        else:
            return x.key

    def __floor(self, x: type(__Node), key: object) -> type(__Node):
        if x is None:
            return None
        if key == x.key:
            return x

        if key < x.key:
            return self.__floor(x.left, key)

        t = self.__floor(x.right, key)
        if t is not None:
            return t
        else:
            return x

    def ceiling(self, key: object) -> object:
        if key is None:
            raise ValueError('argument to ceiling() is None')
        if self.__empty__():
            raise IndexError('calls ceiling() with empty dictionary')

        x = self.__ceiling(self.root, key)
        if x is None:
            return None
        else:
            return x.key

    def __ceiling(self, x: type(__Node), key: object) -> type(__Node):
        if x is None:
            return None
        if key == x.key:
            return x
        if key > x.key:
            return self.__ceiling(x.right, key)
        t = self.__ceiling(x.left, key)
        if t is not None:
            return t
        else:
            return x

    def select(self, k: int) -> object:
        if k < 0 or k >= self.__sizeof__():
            raise ValueError("argument to select() is invalid: {}".format(k))
        x = self.__select(self.root, k)
        return x.key

    def __select(self, x: type(__Node), k: int) -> type(__Node):
        t = self.__size(x.left)
        if t > k:
            return self.__select(x.left, k)
        elif t < k:
            return self.__select(x.right, k - t - 1)
        else:
            return x

    def rank(self, key: object) -> int:
        if key is None:
            raise ValueError("argument to rank() is None")
        return self.__rank(key, self.root)

    def __rank(self, key: object, x: type(__Node)) -> int:
        if x is None:
            return 0
        if key < x.key:
            return self.__rank(key, x.left)
        elif key > x.key:
            return 1 + self.__size(x.left) + self.__rank(key, x.right)
        else:
            return self.__size(x.left)

    def keys(self) -> Iterable():
        if self.__empty__():
            return Queue()
        return self.keyss(self.min(), self.max())

    def keyss(self, lo: object, hi: object) -> type(Queue):
        if lo is None:
            raise ValueError("first argument to keys() is None")
        if hi is None:
            raise ValueError("second argument to keys() is None")

        queue = Queue()
        self.__keys(self.root, queue, lo, hi)
        return queue

    def __keys(self, x: type(__Node), queue: type(Queue), lo: object, hi: object):
        if x is None:
            return
        if lo < x.key:
            self.__keys(x.left, queue, lo, hi)
        if lo <= x.key <= hi:
            queue.enqueue(x.key)
        if hi > x.key:
            self.__keys(x.right, queue, lo, hi)

    def size(self, lo: object, hi: object) -> int:
        if lo is None:
            raise IndexError("first agrument to __sizeof__() is None")
        if hi is None:
            raise IndexError("second argument to __sizeof__() is None")

        if lo > hi:
            return 0
        if self.__contains__(hi):
            return self.rank(hi) - self.rank(lo) + 1
        else:
            return self.rank(hi) - self.rank(lo)

    def check(self) -> bool:
        if not self.__is_bst():
            print("Not in symetric order")
        if not self.__is_size_consistent():
            print("Subtree counts not consistent")
        if not self.__is_rank_consistent():
            print("Ranks not consistent")
        if not self.__is_23():
            print("Not a 2-3 tree")
        if not self.__is_balanced():
            print("Not balanced")
        return self.__is_bst() and self.__is_size_consistent() and self.__is_rank_consistent() and self.__is_23() \
            and self.__is_balanced()

    def __is_bst(self):
        return self.__is_bst_node(self.root, None, None)

    def __is_bst_node(self, x: type(__Node), min: object, max: object) -> bool:
        if x is None:
            return True
        if min is not None and x.key <= min:
            return False
        if max is not None and x.key >= max:
            return False
        return self.__is_bst_node(x.left, min, x.key) and self.__is_bst_node(x.right, x.key, max)

    def __is_size_consistent(self) -> bool:
        return self.__is_size_consistent_node(self.root)

    def __is_size_consistent_node(self, x: type(__Node)) -> bool:
        if x is None:
            return True
        if x.size != self.__size(x.left) + self.__size(x.right) + 1:
            return False
        return self.__is_size_consistent_node(x.left) and self.__is_size_consistent_node(x.right)

    def __is_rank_consistent(self) -> bool:
        for i in range(self.__sizeof__()):
            if i != self.rank(self.select(i)):
                return False

        for key in self.keys():
            if key != self.rank(key):
                return False

        return True

    def __is_23(self) -> bool:
        return self.__is_23_node(self.root)

    def __is_23_node(self, x: type(__Node)) -> bool:
        if x is None:
            return True
        if self.__is_red(x.right):
            return False
        if x != self.root and self.__is_red(x) and self.__is_red(x.left):
            return False
        return self.__is_23_node(x.left) and self.__is_23_node(x.right)

    def __is_balanced(self) -> bool:
        black = 0
        x = self.root
        while x is not None:
            if not self.__is_red(x):
                black += 1
            x = x.left

        return self.__is_balanced_node(self.root, black)

    def __is_balanced_node(self, x: type(__Node), black: int) -> bool:
        if x is None:
            return black == 0
        if not self.__is_red(x):
            black -= 1
        return self.__is_balanced_node(x.left, black) and self.__is_balanced_node(x.right, black)


def main():
    rbt = RedBlackBST()
    mylist = ['ammon', 'jade', 'jake', 'erin', 'nick']
    for i in range(5):
        rbt.put(mylist[i], i)

    print(rbt.select(1))
    for s in rbt.keys():
        print('{} {}'.format(s, rbt.get(s)))

    rbt.check()

    print('\n')


if __name__ == '__main__':
    main()
