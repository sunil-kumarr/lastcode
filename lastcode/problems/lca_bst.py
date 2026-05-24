"""Lowest Common Ancestor of a Binary Search Tree — full implementation."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Lowest Common Ancestor of BST"
CATEGORY   = "tree"
DIFFICULTY = "easy"
RENDERER   = "tree"
DESCRIPTION = (
    "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST. "
    "Input is (list, target) where target encodes p and q as p*10 + q (e.g., 26 for 2 and 6)."
)

DEFAULT_INPUT = ([4, 2, 6, 1, 3, 5, 7], 26)

CODE_LINES = [
    "def lowest_common_ancestor(root, p, q):",
    "    curr = root",
    "    while curr:",
    "        if p.val < curr.val and q.val < curr.val:",
    "            curr = curr.left",
    "        elif p.val > curr.val and q.val > curr.val:",
    "            curr = curr.right",
    "        else:",
    "            return curr",
    "    return None",
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


def _lca_bst_instrumented(root: "_TreeNode", p: "_TreeNode", q: "_TreeNode") -> _TreeNode | None:
    curr = root
    while curr:
        _viz_enter(curr.node_id, curr.val)
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run(input_data: list | tuple) -> list[dict]:
    if isinstance(input_data, tuple):
        arr, target = input_data
    else:
        arr, target = input_data, 26

    root, nodes_map = _build_tree(arr)
    if root is None or not nodes_map:
        return []

    p_val = target // 10
    q_val = target % 10

    p = None
    q = None
    for n in nodes_map.values():
        if n.val == p_val:
            p = n
        if n.val == q_val:
            q = n

    # Fallbacks if values not found
    keys = list(nodes_map.keys())
    if p is None and len(keys) > 0:
        p = nodes_map[keys[0]]
    if q is None and len(keys) > 1:
        q = nodes_map[keys[1]]
    if q is None:
        q = p

    def handle_viz_enter(locs: dict, depth: int) -> dict | None:
        node_id = locs.get("node_id")
        val = locs.get("val")
        if node_id is not None:
            return {"type": "node_visit", "node_id": node_id, "val": val, "depth": depth}
        return None

    recorder = Recorder()
    frames = recorder.record(
        "_lca_bst_instrumented",
        _lca_bst_instrumented,
        root,
        p,
        q,
        marker_fns={"_viz_enter"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enter": handle_viz_enter,
        },
    )
    return frames
