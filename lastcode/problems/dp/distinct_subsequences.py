from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_distinct_subsequences_frames, code_lines_for

TITLE = "Distinct Subsequences"
CATEGORY = "dp"
DIFFICULTY = "hard"
RENDERER = "dp"
DESCRIPTION = "Count how many distinct subsequences of s equal t."
DEFAULT_INPUT = ("rabbbit", "rabbit")
CODE_LINES = code_lines_for(build_distinct_subsequences_frames)


def run(input_data):
    return build_distinct_subsequences_frames(input_data)
