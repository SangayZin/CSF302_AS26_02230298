"""
Lab 5 Q1: Quicksort Variants

Four quicksorts, each sorting in place and returning the number of key
comparisons it made:
  - Lomuto partition, last element as pivot
  - Hoare partition, middle element swapped to the front as pivot
  - randomised quicksort (random pivot, then Lomuto)
  - three-way (Dutch national flag) quicksort with a random pivot

Every version recurses on the smaller side and loops on the larger side,
so the recursion depth stays O(log n) even when the splits are terrible.

Run:  python q1_quicksort.py
(Lomuto on sorted input with n = 16,000 makes about 128 million comparisons,
so the full run takes a few minutes.)
"""

import random
import time

rng = random.Random(2025)


# ---------------------------------------------------------------- Lomuto
def lomuto_partition(a, lo, hi):
    x = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1, hi - lo        # every element except the pivot is compared once


def quicksort_lomuto(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    comparisons = 0
    while lo < hi:
        p, c = lomuto_partition(a, lo, hi)
        comparisons += c
        if p - lo < hi - p:
            comparisons += quicksort_lomuto(a, lo, p - 1)
            lo = p + 1
        else:
            comparisons += quicksort_lomuto(a, p + 1, hi)
            hi = p - 1
    return comparisons


# ---------------------------------------------------------------- Hoare
def hoare_partition(a, lo, hi):
    mid = (lo + hi) // 2
    a[lo], a[mid] = a[mid], a[lo]
    x = a[lo]
    i, j = lo - 1, hi + 1
    comparisons = 0
    while True:
        i += 1
        comparisons += 1
        while a[i] < x:
            i += 1
            comparisons += 1
        j -= 1
        comparisons += 1
        while a[j] > x:
            j -= 1
            comparisons += 1
        if i >= j:
            return j, comparisons
        a[i], a[j] = a[j], a[i]


def quicksort_hoare(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    comparisons = 0
    while lo < hi:
        j, c = hoare_partition(a, lo, hi)
        comparisons += c
        # Hoare's split point j stays inside the left part: A[lo..j] and A[j+1..hi]
        if j - lo < hi - j:
            comparisons += quicksort_hoare(a, lo, j)
            lo = j + 1
        else:
            comparisons += quicksort_hoare(a, j + 1, hi)
            hi = j
    return comparisons


# ---------------------------------------------------------------- randomised
def randomized_partition(a, lo, hi):
    k = rng.randint(lo, hi)
    a[k], a[hi] = a[hi], a[k]
    return lomuto_partition(a, lo, hi)


def quicksort_randomized(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    comparisons = 0
    while lo < hi:
        p, c = randomized_partition(a, lo, hi)
        comparisons += c
        if p - lo < hi - p:
            comparisons += quicksort_randomized(a, lo, p - 1)
            lo = p + 1
        else:
            comparisons += quicksort_randomized(a, p + 1, hi)
            hi = p - 1
    return comparisons


# ---------------------------------------------------------------- three-way
def three_way_partition(a, lo, hi):
    """Rearrange a[lo..hi] into  < x | == x | > x  and return the bounds of the
    middle block. The pointers: a[lo..lt-1] < x, a[lt..i-1] == x,
    a[i..gt] not yet seen, a[gt+1..hi] > x."""
    k = rng.randint(lo, hi)
    x = a[k]
    lt, i, gt = lo, lo, hi
    comparisons = 0
    while i <= gt:
        comparisons += 1
        if a[i] < x:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        else:
            comparisons += 1
            if a[i] > x:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
    return lt, gt, comparisons


def quicksort_three_way(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    comparisons = 0
    while lo < hi:
        lt, gt, c = three_way_partition(a, lo, hi)
        comparisons += c
        if lt - lo < hi - gt:
            comparisons += quicksort_three_way(a, lo, lt - 1)
            lo = gt + 1
        else:
            comparisons += quicksort_three_way(a, gt + 1, hi)
            hi = lt - 1
    return comparisons


# ---------------------------------------------------------------- experiment
VARIANTS = {
    "Lomuto": quicksort_lomuto,
    "Hoare": quicksort_hoare,
    "Randomised": quicksort_randomized,
    "Three-way": quicksort_three_way,
}

INPUT_TYPES = {
    "random": lambda n: [rng.randint(0, 10 * n) for _ in range(n)],
    "sorted": lambda n: list(range(n)),
    "reverse": lambda n: list(range(n, 0, -1)),
    "duplicates": lambda n: [rng.randint(0, 9) for _ in range(n)],
}

SIZES = [1000, 2000, 4000, 8000, 16000]


def run_experiment():
    results = {}
    for kind, make in INPUT_TYPES.items():
        for n in SIZES:
            data = make(n)
            expected = sorted(data)
            for name, sort in VARIANTS.items():
                arr = data[:]
                start = time.perf_counter()
                comps = sort(arr)
                elapsed = time.perf_counter() - start
                if arr != expected:
                    raise AssertionError(f"{name} failed on {kind} input, n = {n}")
                results[(name, kind, n)] = (comps, elapsed)
            print(f"  done: {kind:<10} n = {n}", flush=True)
    return results


def print_tables(results):
    for kind in INPUT_TYPES:
        print(f"\n### Input: {kind}\n")
        head = "| n | " + " | ".join(f"{v} comps | {v} time (s)" for v in VARIANTS) + " |"
        print(head)
        print("|" + "---|" * (1 + 2 * len(VARIANTS)))
        for n in SIZES:
            cells = []
            for name in VARIANTS:
                comps, t = results[(name, kind, n)]
                cells.append(f"{comps:,} | {t:.4f}")
            print(f"| {n:,} | " + " | ".join(cells) + " |")

    print("\n### Growth when n doubles from 8,000 to 16,000 (comparisons ratio)\n")
    print("| input | " + " | ".join(VARIANTS) + " |")
    print("|---|" + "---|" * len(VARIANTS))
    for kind in INPUT_TYPES:
        ratios = [results[(v, kind, 16000)][0] / results[(v, kind, 8000)][0] for v in VARIANTS]
        print(f"| {kind} | " + " | ".join(f"{r:.2f}" for r in ratios) + " |")
    print("\n(about 2.1 means n log n growth, about 4.0 means quadratic growth)")


if __name__ == "__main__":
    print("Running all variants on all inputs...")
    res = run_experiment()
    print_tables(res)
