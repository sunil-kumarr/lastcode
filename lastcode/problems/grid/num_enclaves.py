from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _num_enclaves_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Number of Enclaves"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Count land cells that cannot reach the boundary of the grid."
DEFAULT_INPUT = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
CODE_LINES = code_lines_for(_num_enclaves_instrumented)


def run(input_data):
    return run_grid_algorithm("_num_enclaves_instrumented", _num_enclaves_instrumented, input_data, {"dfs"})
