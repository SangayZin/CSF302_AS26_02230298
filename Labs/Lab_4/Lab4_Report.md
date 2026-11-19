# CSF302 Lab 4: Modular and Matrix Exponentiation

## Files

| File | Contents |
|---|---|
| `part_a_modexp.py` | Naive, binary and bitwise modular exponentiation, validation, output comparison, timing |
| `part_b_matrix.py` | Matrix multiplication mod m, identity matrix, naive and binary matrix power, Fibonacci, walk counting, benchmark |

Run each file with `python part_a_modexp.py` and `python part_b_matrix.py`. Only the standard library is used. All results below were produced with Python 3.13 on a Linux machine, so the exact times will be different on another computer, but the patterns should be the same.

---

## Part A: Efficient Modular Exponentiation

### A1 and A2: Naive and binary exponentiation

The naive version starts with `result = 1 % m` and multiplies by `a` exactly `b` times, reducing modulo `m` after every step so the numbers never grow larger than `m^2`. This takes Θ(b) multiplications.

The binary version (square-and-multiply) looks at the exponent one bit at a time. In each loop it squares the base, and when the current bit is 1 it also multiplies the result by the base. Since the exponent is halved each time, the loop runs about log2(b) times, so the total work is Θ(log b) multiplications.

Starting with `1 % m` instead of `1` matters for the case `m = 1`, where every answer must be 0.

### A3: Comparing the outputs

All three versions were run on 15 test cases (10 fixed cases and 5 random ones) and compared with Python's built-in `pow(a, b, m)`.

| a | b | m | naive | binary | bitwise | pow() |
|---|---|---|---|---|---|---|
| 2 | 10 | 1000 | 24 | 24 | 24 | 24 |
| 3 | 200 | 13 | 9 | 9 | 9 | 9 |
| 7 | 0 | 5 | 1 | 1 | 1 | 1 |
| 5 | 117 | 19 | 1 | 1 | 1 | 1 |
| 123456789 | 1000 | 1000000007 | 620139939 | 620139939 | 620139939 | 620139939 |
| -3 | 5 | 7 | 2 | 2 | 2 | 2 |
| 10 | 25 | 1 | 0 | 0 | 0 | 0 |
| 2 | 12345 | 998244353 | 879276814 | 879276814 | 879276814 | 879276814 |
| 987654321 | 99999 | 1000000009 | 3427790 | 3427790 | 3427790 | 3427790 |
| 0 | 0 | 9 | 1 | 1 | 1 | 1 |
| -504972 | 2484 | 110773682 | 37251298 | 37251298 | 37251298 | 37251298 |
| 512501 | 3244 | 514191761 | 459782379 | 459782379 | 459782379 | 459782379 |
| -675000 | 738 | 71420045 | 70556445 | 70556445 | 70556445 | 70556445 |
| -958441 | 3289 | 589915738 | 562842105 | 562842105 | 562842105 | 562842105 |
| 925091 | 2370 | 859479168 | 751766473 | 751766473 | 751766473 | 751766473 |

All 15 cases agree, including negative bases, `b = 0` and `m = 1`. Note that `0^0` is treated as 1, which is the same convention Python uses.

### A4: Bitwise version

`binary_mod_pow_bitwise` is the same algorithm, but it checks whether the exponent is odd with `b & 1` and halves it with `b >>= 1` instead of using `b % 2` and `b // 2`. The lowest bit of a number is 1 exactly when the number is odd, and shifting right by one position divides by 2 and drops the remainder, so both versions do the same steps.

### A5: Input validation

A shared `validate` function is called at the start of every version:

| Input | a, b, m | Result |
|---|---|---|
| zero exponent | 5, 0, 7 | 1 |
| zero exponent with m = 1 | 5, 0, 1 | 0 |
| negative base | -2, 3, 5 | 2 (since -2 mod 5 = 3 and 3^3 = 27 = 2 mod 5) |
| negative exponent | 2, -3, 5 | ValueError: exponent must be non-negative |
| modulus m = 0 | 2, 3, 0 | ValueError: modulus must be at least 1 |
| negative modulus | 2, 3, -7 | ValueError: modulus must be at least 1 |

A negative base is reduced with `a % m` first. In Python the `%` operator already gives a value in `0..m-1` when `m` is positive, so no extra step is needed.

### A6: Execution time

Base a = 123456789 and modulus m = 10^9 + 7. Small exponents finish in microseconds, so each function was run repeatedly for at least 0.2 seconds and the average was taken.

