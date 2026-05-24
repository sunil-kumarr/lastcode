from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _unique_paths_ii_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Unique Paths II"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Count unique paths from top-left to bottom-right while avoiding blocked cells."
DEFAULT_INPUT = [[0,0,0],[0,1,0],[0,0,0]]
CODE_LINES = code_lines_for(_unique_paths_ii_instrumented)


def run(input_data):
    return run_grid_algorithm("_unique_paths_ii_instrumented", _unique_paths_ii_instrumented, input_data)
