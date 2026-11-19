# CSF302 Lab 7: Greedy and Randomized Algorithms

## Files

| File | Contents |
|---|---|
| `q1_activity_knapsack.py` | Activity selection (three greedy rules), fractional knapsack, greedy vs DP for 0/1 knapsack |
| `q2_huffman.py` | Huffman tree, code table, encoding, decoding, compression ratio |
| `q3_graphs.py` | Dijkstra, Kruskal, Prim, MST check and timing, negative edge example |
| `q4_randomized.py` | Randomized quickselect, Miller-Rabin, trial division, Carmichael number test |
| `data/activities.txt` | Activities as "start finish" pairs |
| `data/english_text.txt`, `data/python_code.txt`, `data/dna_sequence.txt` | Text files for Huffman coding |
| `data/graph.txt` | Weighted directed graph for Dijkstra |

Run each file with `python <file>.py`. Some accept their own input files:

```
python q1_activity_knapsack.py my_activities.txt
python q2_huffman.py file1.txt file2.txt
python q3_graphs.py my_graph.txt 2        (graph file, then source vertex)
```

Only the standard library is used (`heapq` for the priority queues). Times were measured with Python 3.13 on Linux.

---

## Q1: Activity Selection and Knapsack

### Activity selection by earliest finish time

The activities are read from `data/activities.txt`, sorted by finish time, and each one is taken if it starts no earlier than the finish time of the last activity taken. Activities are treated as half-open intervals [start, finish), so one can start at the exact time another ends. After sorting this is a single pass, so the whole algorithm is Θ(n log n).

Input (11 activities):

| activity | a1 | a2 | a3 | a4 | a5 | a6 | a7 | a8 | a9 | a10 | a11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| start | 1 | 3 | 0 | 5 | 3 | 5 | 6 | 8 | 8 | 2 | 12 |
| finish | 4 | 5 | 6 | 7 | 9 | 9 | 10 | 11 | 12 | 14 | 16 |

| greedy rule | number chosen | selected activities |
|---|---|---|
| earliest finish | 4 | a1 (1, 4), a4 (5, 7), a8 (8, 11), a11 (12, 16) |
| earliest start | 3 | a3 (0, 6), a7 (6, 10), a11 (12, 16) |
| shortest duration | 4 | a2 (3, 5), a4 (5, 7), a8 (8, 11), a11 (12, 16) |

### Other greedy rules and counterexamples

For the other two rules, the activities are sorted by start time or by duration, and each one is taken if it does not overlap any activity already taken. Checking against every chosen activity (not only the last one) is needed for shortest duration, because the chosen activities are not picked in time order.

On the file above, shortest duration happened to find an optimal answer. To show that these rules are not always correct, the program generates random small inputs (3 to 5 activities) until each rule chooses fewer activities than earliest finish:

| rule | input found | earliest finish | other rule |
|---|---|---|---|
| earliest start | (8, 9), (6, 11), (9, 14), (3, 5) | 3: (3, 5), (8, 9), (9, 14) | 2: (3, 5), (6, 11) |
| shortest duration | (8, 12), (9, 15), (9, 13), (7, 12), (4, 9) | 2: (4, 9), (9, 13) | 1: (8, 12) |

Earliest start fails because an activity that starts early can be very long. Here (6, 11) starts before (8, 9) but blocks both (8, 9) and (9, 14). Shortest duration fails because a short activity can sit in the middle and overlap two others that would fit together. Here (8, 12) is one of the shortest, but it overlaps every other activity, while (4, 9) and (9, 13) fit next to each other.

Earliest finish always works because choosing the activity that ends first leaves the most time for the rest. If an optimal solution starts with some other activity, it can be swapped for the earliest-finishing one without causing any overlap, so there is always an optimal solution that agrees with the greedy choice.

### Fractional knapsack

Items are sorted by value/weight ratio, highest first. Whole items are taken while they fit, and then a fraction of the next item fills the rest of the capacity.

Items (value, weight) = (60, 10), (100, 20), (120, 30), capacity 50:

| item | value | weight | ratio | taken |
|---|---|---|---|---|
| 1 | 60 | 10 | 6.0 | 100% |
| 2 | 100 | 20 | 5.0 | 100% |
| 3 | 120 | 30 | 4.0 | 66.7% |

