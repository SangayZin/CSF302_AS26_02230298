"""Generate graphs for CSF Assignment 3 report."""

import time
import random
import sys
import matplotlib.pyplot as plt
from sorts import quicksort_basic, quicksort_improved

sys.setrecursionlimit(100000)


def make_input(kind, n):
    if kind == "random":
        return [random.randint(-10**9, 10**9) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":
        return [random.randint(0, 9) for _ in range(n)]


def time_one(sort_fn, arr):
    a = arr[:]
    t0 = time.perf_counter()
    try:
        sort_fn(a)
    except RecursionError:
        return None
    return time.perf_counter() - t0


SIZES = [1000, 2000, 4000, 8000]  # cap for quicksort_basic on sorted input
KINDS = ["random", "sorted", "duplicates"]

# --- figure 1: basic vs improved per input type ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, kind in zip(axes, KINDS):
    basic_times = [time_one(quicksort_basic, make_input(kind, n)) for n in SIZES]
    improved_times = [time_one(quicksort_improved, make_input(kind, n)) for n in SIZES]
    ax.plot(SIZES, [t if t is not None else float('nan') for t in basic_times],
            marker="o", label="quicksort_basic")
    ax.plot(SIZES, [t if t is not None else float('nan') for t in improved_times],
            marker="s", label="quicksort_improved")
    ax.set_title(f"Input: {kind}")
    ax.set_xlabel("n")
    ax.set_ylabel("time (s)")
    ax.legend()
fig.suptitle("Basic vs improved quicksort")
fig.tight_layout()
fig.savefig("figure1_compare.png", dpi=150)

# --- figure 2: cutoff sweep ---
random.seed(42)
data = [random.randint(-10**9, 10**9) for _ in range(100_000)]
cutoffs = [1, 4, 8, 16, 32, 64]
cut_times = []
for c in cutoffs:
    a = data[:]
    t0 = time.perf_counter()
    quicksort_improved(a, cutoff=c)
    cut_times.append(time.perf_counter() - t0)

fig2, ax = plt.subplots(figsize=(6, 4))
ax.plot(cutoffs, cut_times, marker="o")
ax.set_xscale("log", base=2)
ax.set_xlabel("cutoff")
ax.set_ylabel("time (s)")
ax.set_title("quicksort_improved: cutoff sweep, n = 100,000")
fig2.tight_layout()
fig2.savefig("figure2_cutoff.png", dpi=150)

print("Wrote figure1_compare.png and figure2_cutoff.png")
