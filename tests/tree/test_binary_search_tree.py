import sys
from io import StringIO

import pytest

from foal.tree import BinarySearchTree


def test_tree_build(init_tree):
    old_stdout = sys.stdout

    result = StringIO()
    sys.stdout = result

    init_tree.display()

    sys.stdout = old_stdout

    assert(result.getvalue() == '5, 10, 15, 20, 25, 30, 35, ')


def test_search_item_in_tree(init_tree):
    search_result = init_tree.search(10)
    expected = True
    assert search_result == expected


def test_search_item_not_in_tree(init_tree):
    search_result = init_tree.search(11)
    expected = False
    assert search_result == expected


def test_delete_leaf(init_tree):
    tree = init_tree
    tree.delete(5)

    expected_tree = BinarySearchTree()
    expected_tree.insert(20)
    expected_tree.insert(10)
    expected_tree.insert(15)
    expected_tree.insert(30)
    expected_tree.insert(25)
    expected_tree.insert(35)

    assert tree == expected_tree


def test_delete_parent(init_tree):
    tree = init_tree
    tree.delete(10)

    expected_tree = BinarySearchTree()
    expected_tree.insert(20)
    expected_tree.insert(15)
    expected_tree.insert(5)
    expected_tree.insert(30)
    expected_tree.insert(25)
    expected_tree.insert(35)

    assert tree == expected_tree


def test_delete_root(init_tree):
    tree = init_tree
    tree.delete(20)

    expected_tree = BinarySearchTree()
    expected_tree.insert(30)
    expected_tree.insert(25)
    expected_tree.insert(10)
    expected_tree.insert(5)
    expected_tree.insert(15)
    expected_tree.insert(35)

    assert tree == expected_tree


def test_two_trees_equal(init_tree):
    t2 = BinarySearchTree()
    t2.insert(20)
    t2.insert(10)
    t2.insert(5)
    t2.insert(15)
    t2.insert(30)
    t2.insert(25)
    t2.insert(35)
    assert t2 == init_tree


def test_two_trees_not_equal(init_tree):
    print(init_tree)
    t2 = BinarySearchTree()
    t2.insert(20)
    t2.insert(10)
    t2.insert(5)
    t2.insert(15)
    t2.insert(30)
    t2.insert(25)
    assert t2 != init_tree


@pytest.fixture()
def init_tree():
    t = BinarySearchTree()
    t.insert(20)
    t.insert(10)
    t.insert(5)
    t.insert(15)
    t.insert(30)
    t.insert(25)
    t.insert(35)
    return t
