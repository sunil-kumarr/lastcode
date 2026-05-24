"""
dp.py — Generic DP table/array renderer for dynamic programming problems.
"""

from __future__ import annotations

import ast
from typing import Any

from rich.text import Text
from textual.app import RenderResult
from textual.widget import Widget

from lastcode.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL

COLOR_CURRENT = "#F7768E"
COLOR_COMPARE = "#7AA2F7"
COLOR_SOLVED = "#9ECE6A"
COLOR_TRACE = "#E0AF68"
BG_CURRENT = "#321820"
BG_COMPARE = "#1E2A3D"
BG_SOLVED = "#253320"
BG_TRACE = "#2D2010"
BG_CELL = "#2D3250"
COLOR_INDEX = "#3D4566"


class DPWidget(Widget):
    DEFAULT_CSS = f"""
    DPWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 10;
    }}
    """

    def __init__(self, input_data: Any, **kwargs) -> None:
        super().__init__(**kwargs)
        self._states: dict[str, Any] = {}
        self._input_data = input_data

    def update_dp(self, input_data: Any, states: dict[str, Any]) -> None:
        self._input_data = input_data
        self._states = states
        self.refresh()

    def render(self) -> RenderResult:
        table = self._states.get("table")
        if table is None:
            return Text("  (no DP state yet)", style=DIM)

        matrix = self._normalize_table(table)
        row_labels = self._normalize_labels(
            self._states.get("row_labels"),
            len(matrix),
            default_prefix="r",
            row_mode=True,
        )
        col_labels = self._normalize_labels(
            self._states.get("col_labels"),
            len(matrix[0]) if matrix else 0,
            default_prefix="c",
            row_mode=False,
        )

        active_cells = set(tuple(cell) for cell in self._states.get("active_cells", []))
        compare_cells = set(tuple(cell) for cell in self._states.get("compare_cells", []))
        solved_cells = set(tuple(cell) for cell in self._states.get("solved_cells", []))
        trace_cells = set(tuple(cell) for cell in self._states.get("trace_cells", []))

        max_val_width = max(len(str(v)) for row in matrix for v in row) if matrix else 1
        max_col_width = max((len(label) for label in col_labels), default=1)
        cell_w = max(5, max_val_width + 2, max_col_width + 2)
        sep = "─" * cell_w
        row_label_w = max(4, max((len(label) for label in row_labels), default=1) + 1)
        idx_pad = " " * row_label_w

        lines: list[Text] = []

        header = Text(idx_pad + " ", style=COLOR_INDEX)
        for idx, label in enumerate(col_labels):
            header.append(f"{label:^{cell_w}}", style=f"bold {YELLOW}" if self._column_has_active(idx, active_cells) else COLOR_INDEX)
            if idx < len(col_labels) - 1:
                header.append(" ", style=COLOR_INDEX)
        lines.append(header)

        top = Text(idx_pad + "┌", style=COLOR_INDEX)
        for c in range(len(col_labels)):
            top.append(sep, style=COLOR_INDEX)
            top.append("┬" if c < len(col_labels) - 1 else "┐", style=COLOR_INDEX)
        lines.append(top)

        for r, row in enumerate(matrix):
            row_text = Text()
            row_style = f"bold {YELLOW}" if self._row_has_active(r, active_cells) else COLOR_INDEX
            row_text.append(f"{row_labels[r]:>{row_label_w}}│", style=row_style)
            for c, val in enumerate(row):
                state = self._cell_state((r, c), active_cells, compare_cells, solved_cells, trace_cells)
                row_text.append_text(self._render_cell(val, cell_w, state))
                row_text.append("│", style=COLOR_INDEX)
            lines.append(row_text)

            if r < len(matrix) - 1:
                border = Text(idx_pad + "├", style=COLOR_INDEX)
                for c in range(len(col_labels)):
                    border.append(sep, style=COLOR_INDEX)
                    border.append("┼" if c < len(col_labels) - 1 else "┤", style=COLOR_INDEX)
            else:
                border = Text(idx_pad + "└", style=COLOR_INDEX)
                for c in range(len(col_labels)):
                    border.append(sep, style=COLOR_INDEX)
                    border.append("┴" if c < len(col_labels) - 1 else "┘", style=COLOR_INDEX)
            lines.append(border)

        context_lines = self._states.get("context_lines", [])
        if context_lines:
            lines.append(Text(""))
            lines.append(Text("  dp context", style=f"bold {TEAL}"))
            lines.append(Text("  " + "─" * 28, style=COLOR_INDEX))
            for line in context_lines:
                style = f"bold {BLUE}" if line.startswith("Step") else TEXT
                lines.append(Text(f"  {line}", style=style))

        return Text("\n").join(lines)

    @staticmethod
    def _normalize_table(table: Any) -> list[list[Any]]:
        if isinstance(table, list) and table and isinstance(table[0], list):
            return table
        if isinstance(table, list):
            return [table]
        return [[table]]

    @staticmethod
    def _normalize_labels(labels: list[str] | None, size: int, default_prefix: str, row_mode: bool) -> list[str]:
        if labels is not None and len(labels) == size:
            return [str(label) for label in labels]
        if row_mode and size == 1:
            return ["dp "]
        return [f"{default_prefix}{idx}" for idx in range(size)]

    @staticmethod
    def _column_has_active(col: int, active_cells: set[tuple[int, int]]) -> bool:
        return any(c == col for _, c in active_cells)

    @staticmethod
    def _row_has_active(row: int, active_cells: set[tuple[int, int]]) -> bool:
        return any(r == row for r, _ in active_cells)

    @staticmethod
    def _cell_state(
        cell: tuple[int, int],
        active_cells: set[tuple[int, int]],
        compare_cells: set[tuple[int, int]],
        solved_cells: set[tuple[int, int]],
        trace_cells: set[tuple[int, int]],
    ) -> str:
        if cell in active_cells:
            return "current"
        if cell in trace_cells:
            return "trace"
        if cell in compare_cells:
            return "compare"
        if cell in solved_cells:
            return "solved"
        return "default"

    @staticmethod
    def _render_cell(val: Any, cell_w: int, state: str) -> Text:
        content = f"{str(val):^{cell_w}}"
        if state == "current":
            return Text(content, style=f"bold {COLOR_CURRENT} on {BG_CURRENT}")
        if state == "compare":
            return Text(content, style=f"bold {COLOR_COMPARE} on {BG_COMPARE}")
        if state == "solved":
            return Text(content, style=f"bold {COLOR_SOLVED} on {BG_SOLVED}")
        if state == "trace":
            return Text(content, style=f"bold {COLOR_TRACE} on {BG_TRACE}")
        return Text(content, style=f"{TEXT} on {BG_CELL}")


