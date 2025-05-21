import numpy as np
from scipy import linalg
import math

def exercise1(v_list, w):
    A = np.column_stack(v_list)
    try:
        x = np.linalg.solve(A, w)
        return True, x
    except np.linalg.LinAlgError:
        x, residuals, rank, s = np.linalg.lstsq(A, w, rcond=None)
        if len(residuals) == 0 or residuals[0] < 1e-10:
            return True, x
        else:
            return False, x

def exercise2(vectors):
    A = np.column_stack(vectors)
    rank = np.linalg.matrix_rank(A)

    if rank == len(vectors):
        return True, None
    else:
        null_space = linalg.null_space(A)
        if null_space.size > 0:
            return False, null_space[:, 0]
        else:
            return False, np.zeros(len(vectors))

def exercise3(C):
    col_rank = np.linalg.matrix_rank(C)
    U, s, Vh = np.linalg.svd(C)
    col_basis = U[:, :col_rank]

    row_basis = Vh[:col_rank, :]

    return col_basis, row_basis

def exercise4(A):
    null_space = linalg.null_space(A)

    if null_space.size > 0:
        v1 = null_space[:, 0]

        if null_space.shape[1] > 1:
            v2 = null_space[:, 1]
            return v1, v2
        else:
            return v1, None

    return None, None

def exercise5(w, A):
    A_pinv = np.linalg.pinv(A)
    reconstruction = A @ (A_pinv @ w)
    in_col_space = np.allclose(w, reconstruction)

    in_null_space = np.allclose(A @ w, np.zeros(A.shape[0]))

    return in_col_space, in_null_space

def exercise6(A):
    a1, a2, a3, a4, a5 = A[:, 0], A[:, 1], A[:, 2], A[:, 3], A[:, 4]
    B = np.column_stack([a1, a2, a4])

    try:
        x_a3 = np.linalg.lstsq(B, a3, rcond=None)[0]
        a3_reconstruction = B @ x_a3
        a3_in_colspace = np.allclose(a3, a3_reconstruction)
    except:
        a3_in_colspace = False

    try:
        x_a5 = np.linalg.lstsq(B, a5, rcond=None)[0]
        a5_reconstruction = B @ x_a5
        a5_in_colspace = np.allclose(a5, a5_reconstruction)
    except:
        a5_in_colspace = False

    return a3_in_colspace, a5_in_colspace, x_a3, x_a5

def exercise7(vectors):
    A = np.column_stack(vectors)
    rank = np.linalg.matrix_rank(A)

    U, s, Vh = np.linalg.svd(A, full_matrices=False)
    basis = U[:, :rank] @ np.diag(s[:rank])

    return rank, basis

def exercise8(matrix_type, size):
    if matrix_type == 'hilbert':
        A = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                A[i, j] = 1.0 / (i + j + 1)

    elif matrix_type == 'pascal':
        A = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                A[i, j] = math.comb(i + j, j)

    elif matrix_type == 'magic':
        A = np.zeros((size, size))
        n = size
        if n % 2 == 1:
            i, j = 0, n // 2
            for k in range(1, n*n + 1):
                A[i, j] = k
                i_new, j_new = (i - 1) % n, (j + 1) % n
                if A[i_new, j_new] != 0:
                    i = (i + 1) % n
                else:
                    i, j = i_new, j_new
        else:
            A = np.arange(1, n*n + 1).reshape(n, n)

    null_space = linalg.null_space(A)
    return null_space

def exercise9(vectors):
    n = len(vectors)
    is_orthogonal = True

    for i in range(n):
        for j in range(i+1, n):
            dot_product = np.dot(vectors[i], vectors[j])
            if abs(dot_product) > 1e-10:
                is_orthogonal = False
                return is_orthogonal, (i, j, dot_product)

    return is_orthogonal, None

def exercise10(y, u):
    dot_product = np.dot(y, u)
    u_norm_squared = np.dot(u, u)

    if u_norm_squared < 1e-10:
        return np.zeros_like(y)

    projection = (dot_product / u_norm_squared) * u
    return projection

def exercise11(A):
    m, n = A.shape

    ATA = np.dot(A.T, A)

    is_orthonormal = np.allclose(ATA, np.eye(n), rtol=1e-5, atol=1e-8)

    return is_orthonormal

def exercise12(A):
    m, n = A.shape
    Q = np.zeros((m, n))

    for j in range(n):
        v = A[:, j].copy()

        for i in range(j):
            proj = np.dot(Q[:, i], A[:, j]) * Q[:, i]
            v = v - proj

        norm = np.linalg.norm(v)
        if norm > 1e-10:
            Q[:, j] = v / norm
        else:
            Q[:, j] = 0

    non_zero_cols = []
    for j in range(n):
        if not np.allclose(Q[:, j], 0):
            non_zero_cols.append(Q[:, j])

    return np.column_stack(non_zero_cols) if non_zero_cols else np.array([])