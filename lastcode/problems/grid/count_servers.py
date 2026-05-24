from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _count_servers_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Count Servers That Communicate"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Count servers that can communicate with another server in the same row or column."
DEFAULT_INPUT = [[1,0,1],[0,1,0],[1,0,1]]
CODE_LINES = code_lines_for(_count_servers_instrumented)


def run(input_data):
    return run_grid_algorithm("_count_servers_instrumented", _count_servers_instrumented, input_data)
