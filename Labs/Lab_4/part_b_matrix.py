"""
Lab 4 Part B: Efficient Matrix Modular Exponentiation

Covers square matrix multiplication mod m, the identity matrix, naive and
binary matrix powers, Fibonacci numbers mod m, counting walks in a directed
graph, and a benchmark of both power methods.

Run:  python part_b_matrix.py
"""

import random
import time

MOD = 1_000_000_007


def mat_mult(A, B, m):
    """Multiply two square matrices and reduce every entry modulo m."""
    d = len(A)
    if d != len(B) or any(len(row) != d for row in A) or any(len(row) != d for row in B):
        raise ValueError("both matrices must be square and the same size")
    cols = list(zip(*B))    # columns of B, so each entry is a row-column dot product
    return [[sum(x * y for x, y in zip(row, col)) % m for col in cols] for row in A]


def identity(d):
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


def check_power_inputs(A, n, m):
    if m < 1:
        raise ValueError(f"modulus must be at least 1, got m = {m}")
    if n < 0:
        raise ValueError(f"exponent must be non-negative, got n = {n}")
    if any(len(row) != len(A) for row in A):
        raise ValueError("matrix must be square")
    # reducing first also turns negative entries into values in 0..m-1
    return [[x % m for x in row] for row in A]


def naive_mat_pow(A, n, m):
    A = check_power_inputs(A, n, m)
    result = [[x % m for x in row] for row in identity(len(A))]
    for _ in range(n):
        result = mat_mult(result, A, m)
    return result


def binary_mat_pow(A, n, m):
    A = check_power_inputs(A, n, m)
    result = [[x % m for x in row] for row in identity(len(A))]
    while n:
        if n & 1:
            result = mat_mult(result, A, m)
        A = mat_mult(A, A, m)
        n >>= 1
    return result


def fib_mod(n, m):
    """F(n) mod m from [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]."""
    if n == 0:
        return 0 % m
    return binary_mat_pow([[1, 1], [1, 0]], n, m)[0][1]


def fib_iterative(n, m):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % m
    return a


def count_walks(adj, u, v, k, m):
    """Entry (u, v) of adj^k is the number of walks with exactly k edges from u to v."""
    return binary_mat_pow(adj, k, m)[u][v]


def count_walks_brute(adj, u, v, k):
    """Explore every walk of length k with depth-first search (only for small k)."""
    if k == 0:
        return 1 if u == v else 0
    return sum(count_walks_brute(adj, w, v, k - 1) for w in range(len(adj)) if adj[u][w])


def print_matrix(M, indent="    "):
    width = max(len(str(x)) for row in M for x in row)
    for row in M:
        print(indent + " ".join(f"{x:>{width}}" for x in row))


def demo_basics():
    print("=" * 70)
    print("Matrix multiplication and identity matrix")
    print("=" * 70)
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("A =")
    print_matrix(A)
    print("B =")
    print_matrix(B)
    print("A x B mod 10 =")
    print_matrix(mat_mult(A, B, 10))
    print("identity(4) =")
    print_matrix(identity(4))
    print("A x I = A ?", mat_mult(A, identity(2), MOD) == A)
    print()


def compare_methods():
    print("=" * 70)
    print("Naive vs binary matrix exponentiation")
    print("=" * 70)
    rng = random.Random(42)
    cases = [
        ([[1, 1], [1, 0]], 10, 1000),
        ([[2, 0], [0, 3]], 13, 1_000_000),
        ([[1, 2], [3, 4]], 0, 7),
        ([[1, -1], [-2, 5]], 9, 11),
        ([[0, 1, 0], [0, 0, 1], [1, 1, 1]], 50, MOD),
        ([[5, 3], [2, 7]], 100, 1),
    ]
    for _ in range(4):
        d = rng.randint(2, 5)
        M = [[rng.randint(0, 99) for _ in range(d)] for _ in range(d)]
        cases.append((M, rng.randint(1, 300), rng.randint(2, 10**9)))

    print(f"{'d':>2} {'n':>4} {'m':>11} | result (first row, binary)              | same?")
    print("-" * 70)
    for M, n, m in cases:
        naive = naive_mat_pow(M, n, m)
        binary = binary_mat_pow(M, n, m)
        first_row = str(binary[0])
        if len(first_row) > 38:
            first_row = first_row[:35] + "..."
        print(f"{len(M):>2} {n:>4} {m:>11} | {first_row:<38} | {'yes' if naive == binary else 'NO'}")

    print("\nValidation:")
    for label, args in [("negative exponent", ([[1, 1], [1, 0]], -2, 7)),
                        ("modulus 0", ([[1, 1], [1, 0]], 2, 0)),
                        ("non-square matrix", ([[1, 2, 3], [4, 5, 6]], 2, 7))]:
        try:
            binary_mat_pow(*args)
        except ValueError as err:
            print(f"  {label:<18} -> ValueError: {err}")
    print()


