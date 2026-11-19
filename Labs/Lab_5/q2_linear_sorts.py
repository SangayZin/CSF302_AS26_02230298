"""
Lab 5 Q2: Counting Sort and Radix Sort

  - stable counting sort for integers in 0..k
  - LSD radix sort that runs a stable counting sort on each digit
    (base 10 and base 256)
  - merge sort for comparison
  - two timing experiments, saved as plots
  - a stability check using (key, original index) pairs

Run:  python q2_linear_sorts.py
Plots are written to the plots/ folder next to this file.
"""

import os
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# one fixed colour per algorithm so both plots read the same way
COLOURS = {"counting sort": "#1f77b4", "radix base 10": "#ff7f0e",
           "radix base 256": "#2ca02c", "merge sort": "#d62728"}

rng = random.Random(302)
HERE = os.path.dirname(os.path.abspath(__file__))
PLOT_DIR = os.path.join(HERE, "plots")


def counting_sort(a, k, key=None):
    """Stable counting sort. Keys must be integers in 0..k.
    `key` lets us sort records (like tuples) by one integer field."""
    if key is None:
        key = lambda x: x
    count = [0] * (k + 1)
    for item in a:
        count[key(item)] += 1
    # after this loop, count[v] is the number of keys <= v, which is
    # one past the last position a key equal to v should go
    for v in range(1, k + 1):
        count[v] += count[v - 1]
    out = [None] * len(a)
    # walking backwards keeps equal keys in their original order (stability)
    for item in reversed(a):
        kv = key(item)
        count[kv] -= 1
        out[count[kv]] = item
    return out


def radix_sort(a, base=10):
    """LSD radix sort for non-negative integers."""
    if not a:
        return []
    biggest = max(a)
    out = list(a)
    place = 1
    while biggest // place > 0:
        out = counting_sort(out, base - 1, key=lambda x: (x // place) % base)
        place *= base
    return out


def merge_sort(a):
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def timed(func, *args):
    start = time.perf_counter()
    out = func(*args)
    return out, time.perf_counter() - start


def experiment_vary_k():
    print("=" * 72)
    print("Experiment 1: n = 100,000 fixed, k varies")
    print("=" * 72)
    n = 100_000
    ks = [10, 10**3, 10**5, 10**7]
    rows = []
    print("| k | counting sort (s) | radix base 10 (s) | radix base 256 (s) | merge sort (s) |")
    print("|---|---|---|---|---|")
    for k in ks:
        data = [rng.randint(0, k) for _ in range(n)]
        expected = sorted(data)
        c_out, t_c = timed(counting_sort, data, k)
        r10, t_r10 = timed(radix_sort, data, 10)
        r256, t_r256 = timed(radix_sort, data, 256)
        m_out, t_m = timed(merge_sort, data)
        assert c_out == r10 == r256 == m_out == expected
        rows.append((k, t_c, t_r10, t_r256, t_m))
        print(f"| {k:,} | {t_c:.4f} | {t_r10:.4f} | {t_r256:.4f} | {t_m:.4f} |", flush=True)
    print()
    return rows


def experiment_vary_n():
    print("=" * 72)
    print("Experiment 2: k = 10^9 fixed, n varies")
    print("=" * 72)
    k = 10**9
    ns = [10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    rows = []
    print("| n | radix base 10 (s) | radix base 256 (s) | merge sort (s) |")
    print("|---|---|---|---|")
    for n in ns:
        data = [rng.randint(0, k) for _ in range(n)]
        expected = sorted(data)
        r10, t_r10 = timed(radix_sort, data, 10)
        r256, t_r256 = timed(radix_sort, data, 256)
        m_out, t_m = timed(merge_sort, data)
        assert r10 == r256 == m_out == expected
        rows.append((n, t_r10, t_r256, t_m))
        print(f"| {n:,} | {t_r10:.4f} | {t_r256:.4f} | {t_m:.4f} |", flush=True)
    print("\nCounting sort is not run here: with k = 10^9 its count array alone")
    print("would need a billion entries (about 8 GB of pointers in Python).\n")
    return rows


def plot_results(rows_k, rows_n):
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ks = [r[0] for r in rows_k]
    for idx, label, style in [(1, "counting sort", "o-"), (2, "radix base 10", "s-"),
                              (3, "radix base 256", "^-"), (4, "merge sort", "d--")]:
        ax.plot(ks, [r[idx] for r in rows_k], style, label=label, color=COLOURS[label])
    ax.set_xscale("log")
    ax.set_xlabel("k (largest key value)")
    ax.set_ylabel("time (seconds)")
    ax.set_title("n = 100,000: effect of the key range k")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, "vary_k.png"), dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ns = [r[0] for r in rows_n]
    for idx, label, style in [(1, "radix base 10", "s-"), (2, "radix base 256", "^-"),
                              (3, "merge sort", "d--")]:
        ax.plot(ns, [r[idx] for r in rows_n], style, label=label, color=COLOURS[label])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlabel("n (number of keys)")
    ax.set_ylabel("time (seconds)")
    ax.set_title("k = 10^9: effect of the input size n")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(PLOT_DIR, "vary_n.png"), dpi=120)
    plt.close(fig)
    print(f"Plots saved to {PLOT_DIR}\n")


def stability_check():
    print("=" * 72)
    print("Stability check: sorting (key, original index) pairs by key only")
    print("=" * 72)
    keys = [rng.randint(0, 4) for _ in range(15)]
    pairs = [(key, idx) for idx, key in enumerate(keys)]
    print("before:", pairs)
    result = counting_sort(pairs, 4, key=lambda p: p[0])
    print("after: ", result)
    stable = all(result[i][1] < result[i + 1][1]
                 for i in range(len(result) - 1) if result[i][0] == result[i + 1][0])
    print("equal keys keep increasing original indices:", stable)

    big = [(rng.randint(0, 50), i) for i in range(100_000)]
    out = counting_sort(big, 50, key=lambda p: p[0])
    print("same check on 100,000 pairs:", out == sorted(big))
    print()


if __name__ == "__main__":
    rows_k = experiment_vary_k()
    rows_n = experiment_vary_n()
    plot_results(rows_k, rows_n)
    stability_check()
