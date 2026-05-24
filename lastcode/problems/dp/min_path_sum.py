from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_min_path_sum_frames, code_lines_for

TITLE = "Minimum Path Sum"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Find the minimum path sum from top-left to bottom-right."
DEFAULT_INPUT = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
CODE_LINES = code_lines_for(build_min_path_sum_frames)


def run(input_data):
    return build_min_path_sum_frames(input_data)
