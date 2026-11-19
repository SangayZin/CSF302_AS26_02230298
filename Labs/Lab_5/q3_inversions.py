"""
Lab 5 Q3: Counting Inversions

An inversion is a pair of positions i < j with a[i] > a[j].
  - brute force: check every pair, Theta(n^2)
  - merge sort based: count while merging, Theta(n log n)
  - Kendall tau distance between two people's rankings of 10 movies

Run everything:          python q3_inversions.py
Only the movie ranking:  python q3_inversions.py kendall
"""

import random
import sys
import time

rng = random.Random(57)
TIME_LIMIT = 60.0


def brute_force_inversions(a, time_limit=None):
    """Return the inversion count, or None if time_limit seconds pass first."""
    n = len(a)
    count = 0
    start = time.perf_counter()
    for i in range(n - 1):
        ai = a[i]
        for j in range(i + 1, n):
            if ai > a[j]:
                count += 1
        if time_limit is not None and time.perf_counter() - start > time_limit:
            return None
    return count


def sort_and_count(a):
    """Return (sorted copy of a, number of inversions in a)."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, inv_left = sort_and_count(a[:mid])
    right, inv_right = sort_and_count(a[mid:])
    merged = []
    split = 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # right[j] is smaller than every element still waiting in left,
            # so it forms an inversion with each of them
            merged.append(right[j])
            split += len(left) - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_left + inv_right + split


def merge_inversions(a):
    return sort_and_count(a)[1]


def verify():
    print("=" * 66)
    print("Checking that both methods agree")
    print("=" * 66)
    fixed = [[], [1], [1, 2, 3], [3, 2, 1], [2, 4, 1, 3, 5], [5, 4, 3, 2, 1, 0], [1, 1, 1], [2, 1, 2, 1]]
    for arr in fixed:
        print(f"{str(arr):<22} brute = {brute_force_inversions(arr):>2}   merge = {merge_inversions(arr):>2}")

    trials = 300
    mismatches = 0
    for _ in range(trials):
        n = rng.randint(0, 2000)
        arr = [rng.randint(0, rng.choice([5, 100, 10**6])) for _ in range(n)]
        if brute_force_inversions(arr) != merge_inversions(arr):
            mismatches += 1
    print(f"\n{trials} random arrays of size 0 to 2,000 (some with many repeats): "
          f"{mismatches} mismatches\n")


def timing():
    print("=" * 66)
    print(f"Timing (brute force stops once a run goes past {TIME_LIMIT:.0f} s)")
    print("=" * 66)
    sizes = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    brute_alive = True
    print("| n | inversions | brute force (s) | merge sort (s) |")
    print("|---|---|---|---|")
    for n in sizes:
        arr = [rng.randint(0, 10**9) for _ in range(n)]
        start = time.perf_counter()
        inv = merge_inversions(arr)
        t_merge = time.perf_counter() - start

        if brute_alive:
            start = time.perf_counter()
            brute = brute_force_inversions(arr, TIME_LIMIT)
            t_brute = time.perf_counter() - start
            if brute is None:
                brute_text = f"> {TIME_LIMIT:.0f} (stopped)"
                brute_alive = False
            else:
                assert brute == inv
                brute_text = f"{t_brute:.3f}"
        else:
            brute_text = "skipped"
        print(f"| {n:,} | {inv:,} | {brute_text} | {t_merge:.3f} |", flush=True)
    print()


MOVIES = [
    "Inception", "Parasite", "Spirited Away", "The Dark Knight", "Interstellar",
    "Coco", "Whiplash", "The Matrix", "Up", "Gladiator",
]


def read_ranking(person):
    """Ask for a ranking as 10 movie numbers, best first, until it is valid."""
    while True:
        try:
            line = input(f"{person}, enter the 10 movie numbers from favourite to least favourite: ")
        except EOFError:
            sys.exit("\nNo more input, exiting.")
        parts = line.replace(",", " ").split()
        try:
            ranking = [int(p) for p in parts]
        except ValueError:
            print("  Please type numbers only.")
            continue
        if sorted(ranking) != list(range(1, 11)):
            print("  Each of the numbers 1 to 10 must appear exactly once.")
            continue
        return ranking


def kendall_tau():
    print("=" * 66)
    print("Kendall tau distance between two movie rankings")
    print("=" * 66)
    for i, title in enumerate(MOVIES, start=1):
        print(f"  {i:>2}. {title}")
    print()
    user1 = read_ranking("User 1")
    user2 = read_ranking("User 2")

    # position of each movie in user 2's list
    pos2 = {movie: rank for rank, movie in enumerate(user2)}
    # write user 1's list using user 2's positions; every pair the two users
    # order differently now shows up as an inversion
    sequence = [pos2[movie] for movie in user1]
    distance = merge_inversions(sequence)
    pairs = 10 * 9 // 2
    tau = 1 - 2 * distance / pairs

    print("\nUser 1:", " > ".join(MOVIES[m - 1] for m in user1))
    print("User 2:", " > ".join(MOVIES[m - 1] for m in user2))
    print(f"\nKendall tau distance (pairs ordered differently): {distance} out of {pairs}")
    print(f"Normalised distance: {distance / pairs:.3f}")
    print(f"Similarity (1 - normalised distance): {1 - distance / pairs:.3f}")
    print(f"Kendall tau coefficient (from -1 to 1): {tau:.3f}")
    if tau > 0.6:
        print("The two users have very similar taste.")
    elif tau > 0.2:
        print("The two users agree more than they disagree.")
    elif tau >= -0.2:
        print("The rankings are not really related.")
    else:
        print("The two users have mostly opposite taste.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "kendall":
        kendall_tau()
    else:
        verify()
        timing()
        kendall_tau()
