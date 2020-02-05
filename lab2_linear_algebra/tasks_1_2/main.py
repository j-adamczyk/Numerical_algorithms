import numpy as np
import math
import time
import copy


def gauss_jordan_partial_pivoting_solve(A, B):
    n = np.shape(A)[0]

    P = np.zeros((n, n))

    for i in range(0, n):
        P[i][i] = 1

    for i in range(0, n):
        best_pivot_row = i

        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[best_pivot_row][i]):
                best_pivot_row = j

        if A[best_pivot_row][i] == 0 or math.isclose(A[best_pivot_row][i],0.0,abs_tol=1e-9):
            raise ValueError("Unique solution does not exist!")

        if best_pivot_row != i:
            A[[i, best_pivot_row]] = A[[best_pivot_row, i]]
            B[i], B[best_pivot_row] = B[best_pivot_row], B[i]

        for j in range(0, n):
            if i != j:
                multiplier = A[j][i] / A[i][i]
                for k in range(0, n):
                    A[j][k] = A[j][k] - multiplier * A[i][k]
                B[j] = B[j] - multiplier * B[i]

    for i in range(0, n):
        B[i] = B[i] / A[i][i]

    return B


def gauss_jordan_complete_pivoting_solve(A, B):
    n = np.shape(A)[0]

    P = np.zeros((n, n))

    for i in range(0, n):
        P[i][i] = 1

    for i in range(0, n):
        best_pivot_row = i
        best_pivot_column = i

        for j in range(i+1, n):
            for k in range(j, n):
                if abs(A[j][k]) > abs(A[best_pivot_row][best_pivot_column]):
                    best_pivot_row = j
                    best_pivot_column = k

        if A[best_pivot_row][best_pivot_column] == 0 or math.isclose(A[best_pivot_row][best_pivot_column],0.0,abs_tol=1e-9):
            raise ValueError("Unique solution does not exist!")

        if best_pivot_row != i:
            A[[i, best_pivot_row]] = A[[best_pivot_row, i]]
            B[i], B[best_pivot_row] = B[best_pivot_row], B[i]

        if best_pivot_column != i:
            P[[i, best_pivot_column]] = P[[best_pivot_column, i]]
            A[:, [i, best_pivot_column]] = A[:, [best_pivot_column, i]]

        for j in range(0, n):
            if i != j:
                multiplier = A[j][i] / A[i][i]
                for k in range(0, n):
                    A[j][k] = A[j][k] - multiplier * A[i][k]
                B[j] = B[j] - multiplier * B[i]

    inverse_P = np.linalg.inv(P)

    A = np.dot(A, inverse_P)
    A = np.dot(inverse_P, A)
    B = np.dot(inverse_P, B)

    for i in range(0, n):
        B[i] = B[i] / A[i][i]

    return B


# simple LU
def LU_decomposition_solve(A, B):
    n = np.shape(A)[0]

    for k in range(0, n):
        for i in range(k+1, n):
            multiplier = A[i][k] / A[k][k]
            A[i][k+1:n] = A[i][k+1:n] - multiplier * A[k][k+1:n]
            A[i][k] = multiplier

    X = [0] * n
    Y = [0] * n

    # L solve, forward substitution
    for i in range(0, n):
        partial_row_sum = 0
        j = 0
        while j < i:
            partial_row_sum = partial_row_sum + A[i][j] * Y[j]
            j += 1
        Y[i] = B[i] - partial_row_sum

    # U solve, backward substitution
    for i in range(n - 1, -1, -1):
        partial_row_sum = 0
        for j in range(i + 1, n):
            partial_row_sum = partial_row_sum + A[i][j] * X[j]
        X[i] = (Y[i] - partial_row_sum) / A[i][i]

    return X


# LU with partial pivoting
def LU_decomposition_solve_partial_pivoting(A, B):
    n = np.shape(A)[0]

    for k in range(0, n):
        best_pivot_row = k

        for i in range(k+1, n):
            if abs(A[i][k]) > abs(A[best_pivot_row][k]):
                best_pivot_row = i

        if A[best_pivot_row][k] == 0 or math.isclose(A[best_pivot_row][k], 0.0, abs_tol=1e-9):
            raise ValueError("Unique solution does not exist!")

        A[[k, best_pivot_row]] = A[[best_pivot_row, k]]
        B[k], B[best_pivot_row] = B[best_pivot_row], B[k]

        for i in range(k+1, n):
            multiplier = A[i][k] / A[k][k]
            A[i][k+1:n] = A[i][k+1:n] - multiplier * A[k][k+1:n]
            A[i][k] = multiplier

    X = [0] * n
    Y = [0] * n

    # L solve, forward substitution
    for i in range(0, n):
        partial_row_sum = 0
        j = 0
        while j < i:
            partial_row_sum = partial_row_sum + A[i][j] * Y[j]
            j += 1
        Y[i] = B[i] - partial_row_sum

    # U solve, backward substitution
    for i in range(n - 1, -1, -1):
        partial_row_sum = 0
        for j in range(i + 1, n):
            partial_row_sum = partial_row_sum + A[i][j] * X[j]
        X[i] = (Y[i] - partial_row_sum) / A[i][i]

    return X


