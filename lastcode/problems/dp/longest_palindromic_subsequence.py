from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_lps_frames, code_lines_for

TITLE = "Longest Palindromic Subsequence"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Find the length of the longest palindromic subsequence."
DEFAULT_INPUT = "bbbab"
CODE_LINES = code_lines_for(build_lps_frames)


def run(input_data):
    return build_lps_frames(input_data)
