# Lab 1 — Output Screenshots

**Course:** CSF302
**Student Number Suffix used in code (last 3 digits):** 298
**Repository:** CSF302_AS26_02230298
**Folder:** Lab1_AS26

Each question is implemented as a single file containing all required
algorithms plus the benchmarking logic. Running each file prints a
standalone demo followed by the full benchmark table.

---

## Question 1 — `Lab1_Q1_SearchAlgorithms.py`

Contains: Linear Search, Binary Search, dataset generation/sorting, and the
benchmark that measures average execution time (5 runs per size) across
input sizes 1,000 → 1,000,000.

![Q1 Output](screenshots/Screenshot_Q1_SearchAlgorithms.png)

**Observation:** Linear Search's execution time grows roughly linearly
(O(n)) with input size, while Binary Search stays almost constant (O(log n))
because the dataset is sorted beforehand.

---

## Question 2 — `Lab1_Q2_SortAlgorithms.py`

Contains: Bubble Sort, Merge Sort, random array generation, and the
benchmark that measures average execution time (3 runs per size) across
input sizes 100 → 8,000.

![Q2 Output](screenshots/Screenshot_Q2_SortAlgorithms.png)

**Observation:** Bubble Sort's time grows quadratically (O(n²)) — doubling
the input size roughly quadruples the time (e.g. 4000 → 8000 takes ~4x
longer). Merge Sort grows much more slowly (O(n log n)), staying fast even
at 8000 elements.

---

## Question 3 — `Lab1_Q3_PrimeAlgorithms.py`

Contains: Naive Trial Division, Optimized Trial Division (√n), Sieve of
Eratosthenes, and the benchmark that measures execution time across
N = 10,000 → 1,000,000.

![Q3 Output](screenshots/Screenshot_Q3_PrimeAlgorithms.png)

**Note:** Naive Trial Division is O(n²) overall, so testing it at
N = 500,000 or N = 1,000,000 would take tens of minutes to complete. It was
therefore benchmarked only up to N = 100,000 (clearly enough to show its
growth trend), while Optimized Trial Division and the Sieve of Eratosthenes
were benchmarked across the full required range.

**Observation:** Naive Trial Division is by far the slowest, taking over 19
seconds at N = 100,000. Optimized Trial Division (checking divisors only up
to √n) is dramatically faster. The Sieve of Eratosthenes is the fastest of
all three, generating all primes up to 1,000,000 in about 0.1 seconds.

---

## Summary Table of Growth Rates

| Question | Algorithm | Time Complexity |
|---|---|---|
| Q1 | Linear Search | O(n) |
| Q1 | Binary Search | O(log n) |
| Q2 | Bubble Sort | O(n²) |
| Q2 | Merge Sort | O(n log n) |
| Q3 | Naive Trial Division | O(n²) overall |
| Q3 | Optimized Trial Division | O(n√n) overall |
| Q3 | Sieve of Eratosthenes | O(n log log n) |
