from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _island_perimeter_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Island Perimeter"
CATEGORY = "grid"
DIFFICULTY = "easy"
RENDERER = "grid"
DESCRIPTION = "Compute the perimeter of the island in a binary grid."
DEFAULT_INPUT = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]
CODE_LINES = code_lines_for(_island_perimeter_instrumented)


def run(input_data):
    return run_grid_algorithm("_island_perimeter_instrumented", _island_perimeter_instrumented, input_data)
