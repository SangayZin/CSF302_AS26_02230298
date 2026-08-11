"""
Lab 1 - Question 2
Bubble Sort vs Merge Sort (with benchmarking)


Steps performed:
1. Implement Bubble Sort.
2. Implement Merge Sort.
3. Generate random arrays.
4. Measure average execution time.
"""

import random
import time

# Input sizes required by the lab specification
INPUT_SIZES_298 = [100, 500, 1000, 2000, 4000, 8000]

# Number of repetitions used to compute the average time
RUNS_298 = 3


# ---------------------------------------------------------------------------
# Algorithm 1: Bubble Sort
# ---------------------------------------------------------------------------
def BubbleSort_298(data_list):
    """
    Bubble Sort: repeatedly swaps adjacent elements if they
    are in the wrong order, until the whole list is sorted.

    Time Complexity: O(n^2)
    """
    array_298 = data_list.copy()  # avoid mutating the original list
    length_298 = len(array_298)

    for pass_298 in range(length_298 - 1):
        swapped_298 = False
        for index_298 in range(length_298 - pass_298 - 1):
            if array_298[index_298] > array_298[index_298 + 1]:
                array_298[index_298], array_298[index_298 + 1] = (
                    array_298[index_298 + 1],
                    array_298[index_298],
                )
                swapped_298 = True
        if not swapped_298:
            break  # list is already sorted, stop early
    return array_298


# ---------------------------------------------------------------------------
# Algorithm 2: Merge Sort
# ---------------------------------------------------------------------------
def MergeSort_298(data_list):
    """
    Merge Sort: divides the list into halves, recursively sorts
    each half, then merges the sorted halves back together.

    Time Complexity: O(n log n)
    """
    array_298 = data_list.copy()  # avoid mutating the original list

    if len(array_298) <= 1:
        return array_298  # base case: already sorted

    mid_298 = len(array_298) // 2
    left_half_298 = MergeSort_298(array_298[:mid_298])
    right_half_298 = MergeSort_298(array_298[mid_298:])

    return Merge_298(left_half_298, right_half_298)


def Merge_298(left_298, right_298):
    """Merges two sorted lists into a single sorted list."""
    merged_298 = []
    i_298 = j_298 = 0

    while i_298 < len(left_298) and j_298 < len(right_298):
        if left_298[i_298] <= right_298[j_298]:
            merged_298.append(left_298[i_298])
            i_298 += 1
        else:
            merged_298.append(right_298[j_298])
            j_298 += 1

    merged_298.extend(left_298[i_298:])
    merged_298.extend(right_298[j_298:])
    return merged_298


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def GenerateData_298(size_298):
    """Generates a random array of a given size."""
    return [random.randint(0, size_298 * 10) for _ in range(size_298)]


def MeasureAlgorithm_298(sort_function_298, dataset_298, runs_298=RUNS_298):
    """
    Generic timing helper used for both Bubble Sort and Merge Sort.
    Returns the average time (in seconds) across 'runs_298' repetitions.
    """
    total_time_298 = 0.0
    for _ in range(runs_298):
        start_298 = time.perf_counter()
        sort_function_298(dataset_298)
        end_298 = time.perf_counter()
        total_time_298 += (end_298 - start_298)
    return total_time_298 / runs_298


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def RunBenchmark_298():
    """Runs the full benchmark across all required input sizes."""
    print(f"{'Size':>10} | {'Bubble Sort (s)':>18} | {'Merge Sort (s)':>18}")
    print("-" * 52)

    results_298 = []

    for size_298 in INPUT_SIZES_298:
        # Step 1: Generate a random array for this size
        dataset_298 = GenerateData_298(size_298)

        # Step 2: Measure average execution time for Bubble Sort
        bubble_time_298 = MeasureAlgorithm_298(BubbleSort_298, dataset_298)

        # Step 3: Measure average execution time for Merge Sort
        merge_time_298 = MeasureAlgorithm_298(MergeSort_298, dataset_298)

        results_298.append((size_298, bubble_time_298, merge_time_298))
        print(f"{size_298:>10} | {bubble_time_298:>18.6f} | {merge_time_298:>18.6f}")

    return results_298


if __name__ == "__main__":
    # Quick standalone demo of both algorithms
    sample_data_298 = GenerateData_298(10)

    print("=== Standalone Demo ===")
    print("Before Sort:", sample_data_298)
    print("Bubble Sort Result:", BubbleSort_298(sample_data_298))
    print("Merge Sort Result :", MergeSort_298(sample_data_298))
    print()

    # Full benchmark across all required input sizes
    print("=== Benchmark ===")
    RunBenchmark_298()
