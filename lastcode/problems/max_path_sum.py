"""Binary Tree Maximum Path Sum — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Binary Tree Max Path Sum"
CATEGORY   = "tree"
DIFFICULTY = "hard"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree, return the maximum path sum of any non-empty path. "
    "A path is defined as any sequence of nodes from some starting node to any node in the tree "
    "along the parent-child connections. "
    "Input is a level-order array with None for missing nodes."
)

DEFAULT_INPUT = [1, 2, 3]

CODE_LINES = [
    "def max_path_sum(root):",
    "    max_sum = -float('inf')",
    "",
    "    def gain(node):",
    "        nonlocal max_sum",
    "        if not node:",
    "            return 0",
    "        left_gain = max(gain(node.left), 0)",
    "        right_gain = max(gain(node.right), 0)",
    "        max_sum = max(max_sum, node.val + left_gain + right_gain)",
    "        return node.val + max(left_gain, right_gain)",
    "",
    "    gain(root)",
    "    return max_sum",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    13: 13,
    14: 14
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


def _max_path_sum_instrumented(root: "_TreeNode") -> int:
    max_sum = -float("inf")

    def gain(node: "_TreeNode | None") -> int:
        nonlocal max_sum
        if not node:
            return 0
        _viz_enter(node.node_id, node.val)
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)
        max_sum = max(max_sum, node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)

    gain(root)
    return max_sum


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
        "_max_path_sum_instrumented",
        _max_path_sum_instrumented,
        root,
        marker_fns={"_viz_enter"},
        nested_fns={"gain"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
        },
    )
    return frames
