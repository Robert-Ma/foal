import sys


class BioSeq:
    """
    Sequence object

    Biological sequence (e.g. RNA, DNA, protein) is immutable. This BioSeq
    object just provides basic methods (such as count, reverse).
    Sequence alignment will surported by another class.
    """

    def __init__(self, data):
        """
        Create a Sequence object

        Args:
            data: a python string, which is sequence
        """
        if not isinstance(data, str):
            raise TypeError('The sequence data should a python string.')
        self._data = data.upper()

    def __str__(self):
        return self._data

    def __repr__(self):
        return self._data

    def __len__(self):
        """Return the length of the sequence."""
        return len(self._data)

    def __eq__(self, other):
        """
        Compare two BioSeq object.
        """
        if isinstance(other, BioSeq):
            if str(self) == str(other):
                return True
            else:
                return False
        else:
            raise TypeError('Another compare object should be BioSeq.')

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Add another BioSeq or python string to this sequence.

        Args:
            other: a BioSeq or python string.
        """
        if isinstance(other, BioSeq):
            return self.__class__(str(self) + str(other))
        elif isinstance(other, str):
            return self.__class__(str(self) + other)
        else:
            raise TypeError("Another object shoud be a BioSeq object"
                            " or a python string.")

    def __radd__(self, other):
        """Add a sequence on the left.

        Args:
            other: a BioSeq or python string.
        """
        if isinstance(other, BioSeq):
            return self.__class__(str(other) + str(self))
        elif isinstance(other, str):
            return self.__class__(other + str(self))
        else:
            raise TypeError("Another object shoud be a BioSeq object"
                            " or a python string.")

    def __mul__(self, multiple):
        """
        Multiply BioSeq by integer.

        Args:
            multiple: a integer
        """
        if not isinstance(multiple, int):
            raise TypeError("can not multiply {} by non-int type".format(
                self.__class__.__name__))
        return self.__class__(str(self) * multiple)

    def __rmul__(self, multiple):
        """
        Multiply BioSeq by integer.

        Args:
            multiple: a integer
        """
        if not isinstance(multiple, int):
            raise TypeError("can not multiply {} by non-int type".format(
                self.__class__.__name__))
        return self.__class__(str(self) * multiple)

    def __imul__(self, multiple):
        """
        Multiply BioSeq in-place
        """
        if not isinstance(multiple, int):
            raise TypeError("can not multiply {} by non-int type".format(
                self.__class__.__name__))
        return self.__class__(str(self) * multiple)

    def __getitem__(self, index):
        """
        Return a sub-string of single letter. Both indexing and for loop can
        call __getitem__.

        Args:
            index: a integer, and must be smaller than length of BioSeq object.
        """
        return self._data[index]

    def __contains__(self, chars):
        """
        Preferred for 'in'
        """
        return str.upper(chars) in self._data

    def count(self, substr, start=0, end=sys.maxsize):
        """
        Return the number of non-overlapping occurrences of substring substr
        in BioSeq[start:end].
        """
        if not isinstance(substr, str):
            raise TypeError('substring should be a string.')
        return self._data.count(str.upper(substr), start, end)

    def reverse(self):
        """
        Reverse sequence, but DO NOT change itself, return a new BioSeq object.
        """
        return self.__class__(self._data[::-1])


class ScoreCell:
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
