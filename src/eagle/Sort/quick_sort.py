"""
Quick Sort

sort sequence in nondecreasing order.
"""


def quick_sort(Seq):
    """
    Quick Sort
    Sort sequence in nondecreasing order.
    """

    if len(Seq) <= 1:
        return Seq

    pivotpoint = 0
    pivotitem = Seq[pivotpoint]

    for idx, item in enumerate(Seq):
        if item < pivotitem:
            i = idx
            currentItem = Seq[idx]  # keep current item
            # move items
            while i > 0:
                Seq[i] = Seq[i - 1]
                i -= 1
            Seq[0] = currentItem  # move currnt item to the first
            pivotpoint += 1

    low = quick_sort(Seq[:pivotpoint])
    high = quick_sort(Seq[pivotpoint + 1:])
    result = _merge_low_pivot_high(low, pivotitem, high)
    return result


def _merge_low_pivot_high(low, pivotitem, high):
    """
    merge three parts
    """
    result = list()
    result.extend(low)
    result.append(pivotitem)
    result.extend(high)
    return result
