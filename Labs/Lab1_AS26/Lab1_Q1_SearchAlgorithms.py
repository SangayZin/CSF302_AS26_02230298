"""
Lab 1 - Question 1
Linear Search vs Binary Search (with benchmarking)

"""

import random
import time

# Input sizes required by the lab specification
INPUT_SIZES_298 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

# Number of repetitions used to compute the average time
RUNS_298 = 5


# ---------------------------------------------------------------------------
# Algorithm 1: Linear Search
# ---------------------------------------------------------------------------
def LinearSearch_298(data_list, target_value):
    """
    Linear Search: scans the list one element at a time
    from left to right until the target is found or the
    list ends.

    Time Complexity: O(n)
    """
    for index_298 in range(len(data_list)):
        if data_list[index_298] == target_value:
            return index_298  # Found, return the index
    return -1  # Not found


# ---------------------------------------------------------------------------
# Algorithm 2: Binary Search (requires a SORTED list)
# ---------------------------------------------------------------------------
def BinarySearch_298(sorted_list, target_value):
    """
    Binary Search: repeatedly divides the sorted list in half
    to locate the target value.

    Time Complexity: O(log n)
    """
    low_298 = 0
    high_298 = len(sorted_list) - 1

    while low_298 <= high_298:
        mid_298 = (low_298 + high_298) // 2  # Middle index
        if sorted_list[mid_298] == target_value:
            return mid_298  # Found, return the index
        elif sorted_list[mid_298] < target_value:
            low_298 = mid_298 + 1  # Search the right half
        else:
            high_298 = mid_298 - 1  # Search the left half
    return -1  # Not found


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def GenerateData_298(size_298):
    """Generates a random unsorted dataset of the given size."""
    return [random.randint(0, size_298 * 10) for _ in range(size_298)]


def SortData_298(data_list):
    """Sorts the dataset before applying Binary Search."""
    return sorted(data_list)


def MeasureAlgorithm_298(search_function_298, dataset_298, target_298, runs_298=RUNS_298):
    """
    Generic timing helper used for both Linear and Binary Search.
    Returns the average time (in seconds) across 'runs_298' repetitions.
    """
    total_time_298 = 0.0
    for _ in range(runs_298):
        start_298 = time.perf_counter()
        search_function_298(dataset_298, target_298)
        end_298 = time.perf_counter()
        total_time_298 += (end_298 - start_298)
    return total_time_298 / runs_298


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def RunBenchmark_298():
    """Runs the full benchmark across all required input sizes."""
    print(f"{'Size':>10} | {'Linear Search (s)':>20} | {'Binary Search (s)':>20}")
    print("-" * 56)

    results_298 = []

    for size_298 in INPUT_SIZES_298:
        # Step 1: Generate random dataset
        unsorted_data_298 = GenerateData_298(size_298)
        target_298 = unsorted_data_298[size_298 // 2]  # pick a real value to guarantee a hit

        # Step 2: Sort a copy of the dataset for Binary Search
        sorted_data_298 = SortData_298(unsorted_data_298)

        # Step 3: Measure average execution time for Linear Search
        linear_time_298 = MeasureAlgorithm_298(LinearSearch_298, unsorted_data_298, target_298)

        # Step 4: Measure average execution time for Binary Search
        binary_time_298 = MeasureAlgorithm_298(BinarySearch_298, sorted_data_298, target_298)

        results_298.append((size_298, linear_time_298, binary_time_298))
        print(f"{size_298:>10} | {linear_time_298:>20.6f} | {binary_time_298:>20.8f}")

    return results_298


if __name__ == "__main__":
    # Quick standalone demo of both algorithms
    sample_data_298 = GenerateData_298(20)
    sample_sorted_298 = SortData_298(sample_data_298)
    target_298 = sample_sorted_298[10]

    print("=== Standalone Demo ===")
    print("Sample Data (unsorted):", sample_data_298)
    print("Sample Data (sorted)  :", sample_sorted_298)
    print("Target Value:", target_298)
    print("Linear Search found at index:", LinearSearch_298(sample_data_298, target_298))
    print("Binary Search found at index:", BinarySearch_298(sample_sorted_298, target_298))
    print()

    # Full benchmark across all required input sizes
    print("=== Benchmark ===")
    RunBenchmark_298()
