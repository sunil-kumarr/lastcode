from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_climbing_stairs_frames, code_lines_for

TITLE = "Climbing Stairs"
CATEGORY = "dp"
DIFFICULTY = "easy"
RENDERER = "dp"
DESCRIPTION = "Count the number of distinct ways to climb to the top taking 1 or 2 steps."
DEFAULT_INPUT = 6
CODE_LINES = code_lines_for(build_climbing_stairs_frames)


def run(input_data):
    return build_climbing_stairs_frames(input_data)
