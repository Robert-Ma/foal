import foal.Sort as eso


def test_merge_sort_no_repeat_items():
    S = [27, 10, 12, 20, 25, 13, 15, 22]
    assert eso.merge_sort(S) == [10, 12, 13, 15, 20, 22, 25, 27]


def test_merge_sort_with_repeat_items():
    S = [27, 22, 10, 12, 20, 25, 13, 15, 12, 22]
    assert eso.merge_sort(S) == [10, 12, 12, 13, 15, 20, 22, 22, 25, 27]


def test_with_only_one_element():
    S = [1]
    assert eso.merge_sort(S) == [1]


def test_with_zero_element():
    S = []
    assert eso.merge_sort(S) == []
