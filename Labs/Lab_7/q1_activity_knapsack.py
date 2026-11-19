"""
Lab 7 Q1: Activity Selection and Knapsack

  - greedy activity selection by earliest finish time
  - two other greedy rules (earliest start, shortest duration) and a random
    search for inputs where they choose fewer activities
  - fractional knapsack by value/weight ratio
  - the same ratio rule on 0/1 knapsack, compared with an exact DP

Run:  python q1_activity_knapsack.py [activities file]
The activities file has one "start finish" pair per line.
"""

import os
import random
import sys

rng = random.Random(77)
HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------ activities
def read_activities(path):
    acts = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            start, finish = map(int, line.replace(",", " ").split())
            if finish < start:
                raise ValueError(f"line {line_no}: finish time is before start time")
            acts.append((start, finish))
    return acts


def overlaps(a, b):
    """Activities are half-open [start, finish), so (1, 4) and (4, 7) do not overlap."""
    return a[0] < b[1] and b[0] < a[1]


def greedy_select(acts, key):
    """Sort by `key`, then take each activity that does not overlap any activity
    already taken. Checking against every chosen activity (not only the last one)
    matters for rules like shortest duration, where the chosen activities are not
    picked in time order."""
    order = sorted(range(len(acts)), key=lambda i: key(acts[i]))
    chosen = []
    for i in order:
        if not any(overlaps(acts[i], acts[j]) for j in chosen):
            chosen.append(i)
    return chosen


def earliest_finish(acts):
    """The usual Theta(n log n) version: after sorting by finish time, an
    activity fits exactly when it starts no earlier than the last finish."""
    order = sorted(range(len(acts)), key=lambda i: acts[i][1])
    chosen = []
    last_finish = float("-inf")
    for i in order:
        s, f = acts[i]
        if s >= last_finish:
            chosen.append(i)
            last_finish = f
    return chosen


def earliest_start(acts):
    return greedy_select(acts, key=lambda a: a[0])


def shortest_duration(acts):
    return greedy_select(acts, key=lambda a: a[1] - a[0])


def is_compatible(acts, chosen):
    picked = sorted(acts[i] for i in chosen)
    return all(picked[k][1] <= picked[k + 1][0] for k in range(len(picked) - 1))


def demo_activity(path):
    print("=" * 66)
    print(f"Activity selection on {os.path.basename(path)}")
    print("=" * 66)
    acts = read_activities(path)
    for i, (s, f) in enumerate(acts, start=1):
        print(f"  a{i:<2} start {s:>2}  finish {f:>2}")
    for name, rule in [("earliest finish", earliest_finish),
                       ("earliest start", earliest_start),
                       ("shortest duration", shortest_duration)]:
        chosen = sorted(rule(acts))
        assert is_compatible(acts, chosen)
        names = ", ".join(f"a{i + 1}{acts[i]}" for i in chosen)
        print(f"\n{name:<18}: {len(chosen)} activities -> {names}")
    print()


def find_counterexample(rule, trials=100_000):
    """Random small inputs until `rule` picks fewer activities than earliest finish."""
    for _ in range(trials):
        n = rng.randint(3, 5)
        acts = []
        for _ in range(n):
            s = rng.randint(0, 10)
            acts.append((s, s + rng.randint(1, 6)))
        if len(rule(acts)) < len(earliest_finish(acts)):
            return acts
    return None


def demo_counterexamples():
    print("=" * 66)
    print("Random search for inputs where the other rules lose")
    print("=" * 66)
    for name, rule in [("earliest start", earliest_start), ("shortest duration", shortest_duration)]:
        acts = find_counterexample(rule)
        if acts is None:
            print(f"{name}: no counterexample found")
            continue
        best = sorted(earliest_finish(acts))
        worse = sorted(rule(acts))
        print(f"{name}:")
        print(f"  input             : {acts}")
        print(f"  earliest finish   : {len(best)} -> {[acts[i] for i in best]}")
        print(f"  {name:<18}: {len(worse)} -> {[acts[i] for i in worse]}")
    print()


# ------------------------------------------------------------ knapsack
def fractional_knapsack(items, capacity):
    """items are (value, weight). Returns (total value, list of (index, fraction))."""
    order = sorted(range(len(items)), key=lambda i: items[i][0] / items[i][1], reverse=True)
    total = 0.0
    taken = []
    room = capacity
    for i in order:
        if room == 0:
            break
        value, weight = items[i]
        if weight <= room:
            taken.append((i, 1.0))
            total += value
            room -= weight
        else:
            fraction = room / weight
            taken.append((i, fraction))
            total += value * fraction
            room = 0
    return total, taken


def greedy_01_knapsack(items, capacity):
    """Ratio order again, but each item is all or nothing; items that no
    longer fit are skipped and the scan carries on."""
    order = sorted(range(len(items)), key=lambda i: items[i][0] / items[i][1], reverse=True)
    total, room = 0, capacity
    for i in order:
        value, weight = items[i]
        if weight <= room:
            total += value
            room -= weight
    return total


def dp_01_knapsack(items, capacity):
    """best[c] = best value using the items seen so far with capacity c.
    Going through c from high to low makes sure each item is used at most once."""
    best = [0] * (capacity + 1)
    for value, weight in items:
        for c in range(capacity, weight - 1, -1):
            best[c] = max(best[c], best[c - weight] + value)
    return best[capacity]


def demo_knapsack():
    print("=" * 66)
    print("Fractional knapsack")
    print("=" * 66)
    items = [(60, 10), (100, 20), (120, 30)]
    capacity = 50
    total, taken = fractional_knapsack(items, capacity)
    print(f"items (value, weight): {items}, capacity {capacity}")
    for i, frac in taken:
        v, w = items[i]
        print(f"  take {frac * 100:5.1f}% of item {i + 1} (value {v}, weight {w}, ratio {v / w:.1f})")
    print(f"  total value = {total:.1f}")
    print(f"\nSame items as 0/1 knapsack: greedy = {greedy_01_knapsack(items, capacity)}, "
          f"DP optimum = {dp_01_knapsack(items, capacity)}\n")

    print("=" * 66)
    print("0/1 knapsack: greedy by ratio vs exact DP on random inputs")
    print("=" * 66)
    trials = 5000
    worst_ratio, worst_case = 1.0, None
    optimal_count = 0
    ratio_sum = 0.0
    for _ in range(trials):
        n = rng.randint(2, 12)
        items = [(rng.randint(1, 100), rng.randint(1, 40)) for _ in range(n)]
        capacity = rng.randint(1, sum(w for _, w in items))
        g = greedy_01_knapsack(items, capacity)
        opt = dp_01_knapsack(items, capacity)
        ratio = g / opt if opt else 1.0
        ratio_sum += ratio
        optimal_count += g == opt
        if ratio < worst_ratio:
            worst_ratio, worst_case = ratio, (items, capacity, g, opt)
    print(f"trials                     : {trials}")
    print(f"greedy was optimal         : {optimal_count} times ({optimal_count / trials:.1%})")
    print(f"average greedy / optimal   : {ratio_sum / trials:.4f}")
    print(f"worst greedy / optimal     : {worst_ratio:.4f}")
    items, capacity, g, opt = worst_case
    print(f"  worst input: items {items}, capacity {capacity}")
    print(f"  greedy value {g}, optimal value {opt}")
    print()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "activities.txt")
    demo_activity(path)
    demo_counterexamples()
    demo_knapsack()
