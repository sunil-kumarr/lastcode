from __future__ import annotations

from lastcode.problems.grid._grid_algorithms import _game_of_life_instrumented, code_lines_for, run_grid_algorithm

TITLE = "Game of Life"
CATEGORY = "grid"
DIFFICULTY = "medium"
RENDERER = "grid"
DESCRIPTION = "Compute the next state of Conway's Game of Life for the given board."
DEFAULT_INPUT = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]
CODE_LINES = code_lines_for(_game_of_life_instrumented)


def run(input_data):
    return run_grid_algorithm("_game_of_life_instrumented", _game_of_life_instrumented, input_data)
