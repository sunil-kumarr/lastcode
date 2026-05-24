from __future__ import annotations

from lastcode.problems.dp._dp_algorithms import build_interleaving_string_frames, code_lines_for

TITLE = "Interleaving String"
CATEGORY = "dp"
DIFFICULTY = "medium"
RENDERER = "dp"
DESCRIPTION = "Check whether a third string is formed by interleaving two other strings."
DEFAULT_INPUT = ("aabcc", "dbbca", "aadbbcbcac")
CODE_LINES = code_lines_for(build_interleaving_string_frames)


def run(input_data):
    return build_interleaving_string_frames(input_data)
