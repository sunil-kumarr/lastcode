"""Binary Tree Path Sum — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Binary Tree Path Sum"
CATEGORY   = "tree"
DIFFICULTY = "easy"
RENDERER   = "tree"
DESCRIPTION = (
    "Given the root of a binary tree and a targetSum, return true if the tree has a "
    "root-to-leaf path such that adding up all the values along the path equals targetSum. "
    "Input is a level-order array with None for missing nodes, or a (list, target) tuple."
)

DEFAULT_INPUT = ([4, 2, 6, 1, 3, 5, 7], 9)

CODE_LINES = [
    "def has_path_sum(root, targetSum):",
    "    def dfs(node, curr_sum):",
    "        if not node:",
    "            return False",
    "        curr_sum += node.val",
    "        if not node.left and not node.right:",
    "            return curr_sum == targetSum",
    "        return dfs(node.left, curr_sum) or dfs(node.right, curr_sum)",
    "",
    "    return dfs(root, 0)",
]

_LINE_MAP = {
    98: 1,
    100: 2,
    101: 3,
    102: 4,
    103: 5,
    104: 5,
    105: 5,
    106: 6,
    107: 7,
    108: 8,
    110: 10,
    111: 10
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


def _viz_sum(curr_sum: int) -> None:  # noqa: ARG001
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------


def _bt_path_sum_instrumented(root: "_TreeNode", target_sum: int) -> bool:

    def dfs(node: "_TreeNode | None", curr_sum: int) -> bool:
        if not node:
            return False
        _viz_enter(node.node_id, node.val)
        curr_sum += node.val
        _viz_sum(curr_sum)
        if not node.left and not node.right:
            return curr_sum == target_sum
        return dfs(node.left, curr_sum) or dfs(node.right, curr_sum)

    res = dfs(root, 0)
    return res


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run(input_data: list | tuple) -> list[dict]:
    if isinstance(input_data, tuple):
        arr, target = input_data
    else:
        arr, target = input_data, 9

    root, _ = _build_tree(arr)
    if root is None:
        return []

    def handle_viz_enter(locs: dict, depth: int) -> dict | None:
        node_id = locs.get("node_id")
        val = locs.get("val")
        if node_id is not None:
            return {"type": "node_visit", "node_id": node_id, "val": val, "depth": depth}
        return None

    def handle_viz_sum(locs: dict, depth: int) -> dict | None:  # noqa: ARG001
        return None

    recorder = Recorder()
    frames = recorder.record(
        "_bt_path_sum_instrumented",
        _bt_path_sum_instrumented,
        root,
        target,
        marker_fns={"_viz_enter", "_viz_sum"},
        nested_fns={"dfs"},
        marker_handlers={
            "_viz_enter": handle_viz_enter,
            "_viz_sum": handle_viz_sum,
        },
    )
    return frames
