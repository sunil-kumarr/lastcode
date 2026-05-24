from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_triangle_frames, code_lines_for

TITLE = "Triangle"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Find the minimum path sum from top to bottom of a triangle."
DEFAULT_INPUT = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
CODE_LINES = code_lines_for(build_triangle_frames)


def run(input_data):
    return build_triangle_frames(input_data)
