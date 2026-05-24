from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_house_robber_ii_frames, code_lines_for

TITLE = "House Robber II"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Maximize loot when the houses form a circle."
DEFAULT_INPUT = [2, 3, 2, 6, 1]
CODE_LINES = code_lines_for(build_house_robber_ii_frames)


def run(input_data):
    return build_house_robber_ii_frames(input_data)
