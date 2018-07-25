"""
Sequence Alignment

A homologous DNA sequence alignment. The Needleman-Wunsch algorithm is used for
computing global alignments, and the Smith-Waterman algorithm is used for
computing local alignments.

By the way, BioPython (https://github.com/biopython/biopython) is the expert
tool for this problem.
"""

import numpy as np

from .biological_data import BioSeq, ScoreCell
from .memoize import memoize

MATCH = +1
MISMATCH_INDEL = -1


class Align:
    """
    Sequence Alignment

    There are three situation:
        (1) Match: The two letters at the currnt index the same.
        (2) Mismatch: The two letters at the currnt index are different.
        (3) Indel(INsertion or DELetion): The best alignment involves one
            letter aligning to a gap in the other string.
    For now, the system used by Needleman and Wunsch will be used:
        - Match: +1
        - Mismatch or Indel: -1
    For the example above, the score of the alignment would be 0:
        GCATG-CU
        | ||  |
        G-ATTACA
    score = (-1) * 4 + (+1) * 4 = 0

    (From: https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm)
    """

    def __init__(self, seq_left, seq_top, match_score=MATCH,
                 mismatch_score=MISMATCH_INDEL, indel_score=MISMATCH_INDEL):
        """
        Args:
            seq_left: a bd.BioSeq object
            seq_top: a bd.BioSeq object
            match_score: match rewards
            mismatch_score: mismatch penalty
            indel_score: insert or delete penalty
        """
        if not isinstance(seq_left, BioSeq) or not isinstance(seq_top, BioSeq):
            raise TypeError("Object should be bd.BioSeq.")
        self._seq_left = seq_left
        self._seq_top = seq_top

        self._score_table = np.zeros((len(self._seq_left) + 1,
                                      len(self._seq_top) + 1), dtype=ScoreCell)
        self._cal_score_table()

        self._match = match_score  # match score
        self._mismatch = mismatch_score  # mismatch score
        self._indel = indel_score  # insert or delete score

    @memoize()
    def _cal_one_cell_score(self, row, col):
        """
        Calculate one cell score

        Choose order: left-top -> top -> left.

        Returns:
            (match_score, cell_ptr):
                match_score: cell score, a float
                cell_ptr: the previe cedtype=bd.ScoreCell object or None
        """

        match_score = 0
        prev_ptr = None

        if row == 0 and col == 0:
            match_score = 0
            prev_ptr = None
        elif row == 0 and col != 0:
            left_cell = self._score_table[row, col - 1]
            left_cell_score = left_cell.get_score()
            match_score = left_cell_score + MISMATCH_INDEL   # Gap
            prev_ptr = left_cell
        elif row != 0 and col == 0:
            top_cell = self._score_table[row - 1, col]
            top_cell_score = top_cell.get_score()
            match_score = top_cell_score + MISMATCH_INDEL  # Gap
            prev_ptr = top_cell
        else:
            top_cell = self._score_table[row - 1, col]
            left_cell = self._score_table[row, col - 1]
            top_left_cell = self._score_table[row - 1, col - 1]

            if self._seq_left[row - 1] == self._seq_top[col - 1]:
                score_from_left = left_cell.get_score() + self._indel  # Gap
                score_from_top = top_cell.get_score() + self._indel    # Gap
                score_from_top_left = (top_left_cell.get_score() +
                                       self._match)  # Match
            else:
                score_from_left = left_cell.get_score() + self._indel  # Gap
                score_from_top = top_cell.get_score() + self._indel    # Gap
                score_from_top_left = (top_left_cell.get_score() +
                                       self._mismatch)              # Mismatch

            scores = {
                'top_left': (score_from_top_left, top_left_cell),
                'top': (score_from_top, top_cell),
                'left': (score_from_left, left_cell),
            }
            (match_score, prev_ptr) = max(scores.items(),
                                          key=lambda x: x[1][0])[1]

        return match_score, prev_ptr

    def _cal_score_table(self):
        """
        Calculate very cell scores using loop
        """
        for row in range(len(self._seq_left) + 1):
            for col in range(len(self._seq_top) + 1):
                match_score, cell_ptr = self._cal_one_cell_score(row, col)
                self._score_table[row, col] = ScoreCell(match_score, int(row),
                                                        int(col), cell_ptr)

    def get_score_table(self):
        """
        Get all cells' scores, it is a numpy.array
        """
        return self._score_table

    def get_trace_back(self):
        """
        Tracing back to find an actual align sequences.

        Returns:
        Returns two list(), which contain the alignment.
        """
        seq_top_aling = list()
        seq_left_aling = list()

        cur_cell = self._score_table[-1, -1]

        while cur_cell.get_prev_cell() is not None:
            prev_cell = cur_cell.get_prev_cell()

            if (cur_cell.get_row() == prev_cell.get_row() + 1 and
                (cur_cell.get_column() == prev_cell.get_column() + 1)):
                # prev_cell is top_left
                seq_left_aling.append(self._seq_left[cur_cell.get_row() - 1])
                seq_top_aling.append(self._seq_top[cur_cell.get_column() - 1])
            elif (cur_cell.get_row() == prev_cell.get_row() + 1 and
                  cur_cell.get_column() == prev_cell.get_column()):
                # prev_cell is top
                seq_left_aling.append(self._seq_left[cur_cell.get_row() - 1])
                seq_top_aling.append('-')
            elif (cur_cell.get_row() == prev_cell.get_row() and
                  cur_cell.get_column() == prev_cell.get_column() + 1):
                # prev_cell is left
                seq_left_aling.append('-')
                seq_top_aling.append(self._seq_top[cur_cell.get_column() - 1])

            cur_cell = prev_cell

        seq_left_aling.reverse()
        seq_top_aling.reverse()
        return seq_left_aling, seq_top_aling

    def display(self):
        left_aling, top_aling = self.get_trace_back()
        match_sign = list()

        for i in range(len(left_aling)):
            if left_aling[i] == top_aling[i]:
                match_sign.append('|')
            else:
                match_sign.append(' ')

        left_aling_str = ''.join(left_aling)
        top_aling_str = ''.join(top_aling)
        match_sign_str = ''.join(match_sign)

        print('{}\n{}\n{}'.format(top_aling_str, match_sign_str,
                                  left_aling_str))
