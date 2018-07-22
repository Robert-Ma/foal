from foal.dynamic_programming import LCS, BioSeq


def test_lcs():
    seq_left = BioSeq('gcgcaatg')
    seq_top = BioSeq('gccctagcg')
    lcs = LCS(seq_left, seq_top)
    result_lcs = lcs.get_trace_back()
    expect_lcs = ['G', 'C', 'C', 'A', 'G']

    assert result_lcs == expect_lcs
