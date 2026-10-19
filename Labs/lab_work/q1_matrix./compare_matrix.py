"""
Q1 - Part C: Compare Traditional vs Strassen Matrix Multiplication

"""

import time
import random
import matplotlib.pyplot as plt

from matrix_mult import traditional_multiply, generate_matrix
from strassen import strassen_multiply


# ----------------------------------------------------------------------
# Run both methods on one size and return the times
# ----------------------------------------------------------------------
def benchmark(n, seed=42):
    # Returns (traditional_time, strassen_time, do_they_match)
    random.seed(seed)
    A = generate_matrix(n)
    B = generate_matrix(n)

    # Time traditional
    t0 = time.perf_counter()
    C_trad = traditional_multiply(A, B)
    t1 = time.perf_counter()
    t_trad = t1 - t0

    # Time Strassen
    t0 = time.perf_counter()
    C_str = strassen_multiply(A, B)
    t1 = time.perf_counter()
    t_str = t1 - t0

    match = (C_trad == C_str)
    return t_trad, t_str, match


# ----------------------------------------------------------------------
# Main - loop through all sizes and print the comparison
# ----------------------------------------------------------------------
def main():
    sizes = [2, 4, 8, 16, 32, 64, 128, 256]

    results = []  # will hold (n, t_trad, t_str, match, speedup)

    print("=" * 78)
    print(f"{'n':>5} | {'Traditional (s)':>18} | {'Strassen (s)':>18} "
          f"| {'Match?':>7} | {'Speedup':>8}")
    print("=" * 78)

    for n in sizes:
        t_trad, t_str, match = benchmark(n)
        speedup = (t_trad / t_str) if t_str > 0 else float("inf")
        results.append((n, t_trad, t_str, match, speedup))

        print(f"{n:>5} | {t_trad:>18.8f} | {t_str:>18.8f} "
              f"| {'Yes' if match else 'No':>7} | {speedup:>8.2f}x")

    print("=" * 78)

    # Save the table to a text file
    with open("q1_results.txt", "w") as f:
        f.write("Q1 — Traditional vs Strassen Matrix Multiplication\n")
        f.write("=" * 78 + "\n")
        f.write(f"{'n':>5} | {'Traditional (s)':>18} | {'Strassen (s)':>18} "
                f"| {'Match?':>7} | {'Speedup':>8}\n")
        f.write("-" * 78 + "\n")
        for n, t_trad, t_str, match, speedup in results:
            f.write(f"{n:>5} | {t_trad:>18.8f} | {t_str:>18.8f} "
                    f"| {'YES' if match else 'NO':>7} | {speedup:>8.2f}x\n")
        f.write("=" * 78 + "\n")
    print(" Saved table  -> q1_results.txt")

    # Plot both times on a log-log graph
    ns      = [r[0] for r in results]
    t_trads = [r[1] for r in results]
    t_strs  = [r[2] for r in results]

    plt.figure(figsize=(9, 6))
    plt.plot(ns, t_trads, marker="o", linewidth=2,
             label="Traditional  O(n³)")
    plt.plot(ns, t_strs, marker="s", linewidth=2,
             label="Strassen  O(n^2.807)")

    plt.xlabel("Matrix size  n")
    plt.ylabel("Time (seconds)")
    plt.title("Q1: Traditional vs Strassen Matrix Multiplication")
    plt.xscale("log", base=2)   # log scale so powers of 2 look evenly spaced
    plt.yscale("log")           # log scale on y too, easier to compare growth
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    

    print("=" * 78)


if __name__ == "__main__":
    main()