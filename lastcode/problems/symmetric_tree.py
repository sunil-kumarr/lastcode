"""Symmetric Tree — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Symmetric Tree"
CATEGORY   = "tree"
DIFFICULTY = "easy"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree, check whether it is a mirror of itself "
    "(i.e., symmetric around its center). "
    "Input is a level-order array with None for missing nodes."
)

DEFAULT_INPUT = [1, 2, 2, 3, 4, 4, 3]

CODE_LINES = [
    "def is_symmetric(root):",
    "    if not root:",
    "        return True",
    "",
    "    def is_mirror(t1, t2):",
    "        if not t1 and not t2:",
    "            return True",
    "        if not t1 or not t2:",
    "            return False",
    "        return (t1.val == t2.val and",
    "                is_mirror(t1.left, t2.right) and",
    "                is_mirror(t1.right, t2.left))",
    "",
    "    return is_mirror(root.left, root.right)",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    14: 14,
    15: 14
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


def _symmetric_tree_instrumented(root: "_TreeNode") -> bool:
    if not root:
        return True

    def is_mirror(t1: "_TreeNode | None", t2: "_TreeNode | None") -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        if t1:
            _viz_enter(t1.node_id, t1.val)
        if t2:
            _viz_enter(t2.node_id, t2.val)
        return (t1.val == t2.val and
                is_mirror(t1.left, t2.right) and
                is_mirror(t1.right, t2.left))

    res = is_mirror(root.left, root.right)
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
        "_symmetric_tree_instrumented",
        _symmetric_tree_instrumented,
        root,
        marker_fns={"_viz_enter"},
        nested_fns={"is_mirror"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
        },
    )
    return frames