def demo_fibonacci():
    print("=" * 70)
    print("Fibonacci numbers with matrix exponentiation")
    print("=" * 70)
    print("F(0..15) mod 1000:", [fib_mod(n, 1000) for n in range(16)])
    ok = all(fib_mod(n, MOD) == fib_iterative(n, MOD) for n in range(500))
    print("Matches the iterative version for n = 0..499:", ok)
    for n, m in [(50, 10**9), (90, 10**18), (1000, MOD), (10**6, MOD)]:
        print(f"F({n}) mod {m} = {fib_mod(n, m)}")

    start = time.perf_counter()
    big = fib_mod(10**18, MOD)
    elapsed = time.perf_counter() - start
    print(f"\nF(10^18) mod (10^9 + 7) = {big}")
    print(f"computed in {elapsed * 1000:.3f} ms using about {(10**18).bit_length()} squarings")
    print()


def demo_walks():
    print("=" * 70)
    print("Counting walks of exactly k edges")
    print("=" * 70)
    # directed graph on 5 vertices:
    # 0->1, 0->2, 1->2, 1->3, 2->3, 2->0, 3->4, 4->0, 4->1
    adj = [
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0],
    ]
    print("Adjacency matrix:")
    print_matrix(adj)
    print(f"\n{'from':>4} {'to':>3} {'k':>3} | {'matrix power':>12} {'brute force DFS':>16}")
    for u, v, k in [(0, 3, 2), (0, 3, 3), (0, 0, 3), (2, 4, 4), (4, 3, 6), (0, 4, 10)]:
        fast = count_walks(adj, u, v, k, MOD)
        slow = count_walks_brute(adj, u, v, k)
        print(f"{u:>4} {v:>3} {k:>3} | {fast:>12} {slow:>16}")
    k = 10**12
    print(f"\nWalks from 0 to 4 with k = 10^12 edges, mod 10^9 + 7: {count_walks(adj, 0, 4, k, MOD)}")
    print()


def benchmark(repeats_small=5):
    print("=" * 70)
    print("Benchmark: naive vs binary matrix exponentiation (mod 10^9 + 7)")
    print("=" * 70)
    rng = random.Random(7)
    dims = [2, 4, 8, 16, 32]
    exps = [2 ** e for e in range(4, 13)]
    results = {}
    for d in dims:
        M = [[rng.randint(0, MOD - 1) for _ in range(d)] for _ in range(d)]
        for n in exps:
            times = {}
            for name, func in (("naive", naive_mat_pow), ("binary", binary_mat_pow)):
                runs = repeats_small if d <= 8 else 1
                start = time.perf_counter()
                for _ in range(runs):
                    out = func(M, n, MOD)
                times[name] = (time.perf_counter() - start) / runs
                times[name + "_out"] = out
            assert times["naive_out"] == times["binary_out"]
            results[(d, n)] = (times["naive"], times["binary"])

    for d in dims:
        print(f"\nd = {d}")
        print(f"| {'n':>5} | {'naive (s)':>10} | {'binary (s)':>10} | {'speed-up':>9} |")
        print(f"|{'-' * 7}|{'-' * 12}|{'-' * 12}|{'-' * 11}|")
        for n in exps:
            tn, tb = results[(d, n)]
            print(f"| {n:>5} | {tn:>10.5f} | {tb:>10.5f} | {tn / tb:>8.1f}x |")
    print()
    return results


if __name__ == "__main__":
    demo_basics()
    compare_methods()
    demo_fibonacci()
    demo_walks()
    benchmark()
