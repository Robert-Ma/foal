from foal.dynamic_programming import BioSeq
import pytest


INTEGER_MUL = 2
NON_INTEGER_MUL = 2.5


def test_init_with_non_string_value():
    with pytest.raises(TypeError):
        BioSeq(123)


def test_len():
    seq = BioSeq('actgcaggccatc')
    len_of_seq = len(seq)
    expected_len = 13
    assert len_of_seq == expected_len


def test_add_BioSeq():
    left = BioSeq('acgt')
    right = BioSeq('ccgt')
    add_result = left + right
    expected_result = BioSeq('acgtccgt')
    assert add_result == expected_result


def test_add_string():
    left = BioSeq('acgt')
    right = 'tgca'
    add_result = left + right
    exp_result = BioSeq('acgttgca')
    assert add_result == exp_result


def test_radd_string():
    left = 'tgca'
    right = BioSeq('acgt')
    add_result = left + right
    exp_result = BioSeq('tgcaacgt')
    assert add_result == exp_result


def test_mul_with_non_integer():
    seq = BioSeq('acgt')
    with pytest.raises(TypeError):
        seq * NON_INTEGER_MUL


def test_mul_with_integer():
    seq = BioSeq('acgt')
    mul_result = seq * INTEGER_MUL
    exp_result = BioSeq('acgtacgt')
    assert mul_result == exp_result


def test_rmul_with_non_integer():
    seq = BioSeq('acgt')
    with pytest.raises(TypeError):
        NON_INTEGER_MUL * seq


def test_rmul_with_integer():
    seq = BioSeq('acgt')
    mul_result = INTEGER_MUL * seq
    exp_result = BioSeq('acgtacgt')
    assert mul_result == exp_result


def test_imul_with_non_integer():
    seq = BioSeq('acgt')
    with pytest.raises(TypeError):
        seq *= NON_INTEGER_MUL


def test_imul_with_integer():
    seq = BioSeq('acgt')
    seq *= INTEGER_MUL
    mul_result = seq
    exp_result = BioSeq('acgtacgt')
    assert mul_result == exp_result


def test_index():
    seq = BioSeq('acgt')
    index_value = seq[-2]
    expec_value = 'G'
    assert index_value == expec_value


def test_slice():
    seq = BioSeq('acgt')
    slice_values = seq[:2]
    expec_values = 'AC'
    assert slice_values == expec_values


def test_item_in_seq():
    seq = BioSeq('acgt')
    item = 'cg'
    in_result = item in seq
    exp_result = True
    assert in_result == exp_result


def test_count_with_non_string():
    seq = BioSeq('acgttccgccgggg')
    substr = 123
    with pytest.raises(TypeError):
        seq.count(substr)


def test_count_with_string():
    seq = BioSeq('acgttccgccgggg')
    substr = "cg"
    count_result = seq.count(substr)
    exp_result = 3
    assert count_result == exp_result


def test_reverse():
    seq = BioSeq('acgt')
    reverse_result = seq.reverse()
    expect_result = BioSeq('tgca')
    assert reverse_result == expect_result
