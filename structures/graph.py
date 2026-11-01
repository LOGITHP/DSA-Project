"""
structures/graph.py
Graph ADT for Supply Chain Logistics & Depot Networks.

Features:
- Directed and Undirected graphs
- Weighted and Unweighted graphs
- Switchable dual representation:
    * Adjacency Matrix (V x V)
    * Adjacency List (Array/Dict of neighbor-weight lists)
- Memory usage calculation and comparison: O(V^2) vs O(V + E)
- BFS fewest-stops shortest path (hop count)
- DFS with discovery/finish timestamps and edge classification:
    * Tree Edges
    * Back Edges (cycles)
    * Forward Edges
    * Cross Edges
- Connected Components (Undirected)
- Strongly Connected Components (Directed - Tarjan's Algorithm with custom Stack)
"""

from typing import Dict, List, Tuple, Optional, Set, Any
import sys
from structures.common_utils import Stack, Queue


class Edge:
    def __init__(self, u: str, v: str, weight: float = 1.0):
        self.u: str = u
        self.v: str = v
        self.weight: float = weight

    def __repr__(self) -> str:
        return f"Edge({self.u} -> {self.v}, w={self.weight})"


class Graph:
    """
    Graph Abstract Data Type representing a network of logistics depots and shipping routes.
    """
    def __init__(self, is_directed: bool = False, is_weighted: bool = True):
        self.is_directed: bool = is_directed
        self.is_weighted: bool = is_weighted
        self.representation_mode: str = "list"  # 'list' or 'matrix'

        # Vertex directory: label -> index (0..V-1)
        self.vertices: List[str] = []
        self.vertex_to_index: Dict[str, int] = {}
        self.vertex_metadata: Dict[str, Dict[str, Any]] = {}

        # Representations
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}
        self.adj_matrix: List[List[Optional[float]]] = []

        # List of all edges
        self.edges: List[Edge] = []

    def set_representation_mode(self, mode: str) -> None:
        """Switches active representation mode ('list' or 'matrix')."""
        if mode.lower() in ("list", "matrix"):
            self.representation_mode = mode.lower()
        else:
            raise ValueError("Mode must be 'list' or 'matrix'")

    def num_vertices(self) -> int:
        return len(self.vertices)

    def num_edges(self) -> int:
        return len(self.edges)

    def add_vertex(self, label: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Adds a vertex to the graph if not already present."""
        if label in self.vertex_to_index:
            return False
        idx = len(self.vertices)
        self.vertices.append(label)
        self.vertex_to_index[label] = idx
        self.vertex_metadata[label] = metadata or {}
        self.adj_list[label] = []

        # Expand existing rows of adjacency matrix
        for row in self.adj_matrix:
            row.append(None)
        # Add new row
        self.adj_matrix.append([None] * len(self.vertices))
        # Self-distance is 0 for diagonal if weighted
        self.adj_matrix[idx][idx] = 0.0 if self.is_weighted else 0.0

        return True

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> bool:
        """Adds an edge between u and v."""
        if u not in self.vertex_to_index:
            self.add_vertex(u)
        if v not in self.vertex_to_index:
            self.add_vertex(v)

        w = weight if self.is_weighted else 1.0
        u_idx = self.vertex_to_index[u]
        v_idx = self.vertex_to_index[v]

        # 1. Update Adjacency List
        self.adj_list[u].append((v, w))
        if not self.is_directed and u != v:
            self.adj_list[v].append((u, w))

        # 2. Update Adjacency Matrix
        self.adj_matrix[u_idx][v_idx] = w
        if not self.is_directed:
            self.adj_matrix[v_idx][u_idx] = w

        # 3. Store in edge list
        self.edges.append(Edge(u, v, w))
        return True

    def get_neighbors(self, u: str) -> List[Tuple[str, float]]:
        """Returns neighbors based on currently active representation mode."""
        if u not in self.vertex_to_index:
            return []

        if self.representation_mode == "list":
            return list(self.adj_list.get(u, []))
        else:
            # Derived from Adjacency Matrix
            u_idx = self.vertex_to_index[u]
            neighbors = []
            for v_idx, w in enumerate(self.adj_matrix[u_idx]):
                if w is not None and (u_idx != v_idx or self.is_directed):
                    if w > 0 or (u_idx != v_idx):
                        neighbors.append((self.vertices[v_idx], w))
            return neighbors

    # ------------------ Memory Usage Reporting ------------------
    def report_memory_usage(self) -> Dict[str, Any]:
        """
        Reports theoretical and actual memory footprints of Adjacency Matrix vs Adjacency List.
        """
        V = len(self.vertices)
        E = len(self.edges)

        # Theoretical bounds
        # Matrix: V x V table of float pointers (8 bytes per entry)
        matrix_theoretical_bytes = V * V * 8
        # List: V array headers + entries for each directed/undirected edge
        edge_multiplier = 1 if self.is_directed else 2
        list_theoretical_bytes = (V * 8) + (E * edge_multiplier * 16)

        # Python object introspection (sys.getsizeof)
        matrix_actual = sys.getsizeof(self.adj_matrix) + sum(sys.getsizeof(row) for row in self.adj_matrix)
        list_actual = sys.getsizeof(self.adj_list) + sum(sys.getsizeof(neighbors) for neighbors in self.adj_list.values())

        return {
            "num_vertices": V,
            "num_edges": E,
            "matrix_theoretical_bytes": matrix_theoretical_bytes,
            "list_theoretical_bytes": list_theoretical_bytes,
            "matrix_actual_bytes": matrix_actual,
            "list_actual_bytes": list_actual,
            "active_mode": self.representation_mode,
            "recommendation": "Adjacency List is far superior for sparse graphs (E << V^2); Matrix is optimal for dense graphs (E ~ V^2)."
        }

    # ------------------ BFS Fewest-Stops Route ------------------
    def bfs_fewest_stops(self, start: str, target: str) -> Tuple[Optional[List[str]], int]:
        """
        Finds the route with the fewest intermediate hops using BFS.
        Returns: (path_list, hop_count) or (None, -1) if unreachable.
        """
        if start not in self.vertex_to_index or target not in self.vertex_to_index:
            return None, -1

        visited: Set[str] = {start}
        parent: Dict[str, Optional[str]] = {start: None}
        hops: Dict[str, int] = {start: 0}

        q = Queue()
        q.enqueue(start)

        while not q.is_empty():
            curr: str = q.dequeue()
            if curr == target:
                # Reconstruct path
                path = []
                step = target
                while step is not None:
                    path.append(step)
                    step = parent[step]
                path.reverse()
                return path, hops[target]

            for neighbor, _ in self.get_neighbors(curr):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    hops[neighbor] = hops[curr] + 1
                    q.enqueue(neighbor)

        return None, -1

    # ------------------ DFS Discovery/Finish & Edge Classification ------------------
    def dfs_edge_classification(self) -> Dict[str, Any]:
        """
        Performs DFS tracking discovery and finish times.
        Classifies all edges into: Tree, Back (cycle), Forward, Cross.
        """
        time = 0
        discovery: Dict[str, int] = {}
        finish: Dict[str, int] = {}
        # Node states: 0 = unvisited (white), 1 = visiting/on stack (gray), 2 = finished (black)
        color: Dict[str, int] = {v: 0 for v in self.vertices}
        classified_edges: List[Tuple[str, str, str]] = []  # (u, v, edge_type)

        def _dfs_visit(u: str):
            nonlocal time
            time += 1
            discovery[u] = time
            color[u] = 1  # Gray

            for v, _ in self.get_neighbors(u):
                if color[v] == 0:
                    classified_edges.append((u, v, "Tree Edge"))
                    _dfs_visit(v)
                elif color[v] == 1:
                    # Leads to an ancestor currently on the recursion stack -> cycle!
                    classified_edges.append((u, v, "Back Edge (Cycle detected)"))
                else:
                    # Color is 2 (Black)
                    if discovery[u] < discovery[v]:
                        classified_edges.append((u, v, "Forward Edge"))
                    else:
                        classified_edges.append((u, v, "Cross Edge"))

            color[u] = 2  # Black
            time += 1
            finish[u] = time

        for v in self.vertices:
            if color[v] == 0:
                _dfs_visit(v)

        return {
            "discovery_times": discovery,
            "finish_times": finish,
            "classified_edges": classified_edges
        }

    # ------------------ Connected Components (Undirected) ------------------
    def connected_components(self) -> List[List[str]]:
        """
        Finds connected components for undirected graph.
        """
        visited: Set[str] = set()
        components: List[List[str]] = []

        for v in self.vertices:
            if v not in visited:
                comp = []
                q = Queue()
                q.enqueue(v)
                visited.add(v)
                while not q.is_empty():
                    curr = q.dequeue()
                    comp.append(curr)
                    for nxt, _ in self.get_neighbors(curr):
                        if nxt not in visited:
                            visited.add(nxt)
                            q.enqueue(nxt)
                components.append(comp)

        return components

    # ------------------ Strongly Connected Components (Directed - Tarjan) ------------------
    def strongly_connected_components(self) -> List[List[str]]:
        """
        Computes SCCs using Tarjan's linear time algorithm O(V + E) with explicit custom Stack.
        """
        index = 0
        indices: Dict[str, int] = {}
        lowlink: Dict[str, int] = {}
        on_stack: Dict[str, bool] = {v: False for v in self.vertices}
        stack = Stack()
        sccs: List[List[str]] = []

        def _strongconnect(v: str):
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.push(v)
            on_stack[v] = True

            for w, _ in self.get_neighbors(v):
                if w not in indices:
                    # Successor w has not yet been visited; recurse on it
                    _strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack[w]:
                    # Successor w is in stack and hence in the current SCC
                    lowlink[v] = min(lowlink[v], indices[w])

            # If v is a root node, pop the stack and generate an SCC
            if lowlink[v] == indices[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == v:
                        break
                sccs.append(scc)

        for v in self.vertices:
            if v not in indices:
                _strongconnect(v)

        return sccs

