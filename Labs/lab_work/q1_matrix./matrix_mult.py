"""
Q1 - Part A: Traditional Matrix Multiplication
"""

import random


def generate_matrix(n, low=0, high=9):
    # Creates an n x n matrix filled with random numbers between low and high-1
    return [[random.randint(low, high - 1) for _ in range(n)] for _ in range(n)]


def traditional_multiply(A, B):
    # Standard matrix multiplication: C[i][j] = sum of A[i][k] * B[k][j]
    n = len(A)
    
    # Make an n x n result matrix full of zeros
    C = [[0] * n for _ in range(n)]

    # Go through every row of A
    for i in range(n):
        # Go through every column of B
        for j in range(n):
            s = 0
            # Multiply and add up the matching row/column values
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s

    return C


def print_matrix(M, label="Matrix"):
    # Just prints the matrix nicely
    print(f"\n{label}:")
    for row in M:
        print("  ", row)


# Test code below - only runs if itd run this file directly
if __name__ == "__main__":
    print("=" * 60)
    print("Q1 - Traditional Matrix Multiplication (O(n^3))")
    print("=" * 60)

    # Quick 2x2 test
    A = [[1, 2],
         [3, 4]]
    B = [[5, 6],
         [7, 8]]

    C = traditional_multiply(A, B)
    print_matrix(A, "Matrix A")
    print_matrix(B, "Matrix B")
    print_matrix(C, "A x B (Traditional)")

    # Check if the answer is correct
    expected = [[19, 22], [43, 50]]
    assert C == expected, f"FAILED! Got {C}, expected {expected}"
    print("\n 2x2 test PASSED")

    # Random 4x4 test
    random.seed(0)
    A = generate_matrix(4)
    B = generate_matrix(4)
    C = traditional_multiply(A, B)
    print_matrix(C, "Random 4x4 result")

    print("\n Traditional multiplication module ready.")