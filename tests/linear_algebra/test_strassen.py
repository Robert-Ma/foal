from foal.linear_algebra import strassen
import numpy as np
import pytest


def test_2_dim_list_mat():
    mat_left = [[1, 2], [3, 4]]
    mat_right = [[5, 6], [7, 8]]

    result = strassen(mat_left, mat_right)
    expect = np.matmul(mat_left, mat_right)
    assert (result == expect).all()


def test_power_of_2_dim_mat():
    mat_left = np.matrix(np.arange(64).reshape((8, 8)))
    mat_right = mat_left.T

    result = strassen(mat_left, mat_right)
    expect = np.matmul(mat_left, mat_right)

    assert (result == expect).all()


def test_non_power_of_2():
    mat_left = np.matrix(np.arange(49).reshape((7, 7)))
    mat_right = mat_left.T

    with pytest.raises(ValueError):
        strassen(mat_left, mat_right)


def test_non_squre_mat():
    mat_left = np.matrix(np.arange(56).reshape((8, 7)))
    mat_right = np.matrix(np.arange(63).reshape((7, 9)))

    with pytest.raises(ValueError):
        strassen(mat_left, mat_right)


def test_non_same_dim_matrices():
    mat_left = np.matrix(np.arange(49).reshape((7, 7)))
    mat_right = np.matrix(np.arange(36).reshape((6, 6)))

    with pytest.raises(ValueError):
        strassen(mat_left, mat_right)
