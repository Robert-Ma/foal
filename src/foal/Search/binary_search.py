import math


def binary_search(Sequence, target):
    """
    Sequence: a sorted list (nondecreasing order)
    return index if target is in Sequence, or return -1.
    NOTE: -1 does not mean the last item of list.
    """
    if not _is_nondecreasing_sorted(Sequence):
        raise ValueError('Sequence should be a sorted list (nondecreasing order)')

    head = 0
    end = len(Sequence) - 1
    middle = math.floor((head + end) / 2)

    while head <= end:
        if Sequence[middle] == target:
            return middle
        elif Sequence[middle] < target:
            head = middle + 1
            middle = math.floor((head + end) / 2)
        elif Sequence[middle] > target:
            end = middle - 1
            middle = math.floor((head + end) / 2)

    return -1


def _is_nondecreasing_sorted(Sequence):
    return all(Sequence[i] <= Sequence[i+1] for i in range(len(Sequence) - 1))
