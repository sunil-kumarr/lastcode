"""Binary Tree Level Order BFS Traversal — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Binary Tree Level Order BFS"
CATEGORY   = "tree"
DIFFICULTY = "medium"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree, return the level order traversal of its nodes' values. "
    "(i.e., from left to right, level by level). "
    "Input is a level-order array with None for missing nodes."
)

DEFAULT_INPUT = [4, 2, 6, 1, 3, 5, 7]

CODE_LINES = [
    "def level_order(root):",
    "    if not root:",
    "        return []",
    "    result = []",
    "    queue = [root]",
    "    while queue:",
    "        level_size = len(queue)",
    "        current_level = []",
    "        for _ in range(level_size):",
    "            node = queue.pop(0)",
    "            current_level.append(node.val)",
    "            if node.left:",
    "                queue.append(node.left)",
    "            if node.right:",
    "                queue.append(node.right)",
    "        result.append(current_level)",
    "    return result",
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
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    18: 17
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


def _bt_level_order_instrumented(root: "_TreeNode") -> list[list[int]]:
    if not root:
        return []
    result: list[list[int]] = []
    queue: list[_TreeNode] = [root]
    while queue:
        level_size = len(queue)
        current_level: list[int] = []
        for _ in range(level_size):
            node = queue.pop(0)
            _viz_enter(node.node_id, node.val)
            current_level.append(node.val)
            _viz_append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)
    return result


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

    def handle_viz_append(locs: dict, depth: int) -> dict | None:
        val = locs.get("val")
        if val is not None:
            return {"type": "append_result", "val": val, "depth": depth}
        return None

    recorder = Recorder()
    frames = recorder.record(
        "_bt_level_order_instrumented",
        _bt_level_order_instrumented,
        root,
        marker_fns={"_viz_enter", "_viz_append"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enter": handle_viz_enter,
            "_viz_append": handle_viz_append,
        },
    )
    return frames