| b | naive (s) | binary (s) | bitwise (s) | naive / bitwise |
|---|---|---|---|---|
| 10 | 1.083e-06 | 9.588e-07 | 8.468e-07 | 1.3x |
| 100 | 4.308e-06 | 1.207e-06 | 1.142e-06 | 3.8x |
| 1,000 | 4.287e-05 | 1.588e-06 | 1.821e-06 | 23.5x |
| 10,000 | 6.783e-04 | 2.672e-06 | 1.732e-06 | 391.6x |
| 100,000 | 4.182e-03 | 2.121e-06 | 2.085e-06 | 2005.5x |
| 1,000,000 | 4.450e-02 | 2.437e-06 | 2.236e-06 | 19895.4x |

Observations:

- The naive time grows by roughly 10 times whenever b grows by 10 times, which is what Θ(b) predicts.
- The binary time hardly changes. Going from b = 10 to b = 10^6 only adds about 16 extra loop iterations (log2(10^6) is about 20), so the time only goes from about 1 to 2.4 microseconds.
- At b = 10^6 the binary method is about 20,000 times faster. For b = 10^18, which is common in practice, the naive method would never finish, while the binary method would still take only a few microseconds.
- The binary and bitwise versions take almost the same time. In Python both versions spend most of their time on the big integer multiplications, so swapping `% 2` for `& 1` makes very little difference. In a language like C the bitwise version can be slightly faster, but the real gain comes from the algorithm, not from the bit tricks.

---

## Part B: Efficient Matrix Modular Exponentiation

### B1 and B2: Matrix multiplication and identity

`mat_mult(A, B, m)` checks that both matrices are square and the same size, then computes each entry as the dot product of a row of A and a column of B, reduced modulo m. This is Θ(d^3) for d x d matrices. `identity(d)` returns a matrix with 1 on the diagonal and 0 elsewhere.

Example output:

```
A = [[1, 2], [3, 4]], B = [[5, 6], [7, 8]]
A x B mod 10 = [[9, 2], [3, 0]]      (real product is [[19, 22], [43, 50]])
A x I = A ? True
```

### B3 and B4: Naive and binary matrix powers

The naive version starts from the identity matrix and multiplies by A, n times, which costs Θ(n d^3). The binary version uses the same square-and-multiply idea as Part A, which costs Θ(d^3 log n). Both functions also validate the input: a negative exponent, a modulus below 1, or a non-square matrix raises a `ValueError`, and negative entries are reduced modulo m first.

### B5: Comparison

| d | n | m | first row of A^n mod m | naive = binary |
|---|---|---|---|---|
| 2 | 10 | 1000 | [89, 55] | yes |
| 2 | 13 | 1,000,000 | [8192, 0] | yes |
| 2 | 0 | 7 | [1, 0] | yes |
| 2 | 9 | 11 | [9, 0] | yes |
| 3 | 50 | 10^9 + 7 | [490344305, 397193652, 171507379] | yes |
| 2 | 100 | 1 | [0, 0] | yes |
| 2 | 115 | 149827708 | [6004805, 5835374] | yes |
| 2 | 217 | 34126398 | [21073154, 9831514] | yes |
| 2 | 14 | 602632299 | [188876689, 426240423] | yes |
| 3 | 4 | 814763204 | [746180191, 706937637, 532296037] | yes |

The first row checks a known Fibonacci matrix ([[1,1],[1,0]]^10 has F(11) = 89 and F(10) = 55), and the second checks a diagonal matrix (2^13 = 8192). The case with a negative entry and the case with n = 0 also match.

### B6 and B7: Fibonacci numbers

The key identity is

```
[[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
```

so F(n) mod m is the top-right entry of the matrix power.

- F(0..15) mod 1000 = 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610
- The matrix result matches a simple loop for every n from 0 to 499.
- F(90) mod 10^18 = 880067194370816120, which matches the last 18 digits of the real value F(90) = 2880067194370816120.
- F(1000) mod (10^9 + 7) = 517691607

For n = 10^18:

```
F(10^18) mod (10^9 + 7) = 209783453
computed in 0.214 ms using about 60 squarings
```

10^18 has 60 bits, so the binary method needs about 60 squarings and at most 60 extra multiplications of 2 x 2 matrices. Generating Fibonacci numbers one by one would need 10^18 steps, which would take about 32 years even at a billion steps per second, and thousands of years in a Python loop.

### B8: Counting walks in a directed graph

If A is the adjacency matrix of a graph, then entry (u, v) of A^k is the number of walks from u to v using exactly k edges. This works because each matrix multiplication extends every walk by one edge and adds up all the ways to get from u to v.

