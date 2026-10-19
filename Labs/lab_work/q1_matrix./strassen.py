"""
Q1 - Part B: Strassen's Matrix Multiplication
"""

import random
from matrix_mult import traditional_multiply, generate_matrix, print_matrix


# ----------------------------------------------------------------------
# Helper functions for matrices
# ----------------------------------------------------------------------
def add_matrix(A, B):
    # Adds two matrices element by element
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub_matrix(A, B):
    # Subtracts two matrices element by element
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(A):
    # Splits an n x n matrix into 4 quadrants of size n/2 x n/2
    n = len(A)
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]   # top-left
    A12 = [row[mid:] for row in A[:mid]]   # top-right
    A21 = [row[:mid] for row in A[mid:]]   # bottom-left
    A22 = [row[mid:] for row in A[mid:]]   # bottom-right
    return A11, A12, A21, A22


def join_matrix(A11, A12, A21, A22):
    # Combines 4 quadrants back into one big matrix
    top    = [A11[i] + A12[i] for i in range(len(A11))]
    bottom = [A21[i] + A22[i] for i in range(len(A21))]
    return top + bottom


def next_power_of_two(n):
    # Finds the smallest power of 2 that is >= n
    p = 1
    while p < n:
        p <<= 1
    return p


def pad_to_power_of_two(A, size):
    # Adds zero rows/columns to make the matrix size x size
    n = len(A)
    if n == size:
        return A
    padded = [[0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            padded[i][j] = A[i][j]
    return padded


# ----------------------------------------------------------------------
# Strassen's algorithm
# ----------------------------------------------------------------------
def strassen(A, B, base_case=2):
    # Recursive Strassen multiplication
    # If matrix is small enough, just use the normal method
    n = len(A)

    # Base case: small matrix -> use traditional
    if n <= base_case:
        return traditional_multiply(A, B)

    # Split both matrices into quadrants
    mid = n // 2
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # The 7 clever multiplications (this is the heart of Strassen)
    M1 = strassen(add_matrix(A11, A22), add_matrix(B11, B22), base_case)
    M2 = strassen(add_matrix(A21, A22), B11,                    base_case)
    M3 = strassen(A11,               sub_matrix(B12, B22),      base_case)
    M4 = strassen(A22,               sub_matrix(B21, B11),      base_case)
    M5 = strassen(add_matrix(A11, A12), B22,                    base_case)
    M6 = strassen(sub_matrix(A21, A11), add_matrix(B11, B12),   base_case)
    M7 = strassen(sub_matrix(A12, A22), add_matrix(B21, B22),   base_case)

    # Combine the M's to get the 4 quadrants of the result
    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

    return join_matrix(C11, C12, C21, C22)


def strassen_multiply(A, B, base_case=2):
    # Wrapper that handles non-power-of-2 sizes by padding with zeros
    n = len(A)
    size = next_power_of_two(n)

    A_pad = pad_to_power_of_two(A, size)
    B_pad = pad_to_power_of_two(B, size)

    C_pad = strassen(A_pad, B_pad, base_case)

    # Remove the extra zero rows/columns we added
    return [row[:n] for row in C_pad[:n]]


# ----------------------------------------------------------------------
# Tests - only runs when you execute this file directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Q1 - Strassen's Matrix Multiplication  O(n^2.807)")
    print("=" * 60)

    # Test 1: simple 2x2
    A = [[1, 2],
         [3, 4]]
    B = [[5, 6],
         [7, 8]]

    C_str = strassen_multiply(A, B)
    C_trad = traditional_multiply(A, B)
    print_matrix(C_str, "Strassen 2x2 result")
    assert C_str == C_trad, f"MISMATCH: {C_str} vs {C_trad}"
    print(" 2x2 matches traditional")

    # Test 2: random 4x4
    random.seed(1)
    A = generate_matrix(4)
    B = generate_matrix(4)
    assert strassen_multiply(A, B) == traditional_multiply(A, B)
    print(" 4x4 matches traditional")

    # Test 3: random 8x8
    random.seed(2)
    A = generate_matrix(8)
    B = generate_matrix(8)
    assert strassen_multiply(A, B) == traditional_multiply(A, B)
    print(" 8x8 matches traditional")

    # Test 4: 5x5 (not a power of 2, so it gets padded)
    random.seed(3)
    A = generate_matrix(5)
    B = generate_matrix(5)
    assert strassen_multiply(A, B) == traditional_multiply(A, B)
    print(" 5x5 (padded) matches traditional")

    # Test 5: random 16x16
    random.seed(4)
    A = generate_matrix(16)
    B = generate_matrix(16)
    assert strassen_multiply(A, B) == traditional_multiply(A, B)
    print(" 16x16 matches traditional")

    print("\n All Strassen tests PASSED.")