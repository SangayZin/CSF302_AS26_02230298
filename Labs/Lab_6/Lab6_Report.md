# CSF302 Lab 6: Dynamic Programming

## Files

| File | Contents |
|---|---|
| `q1_rod_cutting.py` | Naive, memoized and bottom-up rod cutting, call counts and timing |
| `q2_matrix_chain.py` | Bottom-up matrix chain order, parenthesisation, brute-force check, left-to-right cost |
| `q3_lcs.py` | LCS table, reconstruction, two-row version, brute-force timing, line diff |
| `q4_optimal_bst.py` | Optimal binary search tree (optional question) |
| `texts/old_version.txt`, `texts/new_version.txt` | Sample files for the diff |

Run each file with `python <file>.py`. The diff can also be used on any two files with `python q3_lcs.py diff first.txt second.txt`. Only the standard library is used. Times were measured with Python 3.13 on Linux.

---

## Q1: Rod Cutting

Price table: p[1..10] = 1, 5, 8, 9, 10, 17, 17, 20, 24, 30, extended with p[i] = 3i for i > 10.

### Implementation

The recurrence is

```
r(0) = 0
r(n) = max over 1 <= i <= n of ( p[i] + r(n - i) )
```

where i is the length of the first piece.

1. Naive recursion follows the recurrence directly. It solves the same subproblems again and again, so it makes T(n) = 1 + T(0) + T(1) + ... + T(n - 1) = 2^n calls.
2. Top-down memoization uses the same recursion but stores r(n) in a list the first time it is computed. Every later call for the same n returns the stored value immediately.
3. Bottom-up tabulation fills r[0], r[1], ..., r[n] in order, so every value it needs is already in the table. It also records s[j], the size of the first piece in a best cut, which is used to print the actual pieces.

Each version takes a counter, so the number of calls can be measured.

### Best revenue and pieces for n = 1 to 10

| n | best revenue | pieces |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 5 | 2 |
| 3 | 8 | 3 |
| 4 | 10 | 2 + 2 |
| 5 | 13 | 2 + 3 |
| 6 | 17 | 6 |
| 7 | 18 | 1 + 6 |
| 8 | 22 | 2 + 6 |
| 9 | 25 | 3 + 6 |
| 10 | 30 | 10 |

All three versions gave the same revenue for every n. For example, a rod of length 4 earns 10 when cut into 2 + 2, compared with 9 when sold whole.

### Calls and running time

| n | revenue | naive calls | naive time (s) | memo calls | memo time (s) | bottom-up inner steps | bottom-up time (s) |
|---|---|---|---|---|---|---|---|
| 5 | 13 | 32 | 0.000005 | 16 | 0.000002 | 15 | 0.000003 |
| 10 | 30 | 1,024 | 0.000168 | 56 | 0.000008 | 55 | 0.000007 |
| 15 | 45 | 32,768 | 0.016194 | 121 | 0.000015 | 120 | 0.000011 |
| 20 | 60 | 1,048,576 | 0.196553 | 211 | 0.000025 | 210 | 0.000018 |
| 25 | 75 | 33,554,432 | 6.794158 | 326 | 0.000036 | 325 | 0.000026 |

The bottom-up version makes no recursive calls at all, so the table shows how many times its inner loop runs instead, which is the equivalent amount of work.

### Explanation

The naive call count is exactly 2^n. Every time n grows by 5, the number of calls grows by 2^5 = 32, and the time grows by about the same factor (0.197 s to 6.79 s from n = 20 to n = 25). At n = 30 it would take over 3 minutes, and at n = 40 more than two days. The reason is overlapping subproblems: to compute r(25) the naive version computes r(0) over 16 million times.

The memoized version makes exactly n(n + 1)/2 + 1 calls. There are only n + 1 different subproblems, each is solved once, and solving r(j) makes j calls that mostly just read the table. So the work is Θ(n^2). The bottom-up version does the same Θ(n^2) work, n(n + 1)/2 inner steps, but without the cost of function calls, so it is slightly faster than the memoized version for every n.

