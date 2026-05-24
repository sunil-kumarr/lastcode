from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_coin_change_ii_frames, code_lines_for

TITLE = "Coin Change II"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Count how many combinations of coins produce a target amount."
DEFAULT_INPUT = (5, [1, 2, 5])
CODE_LINES = code_lines_for(build_coin_change_ii_frames)


def run(input_data):
    return build_coin_change_ii_frames(input_data)
