from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _maximal_square_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Maximal Square"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Find the area of the largest square containing only 1s."
DEFAULT_INPUT = [[1,0,1,0],[1,0,1,1],[1,1,1,1],[1,0,1,1]]
CODE_LINES = code_lines_for(_maximal_square_instrumented)


def run(input_data):
    return run_grid_algorithm("_maximal_square_instrumented", _maximal_square_instrumented, input_data)
