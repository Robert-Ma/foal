import eagle.Search
import pytest


def test_search_element_in_seq():
    S = [1, 2, 5, 6, 9]
    assert eagle.Search.binary_search(S, 2) == 1


def test_search_element_not_in_seq():
    S = [1, 2, 5, 6, 9]
    assert eagle.Search.binary_search(S, 10) == -1


def test_search_with_unsorted_list():
    S = [2, 1, 6, 3, 8]
    with pytest.raises(ValueError):
        eagle.Search.binary_search(S, 3)