Total value = 60 + 100 + 80 = 240. For the fractional problem this greedy rule is always optimal, because any weight spent on a lower-ratio item could be moved to a higher-ratio item for more value.

### Greedy vs DP on 0/1 knapsack

In 0/1 knapsack each item must be taken completely or not at all. The greedy version uses the same ratio order but skips an item that does not fit and keeps going. The exact answer comes from the standard DP over capacities, `best[c] = max(best[c], best[c - w] + v)`, which runs in Θ(nW) time.

On the same three items, greedy takes items 1 and 2 for a value of 160, but the optimum is 220 (items 2 and 3).

Random test with 5,000 inputs (2 to 12 items, values 1 to 100, weights 1 to 40, random capacity):

| measure | result |
|---|---|
| greedy was optimal | 3,998 of 5,000 (80.0%) |
| average greedy / optimal | 0.9839 |
| worst greedy / optimal | 0.2157 |

The worst case found was items (51, 36) and (11, 7) with capacity 42. Item 2 has the better ratio (1.57 against 1.42), so greedy takes it first, and then item 1 (weight 36) no longer fits in the remaining 35. Greedy gets 11 while the optimum is 51. The same idea can be pushed further: with one item of value 2 and weight 1, another of value W and weight W, and capacity W, greedy takes the first item and gets 2 while the optimum is W. So the ratio can be made as close to 0 as we like, and the ratio greedy has no guarantee at all on 0/1 knapsack. On typical random inputs it is usually close to optimal, but it is not correct.

---

## Q2: Huffman Coding

### Implementation

1. Count the frequency of each character with `Counter`.
2. Put one leaf per character into a min-heap (`heapq`) ordered by frequency. A running counter is used as a tie-breaker, so equal frequencies never force Python to compare two tree nodes, and the same tree is built on every run.
3. Repeatedly pop the two smallest trees and push a new node whose frequency is their sum, until one tree is left. With c distinct characters this takes Θ(c log c).
4. Walk the tree to build the code table: going left adds 0 and going right adds 1. A file with only one distinct character gets the code "0".
5. Encode by joining the codes. Decode by following the bits from the root, outputting a character every time a leaf is reached, then starting again from the root. This works because Huffman codes are prefix-free: no code is the beginning of another code.

### Code table for `english_text.txt`

| char | freq | code | | char | freq | code |
|---|---|---|---|---|---|---|
| space | 420 | 111 | | y | 31 | 001101 |
| e | 224 | 000 | | . | 23 | 1011110 |
| t | 192 | 1100 | | b | 21 | 1011011 |
| a | 148 | 1010 | | , | 17 | 1000010 |
| o | 147 | 1001 | | v | 17 | 1000011 |
| n | 133 | 0111 | | k | 12 | 10111111 |
| r | 126 | 0101 | | \n | 9 | 10110101 |
| s | 126 | 0110 | | T | 8 | 00110010 |
| i | 125 | 0100 | | x | 7 | 00110001 |
| h | 105 | 0010 | | q | 6 | 101111101 |
| l | 70 | 10001 | | A | 4 | 001100110 |
| d | 64 | 00111 | | I | 4 | 001100111 |
| g | 55 | 110111 | | B | 3 | 1011111001 |
| c | 49 | 110101 | | S | 3 | 001100000 |
| m | 49 | 110110 | | C | 2 | 0011000011 |
| f | 48 | 110100 | | E | 2 | 1011010000 |
| u | 46 | 101110 | | z | 2 | 1011010001 |
| p | 35 | 101100 | | j | 1 | 0011000010 |
| w | 34 | 100000 | | :, D, H, J, L, P | 1 each | 11 bits |

The most common characters (space and e) get 3-bit codes, while characters that appear once get 10 or 11 bits. The other two files print their own tables when the program is run.

### Compression results

| file | characters | distinct | fixed 8-bit (bits) | Huffman (bits) | bits per char | ratio | decoded = original |
|---|---|---|---|---|---|---|---|
| english_text.txt | 2,374 | 43 | 18,992 | 10,245 | 4.316 | 0.539 | yes |
| python_code.txt | 7,921 | 75 | 63,368 | 36,689 | 4.632 | 0.579 | yes |
| dna_sequence.txt | 6,100 | 5 | 48,800 | 12,982 | 2.128 | 0.266 | yes |

