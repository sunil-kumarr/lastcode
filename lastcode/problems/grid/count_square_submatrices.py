from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _count_square_submatrices_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Count Square Submatrices"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Count all square submatrices that contain only 1s."
DEFAULT_INPUT = [[0,1,1],[1,1,1],[0,1,1]]
CODE_LINES = code_lines_for(_count_square_submatrices_instrumented)


def run(input_data):
    return run_grid_algorithm("_count_square_submatrices_instrumented", _count_square_submatrices_instrumented, input_data)
