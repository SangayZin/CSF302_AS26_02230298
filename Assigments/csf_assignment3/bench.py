"""Part C benchmarking harness."""

import time
import random
import sys
from sorts import quicksort_basic, quicksort_improved

sys.setrecursionlimit(100000)


def make_input(kind, n):
    if kind == "random":
        return [random.randint(-10**9, 10**9) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":
        return [random.randint(0, 9) for _ in range(n)]


def time_one(sort_fn, arr, cutoff=None):
    a = arr[:]  # don't mutate original across trials
    start = time.perf_counter()
    try:
        if cutoff is None:
            sort_fn(a)
        else:
            sort_fn(a, cutoff=cutoff)
    except RecursionError:
        return None
    return time.perf_counter() - start


if __name__ == "__main__":
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
    kinds = ["random", "sorted", "duplicates"]

    print(f"{'alg':<20}{'kind':<12}{'n':<8}{'time (s)'}")
    for kind in kinds:
        for n in sizes:
            data = make_input(kind, n)
            t = time_one(quicksort_basic, data)
            print(f"{'quicksort_basic':<20}{kind:<12}{n:<8}{t if t is not None else 'CRASH'}")
            t = time_one(quicksort_improved, data)
            print(f"{'quicksort_improved':<20}{kind:<12}{n:<8}{t if t is not None else 'CRASH'}")
