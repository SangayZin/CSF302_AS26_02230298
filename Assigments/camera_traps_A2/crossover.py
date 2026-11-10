"""Find the smallest n where D&C is faster than brute force.

Uses median of several repeats for stability at tiny n.
"""

import random
import time

from closest import closest_pair, closest_pair_brute


def generate_points(n, seed=7):
    rng = random.Random(seed)
    return [(rng.uniform(0, 1e6), rng.uniform(0, 1e6)) for _ in range(n)]


def time_call(fn, points, repeats=20):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(points)
        times.append(time.perf_counter() - t0)
    times.sort()
    return times[len(times) // 2]


def main():
    print(f"{'n':>5}  {'D&C (ms)':>10}  {'Brute (ms)':>12}  {'faster':>10}")
    print("-" * 46)

    crossover = None
    for n in range(10, 401, 10):
        pts = generate_points(n)
        t_dc = time_call(closest_pair, pts) * 1000
        t_bf = time_call(closest_pair_brute, pts) * 1000
        faster = "D&C" if t_dc < t_bf else "brute"
        print(f"{n:>5}  {t_dc:>10.3f}  {t_bf:>12.3f}  {faster:>10}")
        if crossover is None and t_dc < t_bf:
            crossover = n

    if crossover is not None:
        print(f"\n>>> Crossover: D&C becomes faster at n = {crossover}")
    else:
        print("\n>>> No crossover found in [10, 400]")


if __name__ == "__main__":
    main()
