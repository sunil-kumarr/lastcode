from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _making_large_island_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Making A Large Island"
CATEGORY = "grid"
DIFFICULTY = "hard"
RENDERER = "grid"
DESCRIPTION = "Flip at most one 0 to 1 and return the largest island area possible."
DEFAULT_INPUT = [[1,0,1],[1,0,0],[0,1,1]]
CODE_LINES = code_lines_for(_making_large_island_instrumented)


def run(input_data):
    return run_grid_algorithm("_making_large_island_instrumented", _making_large_island_instrumented, input_data, {"dfs"})
