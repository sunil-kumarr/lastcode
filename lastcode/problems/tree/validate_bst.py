"""Validate Binary Search Tree — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Validate Binary Search Tree"
CATEGORY   = "tree"
DIFFICULTY = "medium"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree, determine if it is a valid binary search tree (BST). "
    "Input is a level-order array with None for missing nodes."
)

DEFAULT_INPUT = [5, 1, 6, None, None, 7, 8]

CODE_LINES = [
    "def is_valid_bst(root):",
    "    def validate(node, low=-float('inf'), high=float('inf')):",
    "        if not node:",
    "            return True",
    "        if not (low < node.val < high):",
    "            return False",
    "        return (validate(node.left, low, node.val) and",
    "                validate(node.right, node.val, high))",
    "",
    "    return validate(root)",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    10: 10
}


# ---------------------------------------------------------------------------
# Internal tree structure
# ---------------------------------------------------------------------------


class _TreeNode:
    def __init__(self, val: int, node_id: int) -> None:
        self.val = val
        self.node_id = node_id
        self.left: "_TreeNode | None" = None
        self.right: "_TreeNode | None" = None


def _build_tree(arr: list) -> tuple["_TreeNode | None", dict[int, "_TreeNode"]]:
    """Build binary tree from level-order array. Returns (root, node_map)."""
    if not arr or arr[0] is None:
        return None, {}
    nodes: dict[int, _TreeNode] = {}
    for i, val in enumerate(arr):
        if val is not None:
            nodes[i + 1] = _TreeNode(val, i + 1)
    for node_id, node in nodes.items():
        left_id, right_id = 2 * node_id, 2 * node_id + 1
        if left_id in nodes:
            node.left = nodes[left_id]
        if right_id in nodes:
            node.right = nodes[right_id]
    return nodes.get(1), nodes


# ---------------------------------------------------------------------------
# Marker stubs
# ---------------------------------------------------------------------------


def _viz_enter(node_id: int, val: int) -> None:  # noqa: ARG001
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------


def _validate_bst_instrumented(root: "_TreeNode") -> bool:
    def validate(node: "_TreeNode | None", low: float = -float("inf"), high: float = float("inf")) -> bool:
        if not node:
            return True
        _viz_enter(node.node_id, node.val)
        if not (low < node.val < high):
            return False
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))

    res = validate(root)
    return res


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run(input_data: list) -> list[dict]:
    root, _ = _build_tree(input_data)
    if root is None:
        return []

    def handle_viz_enter(locs: dict, depth: int) -> dict | None:
        node_id = locs.get("node_id")
        val = locs.get("val")
        if node_id is not None:
            return {"type": "node_visit", "node_id": node_id, "val": val, "depth": depth}
        return None

    recorder = Recorder()
    frames = recorder.record(
        "_validate_bst_instrumented",
        _validate_bst_instrumented,
        root,
        marker_fns={"_viz_enter"},
        nested_fns={"validate"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
        },
    )
    return frames
