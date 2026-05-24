from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_lcs_frames, code_lines_for

TITLE = "Longest Common Subsequence"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Compute the length of the longest common subsequence between two strings."
DEFAULT_INPUT = ("abcde", "ace")
CODE_LINES = code_lines_for(build_lcs_frames)


def run(input_data):
    return build_lcs_frames(input_data)
