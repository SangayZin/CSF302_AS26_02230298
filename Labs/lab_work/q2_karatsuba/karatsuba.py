"""
Q2 - Large Integer Multiplication: Traditional vs Karatsuba

Multiplies two big non-negative integers given as digit strings.

Why use strings instead of Python's int?
    Python's int alread
"""

import random
import sys

# Karatsuba splits deeply, so raise the recursion limit for big inputs
sys.setrecursionlimit(10000)


# ======================================================================
# Helpers for digit strings
# ======================================================================
def random_digits(n, allow_zero_start=True):
    # Returns a random n-digit string
    if n <= 0:
        return "0"
    first = random.choice("123456789") if not allow_zero_start \
            else random.choice("0123456789")
    rest = "".join(random.choice("0123456789") for _ in range(n - 1))
    return first + rest


def strip_leading_zeros(s):
    # Removes leading zeros; returns "0" if string is all zeros
    s = s.lstrip("0")
    return s if s else "0"


def pad_to_equal(a, b):
    # Pads the shorter string with leading zeros so both are the same length
    n = max(len(a), len(b))
    return a.zfill(n), b.zfill(n)


def pad_to_power_of_two(a, b):
    # Pads both strings to the next power-of-2 length (Karatsuba likes this)
    n = max(len(a), len(b))
    p = 1
    while p < n:
        p <<= 1
    return a.zfill(p), b.zfill(p)


# ======================================================================
# 1) Traditional grade-school multiplication  O(n^2)
# ======================================================================
def grade_school_multiply(a: str, b: str) -> str:
    # Multiplies two number-strings the way you'd do it by hand on paper
    a = strip_leading_zeros(a)
    b = strip_leading_zeros(b)
    if a == "0" or b == "0":
        return "0"

    # Turn strings into lists of digits (leftmost = most significant)
    A = [int(c) for c in a]
    B = [int(c) for c in b]
    n, m = len(A), len(B)

    # Result can have at most n + m digits
    result = [0] * (n + m)

    # Multiply each digit of A by each digit of B (right to left)
    for i in range(n - 1, -1, -1):
        carry = 0
        for j in range(m - 1, -1, -1):
            prod = A[i] * B[j] + result[i + j + 1] + carry
            result[i + j + 1] = prod % 10   # keep last digit
            carry = prod // 10              # carry the rest
        result[i] += carry

    # Convert digits back to string and clean up leading zeros
    return strip_leading_zeros("".join(map(str, result)))


# ======================================================================
# 2) Karatsuba multiplication  O(n^1.585)
# ======================================================================
def _add_strings(a: str, b: str) -> str:
    # Adds two number-strings digit by digit
    a, b = pad_to_equal(a, b)
    carry = 0
    out = []
    for i in range(len(a) - 1, -1, -1):
        s = (ord(a[i]) - 48) + (ord(b[i]) - 48) + carry
        out.append(chr((s % 10) + 48))
        carry = s // 10
    if carry:
        out.append(str(carry))
    return strip_leading_zeros("".join(reversed(out)))


def _sub_strings(a: str, b: str) -> str:
    # Subtracts b from a (assumes a >= b), digit by digit
    a, b = pad_to_equal(a, b)
    borrow = 0
    out = []
    for i in range(len(a) - 1, -1, -1):
        d = (ord(a[i]) - 48) - (ord(b[i]) - 48) - borrow
        if d < 0:
            d += 10
            borrow = 1
        else:
            borrow = 0
        out.append(chr(d + 48))
    return strip_leading_zeros("".join(reversed(out)))


def karatsuba_multiply(a: str, b: str, base_case=16) -> str:
    # Recursive Karatsuba multiplication
    # T(n) = 3·T(n/2) + O(n)  →  O(n^log2(3)) ≈ O(n^1.585)
    a = strip_leading_zeros(a)
    b = strip_leading_zeros(b)
    if a == "0" or b == "0":
        return "0"

    n = max(len(a), len(b))

    # For small numbers, just use the normal method
    if n <= base_case:
        return grade_school_multiply(a, b)

    # Make length even so we can split cleanly in half
    if n % 2 != 0:
        n += 1
    a = a.zfill(n)
    b = b.zfill(n)

    half = n // 2
    a_low, a_high = a[half:], a[:half]   # low = right half, high = left half
    b_low, b_high = b[half:], b[:half]

    # Karatsuba's trick: only 3 recursive multiplications instead of 4
    z0 = karatsuba_multiply(a_low,  b_low,  base_case)                 # low * low
    z2 = karatsuba_multiply(a_high, b_high, base_case)                 # high * high
    z1 = karatsuba_multiply(_add_strings(a_low, a_high),
                            _add_strings(b_low, b_high),
                            base_case)                                  # (low+high) * (low+high)
    z1 = _sub_strings(_sub_strings(z1, z2), z0)                         # middle term

    # Combine: result = z2 * 10^(2*half) + z1 * 10^half + z0
    result = _add_strings(
        _add_strings(z2 + "0" * (2 * half), z1 + "0" * half),
        z0
    )
    return strip_leading_zeros(result)


# ======================================================================
# Tests - only run when this file is executed directly
# ======================================================================
if __name__ == "__main__":
    print("=" * 74)
    print("Q2 - Traditional vs Karatsuba Large Integer Multiplication")
    print("=" * 74)

    # ----- Traditional tests -----
    print("\n--- Traditional (grade-school) ---")
    assert grade_school_multiply("12", "34") == str(12 * 34)
    print(" 12 × 34 =", grade_school_multiply("12", "34"))

    assert grade_school_multiply("0", "99999") == "0"
    assert grade_school_multiply("100", "200") == "20000"
    print(" 100 × 200 =", grade_school_multiply("100", "200"))

    # ----- Karatsuba tests -----
    print("\n--- Karatsuba ---")
    assert karatsuba_multiply("12", "34") == str(12 * 34)
    print(" 12 × 34 =", karatsuba_multiply("12", "34"))

    assert karatsuba_multiply("0", "99999") == "0"
    assert karatsuba_multiply("100", "200") == "20000"
    print(" 100 × 200 =", karatsuba_multiply("100", "200"))

    # ----- Check both match Python's int for various sizes -----
    print("\n--- Cross-verification for random sizes ---")
    random.seed(42)
    for n in [8, 16, 32, 64, 128, 256, 512, 1024]:
        a = random_digits(n)
        b = random_digits(n)
        expected = str(int(a) * int(b))

        t = grade_school_multiply(a, b)
        k = karatsuba_multiply(a, b)

        assert t == expected, f"Traditional FAILED at n={n}"
        assert k == expected, f"Karatsuba   FAILED at n={n}"
        assert t == k,         f"MISMATCH between algorithms at n={n}"

        print(f" {n:>4}-digit  Traditional == Karatsuba == Python int")

    print("\n All Q2 tests PASSED (Traditional == Karatsuba == Python int).")