class DPRenderer:
    def make_widget(self, input_data: Any) -> DPWidget:
        return DPWidget(input_data=input_data, id="dp-widget")

    def update_widget(self, widget: DPWidget, input_data: Any, frame_states: dict[str, Any]) -> None:
        widget.update_dp(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict[str, Any]:
        state: dict[str, Any] = {
            "table": None,
            "row_labels": None,
            "col_labels": None,
            "active_cells": [],
            "compare_cells": [],
            "solved_cells": set(),
            "trace_cells": [],
            "context_lines": [],
            "result_label": "result",
            "result_value": "—",
        }

        for frame in frames[:up_to + 1]:
            state["table"] = frame.get("table", state["table"])
            state["row_labels"] = frame.get("row_labels", state["row_labels"])
            state["col_labels"] = frame.get("col_labels", state["col_labels"])
            state["active_cells"] = frame.get("active_cells", state["active_cells"])
            state["compare_cells"] = frame.get("compare_cells", state["compare_cells"])
            state["trace_cells"] = frame.get("trace_cells", state["trace_cells"])
            state["context_lines"] = self._context_lines(frame)
            state["result_label"] = frame.get("result_label", state["result_label"])
            state["result_value"] = frame.get("result_value", state["result_value"])

            for cell in frame.get("solved_cells", []):
                state["solved_cells"].add(tuple(cell))

        state["solved_cells"] = sorted(state["solved_cells"])
        return state

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        return [f for f in frames if f.get("type") != "line"]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        note = frame.get("note", "Advance DP state")
        return f"  [{step + 1}/{total}]  {note}"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURRENT, "■", "current DP state"),
            (COLOR_COMPARE, "■", "states compared"),
            (COLOR_SOLVED, "■", "computed state"),
            (COLOR_TRACE, "■", "trace/backtrack path"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        entries: list[tuple[str, str, str]] = []
        locs = frame.get("locals", {})

        if "i" in locs:
            entries.append(("i", str(locs["i"]), BLUE))
        if "j" in locs:
            entries.append(("j", str(locs["j"]), BLUE))
        if "r" in locs:
            entries.append(("r", str(locs["r"]), BLUE))
        if "c" in locs:
            entries.append(("c", str(locs["c"]), BLUE))

        result_label = frame.get("result_label", "result")
        result_value = frame.get("result_value", "—")
        entries.append((result_label, str(result_value), f"bold {GREEN}"))

        for key in ("n", "m", "amount", "target", "s", "t", "word1", "word2", "s1", "s2", "s3"):
            if key in locs:
                entries.append((key, str(locs[key]), TEAL))

        if not entries:
            entries.append(("state", "ready", DIM))
        return entries

    def parse_input(self, raw: str) -> Any:
        return ast.literal_eval(raw.strip())

    def serialize_input(self, input_data: Any) -> str:
        return repr(input_data)

    @staticmethod
    def _context_lines(frame: dict) -> list[str]:
        note = frame.get("note", "Advance DP state")
        result_label = frame.get("result_label", "result")
        result_value = frame.get("result_value", "—")
        cells = frame.get("active_cells", [])
        compare = frame.get("compare_cells", [])

        lines = [f"Step: {note}"]
        if cells:
            lines.append(f"Focus: {', '.join(str(tuple(cell)) for cell in cells)}")
        else:
            lines.append("Focus: waiting for next DP state")
        if compare:
            lines.append(f"Compare: {', '.join(str(tuple(cell)) for cell in compare)}")
        else:
            lines.append("Compare: no parent comparison on this step")
        lines.append(f"Metric: {result_label} = {result_value}")
        return lines