The ratio is Huffman bits divided by 8-bit fixed-length bits, so smaller is better. In every case the decoded text was exactly equal to the original.

- English text was compressed to 54% of the original size. English has a very uneven letter distribution, which is what Huffman coding takes advantage of.
- Python code (a copy of `q1_activity_knapsack.py`) compressed slightly less well (58%). Source code uses more distinct characters, such as brackets, underscores, digits and capital letters, and spaces for indentation are spread across many symbols, so the frequencies are a bit more even.
- The DNA file has only 5 symbols (A, C, G, T and a newline every 60 characters), so it compresses the most (27%). Note that this mainly comes from needing very few symbols: any fixed 3-bit code would already reach 0.375. The bases were generated with probabilities 0.35, 0.15, 0.15, 0.35, which gives an entropy of about 1.88 bits per base, but Huffman codes must use a whole number of bits per symbol, so the result stays at about 2 bits per base.

These ratios do not include the code table, which a real compressed file would also need to store so it can be decoded. For small files that overhead is noticeable, but for large files it is tiny.

---

## Q3: Shortest Paths and Minimum Spanning Trees

### Dijkstra's algorithm

The graph file has "V E" on the first line, then one directed edge "u v w" per line. Dijkstra uses `heapq` as the priority queue. Instead of a decrease-key operation, a new (distance, vertex) pair is pushed whenever a distance improves, and old entries are skipped when they come out of the heap. A vertex is finalised the first time it leaves the heap. The running time is Θ((V + E) log V). A parent array stores the previous vertex on each shortest path so the path can be printed.

`data/graph.txt` (vertices 0..5, with 5 having no edges):

```
0->1 (10), 0->3 (5), 1->2 (1), 1->3 (2), 2->4 (4),
3->1 (3), 3->2 (9), 3->4 (2), 4->0 (7), 4->2 (6)
```

Output from source 0:

| vertex | distance | path |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 8 | 0 -> 3 -> 1 |
| 2 | 9 | 0 -> 3 -> 1 -> 2 |
| 3 | 5 | 0 -> 3 |
| 4 | 7 | 0 -> 3 -> 4 |
| 5 | inf | unreachable |

Vertex 1 is a good example: the direct edge 0->1 costs 10, but going through 3 costs 5 + 3 = 8.

### Kruskal and Prim

Kruskal sorts all edges by weight and adds each edge whose endpoints are in different components. Components are tracked with union-find using union by rank and path compression, so each operation is almost constant time. It stops once V - 1 edges have been added. Total time: Θ(E log E) for the sort.

Prim starts from vertex 0 and keeps a heap of edges leaving the current tree. It always adds the lightest edge that reaches a new vertex. This is the lazy version, so the heap can hold up to E entries. Total time: Θ(E log E), which is the same as Θ(E log V).

Small example with 6 vertices:

```
edges: (0,1,4) (0,2,3) (1,2,1) (1,3,2) (2,3,4) (3,4,2) (4,5,6) (3,5,5)
Kruskal: weight 13, edges (1,2,1) (1,3,2) (3,4,2) (0,2,3) (3,5,5)
Prim   : weight 13, edges (0,2,3) (2,1,1) (1,3,2) (3,4,2) (3,5,5)
```

Both choose the same tree but add the edges in a different order. Kruskal goes by weight, while Prim grows outwards from vertex 0.

To check the two algorithms against each other, 200 random connected graphs were generated (V from 2 to 60, random number of edges, and some with weights only from 1 to 5 so there are many ties). Each graph starts as a random spanning tree, so it is always connected. The total MST weight was the same for all 200 graphs. The edges themselves can differ when there are equal weights, because a graph can have more than one MST, but the total weight is always the same.

### Timing with V = 1,000 (average of 3 runs)

| graph | E | Kruskal (s) | Prim (s) | same weight |
|---|---|---|---|---|
| sparse (E ≈ 3V) | 3,000 | 0.0021 | 0.0028 | yes |
| dense (E ≈ V^2/4) | 250,000 | 0.0795 | 0.2343 | yes |