At n = 25 the dynamic programming versions are about 200,000 times faster than the naive one, even though all three use the same recurrence. The only difference is that the DP versions never solve a subproblem twice.

---

## Q2: Matrix Chain Multiplication

### Implementation

For a chain A1 A2 ... An where Ai has size p[i-1] × p[i], let m[i][j] be the minimum number of scalar multiplications needed to compute Ai...Aj. Then

```
m[i][i] = 0
m[i][j] = min over i <= k < j of ( m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j] )
```

The table is filled by chain length, from 2 up to n, so the two smaller parts are always ready. The best k for each (i, j) is stored in s[i][j], and the parenthesisation is printed recursively from s. This takes Θ(n^3) time and Θ(n^2) space.

The brute-force check uses the same formula as plain recursion without any table, so it tries every possible parenthesisation. The number of parenthesisations is a Catalan number (429 for 8 matrices), so this is only practical for short chains.

The left-to-right cost multiplies ((A1 A2) A3) ... An in order. The running product is always p[0] × p[i], so the cost is the sum of p[0] × p[i-1] × p[i] for i = 2..n.

### Results

Chain 1, dimensions <30, 35, 15, 5, 10, 20, 25>:

```
optimal cost      : 15,125
parenthesisation  : ((A1(A2A3))((A4A5)A6))
brute-force check : 15,125 (match)
left-to-right cost: 40,500 (2.68 times the optimum)
```

The m table for this chain:

| i \ j | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 15750 | 7875 | 9375 | 11875 | 15125 |
| 2 | | 0 | 2625 | 4375 | 7125 | 10500 |
| 3 | | | 0 | 750 | 2500 | 5375 |
| 4 | | | | 0 | 1000 | 3500 |
| 5 | | | | | 0 | 5000 |
| 6 | | | | | | 0 |

Chain 2, dimensions <5, 4, 6, 2, 7>:

```
optimal cost      : 158
parenthesisation  : ((A1(A2A3))A4)
brute-force check : 158 (match)
left-to-right cost: 250 (1.58 times the optimum)
```

Checking chain 2 by hand: A2A3 costs 4 × 6 × 2 = 48 and gives a 4 × 2 matrix, A1(A2A3) costs 5 × 4 × 2 = 40 and gives 5 × 2, and multiplying by A4 costs 5 × 2 × 7 = 70. The total is 48 + 40 + 70 = 158.

Summary including the 5 random chains (lengths 3 to 8, dimensions 2 to 60):

| chain | dimensions | matrices | optimal cost | parenthesisation | left-to-right cost | ratio | brute force agrees |
|---|---|---|---|---|---|---|---|
| Chain 1 | 30, 35, 15, 5, 10, 20, 25 | 6 | 15,125 | ((A1(A2A3))((A4A5)A6)) | 40,500 | 2.68 | yes |
| Chain 2 | 5, 4, 6, 2, 7 | 4 | 158 | ((A1(A2A3))A4) | 250 | 1.58 | yes |
| Random 1 | 54, 7, 33, 50, 18, 4, 2, 11 | 7 | 7,650 | ((A1(A2(A3(A4(A5A6)))))A7) | 155,682 | 20.35 | yes |
| Random 2 | 39, 32, 50, 49, 25, 22, 51, 3, 19 | 8 | 26,808 | ((A1(A2(A3(A4(A5(A6A7))))))A8) | 279,123 | 10.41 | yes |
| Random 3 | 53, 14, 48, 57, 28, 60, 36 | 6 | 141,120 | (A1((((A2A3)A4)A5)A6)) | 468,732 | 3.32 | yes |
| Random 4 | 45, 8, 14, 38, 37, 46, 53, 48 | 7 | 86,256 | (A1(((((A2A3)A4)A5)A6)A7)) | 393,030 | 4.56 | yes |
| Random 5 | 44, 53, 41, 45, 7, 56 | 5 | 61,698 | ((A1(A2(A3A4)))A5) | 207,900 | 3.37 | yes |

