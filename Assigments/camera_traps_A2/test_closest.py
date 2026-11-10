"""Tests for closest pair of point (Part B).

Run with:
    pytest -v

Covers:
  - 500 random inputs, n between 2 and 50, compared to brute force
  - exactly 2 points
  - duplicate points (answer 0)
  - all points on one vertical line
  - closest pair straddling the dividing line
"""

import random
import math
import pytest

from closest import closest_pair, closest_pair_brute


# ------------------------------------------------------------------ helpers

def _distance(points, i, j):
    """Recompute distance between points[i] and points[j] independently."""
    (x1, y1), (x2, y2) = points[i], points[j]
    return math.hypot(x1 - x2, y1 - y2)


def _check(points):
    """Assert closest_pair agrees with brute force AND its indices are valid."""
    d_dc, i, j = closest_pair(points)
    d_bf, _, _ = closest_pair_brute(points)

    # 1. Distances must match within floating-point tolerance.
    assert math.isclose(d_dc, d_bf, rel_tol=1e-9, abs_tol=1e-9), (
        f"D&C distance {d_dc} != brute force {d_bf} on {points}"
    )

    # 2. Indices must satisfy i < j.
    assert i < j, f"closest_pair returned i={i} >= j={j} on {points}"

    # 3. Returned indices must actually give distance d_dc.
    assert math.isclose(_distance(points, i, j), d_dc,
                        rel_tol=1e-9, abs_tol=1e-9), (
        f"Indices ({i}, {j}) do not yield distance {d_dc} on {points}"
    )


# ------------------------------------------------------- 500 random tests

@pytest.mark.parametrize("seed", range(500))
def test_random_against_brute_force(seed):
    """500 random inputs, n between 2 and 50."""
    rng = random.Random(seed)              # reproducible per seed
    n = rng.randint(2, 50)
    points = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000))
              for _ in range(n)]
    _check(points)


# ------------------------------------------------------------ edge cases

def test_exactly_two_points():
    points = [(3, 7), (10, 2)]
    d, i, j = closest_pair(points)
    assert (i, j) == (0, 1)
    assert math.isclose(d, _distance(points, 0, 1))


def test_duplicate_points():
    points = [(0, 0), (5, 5), (0, 0), (10, 10)]
    d, i, j = closest_pair(points)
    assert d == 0.0
    assert (points[i] == points[j])


def test_all_points_on_vertical_line():
    points = [(1, y) for y in range(0, 40)]
    _check(points)
    # Neighbouring points are distance 1 apart.
    d, _, _ = closest_pair(points)
    assert math.isclose(d, 1.0)


def test_all_points_on_horizontal_line():
    points = [(x, 7) for x in range(0, 40)]
    _check(points)
    d, _, _ = closest_pair(points)
    assert math.isclose(d, 1.0)


def test_closest_pair_straddles_dividing_line():
    """The globally closest pair sits on opposite sides of the split."""
    points = [
        # Left half (x < 0), spaced far apart
        (-100, 0), (-100, 50), (-100, 100), (-100, 150), (-100, 200),
        # The pair that straddles the divide:
        (-1, 0), (1, 0),
        # Right half, spaced far apart
        (100, 0), (100, 50), (100, 100), (100, 150), (100, 200),
    ]
    d, i, j = closest_pair(points)
    assert math.isclose(d, 2.0)
    assert {points[i], points[j]} == {(-1, 0), (1, 0)}


def test_two_points_duplicated():
    """Exactly two points, both equal — expect distance 0."""
    points = [(4, 4), (4, 4)]
    d, i, j = closest_pair(points)
    assert d == 0.0
    assert (i, j) == (0, 1)


def test_input_too_small_raises():
    with pytest.raises(ValueError):
        closest_pair([(0, 0)])
