"""
structures/general_tree.py
Product Category General Tree for Supply Chain Management.
Hierarchy:
  Supply Chain Catalog (Root)
    └── Product Division
          └── Category
                └── Product Line / Item Family

Features:
- Insert child under specified parent
- Delete subtree rooted at node
- Visual ASCII tree hierarchy display
- Preorder traversal (Recursive & Iterative using explicit custom Stack)
- Postorder traversal (Recursive & Iterative using explicit custom Stack)
- Level-order traversal (Recursive & Iterative using explicit custom Queue)
"""

from typing import List, Optional, Any, Tuple
from structures.common_utils import Stack, Queue


class GeneralTreeNode:
    def __init__(self, name: str, data: Optional[Any] = None):
        self.name: str = name
        self.data: Any = data or {}
        self.children: List['GeneralTreeNode'] = []
        self.parent: Optional['GeneralTreeNode'] = None

    def add_child(self, child_node: 'GeneralTreeNode') -> None:
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node: 'GeneralTreeNode') -> bool:
        if child_node in self.children:
            self.children.remove(child_node)
            child_node.parent = None
            return True
        return False

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def __repr__(self) -> str:
        return f"GeneralTreeNode({self.name})"


class GeneralTree:
    """
    General n-ary Tree representing a hierarchical Supply Chain Product Taxonomy.
    """
    def __init__(self, root_name: str = "Supply Chain Master Catalog", root_data: Optional[Any] = None):
        self.root: GeneralTreeNode = GeneralTreeNode(root_name, root_data)

    def find_node(self, name: str) -> Optional[GeneralTreeNode]:
        """Finds a node by name using level-order traversal."""
        if not self.root:
            return None
        q = Queue()
        q.enqueue(self.root)
        while not q.is_empty():
            curr: GeneralTreeNode = q.dequeue()
            if curr.name.lower() == name.lower():
                return curr
            for ch in curr.children:
                q.enqueue(ch)
        return None

    def insert(self, parent_name: str, child_name: str, data: Optional[Any] = None) -> bool:
        """Inserts a child node under the specified parent."""
        parent = self.find_node(parent_name)
        if not parent:
            return False
        # Prevent duplicate sibling names
        for ch in parent.children:
            if ch.name.lower() == child_name.lower():
                return False
        new_node = GeneralTreeNode(child_name, data)
        parent.add_child(new_node)
        return True

    def delete_subtree(self, node_name: str) -> bool:
        """Deletes the entire subtree rooted at node_name (cannot delete root)."""
        if self.root.name.lower() == node_name.lower():
            return False  # Root cannot be deleted
        target = self.find_node(node_name)
        if not target or not target.parent:
            return False
        return target.parent.remove_child(target)

    # ------------------ Traversals ------------------

    # 1. Preorder: Recursive
    def preorder_recursive(self) -> List[str]:
        result = []
        def _pre(node: Optional[GeneralTreeNode]):
            if not node:
                return
            result.append(node.name)
            for ch in node.children:
                _pre(ch)
        _pre(self.root)
        return result

    # 1. Preorder: Iterative (Explicit custom Stack)
    def preorder_iterative(self) -> List[str]:
        if not self.root:
            return []
        result = []
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            curr: GeneralTreeNode = stack.pop()
            result.append(curr.name)
            # Push children in reverse order so leftmost child is popped first
            for ch in reversed(curr.children):
                stack.push(ch)
        return result

    # 2. Postorder: Recursive
    def postorder_recursive(self) -> List[str]:
        result = []
        def _post(node: Optional[GeneralTreeNode]):
            if not node:
                return
            for ch in node.children:
                _post(ch)
            result.append(node.name)
        _post(self.root)
        return result

    # 2. Postorder: Iterative (Explicit custom Stack)
    def postorder_iterative(self) -> List[str]:
        if not self.root:
            return []
        # Two-stack method for general tree postorder
        s1 = Stack()
        s2 = Stack()
        s1.push(self.root)
        while not s1.is_empty():
            curr: GeneralTreeNode = s1.pop()
            s2.push(curr)
            for ch in curr.children:
                s1.push(ch)
        result = []
        while not s2.is_empty():
            result.append(s2.pop().name)
        return result

    # 3. Level-order: Iterative (Explicit custom Queue)
    def level_order_iterative(self) -> List[str]:
        if not self.root:
            return []
        result = []
        q = Queue()
        q.enqueue(self.root)
        while not q.is_empty():
            curr: GeneralTreeNode = q.dequeue()
            result.append(curr.name)
            for ch in curr.children:
                q.enqueue(ch)
        return result

    # 3. Level-order: Recursive
    def level_order_recursive(self) -> List[str]:
        result = []
        height = self._get_height(self.root)
        for level in range(1, height + 1):
            self._get_given_level(self.root, level, result)
        return result

    def _get_height(self, node: Optional[GeneralTreeNode]) -> int:
        if not node:
            return 0
        if not node.children:
            return 1
        return 1 + max(self._get_height(ch) for ch in node.children)

    def _get_given_level(self, node: Optional[GeneralTreeNode], level: int, out: List[str]):
        if not node:
            return
        if level == 1:
            out.append(node.name)
        elif level > 1:
            for ch in node.children:
                self._get_given_level(ch, level - 1, out)

    # ------------------ Display ------------------
    def display_tree(self) -> str:
        """Returns visual hierarchical ASCII tree representation."""
        if not self.root:
            return "(Empty Tree)"
        lines = []

        def _build_str(node: GeneralTreeNode, prefix: str = "", is_tail: bool = True):
            connector = "└── " if is_tail else "├── "
            info = f" [{node.data}]" if node.data else ""
            lines.append(f"{prefix}{connector}{node.name}{info}")
            new_prefix = prefix + ("    " if is_tail else "│   ")
            child_count = len(node.children)
            for i, child in enumerate(node.children):
                _build_str(child, new_prefix, i == (child_count - 1))

        lines.append(f"{self.root.name} (Root)")
        child_count = len(self.root.children)
        for i, child in enumerate(self.root.children):
            _build_str(child, "", i == (child_count - 1))

        return "\n".join(lines)

