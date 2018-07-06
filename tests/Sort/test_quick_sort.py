from eagle.Sort import quick_sort


def test_quick_sort():
    S = [15, 22, 13, 27, 12, 10, 20, 25]
    result = quick_sort(S)
    assert result == [10, 12, 13, 15, 20, 22, 25, 27]
