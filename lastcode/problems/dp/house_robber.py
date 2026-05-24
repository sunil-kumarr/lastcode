from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_house_robber_frames, code_lines_for

TITLE = "House Robber"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Maximize loot without robbing adjacent houses."
DEFAULT_INPUT = [2, 7, 9, 3, 1]
CODE_LINES = code_lines_for(build_house_robber_frames)


def run(input_data):
    return build_house_robber_frames(input_data)
