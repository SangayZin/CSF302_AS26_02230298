"""
Lab 7 Q3: Shortest Paths and Minimum Spanning Trees

  - Dijkstra with a binary heap on a weighted directed graph read from a file
  - Kruskal (union-find) and Prim (heap) for minimum spanning trees
  - check that both MST algorithms agree on random connected graphs
  - timing on sparse and dense graphs with V = 1,000
  - a small graph with one negative edge where Dijkstra goes wrong

Graph file format: first line "V E", then E lines "u v w" (vertices 0..V-1).

Run:  python q3_graphs.py [graph file] [source]
"""

import heapq
import os
import random
import sys
import time

rng = random.Random(1959)
HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------ reading
def read_graph(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.split() for ln in f if ln.strip() and not ln.startswith("#")]
    V, E = int(lines[0][0]), int(lines[0][1])
    edges = [(int(u), int(v), float(w) if "." in w else int(w)) for u, v, w in lines[1:1 + E]]
    if len(edges) != E:
        raise ValueError(f"expected {E} edges but found {len(edges)}")
    return V, edges


def adjacency(V, edges, directed=True):
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))
    return adj


# ------------------------------------------------------------ Dijkstra
def dijkstra(adj, source):
    """Each vertex is finalised the first time it leaves the heap and is never
    changed after that. Stale heap entries are skipped instead of using
    decrease-key."""
    INF = float("inf")
    dist = [INF] * len(adj)
    parent = [None] * len(adj)
    done = [False] * len(adj)
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            if not done[v] and d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, parent


def path_to(parent, v):
    path = []
    while v is not None:
        path.append(v)
        v = parent[v]
    return path[::-1]


def bellman_ford(V, edges, source):
    INF = float("inf")
    dist = [INF] * V
    dist[source] = 0
    for _ in range(V - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return dist


# ------------------------------------------------------------ MST
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:          # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(V, edges):
    uf = UnionFind(V)
    total, tree = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            total += w
            tree.append((u, v, w))
            if len(tree) == V - 1:
                break
    return total, tree


def prim(adj, start=0):
    V = len(adj)
    in_tree = [False] * V
    total, tree = 0, []
    heap = [(0, start, -1)]
    while heap and len(tree) < V - 1:
        w, u, frm = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        if frm != -1:
            total += w
            tree.append((frm, u, w))
        for v, wv in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (wv, v, u))
    return total, tree


def random_connected_graph(V, E, max_w=1000):
    """A random spanning tree first (so the graph is connected), then extra
    random edges until there are E distinct undirected edges."""
    order = list(range(V))
    rng.shuffle(order)
    seen = set()
    edges = []
    for i in range(1, V):
        u, v = order[i], order[rng.randrange(i)]
        seen.add((min(u, v), max(u, v)))
        edges.append((u, v, rng.randint(1, max_w)))
    while len(edges) < E:
        u, v = rng.randrange(V), rng.randrange(V)
        if u == v:
            continue
        key = (min(u, v), max(u, v))
        if key in seen:
            continue
        seen.add(key)
        edges.append((u, v, rng.randint(1, max_w)))
    return edges


# ------------------------------------------------------------ demos
def demo_dijkstra(path, source):
    print("=" * 66)
    print(f"Dijkstra on {os.path.basename(path)} from vertex {source}")
    print("=" * 66)
    V, edges = read_graph(path)
    if any(w < 0 for _, _, w in edges):
        print("warning: the graph has negative edges, Dijkstra may be wrong")
    dist, parent = dijkstra(adjacency(V, edges), source)
    print(f"{'vertex':>6} {'distance':>9}  path")
    for v in range(V):
        if dist[v] == float("inf"):
            print(f"{v:>6} {'inf':>9}  unreachable")
        else:
            print(f"{v:>6} {dist[v]:>9}  {' -> '.join(map(str, path_to(parent, v)))}")
    print()


def demo_mst_agreement(trials=200):
    print("=" * 66)
    print("Kruskal vs Prim on random connected graphs")
    print("=" * 66)
    agree = 0
    for _ in range(trials):
        V = rng.randint(2, 60)
        max_e = V * (V - 1) // 2
        E = rng.randint(V - 1, max_e)
        edges = random_connected_graph(V, E, max_w=rng.choice([5, 100, 10**6]))
        k_total, k_tree = kruskal(V, edges)
        p_total, p_tree = prim(adjacency(V, edges, directed=False))
        agree += k_total == p_total and len(k_tree) == len(p_tree) == V - 1
    print(f"{trials} random graphs (V from 2 to 60, some with many equal weights): "
          f"total weights agree on {agree}\n")

    V = 6
    edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (4, 5, 6), (3, 5, 5)]
    k_total, k_tree = kruskal(V, edges)
    p_total, p_tree = prim(adjacency(V, edges, directed=False))
    print(f"small example, edges (u, v, w): {edges}")
    print(f"  Kruskal: weight {k_total}, edges {k_tree}")
    print(f"  Prim   : weight {p_total}, edges {p_tree}\n")


def demo_mst_timing(repeats=3):
    print("=" * 66)
    print("Timing Kruskal and Prim with V = 1,000")
    print("=" * 66)
    V = 1000
    print("| graph | E | Kruskal (s) | Prim (s) | same weight |")
    print("|---|---|---|---|---|")
    for label, E in [("sparse", 3 * V), ("dense", V * V // 4)]:
        edges = random_connected_graph(V, E, max_w=10**6)
        adj = adjacency(V, edges, directed=False)
        t_k = t_p = 0.0
        for _ in range(repeats):
            start = time.perf_counter()
            k_total, _ = kruskal(V, edges)
            t_k += time.perf_counter() - start
            start = time.perf_counter()
            p_total, _ = prim(adj)
            t_p += time.perf_counter() - start
        print(f"| {label} | {E:,} | {t_k / repeats:.4f} | {t_p / repeats:.4f} | "
              f"{'yes' if k_total == p_total else 'no'} |", flush=True)
    print()


def demo_negative_edge():
    print("=" * 66)
    print("One negative edge: Dijkstra vs Bellman-Ford")
    print("=" * 66)
    V = 4
    edges = [(0, 1, 2), (0, 2, 5), (2, 1, -4), (1, 3, 1)]
    print("edges (u, v, w):", edges)
    dist, parent = dijkstra(adjacency(V, edges), 0)
    correct = bellman_ford(V, edges, 0)
    print(f"{'vertex':>6} {'Dijkstra':>9} {'Bellman-Ford':>13}")
    for v in range(V):
        flag = "" if dist[v] == correct[v] else "   <- wrong"
        print(f"{v:>6} {dist[v]:>9} {correct[v]:>13}{flag}")
    print("\nDijkstra finalises vertex 1 with distance 2 before it looks at vertex 2.")
    print("The cheaper route 0 -> 2 -> 1 (5 - 4 = 1) is found too late, so vertex 1")
    print("and everything reached through it (vertex 3) keep the wrong distance.\n")


if __name__ == "__main__":
    graph_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "graph.txt")
    source = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    demo_dijkstra(graph_path, source)
    demo_mst_agreement()
    demo_mst_timing()
    demo_negative_edge()
