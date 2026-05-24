"""Valid Parentheses — stack-based with visualization."""

from __future__ import annotations

from lastcode.recorder import Recorder

TITLE      = "Valid Parentheses"
CATEGORY   = "string"
DIFFICULTY = "easy"
RENDERER   = "array"
DESCRIPTION = (
    "Given a string of brackets, determine if the brackets are valid. "
    "Each open bracket must close in the correct order."
)

DEFAULT_INPUT = "()[]{}"

CODE_LINES = [
    "def is_valid(s):",
    "    stack = []",
    "    pairs = {')':'(', ']':'[', '}':'{'}",
    "    for char in s:",
    "        if char in '([{':",
    "            stack.append(char)",
    "        elif char in ')]}':",
    "            if not stack or stack[-1] != pairs[char]:",
    "                return False",
    "            stack.pop()",
    "    return len(stack) == 0",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    6: 5,
    7: 6,
    9: 7,
    10: 8,
    12: 9,
    13: 10,
    15: 11
}


def _viz_scan(char: str, idx: int) -> None:  # noqa: ARG001
    pass


def _viz_push(char: str, idx: int) -> None:  # noqa: ARG001
    pass


def _viz_pop(char: str, idx: int) -> None:  # noqa: ARG001
    pass


def _viz_mismatch(char: str, idx: int) -> None:  # noqa: ARG001
    pass


def _is_valid_instrumented(s: str) -> bool:
    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for idx, char in enumerate(s):
        _viz_scan(char, idx)
        if char in "([{":
            stack.append(char)
            _viz_push(char, idx)
        elif char in ")]}":
            if not stack or stack[-1] != pairs[char]:
                _viz_mismatch(char, idx)
                return False
            stack.pop()
            _viz_pop(char, idx)
    return len(stack) == 0


def run(input_data: str) -> list[dict]:
    stack_snapshot: list[str] = []

    def handle_scan(locs: dict, depth: int) -> dict | None:
        return {
            "type": "scan_char",
            "char": locs.get("char"),
            "idx":  locs.get("idx"),
            "stack": list(stack_snapshot),
        }

    def handle_push(locs: dict, depth: int) -> dict | None:
        stack_snapshot.append(locs.get("char", ""))
        return {
            "type": "push_char",
            "char": locs.get("char"),
            "idx":  locs.get("idx"),
            "stack": list(stack_snapshot),
        }

    def handle_pop(locs: dict, depth: int) -> dict | None:
        if stack_snapshot:
            stack_snapshot.pop()
        return {
            "type": "pop_char",
            "char": locs.get("char"),
            "idx":  locs.get("idx"),
            "stack": list(stack_snapshot),
        }

    def handle_mismatch(locs: dict, depth: int) -> dict | None:
        return {
            "type": "mismatch",
            "char": locs.get("char"),
            "idx":  locs.get("idx"),
            "stack": list(stack_snapshot),
        }

    recorder = Recorder()
    return recorder.record(
        "_is_valid_instrumented",
        _is_valid_instrumented,
        input_data,
        marker_fns={"_viz_scan", "_viz_push", "_viz_pop", "_viz_mismatch"},
        nested_fns=set(),
        marker_handlers={
            "_viz_scan":     handle_scan,
            "_viz_push":     handle_push,
            "_viz_pop":      handle_pop,
            "_viz_mismatch": handle_mismatch,
        },
    )
