"""
Lab 6 Q1: Rod Cutting

Three solutions to the same problem:
  - naive recursion           Theta(2^n) calls
  - top-down with memoization Theta(n^2) time, n + 1 distinct subproblems
  - bottom-up table           Theta(n^2) time, no recursion

Run:  python q1_rod_cutting.py
"""

import time

BASE_PRICES = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def price_table(n):
    """p[0] = 0, p[1..10] from the base table, p[i] = 3 * i for i > 10."""
    p = [0] + BASE_PRICES[:]
    for i in range(11, n + 1):
        p.append(3 * i)
    return p


# ------------------------------------------------------------ naive
def cut_rod_naive(p, n, counter):
    counter[0] += 1
    if n == 0:
        return 0
    best = float("-inf")
    for i in range(1, n + 1):
        best = max(best, p[i] + cut_rod_naive(p, n - i, counter))
    return best


# ------------------------------------------------------------ top-down
def cut_rod_memo(p, n, counter):
    memo = [None] * (n + 1)
    return _memo_aux(p, n, memo, counter)


def _memo_aux(p, n, memo, counter):
    counter[0] += 1
    if memo[n] is not None:
        return memo[n]
    if n == 0:
        best = 0
    else:
        best = float("-inf")
        for i in range(1, n + 1):
            best = max(best, p[i] + _memo_aux(p, n - i, memo, counter))
    memo[n] = best
    return best


# ------------------------------------------------------------ bottom-up
def cut_rod_bottom_up(p, n, counter=None):
    """Return (r, s): r[j] is the best revenue for length j and s[j] is the
    size of the first piece in one best way to cut length j."""
    r = [0] * (n + 1)
    s = [0] * (n + 1)
    for j in range(1, n + 1):
        best = float("-inf")
        for i in range(1, j + 1):
            if counter is not None:
                counter[0] += 1
            if p[i] + r[j - i] > best:
                best = p[i] + r[j - i]
                s[j] = i
        r[j] = best
    return r, s


def pieces(s, n):
    out = []
    while n > 0:
        out.append(s[n])
        n -= s[n]
    return out


def show_solutions():
    print("=" * 60)
    print("Best revenue and cuts for n = 1 to 10")
    print("=" * 60)
    p = price_table(10)
    r, s = cut_rod_bottom_up(p, 10)
    print(f"| {'n':>2} | {'revenue':>7} | pieces")
    print(f"|{'-' * 4}|{'-' * 9}|{'-' * 20}")
    for n in range(1, 11):
        naive = cut_rod_naive(p, n, [0])
        memo = cut_rod_memo(p, n, [0])
        assert naive == memo == r[n]
        print(f"| {n:>2} | {r[n]:>7} | {pieces(s, n)}")
    print()


def compare_versions():
    print("=" * 60)
    print("Calls and running time (p[i] = 3i for i > 10)")
    print("=" * 60)
    rows = []
    for n in [5, 10, 15, 20, 25]:
        p = price_table(n)

        c_naive = [0]
        start = time.perf_counter()
        v1 = cut_rod_naive(p, n, c_naive)
        t_naive = time.perf_counter() - start

        c_memo = [0]
        start = time.perf_counter()
        v2 = cut_rod_memo(p, n, c_memo)
        t_memo = time.perf_counter() - start

        c_bu = [0]
        start = time.perf_counter()
        r, _ = cut_rod_bottom_up(p, n, c_bu)
        t_bu = time.perf_counter() - start

        assert v1 == v2 == r[n]
        rows.append((n, r[n], c_naive[0], t_naive, c_memo[0], t_memo, c_bu[0], t_bu))
        print(f"  n = {n} done", flush=True)

    print("\n| n | revenue | naive calls | naive time (s) | memo calls | memo time (s) "
          "| bottom-up inner steps | bottom-up time (s) |")
    print("|---|---|---|---|---|---|---|---|")
    for n, rev, cn, tn, cm, tm, cb, tb in rows:
        print(f"| {n} | {rev} | {cn:,} | {tn:.6f} | {cm:,} | {tm:.6f} | {cb:,} | {tb:.6f} |")
    print("\nnaive calls = 2^n, memo calls = n(n+1)/2 + 1,")
    print("bottom-up makes no recursive calls; its inner loop runs n(n+1)/2 times.\n")


if __name__ == "__main__":
    show_solutions()
    compare_versions()