### Discussion

The DP answer matched the brute force on all 7 chains, and the expected value of 15,125 for chain 1 was reproduced. The order of multiplication makes a big difference. In Random 1 the left-to-right order costs more than 20 times the optimum. The optimal order there works from the inside out to reach the small dimensions 4 and 2 early (A5 is 18 × 4 and A6 is 4 × 2), so the intermediate matrices stay thin and every later multiplication is cheap. A good parenthesisation tries to make small dimensions appear in the middle of each product as early as possible.

---

## Q3: Longest Common Subsequence

### Implementation

c[i][j] is the length of an LCS of the first i characters of X and the first j characters of Y:

```
c[i][j] = 0                                   if i = 0 or j = 0
c[i][j] = c[i-1][j-1] + 1                     if X[i] = Y[j]
c[i][j] = max(c[i-1][j], c[i][j-1])           otherwise
```

The table is filled row by row in Θ(mn) time.

To reconstruct one LCS, the program starts at c[m][n]. If the two characters match, that character is part of the LCS and it moves diagonally. Otherwise it moves up if c[i-1][j] >= c[i][j-1] and left if not. The characters are collected in reverse and flipped at the end.

The space-optimised version only keeps the previous row and the current row, because each entry depends only on the row above and the entry to its left. It also swaps X and Y so the rows are as short as possible, which gives Θ(min(m, n)) extra space. It can return the length but not the subsequence itself, since the older rows are thrown away.

The brute force goes through all 2^m subsets of positions of X using a bitmask, builds that subsequence, and checks if it is also a subsequence of Y with a single scan. This takes Θ(2^m × (m + n)) time.

### LCS table for X = ABCBDAB, Y = BDCABA

| | | B | D | C | A | B | A |
|---|---|---|---|---|---|---|---|
| | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| B | 0 | 1 | 1 | 1 | 1 | 2 | 2 |
| C | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
| B | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
| D | 0 | 1 | 2 | 2 | 2 | 3 | 3 |
| A | 0 | 1 | 2 | 2 | 3 | 3 | 4 |
| B | 0 | 1 | 2 | 2 | 3 | 4 | 4 |

```
LCS length       : 4
one LCS          : BCBA
two-row length   : 4
brute force LCS  : BCBA
```

BCBA can be checked in both strings: it uses positions 2, 3, 4, 6 of X = ABCBDAB and positions 1, 3, 5, 6 of Y = BDCABA. Other LCSs of length 4 also exist, such as BDAB and BCAB, so the answer is not unique.

### DP vs brute force

Random strings over the alphabet {A, C, G, T}, with X and Y the same length. The DP time is the average of 20 runs.

| length | LCS length | DP time (s) | brute force time (s) | brute / DP |
|---|---|---|---|---|
| 5 | 2 | 0.000003 | 0.000020 | 6x |
| 6 | 3 | 0.000004 | 0.000040 | 10x |
| 7 | 4 | 0.000005 | 0.000068 | 12x |
| 8 | 3 | 0.000007 | 0.000170 | 25x |
| 9 | 4 | 0.000009 | 0.000398 | 47x |
| 10 | 7 | 0.000011 | 0.000499 | 45x |
| 11 | 5 | 0.000013 | 0.001519 | 113x |
| 12 | 5 | 0.000016 | 0.003613 | 224x |
| 13 | 7 | 0.000018 | 0.006181 | 338x |
| 14 | 8 | 0.000020 | 0.013871 | 707x |
| 15 | 9 | 0.000024 | 0.026128 | 1,084x |
| 16 | 7 | 0.000025 | 0.071590 | 2,908x |
| 17 | 11 | 0.000027 | 0.113852 | 4,194x |
| 18 | 11 | 0.000035 | 0.236332 | 6,833x |

