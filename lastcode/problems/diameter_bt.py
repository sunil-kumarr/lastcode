"""Diameter of Binary Tree — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Diameter of Binary Tree"
CATEGORY   = "tree"
DIFFICULTY = "medium"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree, return the length of the diameter of the tree. "
    "The diameter is the length of the longest path between any two nodes. "
    "Input is a level-order array with None for missing nodes."
)

DEFAULT_INPUT = [4, 2, 6, 1, 3, 5, 7]

CODE_LINES = [
    "def diameter_of_binary_tree(root):",
    "    diameter = 0",
    "",
    "    def max_depth(node):",
    "        nonlocal diameter",
    "        if not node:",
    "            return 0",
    "",
    "        left = max_depth(node.left)",
    "        right = max_depth(node.right)",
    "        diameter = max(diameter, left + right)",
    "        return 1 + max(left, right)",
    "",
    "    max_depth(root)",
    "    return diameter",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    14: 14,
    15: 15
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


def _diameter_bt_instrumented(root: "_TreeNode") -> int:
    diameter = 0

    def max_depth(node: "_TreeNode | None") -> int:
        nonlocal diameter
        if not node:
            return 0
        _viz_enter(node.node_id, node.val)
        left = max_depth(node.left)
        right = max_depth(node.right)
        diameter = max(diameter, left + right)
        return 1 + max(left, right)

    max_depth(root)
    return diameter


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
        "_diameter_bt_instrumented",
        _diameter_bt_instrumented,
        root,
        marker_fns={"_viz_enter"},
        nested_fns={"max_depth"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
        },
    )
    return frames
