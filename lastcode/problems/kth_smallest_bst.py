"""Kth Smallest Element in a BST — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Kth Smallest Element in BST"
CATEGORY   = "tree"
DIFFICULTY = "medium"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary search tree, and an integer k, return the kth smallest "
    "value (1-indexed) of all the values of the nodes in the tree. "
    "Input is a (list, k) tuple."
)

DEFAULT_INPUT = ([4, 2, 6, 1, 3, 5, 7], 3)

CODE_LINES = [
    "def kth_smallest(root, k):",
    "    res = None",
    "",
    "    def traverse(node):",
    "        nonlocal k, res",
    "        if not node or res is not None:",
    "            return",
    "        traverse(node.left)",
    "        if res is not None: return",
    "        k -= 1",
    "        if k == 0:",
    "            res = node.val",
    "            return",
    "        traverse(node.right)",
    "",
    "    traverse(root)",
    "    return res",
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
    12: 12,
    13: 13,
    14: 14,
    16: 16,
    17: 17
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


def _viz_append(val: int) -> None:  # noqa: ARG001
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------


def _kth_smallest_bst_instrumented(root: "_TreeNode", k: int) -> int:
    res = None

    def traverse(node: "_TreeNode | None") -> None:
        nonlocal k, res
        if not node or res is not None:
            return
        traverse(node.left)
        if res is not None:
            return
        _viz_enter(node.node_id, node.val)
        k -= 1
        if k == 0:
            res = node.val
            _viz_append(node.val)
            return
        traverse(node.right)

    traverse(root)
    return res


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run(input_data: list | tuple) -> list[dict]:
    if isinstance(input_data, tuple):
        arr, k = input_data
    else:
        arr, k = input_data, 3

    root, _ = _build_tree(arr)
    if root is None:
        return []

    def handle_viz_enter(locs: dict, depth: int) -> dict | None:
        node_id = locs.get("node_id")
        val = locs.get("val")
        if node_id is not None:
            return {"type": "node_visit", "node_id": node_id, "val": val, "depth": depth}
        return None

    def handle_viz_append(locs: dict, depth: int) -> dict | None:
        val = locs.get("val")
        if val is not None:
            return {"type": "append_result", "val": val, "depth": depth}
        return None

    recorder = Recorder()
    frames = recorder.record(
        "_kth_smallest_bst_instrumented",
        _kth_smallest_bst_instrumented,
        root,
        k,
        marker_fns={"_viz_enter", "_viz_append"},
        nested_fns={"traverse"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
            "_viz_append": handle_viz_append,
        },
    )
    return frames
