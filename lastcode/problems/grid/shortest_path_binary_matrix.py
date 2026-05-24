from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _shortest_path_binary_matrix_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Shortest Path in Binary Matrix"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Find the shortest 8-direction path from the top-left to the bottom-right through zero-valued cells."
DEFAULT_INPUT = [[0,1,0],[0,0,0],[1,0,0]]
CODE_LINES = code_lines_for(_shortest_path_binary_matrix_instrumented)


def run(input_data):
    return run_grid_algorithm("_shortest_path_binary_matrix_instrumented", _shortest_path_binary_matrix_instrumented, input_data)
