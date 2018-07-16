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

    assert(result.getvalue() == '1, 3, 8, 10, ')


def test_search_item_in_tree(init_tree):
    search_result = init_tree.search(10)
    expected = True
    assert search_result == expected


def test_search_item_not_in_tree(init_tree):
    search_result = init_tree.search(11)
    expected = False
    assert search_result == expected


@pytest.fixture()
def init_tree():
    t = BinarySearchTree()
    t.insert(3)
    t.insert(10)
    t.insert(8)
    t.insert(1)
    return t
