import time


class BST:
    """
    Tree node: left and right child + data which can be any object
    """

    def __init__(self, data):
        """
        Node constructor
        :param data: node data object
        """
        self.left = None
        self.right = None
        self.data = None
        # Initialize the empty tree

        data_types = ['list', 'set']
        if type(data).__name__ in data_types:
            start = time.clock()
            for i in data:
                if self.data is None:
                    self.data = i
                else:
                    self.insert(i)
            end = time.clock()
            print("Total time to initialize set or list", end - start)
        # elif type(data).__name__ == 'set':
        #     for i in data:
        #         if self.data is None
        else:
            self.data = data

    def insert(self, data):
        """
        Insert new node with data
        :param data: node data object to insert
        :return:
        """
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BST(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BST(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def lookup(self, data, parent=None):
        """
        Lookup node containing data
        :param data: node data object to look up
        :param parent: node's parent
        :return: node and node's parent if found or None, None
        """

        if data < self.data:
            if self.left is None:
                return None, None
            return self.left.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            return self, parent

    def delete(self, data):
        """
        Delete node containing data
        :param data: node's content to delete
        :return:
        """
        # get node containing data
        node, parent = self.lookup(data)
        children_count = None
        if node is not None:
            children_count = node.children_count()

        if children_count == 0:
            # if node has no children, just remove it
            if parent:
                if parent.left is node:
                    parent.left = None
                else:
                    parent.right = None
                del node

            else:
                self.data = None

        elif children_count == 1:
            # if node has 1 child
            # replace node with its child
            if node.left:
                n = node.left
            else:
                n = node.right

            if parent:
                if parent.left is node:
                    parent.left = n
                else:
                    parent.right = n
                del node
            else:
                self.left = n.left
                self.right = n.right
                self.data = n.data

        else:
            # if node has 2 children
            # find its successor
            parent = node
            successor = node.right
            while successor.left:
                parent = successor
                successor = successor.left
            # replace node data by its successor data
            node.data = successor.data
            # fix successor's parent's child
            if parent.left == successor:
                parent.left = successor.right
            else:
                parent.right = successor.right

    def children_count(self):
        """
        Returns the number of children
        :return: number of children: 0, 1, 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt

    def print_tree(self):
        """
        Print tree content inorder
        :return: Print tree content inorder
        """
        if self.left:
            self.left.print_tree()
        print(self.data),
        if self.right:
            self.right.print_tree()

    def compare_trees(self, node):
        """
        Compare 2 trees
        :param node: tree's root node to compare to
        :return: True if the tree passed is identical to this tree
        """
        if node is None:
            return False

        if self.data != node.data:
            return False

        res = True
        if self.left is None:
            if node.left:
                return False
        else:
            res = self.left.compare_trees(node.left)

        if res is False:
            return False

        if self.right is None:
            if node.right:
                return False
        else:
            res = self.right.compare_trees(node.right)

        return res

    def tree_data(self):
        """
        Generator to get the tree nodes data
        :return: Generator to get the tree nodes data
        """
        # we use a stack to traverse the tree in a non-recursive way
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:  # we are returning so we pop the node and we yield it
                node = stack.pop()
                yield node.data
                node = node.right