Kruskal won on both graphs in this implementation. On the sparse graph the difference is small, since both only handle 3,000 edges. On the dense graph Kruskal was about 3 times faster.

In theory both are Θ(E log V) with a binary heap, so the constant factors decide the winner:

- Kruskal's main cost is one call to `sorted()`, which runs in fast C code. It can also stop as soon as it has V - 1 edges, which in a dense random graph happens after only a small part of the sorted list.
- Prim calls `heappush` from Python for almost every edge it looks at, and there are 500,000 adjacency entries in the dense graph (each undirected edge is stored twice). Each push and pop is a Python-level operation on a heap that grows to hundreds of thousands of items.

The textbook advice is that Prim is better for dense graphs, but that applies to Prim with an adjacency matrix and a simple array instead of a heap, which is Θ(V^2) and does not depend on E at all. For E ≈ V^2/4 that version would be the best choice in theory. With a heap, as in this lab, Kruskal is simpler and was faster in practice for both graph types.

### Dijkstra with a negative edge

Graph: 0->1 (2), 0->2 (5), 2->1 (-4), 1->3 (1), source 0. The correct distances were computed with Bellman-Ford for comparison.

| vertex | Dijkstra | Bellman-Ford (correct) |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 2 | 1 (wrong in Dijkstra) |
| 2 | 5 | 5 |
| 3 | 3 | 2 (wrong in Dijkstra) |

Dijkstra takes vertex 1 out of the heap first (distance 2, smaller than 5) and finalises it. Only later does it process vertex 2 and see the edge 2->1 with weight -4, which gives the cheaper route 0 -> 2 -> 1 with cost 5 - 4 = 1. By then vertex 1 is already finished, and vertex 3 has already been given distance 3 through it. Dijkstra relies on the fact that a path can never get shorter by adding more edges. That is only true when every weight is non-negative, so one negative edge is enough to break it.

---

## Q4: Randomized Algorithms

### Randomized quickselect

Quickselect picks a random pivot, partitions the array around it (Lomuto partition), and then continues only into the side that contains the k-th position, instead of sorting both sides like quicksort. It works on a copy so the input list is not changed. The expected work is n + n/2 + n/4 + ... ≈ 2n partition steps, so Θ(n) on average, while sorting first costs Θ(n log n).

Results for finding the median (k = n / 2) of random integers:

| n | quickselect (s) | merge sort + index (s) | built-in `sorted()` + index (s) |
|---|---|---|---|
| 10,000 | 0.0015 | 0.0147 | 0.0012 |
| 30,000 | 0.0052 | 0.0536 | 0.0043 |
| 100,000 | 0.0184 | 0.2046 | 0.0176 |
| 300,000 | 0.0655 | 0.7130 | 0.0589 |
| 1,000,000 | 0.2852 | 3.1071 | 0.2612 |

Every answer was checked to be the same for all three methods. A small test on [7, 2, 9, 4, 4, 1, 8] for k = 1 to 7 gave 1, 2, 4, 4, 7, 8, 9.

Compared with a sort written in Python (merge sort), quickselect is about 10 to 11 times faster, and the gap grows slowly with n because of the extra log n factor in sorting. Compared with Python's built-in `sorted()`, the two take almost the same time. This is not because sorting is as cheap as selecting. It is because `sorted()` runs in C, which is roughly 10 times faster per operation than a Python loop, and this cancels out the log n advantage at these sizes. A fair comparison of the algorithms themselves is the one against merge sort, where both are written in Python.

### Miller-Rabin vs trial division

Trial division checks 2 and then every odd number up to √n. For a 12-digit prime this means about 500,000 divisions.

