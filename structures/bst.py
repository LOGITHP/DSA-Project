"""
structures/bst.py
Binary Search Tree (BST) for Inventory Management indexed by SKU (Stock Keeping Unit).

Features:
- Insert, Search, Delete (all three cases: leaf, one child, two children via successor)
- Min, Max, Successor, Predecessor
- Range Query: [sku_min, sku_max]
- Tree Height calculation
- Recursive and Iterative Traversals (Inorder, Preorder, Postorder, Level-Order)
  utilizing explicit custom Stack and Queue.
"""

import sys
# Ensure higher recursion limit for deep degenerate trees
if sys.getrecursionlimit() < 50000:
    sys.setrecursionlimit(50000)

from typing import Optional, List, Tuple, Any
from structures.common_utils import Stack, Queue


class BSTNode:
    def __init__(self, sku: int, name: str, quantity: int = 0, unit_price: float = 0.0, category: str = ""):
        self.sku: int = sku
        self.name: str = name
        self.quantity: int = quantity
        self.unit_price: float = unit_price
        self.category: str = category
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

    def __repr__(self) -> str:
        return f"SKU-{self.sku}: {self.name} (Qty: {self.quantity}, Price: ${self.unit_price:.2f})"


class BinarySearchTree:
    """
    Binary Search Tree storing Inventory Items ordered by numeric SKU ID.
    """
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self.root is None

    def __len__(self) -> int:
        return self._size

    # ------------------ Insert ------------------
    def insert(self, sku: int, name: str, quantity: int = 0, unit_price: float = 0.0, category: str = "") -> bool:
        """Inserts a new SKU into BST. If SKU exists, updates existing item."""
        if self.root is None:
            self.root = BSTNode(sku, name, quantity, unit_price, category)
            self._size += 1
            return True

        curr = self.root
        while True:
            if sku == curr.sku:
                # Update existing record
                curr.name = name
                curr.quantity = quantity
                curr.unit_price = unit_price
                curr.category = category
                return False  # Existing updated
            elif sku < curr.sku:
                if curr.left is None:
                    curr.left = BSTNode(sku, name, quantity, unit_price, category)
                    self._size += 1
                    return True
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(sku, name, quantity, unit_price, category)
                    self._size += 1
                    return True
                curr = curr.right

    # ------------------ Search ------------------
    def search(self, sku: int) -> Optional[BSTNode]:
        """Searches for a node by SKU in O(h) time."""
        curr = self.root
        while curr:
            if sku == curr.sku:
                return curr
            elif sku < curr.sku:
                curr = curr.left
            else:
                curr = curr.right
        return None

    # ------------------ Delete ------------------
    def delete(self, sku: int) -> Tuple[bool, str]:
        """
        Deletes node with given SKU handling all 3 cases:
          Case 1: Leaf node (0 children)
          Case 2: Node with 1 child (left or right)
          Case 3: Node with 2 children (replace with inorder successor)
        Returns: (success_bool, case_description_str)
        """
        reported_case = ["Not Found"]

        def _delete_rec(node: Optional[BSTNode], key: int, is_subcall: bool = False) -> Optional[BSTNode]:
            if node is None:
                return None

            if key < node.sku:
                node.left = _delete_rec(node.left, key, is_subcall)
            elif key > node.sku:
                node.right = _delete_rec(node.right, key, is_subcall)
            else:
                # Node found!
                # Case 1: Leaf node
                if node.left is None and node.right is None:
                    if not is_subcall:
                        reported_case[0] = "Case 1: Leaf Node (0 children)"
                    return None
                # Case 2: One child (only right child)
                elif node.left is None:
                    if not is_subcall:
                        reported_case[0] = "Case 2: Single Right Child"
                    return node.right
                # Case 2: One child (only left child)
                elif node.right is None:
                    if not is_subcall:
                        reported_case[0] = "Case 2: Single Left Child"
                    return node.left
                # Case 3: Two children
                else:
                    reported_case[0] = "Case 3: Two Children (Replaced with Inorder Successor)"
                    # Find minimum in right subtree (Inorder Successor)
                    successor = self._min_node(node.right)
                    # Copy successor data into current node
                    node.sku = successor.sku
                    node.name = successor.name
                    node.quantity = successor.quantity
                    node.unit_price = successor.unit_price
                    node.category = successor.category
                    # Delete the successor from right subtree without overwriting reported_case
                    node.right = _delete_rec(node.right, successor.sku, is_subcall=True)

            return node

        self.root = _delete_rec(self.root, sku)
        if reported_case[0] != "Not Found":
            self._size -= 1
            return True, reported_case[0]
        return False, reported_case[0]

    # ------------------ Min / Max ------------------
    def _min_node(self, node: BSTNode) -> BSTNode:
        curr = node
        while curr.left:
            curr = curr.left
        return curr

    def _max_node(self, node: BSTNode) -> BSTNode:
        curr = node
        while curr.right:
            curr = curr.right
        return curr

    def find_min(self) -> Optional[BSTNode]:
        if not self.root:
            return None
        return self._min_node(self.root)

    def find_max(self) -> Optional[BSTNode]:
        if not self.root:
            return None
        return self._max_node(self.root)

    # ------------------ Predecessor & Successor ------------------
    def successor(self, sku: int) -> Optional[BSTNode]:
        """Finds in-order successor of given SKU."""
        succ = None
        curr = self.root
        while curr:
            if sku < curr.sku:
                succ = curr
                curr = curr.left
            elif sku > curr.sku:
                curr = curr.right
            else:
                if curr.right:
                    return self._min_node(curr.right)
                break
        return succ

    def predecessor(self, sku: int) -> Optional[BSTNode]:
        """Finds in-order predecessor of given SKU."""
        pred = None
        curr = self.root
        while curr:
            if sku > curr.sku:
                pred = curr
                curr = curr.right
            elif sku < curr.sku:
                curr = curr.left
            else:
                if curr.left:
                    return self._max_node(curr.left)
                break
        return pred

    # ------------------ Range Query ------------------
    def range_query(self, a: int, b: int) -> List[BSTNode]:
        """Returns all items whose SKU satisfies a <= SKU <= b in ascending order."""
        result = []
        def _inorder_range(node: Optional[BSTNode]):
            if not node:
                return
            if node.sku > a:
                _inorder_range(node.left)
            if a <= node.sku <= b:
                result.append(node)
            if node.sku < b:
                _inorder_range(node.right)

        _inorder_range(self.root)
        return result

    # ------------------ Height ------------------
    def height(self) -> int:
        """Computes tree height iteratively to prevent RecursionError on degenerate trees."""
        if not self.root:
            return 0
        q = Queue()
        q.enqueue(self.root)
        height = 0
        while not q.is_empty():
            level_size = q.size()
            for _ in range(level_size):
                curr = q.dequeue()
                if curr.left:
                    q.enqueue(curr.left)
                if curr.right:
                    q.enqueue(curr.right)
            height += 1
        return height

    # ------------------ Traversals (Recursive & Iterative) ------------------

    # 1. Inorder: Recursive
    def inorder_recursive(self) -> List[int]:
        res = []
        def _in(n):
            if n:
                _in(n.left)
                res.append(n.sku)
                _in(n.right)
        _in(self.root)
        return res

    # 1. Inorder: Iterative (Explicit Custom Stack)
    def inorder_iterative(self) -> List[int]:
        res = []
        stack = Stack()
        curr = self.root
        while curr is not None or not stack.is_empty():
            while curr is not None:
                stack.push(curr)
                curr = curr.left
            curr = stack.pop()
            res.append(curr.sku)
            curr = curr.right
        return res

    # 2. Preorder: Recursive
    def preorder_recursive(self) -> List[int]:
        res = []
        def _pre(n):
            if n:
                res.append(n.sku)
                _pre(n.left)
                _pre(n.right)
        _pre(self.root)
        return res

    # 2. Preorder: Iterative (Explicit Custom Stack)
    def preorder_iterative(self) -> List[int]:
        if not self.root:
            return []
        res = []
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            curr: BSTNode = stack.pop()
            res.append(curr.sku)
            if curr.right:
                stack.push(curr.right)
            if curr.left:
                stack.push(curr.left)
        return res

    # 3. Postorder: Recursive
    def postorder_recursive(self) -> List[int]:
        res = []
        def _post(n):
            if n:
                _post(n.left)
                _post(n.right)
                res.append(n.sku)
        _post(self.root)
        return res

    # 3. Postorder: Iterative (Explicit Custom Stack - Two Stacks Method)
    def postorder_iterative(self) -> List[int]:
        if not self.root:
            return []
        s1 = Stack()
        s2 = Stack()
        s1.push(self.root)
        while not s1.is_empty():
            curr: BSTNode = s1.pop()
            s2.push(curr)
            if curr.left:
                s1.push(curr.left)
            if curr.right:
                s1.push(curr.right)
        res = []
        while not s2.is_empty():
            res.append(s2.pop().sku)
        return res

    # 4. Level-Order: Iterative (Explicit Custom Queue)
    def level_order_iterative(self) -> List[int]:
        if not self.root:
            return []
        res = []
        q = Queue()
        q.enqueue(self.root)
        while not q.is_empty():
            curr: BSTNode = q.dequeue()
            res.append(curr.sku)
            if curr.left:
                q.enqueue(curr.left)
            if curr.right:
                q.enqueue(curr.right)
        return res

    # 4. Level-Order: Recursive
    def level_order_recursive(self) -> List[int]:
        res = []
        h = self.height()
        for level in range(1, h + 1):
            self._print_level(self.root, level, res)
        return res

    def _print_level(self, node: Optional[BSTNode], level: int, out: List[int]):
        if not node:
            return
        if level == 1:
            out.append(node.sku)
        elif level > 1:
            self._print_level(node.left, level - 1, out)
            self._print_level(node.right, level - 1, out)
