"""
Sequence Alignment

A homologous DNA sequence alignment. The Needleman-Wunsch algorithm is used for
computing global alignments, and the Smith-Waterman algorithm is used for
computing local alignments.

If there are multiple alignments with same best score, Smith-Waterman algorithm
will choose only ONE of those alignments.

By the way, BioPython (https://github.com/biopython/biopython) is the expert
tool for this problem.

For more detail:
    (1) https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
    (2) https://en.wikipedia.org/wiki/Smith–Waterman_algorithm
"""


import numpy as np

from .biological_data import BioSeq, ScoreCell

MATCH = +2
MISMATCH = -1
GAP_OPEN = -2
GAP_EXTEND = -1


class GlobalAlign:
    """
    Sequence Alignment

    There are three situation:
        (1) Match: The two letters at the currnt index the same.
        (2) Mismatch: The two letters at the currnt index are different.
        (3) Gap: The best alignment involves one letter aligning to a gap
            in the other string.
    For now, the system used by Needleman and Wunsch (global alignments)
    will be used (default):
        - Match: +1
        - Mismatch: -1
        - Gap open: -2
        - Gap extend: -1
    (From: https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm)

    >>> from foal.dynamic_programming import BioSeq, GlobalAlign, LocalAlign
    >>> left = BioSeq('gattaga')
    >>> top = BioSeq('gcatgct')
    >>> global_align = GlobalAlign(left, top)
    >>> global_align.display()
    GCA-T-GCT
    | | | |
    G-ATTAG-A
    """
    def __init__(self, seq_left, seq_top,
                 match_score=MATCH,
                 mismatch_score=MISMATCH,
                 gap_open_score=GAP_OPEN,
                 gap_extend_score=GAP_EXTEND):
        """
        Args:
            seq_left: a bd.BioSeq object
            seq_top: a bd.BioSeq object
            match_score: match rewards
            mismatch_score: mismatch penalty
            gap_open_score: create a new gap (InDel)
            gap_extend_score: extend a exist gap
        """

        if not isinstance(seq_left, BioSeq) or not isinstance(seq_top, BioSeq):
            raise TypeError("Object should be bd.BioSeq.")
        self._seq_left = seq_left
        self._seq_top = seq_top
        self._score_table = np.zeros((len(self._seq_left) + 1,
                                      len(self._seq_top) + 1), dtype=ScoreCell)

        self._match = match_score  # match score
        self._mismatch = mismatch_score  # mismatch score
        self._gap_open = gap_open_score
        self._gap_extend = gap_extend_score

        self._cal_score_table()
        self._trace_back()

    def _cal_score_of_one_cell(self, row, col):
        """
        Calculate one cell score for global alignment (Needleman-Wunsch
        algorithm)

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
            if self._is_gap_open(row, col, left_cell):
                match_score = left_cell_score + self._gap_open   # Gap
            else:
                match_score = left_cell_score + self._gap_extend   # Gap
            prev_ptr = left_cell
        elif row != 0 and col == 0:
            top_cell = self._score_table[row - 1, col]
            top_cell_score = top_cell.get_score()
            if self._is_gap_open(row, col, top_cell):
                match_score = top_cell_score + self._gap_open  # Gap
            else:
                match_score = top_cell_score + self._gap_extend
            prev_ptr = top_cell
        else:
            match_score, prev_ptr = self._cal_score_non_zero_index(row, col)

        return match_score, prev_ptr

    def _is_gap_open(self, row, col, tmp_ptr_cell):
        """
        Determine if a new InDel has been created.
        """
        if not tmp_ptr_cell.get_prev_cell():
            return True
        ptr_cell_of_ptr_cell = tmp_ptr_cell.get_prev_cell()
        diff_row_ptr = tmp_ptr_cell.get_row() - ptr_cell_of_ptr_cell.get_row()
        diff_col_ptr = (tmp_ptr_cell.get_column() -
                        ptr_cell_of_ptr_cell.get_column())

        diff_row_cur = row - tmp_ptr_cell.get_row()
        diff_col_cur = col - tmp_ptr_cell.get_column()

        if ((diff_col_ptr + diff_row_ptr == 1) and (
                diff_col_cur + diff_row_cur == 1)):
            return True
        else:
            return False

    def _cal_score_non_zero_index(self, row, col):
        """
        Calculate scores for non-left and non-top edge table cells.
        """
        top_cell = self._score_table[row - 1, col]
        left_cell = self._score_table[row, col - 1]
        top_left_cell = self._score_table[row - 1, col - 1]

        if self._is_gap_open(row, col, left_cell):
            score_from_left = left_cell.get_score() + self._gap_open  # Gap
        else:
            score_from_left = left_cell.get_score() + self._gap_extend  # Gap

        if self._is_gap_open(row, col, top_cell):
            score_from_top = top_cell.get_score() + self._gap_open    # Gap
        else:
            score_from_top = top_cell.get_score() + self._gap_extend    # Gap

        if self._seq_left[row - 1] == self._seq_top[col - 1]:
            score_from_top_left = (top_left_cell.get_score() +
                                   self._match)  # Match
        else:
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
                match_score, cell_ptr = self._cal_score_of_one_cell(row, col)
                self._score_table[row, col] = ScoreCell(match_score, int(row),
                                                        int(col), cell_ptr)

    def get_score_table(self):
        """
        Get all cells' scores, it is a numpy.array
        """
        return self._score_table

    def _trace_back(self):
        """
        Tracing back to find an actual align sequences.
        """
        seq_top_aling = list()
        seq_left_aling = list()

        cur_cell = self._score_table[-1, -1]

        while cur_cell.get_prev_cell() is not None:
            prev_cell = cur_cell.get_prev_cell()

            if (cur_cell.get_row() == prev_cell.get_row() + 1 and (
                    cur_cell.get_column() == prev_cell.get_column() + 1)):
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
        self._align_left = seq_left_aling
        self._align_top = seq_top_aling

    def get_align_results(self):
        return self._align_left, self._align_top

    def display(self):
        """
        Print best alignments in an easy-to-read format.
        """
        left_aling, top_aling = self.get_align_results()
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


class LocalAlign:
    """
    Sequence Alignment

    There are three situation:
        (1) Match: The two letters at the currnt index the same.
        (2) Mismatch: The two letters at the currnt index are different.
        (3) Gap: The best alignment involves one letter aligning to a gap
            in the other string.
    For now, the system used by Needleman and Wunsch (global alignments)
    will be used (default):
        - Match: +1
        - Mismatch: -1
        - Gap open: -2
        - Gap extend: -1

    In this algorithm, if ScoreCell's score has multiple sources, only one of
    them is tracked.
    (From: https://en.wikipedia.org/wiki/Smith–Waterman_algorithm)

    >>> from foal.dynamic_programming import BioSeq, GlobalAlign, LocalAlign
    >>> left = BioSeq('gattaga')
    >>> top = BioSeq('gcatgct')
    >>> local_align = LocalAlign(left, top)
    >>> local_align.display()
    GCATGCT-
    | ||
    G-ATTAGA


    GCA-T-GCT
    | | | |
    G-ATTAGA-
    """
    def __init__(self, seq_left, seq_top,
                 match_score=MATCH,
                 mismatch_score=MISMATCH,
                 gap_open_score=GAP_OPEN,
                 gap_extend_score=GAP_EXTEND):
        """
        Args:
            seq_left: a bd.BioSeq object
            seq_top: a bd.BioSeq object
            match_score: match rewards
            mismatch_score: mismatch penalty
            gap_open_score: create a new gap (InDel)
            gap_extend_score: extend a exist gap
        """

        if not isinstance(seq_left, BioSeq) or not isinstance(seq_top, BioSeq):
            raise TypeError("Object should be bd.BioSeq.")
        self._seq_left = seq_left
        self._seq_top = seq_top
        self._score_table = np.zeros((len(self._seq_left) + 1,
                                      len(self._seq_top) + 1), dtype=ScoreCell)

        self._match = match_score  # match score
        self._mismatch = mismatch_score  # mismatch score
        self._gap_open = gap_open_score
        self._gap_extend = gap_extend_score

        self._max_score_cell = list()

        self._cal_score_table()
        self._trace_back()

    def _cal_score_of_one_cell(self, row, col):
        """
        Calculate one cell score for global alignment (Needleman-Wunsch
        algorithm)

        Choose order: left-top -> top -> left.

        Returns:
            (match_score, cell_ptr):
                match_score: cell score, a float
                cell_ptr: the previe cedtype=bd.ScoreCell object or None
        """

        match_score = 0.
        prev_ptr = None

        if row == 0 or col == 0:
            match_score = 0.
            prev_ptr = None
        else:
            match_score, prev_ptr = self._cal_score_non_zero_index(row, col)
            if match_score < 0:
                match_score = 0
                prev_ptr = None
        return match_score, prev_ptr

    def _is_gap_open(self, row, col, tmp_ptr_cell):
        """
        Determine if a new InDel has been created.
        """
        if not tmp_ptr_cell.get_prev_cell():
            return True
        ptr_cell_of_ptr_cell = tmp_ptr_cell.get_prev_cell()
        diff_row_ptr = tmp_ptr_cell.get_row() - ptr_cell_of_ptr_cell.get_row()
        diff_col_ptr = (tmp_ptr_cell.get_column() -
                        ptr_cell_of_ptr_cell.get_column())

        diff_row_cur = row - tmp_ptr_cell.get_row()
        diff_col_cur = col - tmp_ptr_cell.get_column()

        if ((diff_col_ptr + diff_row_ptr == 1) and (
                diff_col_cur + diff_row_cur == 1)):
            return True
        else:
            return False

    def _cal_score_non_zero_index(self, row, col):
        """
        Calculate scores for non-left and non-top edge table cells.
        """
        top_cell = self._score_table[row - 1, col]
        left_cell = self._score_table[row, col - 1]
        top_left_cell = self._score_table[row - 1, col - 1]

        if self._is_gap_open(row, col, left_cell):
            score_from_left = left_cell.get_score() + self._gap_open  # Gap
        else:
            score_from_left = left_cell.get_score() + self._gap_extend  # Gap

        if self._is_gap_open(row, col, top_cell):
            score_from_top = top_cell.get_score() + self._gap_open    # Gap
        else:
            score_from_top = top_cell.get_score() + self._gap_extend    # Gap

        if self._seq_left[row - 1] == self._seq_top[col - 1]:
            score_from_top_left = (top_left_cell.get_score() +
                                   self._match)  # Match
        else:
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
                match_score, cell_ptr = self._cal_score_of_one_cell(row, col)
                cur_cell = ScoreCell(match_score, int(row), int(col), cell_ptr)
                self._score_table[row, col] = cur_cell
                self._store_max_score(cur_cell)

    def _store_max_score(self, cur_cell):
        """
        Determine if the current ScoreCell's score is the largest, and if so,
        save this cell.

        Args:
            cur_cell: ScoreCell object
        """
        if len(self._max_score_cell) == 0:
            self._max_score_cell.append(cur_cell)
        else:
            if max(self._max_score_cell) < cur_cell:
                self._max_score_cell.clear()
                self._max_score_cell.append(cur_cell)
            elif max(self._max_score_cell) == cur_cell:
                self._max_score_cell.append(cur_cell)

    def get_score_table(self):
        """
        Get all cells' scores, it is a numpy.array
        """
        return self._score_table

    def get_align_results(self):
        return self._best_align

    def _trace_back(self):
        """
        Tracing back to find an actual align sequences.
        """
        best_align = list()
        for max_cell in self._max_score_cell:
            (left_align, top_align) = self._trace_back_start_one_cell(max_cell)
            best_align.append((left_align, top_align))
        self._best_align = best_align

    def _trace_back_start_one_cell(self, start_cell):
        """
        Tracing back to find an actual align sequences.

        Args:
            start_cell: ScoreCell object, trace back starts from this cell.

        Returns:
        Returns two list(), which contain the alignment.
        """
        seq_top_aling = list()
        seq_left_aling = list()

        cur_cell = start_cell
        start_point = cur_cell
        end_point = None

        while cur_cell.get_prev_cell() is not None:
            prev_cell = cur_cell.get_prev_cell()

            if cur_cell.get_row() == prev_cell.get_row() + 1 and (
                    cur_cell.get_column() == prev_cell.get_column() + 1):
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
        end_point = cur_cell

        seq_left_aling, seq_top_aling = self._extend_align_sequences(
            start_point, end_point, seq_left_aling, seq_top_aling)

        return seq_left_aling, seq_top_aling

    def _extend_align_sequences(self, start_cell, end_cell, left_align,
                                top_align):
        """
        Complete of sequences that have not been aligned.

        Args:
            start_cell: ScoreCell object, trace back starts from this cell.
            end_cell: ScoreCell object, trace back ends in this cell.
            left_align: list() object, best align of left sequence.
            top_align: list() object, beset align of top sequence.

        """
        distance_start_right = len(self._seq_top) - start_cell.get_column()
        distance_start_buttom = len(self._seq_left) - start_cell.get_row()

        distance_end_left = end_cell.get_column() - 1
        distance_end_top = end_cell.get_row() - 1

        if distance_end_top <= distance_end_left:
            row_idx = end_cell.get_row() - 1
            for idx in range(end_cell.get_column() - 1, -1, -1):
                top_align.append(self._seq_top[idx])
                if row_idx >= 0:
                    left_align.append(self._seq_left[row_idx])
                else:
                    left_align.append('-')
                row_idx -= 1
        else:
            col_idx = end_cell.get_column() - 1
            for idx in range(end_cell.get_row() - 1, -1, -1):
                left_align.append(self._seq_left[idx])
                if col_idx >= 0:
                    top_align.append(self._seq_top[col_idx])
                else:
                    top_align.append('-')
                col_idx -= 1

        left_align.reverse()
        top_align.reverse()

        if distance_start_buttom <= distance_start_right:
            row_idx = start_cell.get_row()
            for idx in range(start_cell.get_column(), len(self._seq_top)):
                top_align.append(self._seq_top[idx])
                if row_idx < len(self._seq_left):
                    left_align.append(self._seq_left[row_idx])
                else:
                    left_align.append('-')
                row_idx += 1
        else:
            col_idx = start_cell.get_column()
            for idx in range(start_cell.get_row(), len(self._seq_left)):
                left_align.append(self._seq_left[idx])
                if col_idx < len(self._seq_top):
                    top_align.append(self._seq_top[col_idx])
                else:
                    top_align.append('-')
                col_idx += 1

        return left_align, top_align

    def _display_one_best_align(self, align_seqs):
        """
        Args:
            align_seqs: a tuple(left_align, top_align)
        """
        left_aling, top_aling = align_seqs
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

    def display(self):
        """
        Print best alignments in an easy-to-read format.
        """
        best_aligns = self.get_align_results()
        for align_seqs in best_aligns:
            self._display_one_best_align(align_seqs)
            print('\n')
