from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _max_area_island_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Max Area of Island"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Return the size of the largest 4-directionally connected island in a binary grid."
DEFAULT_INPUT = [[0,0,1,0,0],[1,1,1,0,1],[0,1,0,0,1],[0,0,0,1,1]]
CODE_LINES = code_lines_for(_max_area_island_instrumented)


def run(input_data):
    return run_grid_algorithm("_max_area_island_instrumented", _max_area_island_instrumented, input_data, {"dfs"})
