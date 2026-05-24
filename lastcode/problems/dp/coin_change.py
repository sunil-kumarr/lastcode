from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_coin_change_frames, code_lines_for

TITLE = "Coin Change"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Return the minimum number of coins needed to make up a target amount."
DEFAULT_INPUT = ([1, 2, 5], 11)
CODE_LINES = code_lines_for(build_coin_change_frames)


def run(input_data):
    return build_coin_change_frames(input_data)
