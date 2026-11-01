"""
algorithms/mst.py
Minimum Spanning Tree (MST) and Minimum Spanning Forest (MSF) algorithms:
1. Prim's Algorithm (Array-based, O(V^2), unvisited key-array scan, no heap)
2. Kruskal's Algorithm (Custom MergeSort + Union-Find with path compression and rank, O(E log E))

Both algorithms support disconnected graphs by producing a Minimum Spanning Forest (MSF).
Both algorithms guarantee identical total weight across any graph!
"""

from typing import List, Tuple, Dict, Optional, Set, Any
from structures.graph import Graph, Edge
from structures.disjoint_set import DisjointSet
from structures.common_utils import merge_sort


class MSTResult:
    def __init__(self, algorithm_name: str, edges: List[Tuple[str, str, float]], total_weight: float, is_forest: bool = False, component_count: int = 1):
        self.algorithm_name = algorithm_name
        self.edges = edges
        self.total_weight = round(total_weight, 4)
        self.is_forest = is_forest
        self.component_count = component_count

    def display(self) -> str:
        lines = []
        forest_tag = f"Minimum Spanning Forest ({self.component_count} Components)" if self.is_forest else "Minimum Spanning Tree"
        lines.append(f"[{self.algorithm_name}] {forest_tag}")
        lines.append(f"Total Network Cost / Weight: {self.total_weight:.2f}")
        lines.append(f"Total Edges Selected: {len(self.edges)}")
        lines.append("-" * 50)
        lines.append(f"{'Source Depot':<20} <---> {'Destination Depot':<20} | {'Weight':<10}")
        lines.append("-" * 50)
        for u, v, w in self.edges:
            lines.append(f"{u:<20} <---> {v:<20} | {w:<10.2f}")
        lines.append("-" * 50)
        return "\n".join(lines)


def prim_array_based(graph: Graph) -> MSTResult:
    """
    Array-based Prim's Algorithm.
    For disconnected graphs, runs across each component to produce a Minimum Spanning Forest.
    Time Complexity: O(V^2).
    """
    V = graph.vertices
    if not V:
        return MSTResult("Prim (Array-based)", [], 0.0)

    visited: Dict[str, bool] = {v: False for v in V}
    mst_edges: List[Tuple[str, str, float]] = []
    total_weight: float = 0.0
    component_count = 0

    # Handle potentially disconnected components (Spanning Forest)
    for start_node in V:
        if visited[start_node]:
            continue

        component_count += 1
        # Arrays for current component
        key: Dict[str, float] = {v: float('inf') for v in V}
        parent: Dict[str, Optional[str]] = {v: None for v in V}
        key[start_node] = 0.0

        while True:
            # Linear scan over unvisited vertices to find min key
            min_key = float('inf')
            u: Optional[str] = None
            for v in V:
                if not visited[v] and key[v] < min_key:
                    min_key = key[v]
                    u = v

            if u is None or min_key == float('inf'):
                break

            visited[u] = True

            # If u has a parent, add edge to MST
            if parent[u] is not None:
                mst_edges.append((parent[u], u, key[u]))
                total_weight += key[u]

            # Update keys of unvisited neighbors
            for v, weight in graph.get_neighbors(u):
                if not visited[v] and weight < key[v]:
                    key[v] = weight
                    parent[v] = u

    is_forest = component_count > 1
    return MSTResult("Prim (Array-based)", mst_edges, total_weight, is_forest, component_count)


def kruskal_mst(graph: Graph) -> MSTResult:
    """
    Kruskal's Algorithm using:
      1. Custom MergeSort for edge sorting O(E log E)
      2. DisjointSet with path compression & union by rank O(E * alpha(V))
    Supports disconnected graphs producing a Minimum Spanning Forest.
    """
    # 1. Collect all unique undirected edges
    unique_edges = []
    seen = set()
    for edge in graph.edges:
        # Normalize undirected edge representation to prevent duplicates
        pair = tuple(sorted([edge.u, edge.v]))
        if pair not in seen:
            seen.add(pair)
            unique_edges.append(edge)

    # 2. Sort edges by weight using our custom MergeSort from scratch
    sorted_edges: List[Edge] = merge_sort(unique_edges, key=lambda e: e.weight)

    # 3. Initialize Disjoint Set with all vertices
    dsu = DisjointSet(graph.vertices)
    mst_edges: List[Tuple[str, str, float]] = []
    total_weight = 0.0

    # 4. Iterate through edges and add non-cyclical edges
    for edge in sorted_edges:
        if dsu.union(edge.u, edge.v):
            mst_edges.append((edge.u, edge.v, edge.weight))
            total_weight += edge.weight

    # Component count is the number of remaining disjoint sets
    components = dsu.get_components()
    comp_count = len(components)
    is_forest = comp_count > 1

    return MSTResult("Kruskal (MergeSort + DSU)", mst_edges, total_weight, is_forest, comp_count)

