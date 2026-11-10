"""
Part A: closest_pair_brute and closest_pair (divide and conquer).
"""

import math


# ---------------------------------------------------------------- brute force

def closest_pair_brute(points):
    """Return (d, i, j): smallest distance d and indices i < j.

    Brute force: compare every pair. Theta(n^2).
    """
    n = len(points)
    if n < 2:
        raise ValueError("Need at least 2 points")

    best_d = float("inf")
    best_i = best_j = -1

    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            d = math.hypot(xi - xj, yi - yj)
            if d < best_d:
                best_d = d
                best_i, best_j = i, j

    return (best_d, best_i, best_j)


# ------------------------------------------------------- divide and conquer

def closest_pair(points):
    """Return (d, i, j): smallest distance d and indices i < j.

    Divide and conquer. The strip is sorted by y at every level,
    so the recurrence is T(n) = 2 T(n/2) + Theta(n log n),
    which by the Master Method gives Theta(n log^2 n).
    """
    n = len(points)
    if n < 2:
        raise ValueError("Need at least 2 points")

    # Tag each point with its ORIGINAL index, then sort by (x, y).
    tagged = [(x, y, idx) for idx, (x, y) in enumerate(points)]
    tagged.sort(key=lambda p: (p[0], p[1]))

    d, i, j = _closest_rec(tagged)

    # Normalise so that i < j (the strip may find the pair in reverse order).
    if i > j:
        i, j = j, i
    return (d, i, j)


def _closest_rec(pts):
    """Recursive helper on a list of (x, y, original_index) sorted by (x, y)."""
    n = len(pts)
    if n <= 3:
        return _brute_tagged(pts)

    mid = n // 2
    mid_x = pts[mid][0]

    left = pts[:mid]
    right = pts[mid:]

    dl, il, jl = _closest_rec(left)
    dr, ir, jr = _closest_rec(right)

    if dl <= dr:
        d, i, j = dl, il, jl
    else:
        d, i, j = dr, ir, jr

    # Strip: points within distance d of the dividing line.
    strip = [p for p in pts if abs(p[0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])          # sort by y

    # For each point, check at most the next 7 in y-order.
    m = len(strip)
    for a in range(m):
        for b in range(a + 1, min(a + 8, m)):
            dy = strip[b][1] - strip[a][1]
            if dy >= d:
                break                        # no closer pair possible
            d2 = math.hypot(strip[a][0] - strip[b][0], dy)
            if d2 < d:
                d = d2
                i, j = strip[a][2], strip[b][2]

    return (d, i, j)


def _brute_tagged(pts):
    """Brute force on a small list of (x, y, original_index) tuples."""
    n = len(pts)
    best_d = float("inf")
    best_i = best_j = -1
    for a in range(n):
        for b in range(a + 1, n):
            d = math.hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1])
            if d < best_d:
                best_d = d
                best_i, best_j = pts[a][2], pts[b][2]
    return (best_d, best_i, best_j)
