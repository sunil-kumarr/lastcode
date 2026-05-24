from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_lis_frames, code_lines_for

TITLE = "Longest Increasing Subsequence"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Find the length of the longest strictly increasing subsequence."
DEFAULT_INPUT = [10, 9, 2, 5, 3, 7, 101, 18]
CODE_LINES = code_lines_for(build_lis_frames)


def run(input_data):
    return build_lis_frames(input_data)
