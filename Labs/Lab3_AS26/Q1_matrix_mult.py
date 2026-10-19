"""
Lab 3 - Q1: Matrix Multiplication
Compares Traditional O(n^3) vs Strassen's O(n^2.807) algorithm.
"""

import random
import time


# ---------------------------------------------------------------
# 1. TRADITIONAL MATRIX MULTIPLICATION  (triple nested loop)
#    For every cell C[i][j], sum A[i][k] * B[k][j] over all k.
# ---------------------------------------------------------------
def traditional_multiply(A, B):
    n = len(A)
    # Start with an n x n matrix full of zeros
    C = [[0] * n for _ in range(n)]

    for i in range(n):          # row of A
        for j in range(n):      # column of B
            total = 0
            for k in range(n):  # walk along row i / column j
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


# ---------------------------------------------------------------
# 2. HELPER FUNCTIONS for Strassen
#    Add / subtract two matrices element by element.
# ---------------------------------------------------------------
def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------
# 3. STRASSEN'S ALGORITHM  (divide & conquer, 7 multiplications)
#
#    Split each matrix into 4 quadrants:
#        A = | A11  A12 |      B = | B11  B12 |
#            | A21  A22 |          | B21  B22 |
#
#    Compute 7 products M1..M7 and combine into C11..C22.
#    This uses 7 multiplications instead of 8 per level.
# ---------------------------------------------------------------
def strassen(A, B):
    n = len(A)

    # Base case: 1x1 matrix is just a scalar multiply
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    # ---- Split A into 4 quadrants ----
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    # ---- Split B into 4 quadrants ----
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # ---- 7 recursive multiplications (Strassen's trick) ----
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))

    # ---- Combine results into 4 quadrants ----
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)

    # ---- Put quadrants back into one n x n matrix ----
    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j]             = C11[i][j]
            C[i][j + mid]       = C12[i][j]
            C[i + mid][j]       = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]
    return C


# ---------------------------------------------------------------
# 4. UTILITY: random matrix, equality check, pretty printer
# ---------------------------------------------------------------
def random_matrix(n):
    return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]


def matrices_equal(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def print_matrix(M, label=""):
    if label:
        print(label)
    for row in M:
        print("  ", row)


# ---------------------------------------------------------------
# 5. MAIN DRIVER
# ---------------------------------------------------------------
if __name__ == "__main__":

    # ---------- PART A: small visible demo (4x4) ----------
    print("=" * 60)
    print("DEMO: 4x4 multiplication (both methods shown)")
    print("=" * 60)

    random.seed(42)          # fixed seed so results are reproducible
    demo_A = random_matrix(4)
    demo_B = random_matrix(4)

    print_matrix(demo_A, "\nMatrix A (4x4):")
    print_matrix(demo_B, "\nMatrix B (4x4):")

    demo_trad = traditional_multiply(demo_A, demo_B)
    demo_str  = strassen(demo_A, demo_B)

    print_matrix(demo_trad, "\nTraditional result A x B:")
    print_matrix(demo_str,  "\nStrassen result A x B:")
    print("\nResults match? ->", matrices_equal(demo_trad, demo_str))

    # ---------- PART B: timing table across increasing n ----------
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    print(f"{'n':>5} | {'Match?':>6} | {'Traditional (s)':>16} | {'Strassen (s)':>14}")
    print("-" * 60)

    for n in [2, 4, 8, 16, 32, 64, 128]:
        A = random_matrix(n)
        B = random_matrix(n)

        # time traditional
        t0 = time.perf_counter()
        C_trad = traditional_multiply(A, B)
        t1 = time.perf_counter()

        # time Strassen
        t2 = time.perf_counter()
        C_str = strassen(A, B)
        t3 = time.perf_counter()

        match = matrices_equal(C_trad, C_str)

        print(f"{n:>5} | {str(match):>6} | {t1 - t0:>16.6f} | {t3 - t2:>14.6f}")