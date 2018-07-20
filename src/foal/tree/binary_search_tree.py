"""
Binary Search Tree

This module implements binary search tree algorithm, which contains Node class,
and BinarySearchTree class. This module does not contain many complex methods,
and it just a simple implemention.
"""


class Node:
    """
    Node

    This class contains value, parent node and children node.
    """

    def __init__(self, value=None, left=None, right=None, parent=None):
        """
        Args:
            value: any type
            left: a Node object, left child node
            right: a Node object, right child node
            parent: a Node object, parent node
        """
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def insert(self, value):
        """
        Insert values, Put the smaller value in the left child and the
        larger value in the right child.
        """
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
        return True if self._get(value) else False

    def _get(self, value):
        if self.value == value:
            return self
        elif self.value > value and (self.left is not None):
            return self.left._get(value)
        elif self.value < value and (self.right is not None):
            return self.right._get(value)
        return None

    def _is_child(self):
        return self._is_left_child() or self._is_right_child()

    def _is_left_child(self):
        return self.parent and (self.parent.left == self)

    def _is_right_child(self):
        return self.parent and (self.parent.right == self)

    def _is_leaf(self):
        return not (self.left or self.right)

    def _is_parent(self):
        return (self.parent is not None) and (self._has_child() is not False)

    def _is_root(self):
        return not self.parent

    def _has_left_child(self):
        return True if (self.left is not None) else False

    def _has_right_child(self):
        return True if (self.right is not None) else False

    def _has_child(self):
        return self._has_left_child() or self._has_right_child()

    def _has_left_right_children(self):
        return self._has_left_child() and self._has_right_child()

    def _display(self):
        """
        print Nodes with `left -> middle -> right` order
        """
        if self.left is not None:
            self.left._display()

        print(self.value, end=", ")

        if self.right is not None:
            self.right._display()

    def __repr__(self):
        return '{}'.format(self.value)


class BinarySearchTree:
    """
    Binary Search Tree

    This binary search tree class implements such as adding values, deleting
    values, comparing two trees, etc.
    """
    def __init__(self):
        self.root = None

    def insert(self, value):
        """
        The first value should be the root node. Put the smaller value in the
        left subtree and the larger value in the right subtree.
        """
        if self.root:
            self.root.insert(value)
        else:
            self.root = Node(value)

    def display(self):
        if self.root:
            self.root._display()
        else:
            print('Binary Search Tree is empty.\n')

    def search(self, value):
        """
        Determine if a value is in the binary search tree.
        """
        if self.root is None:
            return False
        else:
            return self.root.search(value)

    def _delete_root(self, value):
        cur_node = self.get(value)
        if self.root._has_child() is False:
            self.root = None
        elif self.root._has_left_child() and not self.root._has_right_child():
            self.root = cur_node.left
            cur_node.left.parent = None
            cur_node.left = None
        elif not self.root._has_left_child() and self.root._has_right_child():
            self.root = cur_node.right
            cur_node.right.parent = None
            cur_node.right = None
        elif self.root._has_left_child() and self.root._has_right_child():
            _move_left_children_to_right(self.root)
            self.root = cur_node.right
            cur_node.right.parent = None
            cur_node.right = Node

        del cur_node

    def _delete_parent(self, value):
        cur_node = self.get(value)
        # Get children, right child is prefer heir node. This node is a parent
        # node, so it must have left child node or right child node.
        prefer_heir_child = cur_node.right if cur_node.right else cur_node.left

        if cur_node._has_left_child() and not cur_node._has_right_child():
            prefer_heir_child.parent = cur_node.parent
            cur_node.left = None
        elif (not cur_node._has_left_child()
              and cur_node._has_right_child()):
            prefer_heir_child.parent = cur_node.parent
            cur_node.right = None
        elif cur_node._has_left_child() and cur_node._has_right_child():
            _move_left_children_to_right(cur_node)
            prefer_heir_child.parent = cur_node.parent
            cur_node.right = None

        if cur_node._is_left_child():
            cur_node.parent.left = prefer_heir_child
            cur_node.parent = None

        elif cur_node._is_right_child():
            cur_node.parent.right = prefer_heir_child
            cur_node.parent = None

        del cur_node

    def _delete_leaf(self, value):
        cur_node = self.get(value)
        if cur_node._is_left_child():
            cur_node.parent.left = None
        elif cur_node._is_right_child():
            cur_node.parent.right = None

        cur_node.parent = None
        del cur_node

    def delete(self, value):
        """
        Delete a value from binary search tree.
        """
        cur_node = self.get(value)
        if not cur_node:
            raise ValueError('No such value: {}'.format(value))

        if cur_node._is_root():
            self._delete_root(value)
        elif cur_node._is_leaf():
            self._delete_leaf(value)
        elif cur_node._is_parent():
            self._delete_parent(value)

    def get(self, value):
        """To get the node containing value."""
        if self.root is None:
            return None
        else:
            return self.root._get(value)

    def __eq__(self, other):
        """
        Compare two BinarySearchTree

        Compare every node of these two trees

        Args:
            other: a BinarySearchTree object
        """
        if not isinstance(other, BinarySearchTree):
            raise TypeError('A nother object should be a BinarySearchTree.')
        if self.root is not None and other.root is not None:
            return _walk_equal(self.root, other.root)
        elif self.root ^ other.root:
            return False
        elif self.root is None and other.root is None:
            return True

    def __ne__(self, other):
        return not self.__eq__(other)


def _walk_equal(bstree_left, bstree_right):
    """
    Compare every node using recursive, once two node are not equal, return
    False, or return True.

    Args:
        bstree_left: a Node object
        bstree_right: a Node object

    Returns:
        True: two BinarySearchTree are equal
        False: two BinarySearchTree are not equal
    """

    ptr_left = bstree_left
    ptr_right = bstree_right

    if ptr_left and ptr_right:
        compare_val = ptr_left.value == ptr_right.value
        compare_left = _walk_equal(ptr_left.left, ptr_right.left)
        compare_right = _walk_equal(ptr_left.right, ptr_right.right)
        return compare_val and compare_left and compare_right
    return ptr_left == ptr_right


def _move_left_children_to_right(node_ref):
    """
    Move node_ref.left to node_to_refactor.right

    Args:
        node_ref: Node object, which has both left and right child.
    Returns:
    """
    if not node_ref._has_left_child() or not node_ref._has_right_child():
        raise ValueError('node_ref should have both left and right child.')
    most_left_node = node_ref.right
    while most_left_node.left:
        most_left_node = most_left_node.left

    most_left_node.left = node_ref.left
    node_ref.left.parent = most_left_node
    node_ref.left = None
