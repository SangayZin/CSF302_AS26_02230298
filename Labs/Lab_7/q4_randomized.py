"""
Lab 7 Q4: Randomized Algorithms

  - randomized quickselect for the k-th smallest element, timed against
    sorting and indexing
  - Miller-Rabin primality test compared with trial division on random
    12-digit numbers
  - Miller-Rabin with a single round on the Carmichael number 561

Run:  python q4_randomized.py
"""

import math
import random
import time

rng = random.Random(561)


# ------------------------------------------------------------ quickselect
def quickselect(a, k):
    """Return the k-th smallest element (k = 1 is the minimum).
    Works on a copy and only keeps going into the side that holds k."""
    if not 1 <= k <= len(a):
        raise ValueError("k must be between 1 and len(a)")
    a = list(a)
    target = k - 1
    lo, hi = 0, len(a) - 1
    while True:
        if lo == hi:
            return a[lo]
        r = rng.randint(lo, hi)
        a[r], a[hi] = a[hi], a[r]
        x = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] < x:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        if target == i:
            return a[i]
        if target < i:
            hi = i - 1
        else:
            lo = i + 1


def merge_sort(a):
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def demo_quickselect():
    print("=" * 70)
    print("Quickselect vs sorting then indexing (k = n // 2, the median)")
    print("=" * 70)
    print("| n | quickselect (s) | merge sort + index (s) | built-in sorted() + index (s) |")
    print("|---|---|---|---|")
    for n in [10_000, 30_000, 100_000, 300_000, 1_000_000]:
        data = [rng.randint(0, 10**9) for _ in range(n)]
        k = n // 2
        runs = 5 if n <= 100_000 else 2
        t_q = t_m = t_s = 0.0
        for _ in range(runs):
            start = time.perf_counter()
            q = quickselect(data, k)
            t_q += time.perf_counter() - start
            start = time.perf_counter()
            m = merge_sort(data)[k - 1]
            t_m += time.perf_counter() - start
            start = time.perf_counter()
            s = sorted(data)[k - 1]
            t_s += time.perf_counter() - start
            assert q == m == s
        print(f"| {n:,} | {t_q / runs:.4f} | {t_m / runs:.4f} | {t_s / runs:.4f} |", flush=True)

    small = [7, 2, 9, 4, 4, 1, 8]
    print(f"\nsmall check on {small}: "
          + ", ".join(f"k={k}->{quickselect(small, k)}" for k in range(1, len(small) + 1)))
    print()


# ------------------------------------------------------------ primality
def miller_rabin(n, rounds=20):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    # write n - 1 = 2^s * d with d odd
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randint(2, n - 2)
        if is_witness(a, d, s, n):
            return False
    return True


def is_witness(a, d, s, n):
    """True if a proves n is composite."""
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return False
    return True


def miller_rabin_one_round(n):
    """Same test with exactly one random base and no small-prime shortcut,
    so a composite can only be caught by the witness check."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    a = rng.randint(2, n - 2)
    return not is_witness(a, d, s, n)


def trial_division(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = math.isqrt(n)
    f = 3
    while f <= limit:
        if n % f == 0:
            return False
        f += 2
    return True


def demo_primality():
    print("=" * 70)
    print("Miller-Rabin (20 rounds) vs trial division on 20 random 12-digit numbers")
    print("=" * 70)
    numbers = [rng.randint(10**11, 10**12 - 1) for _ in range(20)]
    # two known 12-digit primes, so the slow path of trial division is also shown
    numbers += [100000000003, 999999999989]
    print("| number | Miller-Rabin | time (µs) | trial division | time (µs) | agree |")
    print("|---|---|---|---|---|---|")
    total_mr = total_td = 0.0
    agree = 0
    for n in numbers:
        start = time.perf_counter()
        mr = miller_rabin(n)
        t_mr = time.perf_counter() - start
        start = time.perf_counter()
        td = trial_division(n)
        t_td = time.perf_counter() - start
        total_mr += t_mr
        total_td += t_td
        agree += mr == td
        print(f"| {n} | {'prime' if mr else 'composite'} | {t_mr * 1e6:.1f} | "
              f"{'prime' if td else 'composite'} | {t_td * 1e6:.1f} | {'yes' if mr == td else 'NO'} |")
    print(f"\n{agree} of {len(numbers)} answers agree")
    print(f"total time: Miller-Rabin {total_mr * 1000:.2f} ms, trial division {total_td * 1000:.2f} ms\n")


def demo_carmichael():
    print("=" * 70)
    print("Miller-Rabin with 1 round on the Carmichael number 561 = 3 x 11 x 17")
    print("=" * 70)
    n, runs = 561, 1000
    fermat_liars = sum(1 for a in range(2, n - 1) if math.gcd(a, n) == 1)
    said_prime = sum(miller_rabin_one_round(n) for _ in range(runs))
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    liars = [a for a in range(2, n - 1) if not is_witness(a, d, s, n)]
    print(f"561 - 1 = 2^{s} x {d}")
    print(f"bases a in 2..559 that fool the plain Fermat test: {fermat_liars} of {n - 3}")
    print(f"bases a in 2..559 that fool Miller-Rabin (strong liars): {len(liars)} -> {liars}")
    print(f"expected 'prime' rate for one round: {len(liars)}/{n - 3} = {len(liars) / (n - 3):.2%}")
    print(f"\nanswered 'prime' in {said_prime} of {runs} runs ({said_prime / runs:.1%})")
    print(f"trial division says 561 is {'prime' if trial_division(561) else 'composite'}")


if __name__ == "__main__":
    demo_quickselect()
    demo_primality()
    demo_carmichael()
