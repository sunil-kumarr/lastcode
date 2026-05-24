"""Two Sum — brute-force O(n²) with visualization."""

from __future__ import annotations

from lastcode.recorder import Recorder

TITLE      = "Two Sum"
CATEGORY   = "array"
DIFFICULTY = "easy"
RENDERER   = "array"
DESCRIPTION = (
    "Given an array of integers and a target, return indices of the two numbers "
    "that add up to target."
)

DEFAULT_INPUT = ([2, 7, 11, 15], 9)

CODE_LINES = [
    "def two_sum(nums, target):",
    "    for i in range(len(nums)):",
    "        for j in range(i+1, len(nums)):",
    "            if nums[i] + nums[j] == target:",
    "                return [i, j]",
    "    return []",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    6: 4,
    8: 5,
    9: 6
}


def _viz_compare(i: int, j: int, s: int) -> None:  # noqa: ARG001
    pass


def _viz_found(i: int, j: int) -> None:  # noqa: ARG001
    pass


def _two_sum_instrumented(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            s = nums[i] + nums[j]
            _viz_compare(i, j, s)
            if s == target:
                _viz_found(i, j)
                return [i, j]
    return []


def run(input_data: tuple) -> list[dict]:
    nums, target = input_data

    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {
            "type": "pair_check",
            "i": locs.get("i"),
            "j": locs.get("j"),
            "sum": locs.get("s"),
            "target": target,
        }

    def handle_found(locs: dict, depth: int) -> dict | None:
        return {
            "type": "pair_found",
            "i": locs.get("i"),
            "j": locs.get("j"),
            "target": target,
        }

    recorder = Recorder()
    return recorder.record(
        "_two_sum_instrumented",
        _two_sum_instrumented,
        nums,
        target,
        marker_fns={"_viz_compare", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_found":   handle_found,
        },
    )
