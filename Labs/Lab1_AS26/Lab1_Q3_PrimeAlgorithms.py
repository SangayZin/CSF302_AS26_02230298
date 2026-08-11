"""
Lab 1 - Question 3
Naive Trial Division vs Optimized Trial Division vs Sieve of Eratosthenes

"""

import math
import time

# Input sizes required by the lab specification
INPUT_SIZES_298 = [10000, 50000, 100000, 500000, 1000000]

# Naive Trial Division is only run up to this size.
NAIVE_LIMIT_298 = 100000


# ---------------------------------------------------------------------------
# Algorithm 1: Naive Prime Checking using Trial Division
# ---------------------------------------------------------------------------
def IsPrimeNaive_298(number_298):
    """
    Naive primality test: checks divisibility by every
    integer from 2 up to (number_298 - 1).

    Time Complexity: O(n) per number
    """
    if number_298 < 2:
        return False
    for divisor_298 in range(2, number_298):
        if number_298 % divisor_298 == 0:
            return False
    return True


def NaiveTrialDivision_298(limit_298):
    """
    Generates all prime numbers up to (and including) limit_298
    using naive trial division for every candidate number.

    Overall Time Complexity: O(n^2)
    """
    primes_298 = []
    for candidate_298 in range(2, limit_298 + 1):
        if IsPrimeNaive_298(candidate_298):
            primes_298.append(candidate_298)
    return primes_298


# ---------------------------------------------------------------------------
# Algorithm 2: Optimized Trial Division (checking only up to sqrt(n))
# ---------------------------------------------------------------------------
def IsPrimeOptimized_298(number_298):
    """
    Optimized primality test: only checks divisors up to
    sqrt(number_298), since a larger factor would require a
    matching smaller factor that would already have been found.

    Time Complexity: O(sqrt(n)) per number
    """
    if number_298 < 2:
        return False
    if number_298 in (2, 3):
        return True
    if number_298 % 2 == 0:
        return False

    limit_298 = int(math.sqrt(number_298)) + 1
    for divisor_298 in range(3, limit_298, 2):  # only check odd divisors
        if number_298 % divisor_298 == 0:
            return False
    return True


def OptimizedTrialDivision_298(limit_298):
    """
    Generates all prime numbers up to (and including) limit_298
    using optimized trial division (checking divisors up to sqrt(n)).

    Overall Time Complexity: O(n * sqrt(n))
    """
    primes_298 = []
    for candidate_298 in range(2, limit_298 + 1):
        if IsPrimeOptimized_298(candidate_298):
            primes_298.append(candidate_298)
    return primes_298


# ---------------------------------------------------------------------------
# Algorithm 3: Sieve of Eratosthenes
# ---------------------------------------------------------------------------
def SieveOfEratosthenes_298(limit_298):
    """
    Sieve of Eratosthenes: builds a boolean array marking
    non-prime numbers by crossing out multiples of each
    prime starting from 2.

    Time Complexity: O(n log log n)
    """
    if limit_298 < 2:
        return []

    is_prime_298 = [True] * (limit_298 + 1)
    is_prime_298[0] = is_prime_298[1] = False  # 0 and 1 are not prime

    for number_298 in range(2, int(limit_298 ** 0.5) + 1):
        if is_prime_298[number_298]:
            for multiple_298 in range(number_298 * number_298, limit_298 + 1, number_298):
                is_prime_298[multiple_298] = False

    primes_298 = [index_298 for index_298, prime_flag_298 in enumerate(is_prime_298) if prime_flag_298]
    return primes_298


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def MeasureAlgorithm_298(prime_function_298, limit_298, runs_298=1):
    """
    Generic timing helper used for all three prime generation methods.
    Returns the average time (in seconds) across 'runs_298' repetitions.
    """
    total_time_298 = 0.0
    for _ in range(runs_298):
        start_298 = time.perf_counter()
        prime_function_298(limit_298)
        end_298 = time.perf_counter()
        total_time_298 += (end_298 - start_298)
    return total_time_298 / runs_298


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def RunBenchmark_298():
    """Runs the full benchmark across all required input sizes (N)."""
    print(f"{'N':>10} | {'Naive Trial (s)':>18} | {'Optimized Trial (s)':>20} | {'Sieve (s)':>15}")
    print("-" * 72)

    results_298 = []

    for limit_298 in INPUT_SIZES_298:
        # Naive trial division is skipped above NAIVE_LIMIT_298 (too slow, O(n^2))
        if limit_298 <= NAIVE_LIMIT_298:
            naive_time_298 = MeasureAlgorithm_298(NaiveTrialDivision_298, limit_298)
            naive_display_298 = f"{naive_time_298:.6f}"
        else:
            naive_time_298 = None
            naive_display_298 = "skipped (too slow)"

        optimized_time_298 = MeasureAlgorithm_298(OptimizedTrialDivision_298, limit_298)
        sieve_time_298 = MeasureAlgorithm_298(SieveOfEratosthenes_298, limit_298)

        results_298.append((limit_298, naive_time_298, optimized_time_298, sieve_time_298))
        print(f"{limit_298:>10} | {naive_display_298:>18} | {optimized_time_298:>20.6f} | {sieve_time_298:>15.6f}")

    return results_298


if __name__ == "__main__":
    # Quick standalone demo of all three algorithms
    print("=== Standalone Demo ===")
    print("Naive Trial     - Primes up to 100:", NaiveTrialDivision_298(100))
    print("Optimized Trial - Primes up to 100:", OptimizedTrialDivision_298(100))
    print("Sieve           - Primes up to 100:", SieveOfEratosthenes_298(100))
    print()

    # Full benchmark across all required input sizes
    print("=== Benchmark ===")
    RunBenchmark_298()
