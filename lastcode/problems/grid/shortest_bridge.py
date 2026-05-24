from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _shortest_bridge_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Shortest Bridge"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Flip the fewest 0s needed to connect two islands."
DEFAULT_INPUT = [[0,1,0],[0,0,0],[0,0,1]]
CODE_LINES = code_lines_for(_shortest_bridge_instrumented)


def run(input_data):
    return run_grid_algorithm("_shortest_bridge_instrumented", _shortest_bridge_instrumented, input_data, {"dfs"})
