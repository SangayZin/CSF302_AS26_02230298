"""
Lab 6 Q4 (optional): Optimal Binary Search Tree

p[i] is the probability of searching for key k_i (i = 1..n) and q[i] is the
probability of a search that ends in dummy key d_i, i.e. a value between
k_i and k_{i+1} (i = 0..n).

Run:  python q4_optimal_bst.py
"""

P = [None, 0.15, 0.10, 0.05, 0.10, 0.20]   # P[0] is unused so keys start at 1
Q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]


def optimal_bst(p, q, n):
    """e[i][j]: expected cost of the best tree on keys k_i..k_j
    w[i][j]: total probability of that subtree (every node gets one level deeper
             when the subtree is hung below a root, which adds w to the cost)
    root[i][j]: the key chosen as root. e and w use j = i - 1 for empty trees."""
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j] - 1e-12:
                    e[i][j] = cost
                    root[i][j] = r
    return e, w, root


def describe_tree(root, i, j, parent=None, side=None, lines=None):
    """List every parent-child link, with dummy keys as leaves."""
    if lines is None:
        lines = []
    if i > j:
        lines.append(f"d{j} is the {side} child of k{parent}")
        return lines
    r = root[i][j]
    if parent is None:
        lines.append(f"k{r} is the root")
    else:
        lines.append(f"k{r} is the {side} child of k{parent}")
    describe_tree(root, i, r - 1, r, "left", lines)
    describe_tree(root, r + 1, j, r, "right", lines)
    return lines


def draw_tree(root, i, j, prefix="", is_left=None, out=None):
    """Sideways drawing: right subtree above, left subtree below."""
    if out is None:
        out = []
    if i > j:
        out.append(prefix + ("└── " if is_left else "┌── " if is_left is not None else "") + f"d{j}")
        return out
    r = root[i][j]
    right_prefix = prefix + ("    " if is_left is False or is_left is None else "│   ")
    draw_tree(root, r + 1, j, right_prefix, False, out)
    out.append(prefix + ("└── " if is_left else "┌── " if is_left is not None else "") + f"k{r}")
    left_prefix = prefix + ("│   " if is_left is False else "    ")
    draw_tree(root, i, r - 1, left_prefix, True, out)
    return out


if __name__ == "__main__":
    n = 5
    e, w, root = optimal_bst(P, Q, n)
    print("=" * 50)
    print("Optimal binary search tree")
    print("=" * 50)
    print(f"Expected search cost: {e[1][n]:.2f}")
    print("\nRoot table root[i][j]:")
    print("      " + "".join(f"j={j:<4}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        print(f"  i={i} " + "".join(f"{root[i][j]:<6}" if j >= i else " " * 6 for j in range(1, n + 1)))
    print("\nStructure:")
    for line in describe_tree(root, 1, n):
        print("  " + line)
    print("\nDrawing (turn your head left, right children are above):")
    for line in draw_tree(root, 1, n):
        print("  " + line)
