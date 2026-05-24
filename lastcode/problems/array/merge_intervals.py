"""Merge Intervals — full implementation with visualization tracing."""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

TITLE      = "Merge Intervals"
CATEGORY   = "array"
DIFFICULTY = "medium"
RENDERER   = "array"
DESCRIPTION = (
    "Given an array of intervals where intervals[i] = [start, end], "
    "merge all overlapping intervals, and return an array of the non-overlapping intervals."
)

DEFAULT_INPUT = [[1, 3], [2, 6], [8, 10], [15, 18]]

CODE_LINES = [
    "def merge(intervals):",
    "    if not intervals:",
    "        return []",
    "    intervals.sort(key=lambda x: x[0])",
    "    merged = [intervals[0]]",
    "    for i in range(1, len(intervals)):",
    "        curr = intervals[i]",
    "        last = merged[-1]",
    "        if curr[0] <= last[1]:",
    "            last[1] = max(last[1], curr[1])",
    "        else:",
    "            merged.append(curr)",
    "    return merged",
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
    13: 13
}


# ---------------------------------------------------------------------------
# Marker stubs
# ---------------------------------------------------------------------------

def _viz_init(intervals: list) -> None:  # noqa: ARG001
    pass

def _viz_compare(i: int, curr: list, last: list, merged: list) -> None:  # noqa: ARG001
    pass

def _viz_merge(i: int, curr: list, last: list, merged: list) -> None:  # noqa: ARG001
    pass

def _viz_add(i: int, curr: list, merged: list) -> None:  # noqa: ARG001
    pass

def _viz_done(merged: list) -> None:  # noqa: ARG001
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------

def _merge_intervals_instrumented(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    intervals_sorted = sorted(intervals, key=lambda x: x[0])
    _viz_init(intervals_sorted)
    
    merged = [copy.deepcopy(intervals_sorted[0])]
    _viz_add(0, intervals_sorted[0], copy.deepcopy(merged))
    
    for i in range(1, len(intervals_sorted)):
        curr = intervals_sorted[i]
        last = merged[-1]
        _viz_compare(i, curr, last, copy.deepcopy(merged))
        
        if curr[0] <= last[1]:
            last[1] = max(last[1], curr[1])
            _viz_merge(i, curr, last, copy.deepcopy(merged))
        else:
            merged.append(copy.deepcopy(curr))
            _viz_add(i, curr, copy.deepcopy(merged))
            
    _viz_done(copy.deepcopy(merged))
    return merged


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(input_data: list[list[int]]) -> list[dict]:
    intervals_snapshot: list = []
    merged_snapshot: list = []

    def handle_init(locs: dict, depth: int) -> dict | None:
        nonlocal intervals_snapshot
        intervals_snapshot = locs.get("intervals_sorted", [])
        return {
            "type": "init",
            "intervals": copy.deepcopy(intervals_snapshot),
            "merged": [],
        }

    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {
            "type": "compare",
            "i": locs.get("i"),
            "curr": locs.get("curr"),
            "last": locs.get("last"),
            "intervals": copy.deepcopy(intervals_snapshot),
            "merged": locs.get("merged", []),
        }

    def handle_merge(locs: dict, depth: int) -> dict | None:
        return {
            "type": "merge",
            "i": locs.get("i"),
            "curr": locs.get("curr"),
            "last": locs.get("last"),
            "intervals": copy.deepcopy(intervals_snapshot),
            "merged": locs.get("merged", []),
        }

    def handle_add(locs: dict, depth: int) -> dict | None:
        return {
            "type": "add",
            "i": locs.get("i"),
            "curr": locs.get("curr"),
            "intervals": copy.deepcopy(intervals_snapshot),
            "merged": locs.get("merged", []),
        }

    def handle_done(locs: dict, depth: int) -> dict | None:
        return {
            "type": "done",
            "intervals": copy.deepcopy(intervals_snapshot),
            "merged": locs.get("merged", []),
        }

    recorder = Recorder()
    return recorder.record(
        "_merge_intervals_instrumented",
        _merge_intervals_instrumented,
        input_data,
        marker_fns={"_viz_init", "_viz_compare", "_viz_merge", "_viz_add", "_viz_done"},
        nested_fns=set(),
        marker_handlers={
            "_viz_init": handle_init,
            "_viz_compare": handle_compare,
            "_viz_merge": handle_merge,
            "_viz_add": handle_add,
            "_viz_done": handle_done,
        },
    )
