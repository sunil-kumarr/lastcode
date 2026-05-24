from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_min_cost_climbing_stairs_frames, code_lines_for

TITLE = "Min Cost Climbing Stairs"
CATEGORY = "dp"
DIFFICULTY = "easy"
RENDERER = "dp"
DESCRIPTION = "Pay the minimum total cost to reach the top of the staircase."
DEFAULT_INPUT = [10, 15, 20, 8, 9]
CODE_LINES = code_lines_for(build_min_cost_climbing_stairs_frames)


def run(input_data):
    return build_min_cost_climbing_stairs_frames(input_data)
