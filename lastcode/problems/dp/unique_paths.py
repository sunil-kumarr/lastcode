from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_unique_paths_frames, code_lines_for

TITLE = "Unique Paths"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Count how many ways exist to move from top-left to bottom-right in an empty grid."
DEFAULT_INPUT = (3, 7)
CODE_LINES = code_lines_for(build_unique_paths_frames)


def run(input_data):
    return build_unique_paths_frames(input_data)
