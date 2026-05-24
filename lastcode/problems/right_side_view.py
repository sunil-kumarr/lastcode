"""Binary Tree Right Side View — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Binary Tree Right Side View"
CATEGORY   = "tree"
DIFFICULTY = "medium"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree, imagine yourself standing on the right side of it, "
    "return the values of the nodes you can see ordered from top to bottom. "
    "Input is a level-order array with None for missing nodes."
)

DEFAULT_INPUT = [1, 2, 3, None, 5, None, 4]

CODE_LINES = [
    "def right_side_view(root):",
    "    result = []",
    "",
    "    def dfs(node, depth):",
    "        if not node:",
    "            return",
    "        if depth == len(result):",
    "            result.append(node.val)",
    "        dfs(node.right, depth + 1)",
    "        dfs(node.left, depth + 1)",
    "",
    "    dfs(root, 0)",
    "    return result",
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
    12: 12,
    13: 13
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


def _right_side_view_instrumented(root: "_TreeNode") -> list[int]:
    result: list[int] = []

    def dfs(node: "_TreeNode | None", depth: int) -> None:
        if not node:
            return
        _viz_enter(node.node_id, node.val)
        if depth == len(result):
            result.append(node.val)
            _viz_append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
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
        "_right_side_view_instrumented",
        _right_side_view_instrumented,
        root,
        marker_fns={"_viz_enter", "_viz_append"},
        nested_fns={"dfs"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
            "_viz_append": handle_viz_append,
        },
    )
    return frames
