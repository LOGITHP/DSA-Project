"""
algorithms/dijkstra.py
Array-based Dijkstra's Algorithm for Shortest Shipping Route between Depots.
No heap library used (scans array for minimum unvisited distance in O(V) time).
Time Complexity: O(V^2).

Features:
- Array-based selection of minimum distance vertex
- Full shortest path reconstruction and distance calculation
- Step-by-step distance table output for debugging and viva demonstration
- Negative weight failure demonstration explaining why greedy choice fails
"""

from typing import Dict, List, Optional, Tuple, Any
from structures.graph import Graph


class DijkstraResult:
    def __init__(self, start_node: str, distances: Dict[str, float], predecessors: Dict[str, Optional[str]], step_table: List[Dict[str, Any]]):
        self.start_node = start_node
        self.distances = distances
        self.predecessors = predecessors
        self.step_table = step_table

    def get_path(self, target: str) -> Tuple[Optional[List[str]], float]:
        """Reconstructs shortest path from start_node to target."""
        if target not in self.distances or self.distances[target] == float('inf'):
            return None, float('inf')

        path = []
        curr: Optional[str] = target
        while curr is not None:
            path.append(curr)
            curr = self.predecessors[curr]
        path.reverse()
        return path, self.distances[target]

    def print_step_table(self) -> str:
        """Formats the step-by-step relaxation table."""
        lines = []
        lines.append("=" * 80)
        lines.append(f"{'Step':<6} | {'Settled Node':<14} | {'Current Dist':<14} | {'Relaxed Neighbors / Updates':<40}")
        lines.append("-" * 80)
        for row in self.step_table:
            updates_str = ", ".join([f"{v}: {d:.1f}" for v, d in row['updates']]) if row['updates'] else "(None)"
            node_str = row['settled_node'] or "Done"
            dist_str = f"{row['settled_dist']:.1f}" if row['settled_dist'] is not None else "-"
            lines.append(f"{row['step']:<6} | {node_str:<14} | {dist_str:<14} | {updates_str:<40}")
        lines.append("=" * 80)
        return "\n".join(lines)


def dijkstra_array_based(graph: Graph, start: str) -> DijkstraResult:
    """
    Executes Array-based Dijkstra's Algorithm from start vertex.
    Maintains:
      - dist[v]: shortest known distance
      - visited[v]: settled boolean flag
      - parent[v]: predecessor node
    In each of the V iterations, scans the dist array over unvisited vertices to find min.
    """
    if start not in graph.vertex_to_index:
        raise ValueError(f"Start vertex '{start}' not in graph")

    V = graph.vertices
    dist: Dict[str, float] = {v: float('inf') for v in V}
    visited: Dict[str, bool] = {v: False for v in V}
    parent: Dict[str, Optional[str]] = {v: None for v in V}

    dist[start] = 0.0
    step_table: List[Dict[str, Any]] = []

    for step in range(1, len(V) + 1):
        # 1. Linear scan over unvisited vertices to find node with minimum dist (Array-based)
        min_dist = float('inf')
        u: Optional[str] = None
        for v in V:
            if not visited[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u is None or min_dist == float('inf'):
            # All remaining unvisited vertices are unreachable
            break

        # Settle vertex u
        visited[u] = True
        updates: List[Tuple[str, float]] = []

        # 2. Relax all outgoing edges from u
        for v, weight in graph.get_neighbors(u):
            if not visited[v]:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    updates.append((v, new_dist))

        step_table.append({
            "step": step,
            "settled_node": u,
            "settled_dist": min_dist,
            "updates": updates
        })

    return DijkstraResult(start, dist, parent, step_table)


def demonstrate_negative_edge_failure() -> Dict[str, Any]:
    """
    Constructs a 3-node counterexample showing why Dijkstra fails with negative weights.
    Graph:
      A --(3)--> B
      A --(5)--> C
      C --(-4)--> B

    Actual shortest path from A to B: A -> C -> B (cost = 5 + (-4) = 1)
    Dijkstra's result:
      Step 1: Settles B with distance 3 (since 3 < 5). B is marked VISITED.
      Step 2: Settles C with distance 5. Attempts to relax C -> B (5 - 4 = 1),
              but B is already marked visited/permanently settled and is IGNORED.
      Dijkstra outputs path A -> B with cost 3, which is WRONG!
    """
    g = Graph(is_directed=True, is_weighted=True)
    g.add_edge("Hub-A", "Hub-B", 3.0)
    g.add_edge("Hub-A", "Hub-C", 5.0)
    g.add_edge("Hub-C", "Hub-B", -4.0)

    res = dijkstra_array_based(g, "Hub-A")
    dijkstra_path, dijkstra_cost = res.get_path("Hub-B")

    true_path = ["Hub-A", "Hub-C", "Hub-B"]
    true_cost = 1.0

    explanation = (
        "WHY DIJKSTRA FAILS WITH NEGATIVE EDGES:\n"
        "----------------------------------------\n"
        "Dijkstra relies on the Greedy Choice Property and Monotonicity: once a vertex u\n"
        "is extracted from the unvisited set with minimal distance, its shortest distance is\n"
        "assumed finalized (settled) because all remaining edge weights are assumed non-negative,\n"
        "meaning future paths could only increase in cost.\n\n"
        f"In this counterexample:\n"
        f"  Dijkstra permanently settled Hub-B at Step 1 with cost {dijkstra_cost:.1f} (Path: {' -> '.join(dijkstra_path)}).\n"
        f"  However, the true optimal path is Hub-A -> Hub-C -> Hub-B with cost {true_cost:.1f}!\n"
        "  Because Hub-B was already marked visited, Dijkstra never reopened it, producing an incorrect answer.\n"
        "  (To correctly handle negative weights without negative cycles, Bellman-Ford O(V*E) must be used)."
    )

    return {
        "graph": g,
        "dijkstra_path": dijkstra_path,
        "dijkstra_cost": dijkstra_cost,
        "true_path": true_path,
        "true_cost": true_cost,
        "explanation": explanation
    }

