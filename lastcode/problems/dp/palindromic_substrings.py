from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_palindromic_substrings_frames, code_lines_for

TITLE = "Palindromic Substrings"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Count all palindromic substrings in the string."
DEFAULT_INPUT = "aaa"
CODE_LINES = code_lines_for(build_palindromic_substrings_frames)


def run(input_data):
    return build_palindromic_substrings_frames(input_data)
