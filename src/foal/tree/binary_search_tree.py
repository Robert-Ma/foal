class Node:
    def __init__(self, value=None, left=None, right=None, parent=None):
        """
        @param left Node object or None
        @param right None object or None
        """
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def insert(self, value):
        if self.value is not None:
            if value < self.value:
                if self.left is None:
                    self.left = Node(value)
                    self.left.parent = self
                else:
                    self.left.insert(value)
            elif value > self.value:
                if self.right is None:
                    self.right = Node(value)
                    self.right.parent = self
                else:
                    self.right.insert(value)
        else:
            self.value = value

    def search(self, value):
        if self.value == value:
            return True
        elif self.value > value and (self.left is not None):
            return self.left.search(value)
        elif self.value < value and (self.right is not None):
            return self.right.search(value)
        return False

    def __display__(self):
        """
        print Nodes with `left -> middle -> right` order
        """
        if self.left is not None:
            self.left.__display__()

        print(self.value, end=", ")

        if self.right is not None:
            self.right.__display__()

    def __repr__(self):
        return '{}'.format(self.value)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root:
            self.root.insert(value)
        else:
            self.root = Node(value)

    def display(self):
        if self.root:
            self.root.__display__()
        else:
            print('Binary Search Tree is empty.')

    def search(self, value):
        if self.root is None:
            return False
        else:
            return self.root.search(value)
