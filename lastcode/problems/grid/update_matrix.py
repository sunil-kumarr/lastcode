from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _update_matrix_instrumented, code_lines_for, run_grid_algorithm

TITLE = "01 Matrix"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "For each 1-cell, compute its distance to the nearest 0-cell."
DEFAULT_INPUT = [[0,0,0],[0,1,0],[1,1,1]]
CODE_LINES = code_lines_for(_update_matrix_instrumented)


def run(input_data):
    return run_grid_algorithm("_update_matrix_instrumented", _update_matrix_instrumented, input_data)