# LU with partial pivoting and matrix scaling
def LU_decomposition_solve_partial_pivoting_scaling(A, B):
    n = np.shape(A)[0]

    for k in range(0, n):
        max_row_element = 0
        for i in range(0, n):
            if abs(A[k][i]) > max_row_element:
                max_row_element = abs(A[k][i])
        if B[k] > max_row_element:
            max_row_element = abs(B[k])

        if math.isclose(max_row_element, 0.0, abs_tol=1e-9):
            raise ValueError("Unique solution does not exist!")

        for i in range(0, n):
            A[k][i] = A[k][i] / max_row_element

    for k in range(0, n):
        best_pivot_row = k

        for i in range(k+1, n):
            if abs(A[i][k]) > abs(A[best_pivot_row][k]):
                best_pivot_row = i

        if A[best_pivot_row][k] == 0 or math.isclose(A[best_pivot_row][k], 0.0, abs_tol=1e-9):
            raise ValueError("Unique solution does not exist!")

        A[[k, best_pivot_row]] = A[[best_pivot_row, k]]
        B[k], B[best_pivot_row] = B[best_pivot_row], B[k]

        for i in range(k+1, n):
            multiplier = A[i][k] / A[k][k]
            A[i][k+1:n] = A[i][k+1:n] - multiplier * A[k][k+1:n]
            A[i][k] = multiplier

    X = [0] * n
    Y = [0] * n

    # L solve, forward substitution
    for i in range(0, n):
        partial_row_sum = 0
        j = 0
        while j < i:
            partial_row_sum = partial_row_sum + A[i][j] * Y[j]
            j += 1
        Y[i] = B[i] - partial_row_sum

    # U solve, backward substitution
    for i in range(n - 1, -1, -1):
        partial_row_sum = 0
        for j in range(i + 1, n):
            partial_row_sum = partial_row_sum + A[i][j] * X[j]
        X[i] = (Y[i] - partial_row_sum) / A[i][i]

    return X


A = 100 * np.random.rand(500, 500)
A1 = copy.deepcopy(A)
A2 = copy.deepcopy(A)
A3 = copy.deepcopy(A)
A4 = copy.deepcopy(A)
A5 = copy.deepcopy(A)

B = 100 * np.random.rand(500)
B1 = copy.deepcopy(B)
B2 = copy.deepcopy(B)
B3 = copy.deepcopy(B)
B4 = copy.deepcopy(B)
B5 = copy.deepcopy(B)

simple_LU_start_time = time.time()
Xs2 = LU_decomposition_solve(A2, B2)
simple_LU_end_time = time.time()

pivoting_LU_start_time = time.time()
Xs3 = LU_decomposition_solve_partial_pivoting(A3, B3)
pivoting_LU_end_time = time.time()

simple_LU_time = simple_LU_end_time - simple_LU_start_time
pivoting_LU_time = pivoting_LU_end_time - pivoting_LU_start_time

print("Simple LU decomposition: " + str(simple_LU_time) + "s")
print("Partial pivoting LU decomposition: " + str(pivoting_LU_time) + "s")

"""
custom_partial_pivoting_start_time = time.time()
Xs = gauss_jordan_partial_pivoting_solve(A, B)
custom_partial_pivoting_end_time = time.time()

custom_complete_pivoting_start_time = time.time()
Xs1 = gauss_jordan_partial_pivoting_solve(A1, B1)
custom_complete_pivoting_end_time = time.time()

simple_LU_start_time = time.time()
Xs2 = LU_decomposition_solve(A2, B2)
simple_LU_end_time = time.time()

pivoting_LU_start_time = time.time()
Xs3 = LU_decomposition_solve_partial_pivoting(A3, B3)
pivoting_LU_end_time = time.time()

pivoting_scaling_LU_start_time = time.time()
Xs4 = LU_decomposition_solve_partial_pivoting_scaling(A4, B4)
pivoting_scaling_LU_end_time = time.time()

library_start_time = time.time()
Xs5 = np.linalg.solve(A5, B5)
library_end_time = time.time()

custom_partial_pivoting_time = custom_partial_pivoting_end_time - custom_partial_pivoting_start_time
custom_complete_pivoting_time = custom_complete_pivoting_end_time - custom_complete_pivoting_start_time
simple_LU_time = simple_LU_end_time - simple_LU_start_time
pivoting_LU_time = pivoting_LU_end_time - pivoting_LU_start_time
pivoting_scaling_LU_time = pivoting_scaling_LU_end_time - pivoting_scaling_LU_start_time
library_time = library_end_time - library_start_time

print("Partial pivoting Gauss-Jordan: " + str(custom_partial_pivoting_time) + "s")
print("Complete pivoting Gauss-Jordan: " + str(custom_complete_pivoting_time) + "s")
print("Simple LU decomposition: " + str(simple_LU_time) + "s")
print("Partial pivoting LU decomposition: " + str(pivoting_LU_time) + "s")
print("Partial pivoting and matrix scaling LU decomposition: " + str(pivoting_scaling_LU_time) + "s")
print("Library LU decomposition: " + str(library_time) + "s")
"""