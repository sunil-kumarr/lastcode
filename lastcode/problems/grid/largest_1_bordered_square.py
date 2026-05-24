from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _largest_1_bordered_square_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Largest 1-Bordered Square"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Return the area of the largest square whose border is entirely 1s."
DEFAULT_INPUT = [[1,1,1],[1,0,1],[1,1,1]]
CODE_LINES = code_lines_for(_largest_1_bordered_square_instrumented)


def run(input_data):
    return run_grid_algorithm("_largest_1_bordered_square_instrumented", _largest_1_bordered_square_instrumented, input_data)
