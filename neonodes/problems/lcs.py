"""Longest Common Subsequence — full implementation with visualization tracing."""

from __future__ import annotations

from neonodes.recorder import Recorder

TITLE      = "Longest Common Subsequence"
CATEGORY   = "dp"
DIFFICULTY = "medium"
RENDERER   = "dp"
DESCRIPTION = (
    "Given two strings s1 and s2, find the length of their longest common subsequence. "
    "Input must be two comma-separated strings of max length 10."
)

DEFAULT_INPUT = ("abcde", "ace")

CODE_LINES = [
    "def lcs(s1, s2):",
    "    m, n = len(s1), len(s2)",
    "    dp = [[0] * (m + 1) for _ in range(n + 1)]",
    "    for r in range(1, n + 1):",
    "        for c in range(1, m + 1):",
    "            if s2[r-1] == s1[c-1]:",
    "                dp[r][c] = dp[r-1][c-1] + 1",
    "            else:",
    "                dp[r][c] = max(dp[r-1][c], dp[r][c-1])",
    "",
    "    # Backtrack to reconstruct LCS",
    "    r, c = n, m",
    "    lcs_chars = []",
    "    while r > 0 and c > 0:",
    "        if s2[r-1] == s1[c-1]:",
    "            lcs_chars.append(s2[r-1])",
    "            r -= 1",
    "            c -= 1",
    "        elif dp[r-1][c] >= dp[r][c-1]:",
    "            r -= 1",
    "        else:",
    "            c -= 1",
    "    return ''.join(reversed(lcs_chars))",
]

_LINE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
    22: 22,
    23: 23
}


# ---------------------------------------------------------------------------
# Marker stubs
# ---------------------------------------------------------------------------

def _viz_dp_update(dp: list, r: int | None, c: int | None) -> None:  # noqa: ARG001
    pass

def _viz_cell_start(r: int, c: int) -> None:  # noqa: ARG001
    pass

def _viz_cell_match(r: int, c: int, val: int) -> None:  # noqa: ARG001
    pass

def _viz_cell_compare(r: int, c: int, val: int) -> None:  # noqa: ARG001
    pass

def _viz_backtrack(r: int, c: int, path: list) -> None:  # noqa: ARG001
    pass

def _viz_lcs_done(lcs_str: str, path: list) -> None:  # noqa: ARG001
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------

def _lcs_instrumented(s1: str, s2: str) -> str:
    m, n = len(s1), len(s2)  # s1 = cols, s2 = rows
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    _viz_dp_update(dp, None, None)

    for r in range(1, n + 1):
        for c in range(1, m + 1):
            _viz_cell_start(r, c)
            if s2[r-1] == s1[c-1]:
                dp[r][c] = dp[r-1][c-1] + 1
                _viz_cell_match(r, c, dp[r][c])
            else:
                dp[r][c] = max(dp[r-1][c], dp[r][c-1])
                _viz_cell_compare(r, c, dp[r][c])
            _viz_dp_update(dp, r, c)
            
    r, c = n, m
    path = []
    lcs_chars = []
    while r > 0 and c > 0:
        path.append((r, c))
        _viz_backtrack(r, c, list(path))
        if s2[r-1] == s1[c-1]:
            lcs_chars.append(s2[r-1])
            r -= 1
            c -= 1
        elif dp[r-1][c] >= dp[r][c-1]:
            r -= 1
        else:
            c -= 1
    path.append((r, c))
    _viz_backtrack(r, c, list(path))
    
    lcs_str = "".join(reversed(lcs_chars))
    _viz_lcs_done(lcs_str, list(path))
    return lcs_str


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(input_data: tuple[str, str]) -> list[dict]:
    s1, s2 = input_data
    dp_snapshot = [[0] * (len(s1) + 1) for _ in range(len(s2) + 1)]
    backtrack_path: list = []
    lcs_snapshot = ""

    def handle_dp_update(locs: dict, depth: int) -> dict | None:
        nonlocal dp_snapshot
        dp_val = locs.get("dp")
        if dp_val:
            import copy
            dp_snapshot = copy.deepcopy(dp_val)
        return {
            "type": "dp_update",
            "dp": dp_snapshot,
            "r": locs.get("r"),
            "c": locs.get("c"),
        }

    def handle_cell_start(locs: dict, depth: int) -> dict | None:
        return {
            "type": "cell_start",
            "r": locs.get("r"),
            "c": locs.get("c"),
            "dp": dp_snapshot,
        }

    def handle_cell_match(locs: dict, depth: int) -> dict | None:
        return {
            "type": "cell_match",
            "r": locs.get("r"),
            "c": locs.get("c"),
            "val": locs.get("val"),
            "dp": dp_snapshot,
        }

    def handle_cell_compare(locs: dict, depth: int) -> dict | None:
        return {
            "type": "cell_compare",
            "r": locs.get("r"),
            "c": locs.get("c"),
            "val": locs.get("val"),
            "dp": dp_snapshot,
        }

    def handle_backtrack(locs: dict, depth: int) -> dict | None:
        nonlocal backtrack_path
        backtrack_path = list(locs.get("path", []))
        return {
            "type": "backtrack",
            "r": locs.get("r"),
            "c": locs.get("c"),
            "path": backtrack_path,
            "dp": dp_snapshot,
        }

    def handle_lcs_done(locs: dict, depth: int) -> dict | None:
        nonlocal lcs_snapshot
        lcs_snapshot = locs.get("lcs_str", "")
        return {
            "type": "lcs_done",
            "lcs_str": lcs_snapshot,
            "path": backtrack_path,
            "dp": dp_snapshot,
        }

    recorder = Recorder()
    return recorder.record(
        "_lcs_instrumented",
        _lcs_instrumented,
        s1,
        s2,
        marker_fns={"_viz_dp_update", "_viz_cell_start", "_viz_cell_match", "_viz_cell_compare", "_viz_backtrack", "_viz_lcs_done"},
        nested_fns=set(),
        marker_handlers={
            "_viz_dp_update": handle_dp_update,
            "_viz_cell_start": handle_cell_start,
            "_viz_cell_match": handle_cell_match,
            "_viz_cell_compare": handle_cell_compare,
            "_viz_backtrack": handle_backtrack,
            "_viz_lcs_done": handle_lcs_done,
        },
    )
