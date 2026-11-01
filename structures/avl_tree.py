"""
structures/avl_tree.py
AVL Tree for Supplier Index in Supply Chain Management.
Guarantees O(log N) worst-case time for Insert, Search, and Delete.

Features:
- Insert and Delete with all four balancing rotations:
  * LL (Left-Left: Single Right Rotation)
  * RR (Right-Right: Single Left Rotation)
  * LR (Left-Right: Double Rotation - Left then Right)
  * RL (Right-Left: Double Rotation - Right then Left)
- Configurable rotation tracing with detailed pivot info
- verify() function checking:
  1. Strict BST ordering property across all subtrees
  2. Height property correctness (stored == 1 + max(h(left), h(right)))
  3. Balance factor validity (|BF| <= 1 for all nodes)
"""

from typing import Optional, List, Tuple, Any
import random


class AVLNode:
    def __init__(self, supplier_id: int, name: str, category: str = "", lead_time: int = 0, reliability: float = 0.0, location: str = ""):
        self.supplier_id: int = supplier_id
        self.name: str = name
        self.category: str = category
        self.lead_time: int = lead_time          # in days
        self.reliability: float = reliability    # 0.0 to 5.0
        self.location: str = location
        self.height: int = 1
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None

    def __repr__(self) -> str:
        return f"Supplier({self.supplier_id}, '{self.name}', loc='{self.location}', lead={self.lead_time}d, rating={self.reliability})"


