"""
Mergesort: sort n items in nondecreasing order.
"""
import math


def merge_sort(Sequence):
    if len(Sequence) <= 1:
        return Sequence
    middle = math.floor(len(Sequence) / 2)
    head_Seq = Sequence[:middle]
    tail_Seq = Sequence[middle:]

    sorted_head_Seq = merge_sort(head_Seq)
    sorted_tail_Seq = merge_sort(tail_Seq)

    return _merge_two_sorted_list(sorted_head_Seq, sorted_tail_Seq)


def _merge_two_sorted_list(sorted_list_head, sorted_list_tail):
    """Merge two soretd list into one soreted list."""
    sorted_list_result = list()
    head_index = 0
    tail_index = 0
    len_head = len(sorted_list_head)
    len_tail = len(sorted_list_tail)

    while head_index < len_head and tail_index < len_tail:
        print(sorted_list_head, ' : ', sorted_list_tail)
        if sorted_list_head[head_index] < sorted_list_tail[tail_index]:
            sorted_list_result.append(sorted_list_head[head_index])
            head_index += 1
        elif sorted_list_head[head_index] > sorted_list_tail[tail_index]:
            sorted_list_result.append(sorted_list_tail[tail_index])
            tail_index += 1
        elif sorted_list_head[head_index] == sorted_list_tail[tail_index]:
            sorted_list_result.append(sorted_list_head[head_index])
            sorted_list_result.append(sorted_list_tail[tail_index])
            head_index += 1
            tail_index += 1

    if head_index < len_head:
        sorted_list_result.extend(sorted_list_head[head_index:])
    elif tail_index < len_tail:
        sorted_list_result.extend(sorted_list_tail[tail_index:])

    return sorted_list_result
