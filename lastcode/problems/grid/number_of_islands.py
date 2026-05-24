"""
number_of_islands.py — Number of Islands II problem definition and instrumented implementation.
"""

from __future__ import annotations

import copy
from lastcode.recorder import Recorder

# ---------------------------------------------------------------------------
# Problem metadata
# ---------------------------------------------------------------------------

TITLE       = "Number of Islands II"
CATEGORY    = "grid"
DIFFICULTY  = "hard"
RENDERER    = "grid"

DESCRIPTION = (
    "You are given an empty m x n grid and a sequence of addLand operations. "
    "Each operation turns the cell at (r, c) from water into land. "
    "Return the number of islands after each addLand operation."
)

DEFAULT_INPUT = DEFAULT_GRID = [
    [1, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
]

# ---------------------------------------------------------------------------
# Source code lines shown in the code pane (1-indexed display)
# ---------------------------------------------------------------------------

CODE_LINES = [
    "def num_islands_ii(m, n, positions):",
    "    parent = {}",
    "    count = 0",
    "    grid = [[0]*n for _ in range(m)]",
    "",
    "    def find(x):",
    "        if parent[x] != x:",
    "            parent[x] = find(parent[x])",
    "        return parent[x]",
    "",
    "    def union(x, y):",
    "        rx, ry = find(x), find(y)",
    "        if rx != ry:",
    "            parent[rx] = ry",
    "            return True",
    "        return False",
    "",
    "    ans = []",
    "    for r, c in positions:",
    "        if grid[r][c] == 1:",
    "            continue",
    "        grid[r][c] = 1",
    "        parent[(r, c)] = (r, c)",
    "        count += 1",
    "        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:",
    "            nr, nc = r + dr, c + dc",
    "            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:",
    "                if union((r, c), (nr, nc)):",
    "                    count -= 1",
    "        ans.append(count)",
    "    return ans",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
    22: 22,
    23: 23,
    24: 24,
    25: 25,
    26: 26,
    27: 27,
    28: 28,
    29: 29,
    30: 30,
    31: 31,
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

def _num_islands_ii_instrumented(grid: list[list[int]]) -> list[int]:
    m, n = len(grid), len(grid[0])
    # Extract positions from cells that are final land (1s)
    positions = []
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                positions.append((r, c))

    # Reset the grid to all water (0s) to simulate growth
    for r in range(m):
        for c in range(n):
            grid[r][c] = 0

    parent = {}
    count = 0

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry
            return True
        return False

    ans = []
    for r, c in positions:
        _viz_probe(r, c)
        grid[r][c] = 1
        _viz_visit(r, c)
        parent[(r, c)] = (r, c)
        count += 1
        _viz_mark(r, c)
        _viz_count(count)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                _viz_probe(nr, nc)
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                _viz_mark(nr, nc)
                if union((r, c), (nr, nc)):
                    count -= 1
                    _viz_count(count)
            elif 0 <= nr < m and 0 <= nc < n:
                _viz_water(nr, nc)
        ans.append(count)
        _viz_complete()
    return ans


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(grid: list[list[int]]) -> list[dict]:
    """Execute num_islands_ii on grid and return a list of visualization frames."""
    recorder = Recorder()
    grid_copy = copy.deepcopy(grid)
    frames = recorder.record(
        "_num_islands_ii_instrumented",
        _num_islands_ii_instrumented,
        grid_copy,
        nested_fns={"find", "union"},
    )
    return frames
