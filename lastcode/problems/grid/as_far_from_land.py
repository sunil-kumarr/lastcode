from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _as_far_from_land_instrumented, code_lines_for, run_grid_algorithm

TITLE = "As Far from Land as Possible"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Return the water cell whose distance to the nearest land cell is maximal."
DEFAULT_INPUT = [[1,0,1],[0,0,0],[1,0,1]]
CODE_LINES = code_lines_for(_as_far_from_land_instrumented)


def run(input_data):
    return run_grid_algorithm("_as_far_from_land_instrumented", _as_far_from_land_instrumented, input_data)
