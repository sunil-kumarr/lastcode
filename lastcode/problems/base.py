"""Protocol defining the interface every problem module must satisfy."""

from __future__ import annotations
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProblemModule(Protocol):
    TITLE: str
    CATEGORY: str
    DIFFICULTY: str
    DESCRIPTION: str
    DEFAULT_INPUT: Any   # grid, tree node, array, etc.
    CODE_LINES: list[str]
    RENDERER: str        # "grid" | "tree" | "array" | "sliding_window" | "two_pointer" | "stack" | "queue" | "linked_list"

    def run(self, input_data: Any) -> list[dict]: ...


class ListNode:
    def __init__(self, val: int = 0, next_node: ListNode | None = None, random_node: ListNode | None = None) -> None:
        self.val = val
        self.next = next_node
        self.random = random_node
        self.node_id = id(self)

    def __repr__(self) -> str:
        return f"Node({self.val})"