class AVLTree:
    """
    Self-balancing AVL Tree maintaining Supplier Directory by Supplier ID.
    """
    def __init__(self, trace_rotations: bool = False):
        self.root: Optional[AVLNode] = None
        self._size: int = 0
        self.trace_rotations: bool = trace_rotations
        self.last_rotation_log: List[str] = []

    def _log_rotation(self, rotation_type: str, node_key: int, child_key: int):
        msg = f"[AVL ROTATION] {rotation_type} executed at Node ID {node_key} (Child ID {child_key})"
        self.last_rotation_log.append(msg)
        if self.trace_rotations:
            print(msg)

    # ------------------ Height & Balance Factor ------------------
    @staticmethod
    def _get_height(node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    # ------------------ Rotations ------------------
    def _rotate_right(self, y: AVLNode) -> AVLNode:
        r"""
        Right Rotation (LL fix).
             y                     x
            / \                   / \
           x   T3   ----->       T1  y
          / \                       / \
         T1  T2                    T2  T3
        """
        assert y.left is not None
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights (y first, then x)
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        r"""
        Left Rotation (RR fix).
           x                         y
          / \                       / \
         T1  y       ----->        x   T3
            / \                   / \
           T2  T3                T1  T2
        """
        assert x.right is not None
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights (x first, then y)
        self._update_height(x)
        self._update_height(y)

        return y

    # ------------------ Insert ------------------
    def insert(self, supplier_id: int, name: str, category: str = "", lead_time: int = 0, reliability: float = 0.0, location: str = "") -> bool:
        """
        Inserts new supplier. Rebalances automatically on unwind.
        Returns True if inserted, False if updated existing record.
        """
        inserted = [False]

        def _insert_rec(node: Optional[AVLNode]) -> AVLNode:
            if not node:
                inserted[0] = True
                return AVLNode(supplier_id, name, category, lead_time, reliability, location)

            if supplier_id < node.supplier_id:
                node.left = _insert_rec(node.left)
            elif supplier_id > node.supplier_id:
                node.right = _insert_rec(node.right)
            else:
                # Update existing record
                node.name = name
                node.category = category
                node.lead_time = lead_time
                node.reliability = reliability
                node.location = location
                return node

            # 1. Update height of this ancestor node
            self._update_height(node)

            # 2. Get balance factor
            balance = self._get_balance(node)

            # 3. Check for 4 rotation cases:
            # Case 1: Left-Left (LL)
            if balance > 1 and node.left and supplier_id < node.left.supplier_id:
                self._log_rotation("LL (Single Right Rotation)", node.supplier_id, node.left.supplier_id)
                return self._rotate_right(node)

            # Case 2: Right-Right (RR)
            if balance < -1 and node.right and supplier_id > node.right.supplier_id:
                self._log_rotation("RR (Single Left Rotation)", node.supplier_id, node.right.supplier_id)
                return self._rotate_left(node)

            # Case 3: Left-Right (LR)
            if balance > 1 and node.left and supplier_id > node.left.supplier_id:
                self._log_rotation("LR (Left-Right Double Rotation)", node.supplier_id, node.left.supplier_id)
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # Case 4: Right-Left (RL)
            if balance < -1 and node.right and supplier_id < node.right.supplier_id:
                self._log_rotation("RL (Right-Left Double Rotation)", node.supplier_id, node.right.supplier_id)
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _insert_rec(self.root)
        if inserted[0]:
            self._size += 1
        return inserted[0]

    # ------------------ Delete ------------------
    def delete(self, supplier_id: int) -> bool:
        """
        Deletes supplier by ID and rebalances the tree.
        """
        deleted = [False]

        def _min_value_node(n: AVLNode) -> AVLNode:
            curr = n
            while curr.left:
                curr = curr.left
            return curr

        def _delete_rec(node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
            if not node:
                return None

            if key < node.supplier_id:
                node.left = _delete_rec(node.left, key)
            elif key > node.supplier_id:
                node.right = _delete_rec(node.right, key)
            else:
                # Target node found
                deleted[0] = True
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    # Node with two children: get inorder successor
                    succ = _min_value_node(node.right)
                    # Copy successor data
                    node.supplier_id = succ.supplier_id
                    node.name = succ.name
                    node.category = succ.category
                    node.lead_time = succ.lead_time
                    node.reliability = succ.reliability
                    node.location = succ.location
                    # Delete successor
                    node.right = _delete_rec(node.right, succ.supplier_id)

            if not node:
                return None

            # 1. Update height
            self._update_height(node)

            # 2. Check balance factor
            balance = self._get_balance(node)

            # 3. Rebalance if needed
            # Case 1: Left-Left
            if balance > 1 and self._get_balance(node.left) >= 0:
                assert node.left is not None
                self._log_rotation("LL (Single Right Rotation on Delete)", node.supplier_id, node.left.supplier_id)
                return self._rotate_right(node)

            # Case 2: Left-Right
            if balance > 1 and self._get_balance(node.left) < 0:
                assert node.left is not None
                self._log_rotation("LR (Left-Right Double Rotation on Delete)", node.supplier_id, node.left.supplier_id)
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # Case 3: Right-Right
            if balance < -1 and self._get_balance(node.right) <= 0:
                assert node.right is not None
                self._log_rotation("RR (Single Left Rotation on Delete)", node.supplier_id, node.right.supplier_id)
                return self._rotate_left(node)

            # Case 4: Right-Left
            if balance < -1 and self._get_balance(node.right) > 0:
                assert node.right is not None
                self._log_rotation("RL (Right-Left Double Rotation on Delete)", node.supplier_id, node.right.supplier_id)
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _delete_rec(self.root, supplier_id)
        if deleted[0]:
            self._size -= 1
        return deleted[0]

    # ------------------ Search ------------------
    def search(self, supplier_id: int) -> Optional[AVLNode]:
        curr = self.root
        while curr:
            if supplier_id == curr.supplier_id:
                return curr
            elif supplier_id < curr.supplier_id:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def height(self) -> int:
        return self._get_height(self.root)

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    # ------------------ Verification Function ------------------
    def verify(self) -> Tuple[bool, str]:
        """
        Exhaustively validates:
          1. BST Property: keys strictly increasing in In-Order traversal.
          2. Stored Height: node.height == 1 + max(h(left), h(right)) for every node.
          3. Balance Factor: |h(left) - h(right)| <= 1 for every node.
        Returns: (True, "Valid") or (False, failure_reason)
        """
        if not self.root:
            return True, "Tree is empty (Valid)"

        # Check BST Property and heights recursively
        def _check(node: Optional[AVLNode], min_val: float, max_val: float) -> Tuple[bool, int, str]:
            if not node:
                return True, 0, ""

            # Check BST Ordering
            if not (min_val < node.supplier_id < max_val):
                return False, 0, f"BST Violation at key {node.supplier_id} outside bounds ({min_val}, {max_val})"

            # Recurse left
            left_ok, left_h, left_err = _check(node.left, min_val, node.supplier_id)
            if not left_ok:
                return False, 0, left_err

            # Recurse right
            right_ok, right_h, right_err = _check(node.right, node.supplier_id, max_val)
            if not right_ok:
                return False, 0, right_err

            # Check Stored Height
            expected_h = 1 + max(left_h, right_h)
            if node.height != expected_h:
                return False, 0, f"Height Violation at key {node.supplier_id}: stored={node.height}, computed={expected_h}"

            # Check Balance Factor
            bf = left_h - right_h
            if abs(bf) > 1:
                return False, 0, f"Balance Factor Violation at key {node.supplier_id}: BF={bf}"

            return True, expected_h, ""

        ok, _, err = _check(self.root, float('-inf'), float('inf'))
        return ok, "Valid AVL Tree (BST property, heights, and balance factors verified)" if ok else err

    # ------------------ Inorder Traversal ------------------
    def inorder(self) -> List[AVLNode]:
        res = []
        def _in(n):
            if n:
                _in(n.left)
                res.append(n)
                _in(n.right)
        _in(self.root)
        return res
