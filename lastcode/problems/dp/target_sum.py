from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_target_sum_frames, code_lines_for

TITLE = "Target Sum"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Assign plus or minus signs to reach the target sum."
DEFAULT_INPUT = ([1, 1, 1, 1, 1], 3)
CODE_LINES = code_lines_for(build_target_sum_frames)


def run(input_data):
    return build_target_sum_frames(input_data)
