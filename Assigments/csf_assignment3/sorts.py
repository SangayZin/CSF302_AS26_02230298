"""Sorting algorithms."""

import random


def quicksort_basic(a):
    """Lomuto partition quicksort with the last element as pivot."""
    _quicksort_basic(a, 0, len(a) - 1)


def _quicksort_basic(a, low, high):
    if low < high:
        p = _partition_lomuto(a, low, high)
        _quicksort_basic(a, low, p - 1)
        _quicksort_basic(a, p + 1, high)


def _partition_lomuto(a, low, high):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1

def insertion_sort_range(a, low, high):
    """Insertion sort a[low..high] inclusive."""
    for i in range(low + 1, high + 1):
        key = a[i]
        j = i - 1
        while j >= low and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def quicksort_improved(a, cutoff=16):
    """Randomised quicksort with insertion-sort cutoff and tail recursion."""
    _quicksort_improved(a, 0, len(a) - 1, cutoff)


def _quicksort_improved(a, low, high, cutoff):
    while low < high:
        # base case: small slice -> insertion sort
        if high - low + 1 <= cutoff:
            insertion_sort_range(a, low, high)
            return

        # random pivot: swap a random index with a[high], then Lomuto
        rand_idx = random.randint(low, high)
        a[rand_idx], a[high] = a[high], a[rand_idx]
        p = _partition_lomuto(a, low, high)

        # recurse on the smaller part, loop on the larger
        if p - low < high - p:
            _quicksort_improved(a, low, p - 1, cutoff)
            low = p + 1
        else:
            _quicksort_improved(a, p + 1, high, cutoff)
            high = p - 1