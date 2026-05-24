from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_partition_equal_subset_sum_frames, code_lines_for

TITLE = "Partition Equal Subset Sum"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Decide whether the array can be split into two subsets with equal sum."
DEFAULT_INPUT = [1, 5, 11, 5]
CODE_LINES = code_lines_for(build_partition_equal_subset_sum_frames)


def run(input_data):
    return build_partition_equal_subset_sum_frames(input_data)
