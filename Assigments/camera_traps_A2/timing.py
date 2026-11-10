"""Timing harness for closest pair (Part C).

Run:  python3 timing.py
Outputs:
    - prints a table to stdout
    - saves timings.csv
    - saves timing_graph.png
"""

import csv
import random
import time

import matplotlib
matplotlib.use("Agg")               # non-interactive backend (safe on Linux)
import matplotlib.pyplot as plt

from closest import closest_pair, closest_pair_brute


N_VALUES = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
BRUTE_FORCE_LIMIT_S = 60.0          # stop brute force after this many seconds
REPEATS = 3                          # take the median of 3 runs


def generate_points(n, seed=42):
    """Random points with a fixed seed for reproducibility."""
    rng = random.Random(seed)
    return [(rng.uniform(0, 1e6), rng.uniform(0, 1e6)) for _ in range(n)]


def time_call(fn, points):
    """Run fn(points) and return elapsed seconds (median of REPEATS)."""
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn(points)
        times.append(time.perf_counter() - t0)
    times.sort()
    return times[len(times) // 2]    # median


def main():
    rows = []

    print(f"{'n':>7}  {'D&C (s)':>10}  {'Brute (s)':>12}")
    print("-" * 34)

    for n in N_VALUES:
        pts = generate_points(n)

        t_dc = time_call(closest_pair, pts)

        t_bf = None
        if n <= 32000:               # brute force gets very slow past ~32k
            t_bf = time_call(closest_pair_brute, pts)
            if t_bf > BRUTE_FORCE_LIMIT_S:
                t_bf = None

        rows.append((n, t_dc, t_bf))
        bf_str = f"{t_bf:.4f}" if t_bf is not None else "skipped"
        print(f"{n:>7}  {t_dc:>10.4f}  {bf_str:>12}")

    # ---- save the table as CSV for the report ----
    with open("timings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "D&C_time_s", "Brute_time_s"])
        for n, t_dc, t_bf in rows:
            w.writerow([n, f"{t_dc:.6f}", "" if t_bf is None else f"{t_bf:.6f}"])

    # ---- log-log graph ----
    ns = [r[0] for r in rows]
    dc = [r[1] for r in rows]
    bf_ns = [r[0] for r in rows if r[2] is not None]
    bf = [r[2] for r in rows if r[2] is not None]

    plt.figure(figsize=(8, 5.5))
    plt.loglog(ns, dc, "o-", label="Divide & Conquer", linewidth=2)
    if bf:
        plt.loglog(bf_ns, bf, "s-", label="Brute force", linewidth=2)
    plt.xlabel("n (log scale)")
    plt.ylabel("time (s, log scale)")
    plt.title("Closest pair: divide-and-conquer vs brute force")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("timing_graph.png", dpi=150)
    print("\nSaved: timing_graph.png, timings.csv")


if __name__ == "__main__":
    main()
