"""Tests for sorts.py, Part B."""

import random
from sorts import quicksort_basic, quicksort_improved


def check(sort_fn):
    # random lists
    for _ in range(500):
        n = random.randint(0, 100)
        a = [random.randint(-1000, 1000) for _ in range(n)]
        b = sorted(a)
        sort_fn(a)
        assert a == b, f"random failed: in {b} out {a}"

    # specific cases
    cases = [
        [],
        [1],
        [7, 7, 7, 7, 7],
        list(range(100)),
        list(range(100, 0, -1)),
        [-5, -1, -100, 3, -7, 0, -2],
    ]
    for case in cases:
        a = case[:]
        b = sorted(a)
        sort_fn(a)
        assert a == b, f"case {case} failed: got {a}, want {b}"


def test_quicksort_basic():
    check(quicksort_basic)


def test_quicksort_improved():
    check(quicksort_improved)


if __name__ == "__main__":
    test_quicksort_basic()
    test_quicksort_improved()
    print("All tests passed.")