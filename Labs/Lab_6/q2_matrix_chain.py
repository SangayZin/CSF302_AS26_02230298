"""
Lab 6 Q2: Matrix Chain Multiplication

Matrix A_i has dimensions p[i-1] x p[i], for i = 1..n.
  - bottom-up DP for the minimum number of scalar multiplications
  - optimal parenthesisation printed from the split table
  - brute-force recursion that tries every parenthesisation (n <= 8)
  - cost of plain left-to-right order for comparison

Run:  python q2_matrix_chain.py
"""

import random

rng = random.Random(6)


def matrix_chain_order(p):
    """Return (m, s) where m[i][j] is the minimum cost of A_i..A_j and
    s[i][j] is the k where the best split happens. Indices start at 1."""
    n = len(p) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


def parenthesise(s, i, j):
    if i == j:
        return f"A{i}"
    k = s[i][j]
    return "(" + parenthesise(s, i, k) + parenthesise(s, k + 1, j) + ")"


def brute_force(p, i, j):
    """Try every split point, with no table, so every subproblem is solved
    again each time it appears."""
    if i == j:
        return 0
    return min(brute_force(p, i, k) + brute_force(p, k + 1, j) + p[i - 1] * p[k] * p[j]
               for k in range(i, j))


def left_to_right_cost(p):
    """Cost of ((A1 A2) A3) ... : the running product is always p[0] x p[i]."""
    return sum(p[0] * p[i - 1] * p[i] for i in range(2, len(p)))


def solve(p, label):
    n = len(p) - 1
    m, s = matrix_chain_order(p)
    best = m[1][n]
    brute = brute_force(p, 1, n) if n <= 8 else None
    lr = left_to_right_cost(p)
    print(f"{label}: dimensions {p}  ({n} matrices)")
    print(f"  optimal cost        : {best:,}")
    print(f"  parenthesisation    : {parenthesise(s, 1, n)}")
    print(f"  brute-force check   : {brute:,}  ->  {'match' if brute == best else 'MISMATCH'}")
    print(f"  left-to-right cost  : {lr:,}  ({lr / best:.2f} times the optimum)")
    print()
    return n, best, lr, brute == best


def print_cost_table(p):
    n = len(p) - 1
    m, _ = matrix_chain_order(p)
    print(f"m[i][j] table for {p}:")
    print("      " + "".join(f"{'j=' + str(j):>9}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        cells = "".join(f"{m[i][j]:>9}" if j >= i else f"{'':>9}" for j in range(1, n + 1))
        print(f"  i={i} {cells}")
    print()


if __name__ == "__main__":
    print("=" * 66)
    print("Matrix chain multiplication")
    print("=" * 66)
    summary = []
    summary.append(("Chain 1",) + solve([30, 35, 15, 5, 10, 20, 25], "Chain 1"))
    print_cost_table([30, 35, 15, 5, 10, 20, 25])
    summary.append(("Chain 2",) + solve([5, 4, 6, 2, 7], "Chain 2"))
    for t in range(1, 6):
        n = rng.randint(3, 8)
        dims = [rng.randint(2, 60) for _ in range(n + 1)]
        summary.append((f"Random {t}",) + solve(dims, f"Random {t}"))

    print("| chain | matrices | optimal cost | left-to-right cost | brute force agrees |")
    print("|---|---|---|---|---|")
    for label, n, best, lr, ok in summary:
        print(f"| {label} | {n} | {best:,} | {lr:,} | {'yes' if ok else 'no'} |")
