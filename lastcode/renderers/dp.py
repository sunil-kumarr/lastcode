"""
dp.py — 2D DP Table renderer for LCS.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from lastcode.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED, BG

COLOR_CURRENT  = "#F7768E"  # coral
COLOR_VISITED  = "#9ECE6A"  # green
COLOR_COMPARE  = "#7AA2F7"  # blue
BG_CURRENT     = "#321820"
BG_VISITED     = "#253320"
BG_COMPARE     = "#1E2A3D"
BG_CELL        = "#2D3250"
COLOR_INDEX    = "#3D4566"


class DPWidget(Widget):
    DEFAULT_CSS = f"""
    DPWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 10;
    }}
    """

    def __init__(self, input_data: tuple[str, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self._s1, self._s2 = input_data
        self._dp = [[0] * (len(self._s1) + 1) for _ in range(len(self._s2) + 1)]
        self._states: dict = {}

    def update_dp(self, input_data: tuple[str, str], states: dict) -> None:
        self._s1, self._s2 = input_data
        self._states = states
        self._dp = states.get("dp", [[0] * (len(self._s1) + 1) for _ in range(len(self._s2) + 1)])
        self.refresh()

    def render(self) -> RenderResult:
        s1, s2 = self._s1, self._s2
        dp = self._dp
        states = self._states
        
        r_curr = states.get("r")
        c_curr = states.get("c")
        cell_status = states.get("cell_status", "")
        backtrack_path = states.get("backtrack_path", [])
        lcs_str = states.get("lcs_str", "")

        rows = len(s2) + 1
        cols = len(s1) + 1

        CELL_W = 5
        SEP = "─" * CELL_W
        idx_pad = "     "

        lines: list[Text] = []

        # ── Column headers (s1 characters) ──────────────────────────────
        header = Text(idx_pad + " ", style=COLOR_INDEX)
        header.append("  Ø  ", style=COLOR_INDEX)
        for c in range(1, cols):
            header.append(" ", style=COLOR_INDEX)
            header.append(f"  {s1[c-1]}  ", style=COLOR_INDEX)
        lines.append(header)

        # ── Top border ──────────────────────────────────────────────────
        top = Text(idx_pad + "┌", style=COLOR_INDEX)
        for c in range(cols):
            top.append(SEP, style=COLOR_INDEX)
            top.append("┬" if c < cols - 1 else "┐", style=COLOR_INDEX)
        lines.append(top)

        for r in range(rows):
            # ── Cell content row ────────────────────────────────────────
            row_text = Text()
            row_label = "Ø" if r == 0 else s2[r-1]
            row_text.append(f" {row_label:2}  │", style=COLOR_INDEX)
            for c in range(cols):
                val = dp[r][c]
                
                # Determine cell state
                state = "default"
                if (r, c) == (r_curr, c_curr):
                    state = cell_status or "current"
                elif (r, c) in backtrack_path:
                    state = "backtrack"
                elif r_curr is not None and c_curr is not None:
                    # Highlight comparison cells when computing (r_curr, c_curr)
                    if cell_status == "compare" and ((r, c) == (r_curr - 1, c) or (r, c) == (r, c - 1)):
                        state = "compare"
                    elif cell_status == "match" and (r, c) == (r - 1, c - 1):
                        state = "compare"

                row_text.append_text(self._render_cell(val, state))
                row_text.append("│", style=COLOR_INDEX)
            lines.append(row_text)

            # ── Row separator or bottom border ──────────────────────────
            if r < rows - 1:
                sep = Text(idx_pad + "├", style=COLOR_INDEX)
                for c in range(cols):
                    sep.append(SEP, style=COLOR_INDEX)
                    sep.append("┼" if c < cols - 1 else "┤", style=COLOR_INDEX)
            else:
                sep = Text(idx_pad + "└", style=COLOR_INDEX)
                for c in range(cols):
                    sep.append(SEP, style=COLOR_INDEX)
                    sep.append("┴" if c < cols - 1 else "┘", style=COLOR_INDEX)
            lines.append(sep)

        result = Text("\n").join(lines)
        
        # Backtrack list
        if backtrack_path:
            result.append(f"\n\n  LCS Backtrack Path: ", style=DIM)
            # Reversing path for visual flow starting from (0,0) or (m,n)
            path_str = " → ".join(f"({r},{c})" for r, c in backtrack_path)
            result.append(path_str, style=YELLOW)
            if lcs_str:
                result.append(f"\n  LCS String:         ", style=DIM)
                result.append(f"\"{lcs_str}\"", style=f"bold {COLOR_VISITED}")
                
        return result

    def _render_cell(self, val: int, state: str) -> Text:
        content = f"  {val}  "
        if state == "current":
            return Text(content, style=f"bold {COLOR_CURRENT} on {BG_CURRENT}")
        elif state == "match":
            return Text(content, style=f"bold {COLOR_VISITED} on {BG_VISITED}")
        elif state == "compare":
            return Text(content, style=f"bold {COLOR_COMPARE} on {BG_COMPARE}")
        elif state == "backtrack":
            return Text(content, style=f"bold {YELLOW} on #2D2010")
        else:
            return Text(content, style=f"{TEXT} on {BG_CELL}")


# ---------------------------------------------------------------------------
# DPRenderer
# ---------------------------------------------------------------------------


class DPRenderer:

    def make_widget(self, input_data: tuple[str, str]) -> DPWidget:
        return DPWidget(input_data=input_data, id="dp-widget")

    def update_widget(self, widget: DPWidget, input_data: tuple[str, str], frame_states: dict) -> None:
        widget.update_dp(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        dp = []
        r = None
        c = None
        cell_status = ""
        backtrack_path = []
        lcs_str = ""

        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            if ft == "dp_update":
                dp = frame.get("dp", [])
                r = frame.get("r")
                c = frame.get("c")
                cell_status = ""
            elif ft == "cell_start":
                r = frame.get("r")
                c = frame.get("c")
                cell_status = "current"
            elif ft == "cell_match":
                r = frame.get("r")
                c = frame.get("c")
                cell_status = "match"
            elif ft == "cell_compare":
                r = frame.get("r")
                c = frame.get("c")
                cell_status = "compare"
            elif ft == "backtrack":
                r = frame.get("r")
                c = frame.get("c")
                backtrack_path = list(frame.get("path", []))
                cell_status = "backtrack"
            elif ft == "lcs_done":
                lcs_str = frame.get("lcs_str", "")
                backtrack_path = list(frame.get("path", []))
                r = None
                c = None
                cell_status = ""

        return {
            "dp": dp,
            "r": r,
            "c": c,
            "cell_status": cell_status,
            "backtrack_path": backtrack_path,
            "lcs_str": lcs_str,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"dp_update", "cell_start", "cell_match", "cell_compare", "backtrack", "lcs_done", "line"}
        return [f for f in frames if f.get("type") in keep_types]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        if ft == "dp_update":
            r = frame.get("r")
            c = frame.get("c")
            if r is not None and c is not None:
                return f"{prefix}Updated cell ({r},{c}) in DP table"
            return f"{prefix}Initialized DP table with zeros"
        if ft == "cell_start":
            return f"{prefix}Computing cell ({frame.get('r')},{frame.get('c')})"
        if ft == "cell_match":
            return f"{prefix}Characters match! Value is 1 + diagonal: dp[{frame.get('r')}][{frame.get('c')}] = {frame.get('val')}"
        if ft == "cell_compare":
            return f"{prefix}No match. Value is max of top and left: dp[{frame.get('r')}][{frame.get('c')}] = {frame.get('val')}"
        if ft == "backtrack":
            return f"{prefix}Backtracking step at cell ({frame.get('r')},{frame.get('c')})"
        if ft == "lcs_done":
            return f"{prefix}Reconstructed LCS string: \"{frame.get('lcs_str')}\""
        if ft == "line":
            return f"{prefix}Running LCS algorithm..."
        return f"{prefix}—"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURRENT, "■", "current cell"),
            (COLOR_COMPARE, "■", "parent cell(s) compared"),
            (COLOR_VISITED, "■", "matching character cell"),
            (YELLOW,        "■", "backtrack path cell"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locs = frame.get("locals", {})
        r = locs.get("r", "—")
        c = locs.get("c", "—")
        s1 = locs.get("s1", "—")
        s2 = locs.get("s2", "—")
        lcs_val = locs.get("lcs_str", "—")
        
        return [
            ("s1 (cols)",  str(s1),     TEAL),
            ("s2 (rows)",  str(s2),     TEAL),
            ("r (row)",    str(r),      BLUE),
            ("c (col)",    str(c),      BLUE),
            ("LCS output", str(lcs_val), f"bold {COLOR_VISITED}"),
        ]

    def parse_input(self, raw: str) -> tuple[str, str]:
        try:
            parsed = ast.literal_eval(f"({raw})")
            if isinstance(parsed, tuple) and len(parsed) == 2 and isinstance(parsed[0], str) and isinstance(parsed[1], str):
                s1, s2 = parsed
                if len(s1) > 10 or len(s2) > 10:
                    raise ValueError("Max string length is 10 to fit screen")
                return s1, s2
        except Exception:
            pass
        raise ValueError('Expected two comma-separated strings of max length 10, e.g. "abcde", "ace"')

    def serialize_input(self, input_data: tuple[str, str]) -> str:
        s1, s2 = input_data
        return f'"{s1}", "{s2}"'
