"""
structures/common_utils.py
Fundamental building blocks built from scratch:
- Custom Stack (LIFO)
- Custom Queue (FIFO via linked nodes, strictly O(1) enqueue/dequeue)
- Custom MergeSort (used for Kruskal's edge sorting, O(E log E) worst-case)
"""

from typing import Any, Callable, Optional, List


class StackNode:
    """Node used in custom linked-based Stack."""
    def __init__(self, value: Any, next_node: Optional['StackNode'] = None):
        self.value = value
        self.next = next_node


class Stack:
    """
    Explicit LIFO Stack implementation without using Python deque or queue modules.
    Provides O(1) push, pop, and peek.
    """
    def __init__(self):
        self._top: Optional[StackNode] = None
        self._size: int = 0

    def push(self, item: Any) -> None:
        self._top = StackNode(item, self._top)
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        assert self._top is not None
        val = self._top.value
        self._top = self._top.next
        self._size -= 1
        return val

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        assert self._top is not None
        return self._top.value

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = []
        curr = self._top
        while curr:
            items.append(repr(curr.value))
            curr = curr.next
        return f"Stack([{', '.join(items)}])"


class QueueNode:
    """Node used in custom linked-based Queue."""
    def __init__(self, value: Any):
        self.value = value
        self.next: Optional['QueueNode'] = None


class Queue:
    """
    Explicit FIFO Queue implementation without using collections.deque or queue.Queue.
    Guarantees strict O(1) enqueue and O(1) dequeue operations.
    """
    def __init__(self):
        self._head: Optional[QueueNode] = None
        self._tail: Optional[QueueNode] = None
        self._size: int = 0

    def enqueue(self, item: Any) -> None:
        new_node = QueueNode(item)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        assert self._head is not None
        val = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return val

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        assert self._head is not None
        return self._head.value

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = []
        curr = self._head
        while curr:
            items.append(repr(curr.value))
            curr = curr.next
        return f"Queue([{', '.join(items)}])"


def merge_sort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    """
    Out-of-place MergeSort implemented from first principles.
    Time Complexity: O(N log N) in all cases (best, worst, average).
    Space Complexity: O(N).
    Satisfies assignment mandate to implement own sorting without built-in sort().
    """
    if len(arr) <= 1:
        return list(arr)

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key)
    right = merge_sort(arr[mid:], key=key)

    result = []
    i = 0
    j = 0

    def get_val(x):
        return key(x) if key else x

    while i < len(left) and j < len(right):
        if get_val(left[i]) <= get_val(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result

