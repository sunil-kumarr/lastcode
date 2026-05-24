from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_word_break_frames, code_lines_for

TITLE = "Word Break"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Determine whether a string can be segmented into dictionary words."
DEFAULT_INPUT = ("leetcode", ["leet", "code"])
CODE_LINES = code_lines_for(build_word_break_frames)


def run(input_data):
    return build_word_break_frames(input_data)