Miller-Rabin writes n - 1 = 2^s × d with d odd, picks a random base a, and computes a^d mod n by fast modular exponentiation (Python's built-in `pow`, which uses the same square-and-multiply method as Lab 4). If the result is not 1 or n - 1, it squares up to s - 1 more times looking for n - 1. If n - 1 never appears, a is a witness that n is composite. A prime can never fail this test, and for a composite at most 1/4 of the bases are liars, so 20 rounds give an error chance of at most 4^-20 ≈ 10^-12. Small prime factors are checked first as a shortcut. Each round costs Θ(log n) multiplications.

Twenty random 12-digit numbers were tested, plus two known 12-digit primes at the end, because random numbers of this size are prime only about once in 27 tries and none of the 20 turned out to be prime.

| number | Miller-Rabin | time (µs) | trial division | time (µs) | agree |
|---|---|---|---|---|---|
| 258764895825 | composite | 5.2 | composite | 13.1 | yes |
| 598915052275 | composite | 1.0 | composite | 1.4 | yes |
| 287308569224 | composite | 0.4 | composite | 1.9 | yes |
| 837568609737 | composite | 0.4 | composite | 0.6 | yes |
| 843155921132 | composite | 0.3 | composite | 0.3 | yes |
| 693357009822 | composite | 0.2 | composite | 0.2 | yes |
| 322188469821 | composite | 0.3 | composite | 0.3 | yes |
| 105779856383 | composite | 13.6 | composite | 3.8 | yes |
| 261175775046 | composite | 1.4 | composite | 0.2 | yes |
| 504558295510 | composite | 0.2 | composite | 0.2 | yes |
| 402250843531 | composite | 8.6 | composite | 5.3 | yes |
| 511398274457 | composite | 0.5 | composite | 0.6 | yes |
| 198394987041 | composite | 0.3 | composite | 0.4 | yes |
| 223439745798 | composite | 1.7 | composite | 0.1 | yes |
| 868911825454 | composite | 0.2 | composite | 0.1 | yes |
| 330420983054 | composite | 0.2 | composite | 0.1 | yes |
| 330548485752 | composite | 0.2 | composite | 0.1 | yes |
| 240668969151 | composite | 0.3 | composite | 0.2 | yes |
| 106549829918 | composite | 0.2 | composite | 0.1 | yes |
| 181580033497 | composite | 8.3 | composite | 0.7 | yes |
| 100000000003 (extra) | prime | 89.6 | prime | 8,688.4 | yes |
| 999999999989 (extra) | prime | 121.0 | prime | 26,523.4 | yes |

All 22 answers agree. Total time: Miller-Rabin 0.25 ms, trial division 35.24 ms.

For most random composites both methods are almost instant, because the number has a small factor that trial division finds in a few steps. Trial division only becomes slow when the smallest factor is large, and the worst case is a prime, where it must try every odd number up to √n ≈ 10^6. For the prime 999999999989, trial division took 26.5 ms while Miller-Rabin took 0.12 ms, about 220 times faster. The gap grows quickly with the size of n: trial division is Θ(√n), while Miller-Rabin is polynomial in the number of digits. For the 300-digit numbers used in RSA, trial division is impossible, but Miller-Rabin still takes milliseconds.

### Miller-Rabin with one round on 561

561 = 3 × 11 × 17 is the smallest Carmichael number. For every base a that is coprime to 561, a^560 ≡ 1 (mod 561), so the plain Fermat test is fooled by 318 of the 558 possible bases (57%).

```
561 - 1 = 2^4 x 35
strong liars in 2..559: 8 -> [50, 101, 103, 256, 305, 458, 460, 511]
expected 'prime' rate for one round: 8/558 = 1.43%

answered 'prime' in 14 of 1000 runs (1.4%)
trial division says 561 is composite
```

Miller-Rabin is much harder to fool, because it also checks the chain of square roots. Only 8 of the 558 bases are strong liars for 561, so one round should wrongly say "prime" about 1.43% of the time. The measured rate was 14 out of 1,000 runs (1.4%), which matches. This is well below the general bound of 1/4. With 20 rounds the chance of a wrong answer for 561 would be about (8/558)^20 ≈ 10^-37.

---

## Conclusion

Greedy algorithms are fast and simple, but they only work when the problem has the greedy-choice property. Earliest finish time and the fractional knapsack ratio rule are provably optimal, while earliest start, shortest duration and the ratio rule for 0/1 knapsack all failed on inputs that were easy to find. Huffman coding saved 42% to 73% of the space on the three files, and the MST algorithms always agreed on the total weight. Dijkstra gave wrong answers with just one negative edge. Finally, randomization gave a linear-time selection algorithm and a primality test that is hundreds of times faster than trial division, with an error rate that matched the theory almost exactly.