The brute-force time roughly doubles with every extra character, which matches 2^m growth. The DP time grows slowly, following m × n (from 25 table cells at length 5 to 324 cells at length 18). At length 18 the DP is already about 6,800 times faster. Continuing the doubling, a length of 30 would take the brute force around 15 minutes and a length of 50 would take about 30 years, while the DP would still finish in well under a millisecond.

### Line-by-line diff

The same idea works with whole lines instead of characters. The program builds the LCS table on the two lists of lines. Lines that are part of the LCS are printed as unchanged (two spaces), lines only in the old file are printed with `-`, and lines only in the new file with `+`. The table is built on suffixes (L[i][j] = LCS of old[i:] and new[j:]) so the diff can be printed from the top of the files downwards.

Output for the two sample shopping lists:

```
  Shopping list for the hostel trip
  rice 5 kg
  dal 2 kg
- cooking oil 1 litre
+ cooking oil 2 litres
  chillies
  onions
+ cheese
  tomatoes
- instant noodles
  tea leaves
+ milk powder
  sugar 1 kg

8 lines unchanged, 2 removed, 3 added
```

This is the same basic idea that tools like `diff` and `git diff` are built on. Because LCS keeps as many lines unchanged as possible, the diff shows the smallest number of added and removed lines. A changed line shows up as one removal and one addition, as with the cooking oil line.

---

## Q4 (Optional): Optimal Binary Search Tree

### Implementation

Keys k1 < k2 < ... < k5 are searched with probabilities p, and the dummy keys d0..d5 (searches that fall between keys) have probabilities q. The tables are:

- w[i][j] = sum of p[i..j] and q[i-1..j], the total probability of a subtree on keys ki..kj,
- e[i][j] = expected search cost of the best subtree on ki..kj,
- root[i][j] = the key chosen as root of that subtree.

```
e[i][i-1] = q[i-1]
e[i][j]   = min over i <= r <= j of ( e[i][r-1] + e[r+1][j] + w[i][j] )
```

Adding w[i][j] accounts for every node in the subtree becoming one level deeper when it is placed under the root. The tables are filled by subtree size in Θ(n^3) time.

### Results

With p = 0.15, 0.10, 0.05, 0.10, 0.20 and q = 0.05, 0.10, 0.05, 0.05, 0.05, 0.10:

```
Expected search cost: 2.75
```

which matches the expected value. The root table:

| i \ j | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 2 | 2 | 2 |
| 2 | | 2 | 2 | 2 | 4 |
| 3 | | | 3 | 4 | 5 |
| 4 | | | | 4 | 5 |
| 5 | | | | | 5 |

Structure of the optimal tree:

```
k2 is the root
k1 is the left child of k2
d0 is the left child of k1
d1 is the right child of k1
k5 is the right child of k2
k4 is the left child of k5
k3 is the left child of k4
d2 is the left child of k3
d3 is the right child of k3
d4 is the right child of k4
d5 is the right child of k5
```

Drawn as a tree:

```
              k2
            /    \
          k1      k5
         /  \    /  \
        d0  d1  k4   d5
               /  \
              k3   d4
             /  \
            d2   d3
```

It is interesting that the root is k2 and not k5, even though k5 has the highest probability (0.20). Putting k5 at the root would push k1 and k2, which together have probability 0.25, plus several dummy keys further down. The DP balances all of these costs, which a simple greedy rule like "put the most likely key at the root" does not do.

---

## Conclusion

All four problems have overlapping subproblems and optimal substructure, so a table turns an exponential search into a polynomial one. The rod cutting experiment shows this most directly: the same recurrence went from 33.5 million calls to 326 calls at n = 25. Matrix chain and LCS were checked against brute force and gave identical answers, and the LCS idea also gave a working line-by-line diff tool.
