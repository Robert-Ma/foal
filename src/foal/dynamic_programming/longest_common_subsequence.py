"""
Longest Common Subsequence

To use dynamic programming to find a `longest common subsequence (LCS)` of two
DNA sequences.

LCS algorithm

First, think about how you might compute an LCS recursively. Let:
    - C1 be the right-most character of S1
    - C2 be the right-most character of S2
    - S1' be S1 with C1 "chopped-off"
    - S2' be S2 with C2 "chopped-off"
There are three recursive subproblems:
    - L1 = LCS(S1', S2)
    - L2 = LCS(S1, S2')
    - L3 = LCS(S1', S2')
So, the solution to the original problem is whichever of these is the longest:
    - L1
    - L2
    - L3 appened with C1 if C1 equals C2, or L3 if C1 is not equals to C2
The base case is whenever S1 or S2 is a zero-length string. In this case, the
LCS of S1 and S2 is clearly a zero-length string.
(from https://www.ibm.com/developerworks/java/library/j-seqalign/?S_TACT=105AGX52&S_CMP=cn-a-j)
"""

import numpy as np
from foal.dynamic_programming import BioSeq, memoize


class _Cell:
    """
    Cell of Score Table

    Store score, and tracing back.
    """
    def __init__(self, score=None, row=None, col=None, prev_cell=None):
        self._score = score
        self._row = row
        self._column = col
        self._prev_cell = prev_cell

    def get_score(self):
        return self._score

    def set_prev_cell(self, cell):
        self._prev_cell = cell

    def get_prev_cell(self):
        return self._prev_cell

    def get_row(self):
        return self._row

    def get_column(self):
        return self._column

    def __str__(self):
        return self._score

    def __repr__(self):
        format_string = ''
        if self._prev_cell:
            format_string = '({}, {}, {})'.format(self.get_score(),
                                                  self._prev_cell.get_row(),
                                                  self._prev_cell.get_column())
        else:
            format_string = '({}, {}, {})'.format(self.get_score(), None, None)
        return format_string


class LCS:
    """
    Longest Common Subsequence

    To use dynamic programming to find a `longest common subsequence (LCS)` of
    two DNA sequences.
    """
    def __init__(self, seq_left, seq_top):
        """
        Args:
            seq_left: a BioSeq object
            seq_top: a BioSeq object
        """
        if not isinstance(seq_left, BioSeq) or not isinstance(seq_top, BioSeq):
            raise TypeError("Object should be BioSeq.")
        self._seq_left = seq_left
        self._seq_top = seq_top
        self._score_table = np.zeros((len(self._seq_left) + 1,
                                      len(self._seq_top) + 1), dtype=_Cell)
        self._cal_score_table()

    @memoize()
    def _cal_one_cell_score(self, row, col):
        """
        Calculate one cell score

        Choose order: left-top -> top -> left.

        Returns:
            (match_score, cell_ptr):
                match_score: cell score, a float
                cell_ptr: the previe cell, a _Cell object or None
        """

        match_score = 0.
        cell_ptr = None

        if row == 0 or col == 0:
            match_score = 0.
            cell_ptr = None
        else:
            top_score = self._score_table[row - 1, col].get_score()
            left_score = self._score_table[row, col - 1].get_score()
            left_top_score = self._score_table[row - 1, col - 1].get_score()

            if self._seq_left[row - 1] == self._seq_top[col - 1]:
                # choose left-top cell
                match_score = left_top_score + 1.0
                cell_ptr = self._score_table[row - 1, col - 1]
            else:
                # choose left-top cell as temp cell
                match_score = left_top_score
                cell_ptr = self._score_table[row - 1, col - 1]

            if top_score > match_score:
                match_score = top_score
                cell_ptr = self._score_table[row - 1, col]
            elif left_score > match_score:
                match_score = left_score
                cell_ptr = self._score_table[row, col - 1]

        return match_score, cell_ptr

    def _cal_score_table(self):
        """
        Calculate very cell scores using loop
        """
        for row in range(len(self._seq_left) + 1):
            for col in range(len(self._seq_top) + 1):
                match_score, cell_ptr = self._cal_one_cell_score(row, col)
                self._score_table[row, col] = _Cell(match_score, int(row),
                                                    int(col), cell_ptr)

    def get_score_table(self):
        """
        Get all cells' scores, it is a numpy.array
        """
        return self._score_table

    def get_trace_back(self):
        """
        Tracing back to find an actual LCS.
        """
        lcs = list()
        cur_cell = self._score_table[-1, -1]

        while cur_cell.get_prev_cell() is not None:
            prev_cell = cur_cell.get_prev_cell()

            if cur_cell.get_score() == prev_cell.get_score() + 1:
                common_char = self._seq_left[cur_cell.get_row() - 1]
                lcs.append(common_char)

            cur_cell = prev_cell

        lcs.reverse()
        return lcs
