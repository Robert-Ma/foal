"""
Determine the product of two n-by-n matrices where n is a power of 2.
Because matrix has been converted to np.matrix, its associated addition,
subtraction will be directly added and subtracted, and its multiplication
uses np.matmul().
"""
import numpy as np

POWER = 2


def _determine_dim_of_matrix(mat_left, mat_right):
    """
    Determine the dimesion of matrix is the power of 2, or not, and make sure
    matrix is a squre matrix.
    """
    dim_left = np.shape(mat_left)
    dim_right = np.shape(mat_right)

    if not _is_same_dimesion(mat_left, mat_right):  # the same dimesion
        return False
    elif dim_left[0] != dim_left[1]:  # squre matrix
        return False
    elif dim_right[0] != dim_right[1]:
        return False
    elif dim_left[0] % POWER != 0:  # power of POWER
        return False
    return True


def _is_same_dimesion(mat_A, mat_B):
    """
    Determine two matrices have same dimesion(retrun True) or not (return
    False).
    """
    dim_a = np.shape(mat_A)
    dim_b = np.shape(mat_B)

    if dim_a == dim_b:
        return True
    else:
        return False


def _split_matrix_to_four_submat(mat):
    """
    Split the matrix into four sub-matrices.
    mat is a numpy.matrix
    """
    dim = np.shape(mat)
    # now, dim is a power of POWER
    sub_dim = int(dim[0] / POWER)
    mat_1_1 = mat[:sub_dim, :sub_dim]
    mat_1_2 = mat[:sub_dim, sub_dim:]
    mat_2_1 = mat[sub_dim:, :sub_dim]
    mat_2_2 = mat[sub_dim:, sub_dim:]
    return mat_1_1, mat_1_2, mat_2_1, mat_2_2


def _merge_matrix(mat_11, mat_12, mat_21, mat_22):
    dim = np.shape(mat_11)
    n_dim = dim[0]
    result = np.zeros((2*n_dim, 2*n_dim))

    result[:n_dim, :n_dim] = mat_11
    result[:n_dim, n_dim:] = mat_12
    result[n_dim:, :n_dim] = mat_21
    result[n_dim:, n_dim:] = mat_22

    return result


def strassen(mat_left, mat_right, threshold=2):
    """
    Determine the product of two n-by-n matrices where n is power of POWER.
    """
    if not _determine_dim_of_matrix(mat_left, mat_right):
        raise ValueError('The dimesion of matrix must be a power of 2, and \
        matrix must be a squre matrix. Two matrices must be the same power.')
    # transfrom list-matrix to np.matrix
    mat_left = np.matrix(mat_left)
    mat_right = np.matrix(mat_right)

    if np.shape(mat_left)[0] <= threshold:
        return np.matmul(mat_left, mat_right)
    else:
        A_1_1, A_1_2, A_2_1, A_2_2 = _split_matrix_to_four_submat(mat_left)
        B_1_1, B_1_2, B_2_1, B_2_2 = _split_matrix_to_four_submat(mat_right)

        M_1 = strassen(A_1_1 + A_2_2, B_1_1 + B_2_2)
        M_2 = strassen(A_2_1 + A_2_2, B_1_1)
        M_3 = strassen(A_1_1, B_1_2 - B_2_2)
        M_4 = strassen(A_2_2, B_2_1 - B_1_1)
        M_5 = strassen(A_1_1 + A_1_2, B_2_2)
        M_6 = strassen(A_2_1 - A_1_1, B_1_1 + B_1_2)
        M_7 = strassen(A_1_2 - A_2_2, B_2_1 + B_2_2)

        C_1_1 = M_1 + M_4 - M_5 + M_7
        C_1_2 = M_3 + M_5
        C_2_1 = M_2 + M_4
        C_2_2 = M_1 + M_3 - M_2 + M_6

        return _merge_matrix(C_1_1, C_1_2, C_2_1, C_2_2)
