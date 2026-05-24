from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _closed_island_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Closed Island"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Count islands of 0s that are completely surrounded by 1s and do not touch the border."
DEFAULT_INPUT = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
CODE_LINES = code_lines_for(_closed_island_instrumented)


def run(input_data):
    return run_grid_algorithm("_closed_island_instrumented", _closed_island_instrumented, input_data, {"dfs"})