Graph used (5 vertices): 0→1, 0→2, 1→2, 1→3, 2→3, 2→0, 3→4, 4→0, 4→1.

To check the answers, a brute-force depth-first search counts the walks directly for small k.

| from | to | k | matrix power | brute-force DFS |
|---|---|---|---|---|
| 0 | 3 | 2 | 2 | 2 |
| 0 | 3 | 3 | 1 | 1 |
| 0 | 0 | 3 | 1 | 1 |
| 2 | 4 | 4 | 2 | 2 |
| 4 | 3 | 6 | 10 | 10 |
| 0 | 4 | 10 | 47 | 47 |

For example, the two walks from 0 to 3 with 2 edges are 0→1→3 and 0→2→3. With k = 10^12 the number of walks from 0 to 4, modulo 10^9 + 7, is 839991412. The brute force would be hopeless here, but the matrix method only needs about 40 squarings.

### B9: Benchmark

Random matrices with entries below 10^9 + 7. Times are in seconds (averaged over 5 runs for d ≤ 8, one run for d = 16 and 32).

| n | d=2 naive | d=2 binary | d=4 naive | d=4 binary | d=8 naive | d=8 binary | d=16 naive | d=16 binary | d=32 naive | d=32 binary |
|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 0.00004 | 0.00002 | 0.00014 | 0.00006 | 0.00072 | 0.00029 | 0.00449 | 0.00172 | 0.02737 | 0.01484 |
| 32 | 0.00009 | 0.00002 | 0.00029 | 0.00007 | 0.00143 | 0.00034 | 0.00878 | 0.00180 | 0.08902 | 0.01985 |
| 64 | 0.00018 | 0.00003 | 0.00058 | 0.00008 | 0.00291 | 0.00037 | 0.02338 | 0.00343 | 0.14276 | 0.01423 |
| 128 | 0.00040 | 0.00003 | 0.00119 | 0.00009 | 0.00590 | 0.00042 | 0.04338 | 0.00287 | 0.26836 | 0.01637 |
| 256 | 0.00066 | 0.00003 | 0.00235 | 0.00010 | 0.01183 | 0.00048 | 0.07749 | 0.00299 | 0.54095 | 0.01726 |
| 512 | 0.00144 | 0.00003 | 0.00470 | 0.00010 | 0.02362 | 0.00051 | 0.14169 | 0.00318 | 1.09148 | 0.02061 |
| 1024 | 0.00267 | 0.00003 | 0.00934 | 0.00012 | 0.06434 | 0.00091 | 0.28825 | 0.00312 | 1.92996 | 0.02105 |
| 2048 | 0.00530 | 0.00003 | 0.01877 | 0.00013 | 0.10498 | 0.00061 | 0.55606 | 0.00348 | 3.92241 | 0.02400 |
| 4096 | 0.01068 | 0.00004 | 0.04226 | 0.00014 | 0.25352 | 0.00070 | 1.12650 | 0.00368 | 8.56335 | 0.04650 |

Speed-up of binary over naive:

| n | d=2 | d=4 | d=8 | d=16 | d=32 |
|---|---|---|---|---|---|
| 16 | 2.4x | 2.3x | 2.5x | 2.6x | 1.8x |
| 256 | 22.1x | 22.6x | 24.5x | 25.9x | 31.3x |
| 4096 | 277.3x | 311.1x | 364.6x | 306.0x | 184.2x |

Observations:

- Effect of n: the naive time doubles every time n doubles, so it is linear in n. The binary time only grows a little, because doubling n adds just one more squaring.
- Effect of d: going from d = 16 to d = 32 makes the naive time about 7.6 times larger (1.13 s to 8.56 s), which is close to the factor of 8 expected from Θ(d^3) multiplication.
- Expected speed-up: for n = 2^12 the naive method does 4096 multiplications while the binary method does 12 squarings and 1 multiplication (13 in total), so the speed-up should be about 4096 / 13 ≈ 315. The measured values are close to this. The lower value for d = 32 comes from a single noisy measurement of the binary time (0.0465 s, almost double the time at n = 2048).
- Both methods have the same d^3 cost per multiplication, so the dimension does not change the speed-up much. What matters is the number of multiplications: n versus about log2(n).

---

## Conclusion

Repeated squaring turns a problem that needs n multiplications into one that needs about 2 log2(n) multiplications. This works for both numbers and matrices, because matrix multiplication is associative just like integer multiplication. With this idea, values like F(10^18) mod (10^9 + 7) or the number of walks of length 10^12 in a graph can be computed in well under a millisecond, while the naive approach would never finish.
