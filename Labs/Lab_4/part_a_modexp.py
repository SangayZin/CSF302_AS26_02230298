"""
Lab 4 Part A: Efficient Modular Exponentiation

Computes a^b mod m in three ways:
  1. naive repeated multiplication          O(b) multiplications
  2. binary exponentiation (square-and-multiply, using % and //)   O(log b)
  3. binary exponentiation using bitwise operations (b & 1, b >>= 1)

Run:  python part_a_modexp.py
"""

import random
import time


def validate(a, b, m):
    """Check the inputs and return the base reduced into the range 0..m-1."""
    if not all(isinstance(x, int) for x in (a, b, m)):
        raise TypeError("a, b and m must all be integers")
    if m < 1:
        raise ValueError(f"modulus must be at least 1, got m = {m}")
    if b < 0:
        raise ValueError(f"exponent must be non-negative, got b = {b}")
    # Python's % already returns a non-negative result for a positive m,
    # so a negative base like -3 becomes m - 3 here.
    return a % m


def naive_mod_pow(a, b, m):
    a = validate(a, b, m)
    result = 1 % m          # 1 % m handles m = 1, where every answer is 0
    for _ in range(b):
        result = (result * a) % m
    return result


def binary_mod_pow(a, b, m):
    a = validate(a, b, m)
    result = 1 % m
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        b = b // 2
    return result


def binary_mod_pow_bitwise(a, b, m):
    a = validate(a, b, m)
    result = 1 % m
    while b:
        if b & 1:               # lowest bit set means the exponent is odd
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1                 # shifting right by one halves the exponent
    return result


def compare_outputs():
    print("=" * 78)
    print("Output comparison: naive vs binary vs bitwise vs Python's pow()")
    print("=" * 78)
    cases = [
        (2, 10, 1000),
        (3, 200, 13),
        (7, 0, 5),
        (5, 117, 19),
        (123456789, 1000, 1_000_000_007),
        (-3, 5, 7),
        (10, 25, 1),
        (2, 12345, 998_244_353),
        (987654321, 99999, 1_000_000_009),
        (0, 0, 9),
    ]
    rng = random.Random(4)
    for _ in range(5):
        cases.append((rng.randint(-10**6, 10**6), rng.randint(0, 5000), rng.randint(1, 10**9)))

    header = f"{'a':>12} {'b':>6} {'m':>14} | {'naive':>11} {'binary':>11} {'bitwise':>11} {'pow()':>11} | match"
    print(header)
    print("-" * len(header))
    all_ok = True
    for a, b, m in cases:
        n = naive_mod_pow(a, b, m)
        bi = binary_mod_pow(a, b, m)
        bw = binary_mod_pow_bitwise(a, b, m)
        ref = pow(a, b, m)
        ok = n == bi == bw == ref
        all_ok = all_ok and ok
        print(f"{a:>12} {b:>6} {m:>14} | {n:>11} {bi:>11} {bw:>11} {ref:>11} | {'yes' if ok else 'NO'}")
    print(f"\nAll {len(cases)} cases agree: {all_ok}\n")


def show_validation():
    print("=" * 78)
    print("Input validation")
    print("=" * 78)
    tests = [
        ("zero exponent", (5, 0, 7)),
        ("zero exponent with m = 1", (5, 0, 1)),
        ("negative base", (-2, 3, 5)),
        ("negative exponent", (2, -3, 5)),
        ("modulus m = 0", (2, 3, 0)),
        ("negative modulus", (2, 3, -7)),
    ]
    for label, (a, b, m) in tests:
        try:
            value = binary_mod_pow_bitwise(a, b, m)
            print(f"{label:<26} a={a}, b={b}, m={m}  ->  {value}")
        except (ValueError, TypeError) as err:
            print(f"{label:<26} a={a}, b={b}, m={m}  ->  {type(err).__name__}: {err}")
    print()


def average_time(func, args, min_total=0.2):
    """Run func repeatedly until min_total seconds have passed and return the
    average time per call. Small exponents finish in microseconds, so a single
    measurement would be mostly timer noise."""
    runs = 0
    start = time.perf_counter()
    while True:
        func(*args)
        runs += 1
        elapsed = time.perf_counter() - start
        if elapsed >= min_total:
            return elapsed / runs


def timing_experiment():
    print("=" * 78)
    print("Execution time (a = 123456789, m = 10^9 + 7)")
    print("=" * 78)
    a, m = 123456789, 1_000_000_007
    print(f"| {'b':>9} | {'naive (s)':>12} | {'binary (s)':>12} | {'bitwise (s)':>12} | {'naive / bitwise':>15} |")
    print(f"|{'-' * 11}|{'-' * 14}|{'-' * 14}|{'-' * 14}|{'-' * 17}|")
    for exp in range(1, 7):
        b = 10 ** exp
        t_naive = average_time(naive_mod_pow, (a, b, m))
        t_bin = average_time(binary_mod_pow, (a, b, m))
        t_bit = average_time(binary_mod_pow_bitwise, (a, b, m))
        print(f"| {b:>9} | {t_naive:>12.3e} | {t_bin:>12.3e} | {t_bit:>12.3e} | {t_naive / t_bit:>14.1f}x |")
    print()


if __name__ == "__main__":
    compare_outputs()
    show_validation()
    timing_experiment()
