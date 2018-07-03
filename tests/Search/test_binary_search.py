import pytest
import basalg


def test_search_element_in_seq():
    S = [1, 5, 2, 6, 9]
    assert basalg.binary_search(S, 2) is True


def test_search_element_not_in_seq():
    pass
