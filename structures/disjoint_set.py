"""
structures/disjoint_set.py
Disjoint Set Union (DSU) / Union-Find data structure with:
1. Path Compression: Flattens tree during find() operations.
2. Union by Rank: Attaches tree of smaller rank to root of larger rank.

Together, these optimizations achieve an amortized time complexity of O(alpha(V)) per operation,
where alpha is the Inverse Ackermann function (effectively <= 4 for all practical universe sizes).
"""

from typing import Dict, Any, List, Set


class DisjointSet:
    """
    Union-Find Data Structure supporting elements of any hashable type (IDs, strings, integers).
    """
    def __init__(self, elements: List[Any] = None):
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
        self.num_sets: int = 0
        if elements:
            for elem in elements:
                self.make_set(elem)

    def make_set(self, x: Any) -> None:
        """Initializes a new singleton set with representative x."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.num_sets += 1

    def find(self, x: Any) -> Any:
        """
        Finds the representative/root of the set containing x with Path Compression.
        All visited nodes on the search path point directly to the root.
        """
        if x not in self.parent:
            self.make_set(x)

        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """
        Merges sets containing x and y using Union by Rank.
        Returns True if a merge occurred (were in different sets),
        False if x and y were already in the same set (cycle detected).
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.num_sets -= 1
        return True

    def connected(self, x: Any, y: Any) -> bool:
        """Checks if x and y belong to the same connected component."""
        return self.find(x) == self.find(y)

    def get_components(self) -> Dict[Any, List[Any]]:
        """Groups all elements into their respective disjoint sets."""
        groups: Dict[Any, List[Any]] = {}
        for elem in self.parent:
            root = self.find(elem)
            if root not in groups:
                groups[root] = []
            groups[root].append(elem)
        return groups

