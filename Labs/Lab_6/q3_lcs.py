"""
Lab 6 Q3: Longest Common Subsequence

  - bottom-up LCS table, printed for X = ABCBDAB, Y = BDCABA
  - reconstruction of one LCS from the table
  - two-row version that only returns the length (O(min) extra space)
  - brute force that tries every subsequence of X, timed against the DP
  - a line-by-line diff of two text files built on the LCS of their lines

Run:            python q3_lcs.py
Diff only:      python q3_lcs.py diff old.txt new.txt
"""

import os
import random
import sys
import time

rng = random.Random(64)
HERE = os.path.dirname(os.path.abspath(__file__))


def lcs_table(X, Y):
    m, n = len(X), len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
            else:
                c[i][j] = c[i][j - 1]
    return c


def reconstruct(c, X, Y):
    """Walk back from c[m][n]. A match means the character is in the LCS;
    otherwise move towards the neighbour that holds the same value."""
    i, j = len(X), len(Y)
    out = []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            out.append(X[i - 1])
            i -= 1
            j -= 1
        elif c[i - 1][j] >= c[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def lcs_length_two_rows(X, Y):
    if len(Y) > len(X):
        X, Y = Y, X              # keep the rows as short as possible
    prev = [0] * (len(Y) + 1)
    for i in range(1, len(X) + 1):
        curr = [0] * (len(Y) + 1)
        for j in range(1, len(Y) + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[-1]


def is_subsequence(sub, Y):
    it = iter(Y)
    return all(ch in it for ch in sub)   # `in` on an iterator consumes it, keeping order


def lcs_brute_force(X, Y):
    """Try all 2^m subsequences of X and keep the longest one that is also in Y."""
    m = len(X)
    best = ""
    for mask in range(1 << m):
        sub = [X[i] for i in range(m) if mask >> i & 1]
        if len(sub) > len(best) and is_subsequence(sub, Y):
            best = "".join(sub)
    return best


def print_table(c, X, Y):
    print("      " + "   ".join(f"{ch}" for ch in " " + Y))
    for i in range(len(X) + 1):
        label = X[i - 1] if i > 0 else " "
        print(f"  {label}   " + "   ".join(str(v) for v in c[i]))


def demo_table():
    print("=" * 62)
    print("LCS table for X = ABCBDAB, Y = BDCABA")
    print("=" * 62)
    X, Y = "ABCBDAB", "BDCABA"
    c = lcs_table(X, Y)
    print_table(c, X, Y)
    print(f"\nLCS length        : {c[-1][-1]}")
    print(f"one LCS           : {reconstruct(c, X, Y)}")
    print(f"two-row length    : {lcs_length_two_rows(X, Y)}")
    print(f"brute force LCS   : {lcs_brute_force(X, Y)}")
    print()


def timing():
    print("=" * 62)
    print("DP vs brute force on random strings over {A, C, G, T}")
    print("=" * 62)
    print("| length | LCS length | DP time (s) | brute force time (s) | brute / DP |")
    print("|---|---|---|---|---|")
    for n in range(5, 19):
        X = "".join(rng.choice("ACGT") for _ in range(n))
        Y = "".join(rng.choice("ACGT") for _ in range(n))
        start = time.perf_counter()
        for _ in range(20):
            c = lcs_table(X, Y)
        t_dp = (time.perf_counter() - start) / 20
        start = time.perf_counter()
        brute = lcs_brute_force(X, Y)
        t_bf = time.perf_counter() - start
        assert len(brute) == c[-1][-1] == lcs_length_two_rows(X, Y)
        assert is_subsequence(reconstruct(c, X, Y), Y)
        print(f"| {n} | {c[-1][-1]} | {t_dp:.6f} | {t_bf:.6f} | {t_bf / t_dp:,.0f}x |", flush=True)
    print()


def diff_lines(old, new):
    """Return diff lines: '  ' unchanged, '- ' removed from old, '+ ' added in new.
    Uses a suffix table L[i][j] = LCS length of old[i:] and new[j:] so the
    output can be produced from the top of the files downwards."""
    a, b = len(old), len(new)
    L = [[0] * (b + 1) for _ in range(a + 1)]
    for i in range(a - 1, -1, -1):
        for j in range(b - 1, -1, -1):
            if old[i] == new[j]:
                L[i][j] = L[i + 1][j + 1] + 1
            else:
                L[i][j] = max(L[i + 1][j], L[i][j + 1])
    out = []
    i = j = 0
    while i < a and j < b:
        if old[i] == new[j]:
            out.append("  " + old[i])
            i += 1
            j += 1
        elif L[i + 1][j] >= L[i][j + 1]:
            out.append("- " + old[i])
            i += 1
        else:
            out.append("+ " + new[j])
            j += 1
    out.extend("- " + line for line in old[i:])
    out.extend("+ " + line for line in new[j:])
    return out


def run_diff(old_path, new_path):
    print("=" * 62)
    print(f"diff {os.path.basename(old_path)} {os.path.basename(new_path)}")
    print("=" * 62)
    with open(old_path, encoding="utf-8") as f:
        old = f.read().splitlines()
    with open(new_path, encoding="utf-8") as f:
        new = f.read().splitlines()
    result = diff_lines(old, new)
    for line in result:
        print(line)
    kept = sum(1 for line in result if line.startswith("  "))
    print(f"\n{kept} lines unchanged, "
          f"{sum(1 for l in result if l.startswith('- '))} removed, "
          f"{sum(1 for l in result if l.startswith('+ '))} added")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "diff":
        run_diff(sys.argv[2], sys.argv[3])
    else:
        demo_table()
        timing()
        run_diff(os.path.join(HERE, "texts", "old_version.txt"),
                 os.path.join(HERE, "texts", "new_version.txt"))
