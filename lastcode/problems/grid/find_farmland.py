from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _find_farmland_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Find All Groups of Farmland"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Find the top-left and bottom-right corners of each rectangular farmland group."
DEFAULT_INPUT = [[1,0,0],[0,1,1],[0,1,1]]
CODE_LINES = code_lines_for(_find_farmland_instrumented)


def run(input_data):
    return run_grid_algorithm("_find_farmland_instrumented", _find_farmland_instrumented, input_data)
