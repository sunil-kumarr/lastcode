from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_edit_distance_frames, code_lines_for

TITLE = "Edit Distance"
CATEGORY = "dp"
DIFFICULTY = "hard"
RENDERER = "dp"
DESCRIPTION = "Compute the minimum edit distance between two strings."
DEFAULT_INPUT = ("horse", "ros")
CODE_LINES = code_lines_for(build_edit_distance_frames)


def run(input_data):
    return build_edit_distance_frames(input_data)
