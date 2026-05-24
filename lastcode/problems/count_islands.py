"""
count_islands.py — Count Islands problem definition and instrumented implementation.

The algorithm uses DFS to traverse connected land cells (1s). Marker functions
_viz_visit / _viz_mark / _viz_count are called inline; the Recorder intercepts
them via sys.settrace to emit structured visualization frames.
"""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

# ---------------------------------------------------------------------------
# Problem metadata
# ---------------------------------------------------------------------------

TITLE       = "Count Islands"
CATEGORY    = "grid"
DIFFICULTY  = "medium"
RENDERER    = "grid"

DESCRIPTION = (
    "Given a 2D grid of 1s (land) and 0s (water), count the number of islands. "
    "An island is surrounded by water and is formed by connecting adjacent land "
    "cells horizontally or vertically."
)

DEFAULT_INPUT = DEFAULT_GRID = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1],
]

# ---------------------------------------------------------------------------
# Source code lines shown in the code pane (1-indexed display)
# ---------------------------------------------------------------------------

CODE_LINES = [
    "def count_islands(grid):",
    "    rows, cols = len(grid), len(grid[0])",
    "    visited = [[False]*cols for _ in range(rows)]",
    "    count = 0",
    "",
    "    def dfs(r, c):",
    "        if r < 0 or r >= rows: return",
    "        if c < 0 or c >= cols: return",
    "        if visited[r][c] or grid[r][c] == 0: return",
    "        visited[r][c] = True",
    "        dfs(r+1, c)",
    "        dfs(r-1, c)",
    "        dfs(r, c+1)",
    "        dfs(r, c-1)",
    "",
    "    for r in range(rows):",
    "        for c in range(cols):",
    "            if not visited[r][c] and grid[r][c] == 1:",
    "                dfs(r, c)",
    "                count += 1",
    "",
    "    return count",
]

_LINE_MAP = {
    1: 1,
    3: 2,
    4: 3,
    5: 4,
    7: 6,
    8: 7,
    9: 7,
    10: 8,
    11: 8,
    12: 9,
    13: 9,
    15: 10,
    17: 11,
    18: 12,
    19: 13,
    20: 14,
    22: 16,
    23: 17,
    24: 18,
    25: 19,
    26: 20,
    29: 22,
}


# ---------------------------------------------------------------------------
# Marker stubs — no-ops at runtime, intercepted by Recorder via settrace
# ---------------------------------------------------------------------------

def _viz_visit(r: int, c: int) -> None:  # noqa: ARG001
    pass


def _viz_probe(r: int, c: int) -> None:  # noqa: ARG001
    pass


def _viz_mark(r: int, c: int) -> None:  # noqa: ARG001
    pass


def _viz_water(r: int, c: int) -> None:  # noqa: ARG001
    pass


def _viz_count(count: int) -> None:  # noqa: ARG001
    pass


def _viz_complete() -> None:
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------

def _count_islands_instrumented(grid: list[list[int]]) -> int:
    """Instrumented version that calls _viz_* markers."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    count = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows:
            return
        if c < 0 or c >= cols:
            return
        _viz_probe(r, c)
        if visited[r][c]:
            _viz_mark(r, c)
            return
        if grid[r][c] == 0:
            _viz_water(r, c)
            return
        _viz_visit(r, c)
        visited[r][c] = True
        _viz_mark(r, c)
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and grid[r][c] == 1:
                dfs(r, c)
                count += 1
                _viz_count(count)
                _viz_complete()

    return count


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(grid: list[list[int]]) -> list[dict]:
    """Execute count_islands on grid and return a list of visualization frames."""
    recorder = Recorder()
    grid_copy = copy.deepcopy(grid)
    frames = recorder.record(
        "_count_islands_instrumented",
        _count_islands_instrumented,
        grid_copy,
        nested_fns={"dfs"},
    )
    return frames
