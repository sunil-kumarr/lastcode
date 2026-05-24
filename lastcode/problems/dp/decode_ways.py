from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_decode_ways_frames, code_lines_for

TITLE = "Decode Ways"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Count how many ways a numeric string can be decoded to letters."
DEFAULT_INPUT = "226"
CODE_LINES = code_lines_for(build_decode_ways_frames)


def run(input_data):
    return build_decode_ways_frames(input_data)
