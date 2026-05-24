"""
grid.py — Textual Widget that renders a 2D grid with per-cell color states.

Cell states:
  'visited'       — green
  'current'       — red/coral
  'checked_water' — blue
  default         — unified dark bg, land vs water by text color only
"""

from __future__ import annotations

import ast
from typing import Any

from rich.text import Text

from textual.widget import Widget
from textual.app import RenderResult

from lastcode.theme import YELLOW, TEXT, DIM, BLUE, TEAL

# Unified background — same for all cells
BG_CELL    = "#1E2230"

# Text/highlight colors
COLOR_VISITED  = "#9ECE6A"   # green
COLOR_CURRENT  = "#F7768E"   # coral
COLOR_WATER_SEEN = "#7AA2F7" # blue
BG_VISITED     = "#253320"   # subtle green tint
BG_CURRENT     = "#321820"   # subtle red tint
BG_WATER_SEEN  = "#1D2A42"   # subtle blue tint
COLOR_LAND     = "#73DACA"   # teal
COLOR_WATER    = "#3D4566"   # dim
COLOR_INDEX    = "#3D4566"

# Arrow characters for movement direction
_ARROWS: dict[tuple[int, int], str] = {
    (-1,  0): "↑",
    ( 1,  0): "↓",
    ( 0, -1): "←",
    ( 0,  1): "→",
}


class GridWidget(Widget):
    """Renders a 2D grid with optional per-cell highlight states and movement arrows."""

    DEFAULT_CSS = """
    GridWidget {
        background: #1E2230;
        padding: 1 2;
        height: auto;
        min-height: 10;
    }
    """

    def __init__(
        self,
        grid: list[list[int]],
        cell_states: dict[tuple[int, int], str] | None = None,
        prev_cell: tuple[int, int] | None = None,
        current_cell: tuple[int, int] | None = None,
        context_lines: list[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._grid = grid
        self._cell_states: dict[tuple[int, int], str] = cell_states or {}
        self._prev_cell = prev_cell
        self._current_cell = current_cell
        self._context_lines = context_lines or []

    def update_grid(
        self,
        grid: list[list[int]],
        cell_states: dict[tuple[int, int], str],
        prev_cell: tuple[int, int] | None = None,
        current_cell: tuple[int, int] | None = None,
        context_lines: list[str] | None = None,
    ) -> None:
        self._grid = grid
        self._cell_states = cell_states
        self._prev_cell = prev_cell
        self._current_cell = current_cell
        self._context_lines = context_lines or []
        self.refresh()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> RenderResult:
        if not self._grid or not self._grid[0]:
            return Text("  (empty grid)", style="dim")

        rows = len(self._grid)
        cols = len(self._grid[0])

        # Compute arrow direction
        arrow_cell: tuple[int, int] | None = None
        arrow_char = " "
        if self._prev_cell and self._current_cell:
            delta = (self._current_cell[0] - self._prev_cell[0],
                     self._current_cell[1] - self._prev_cell[1])
            if delta in _ARROWS:
                arrow_cell = self._prev_cell
                arrow_char = _ARROWS[delta]

        max_val_width = max(len(str(val)) for row in self._grid for val in row)
        CELL_W = max(5, max_val_width + 4)
        SEP = "─" * CELL_W
        idx_pad = "     "
        active_row = self._current_cell[0] if self._current_cell else None
        active_col = self._current_cell[1] if self._current_cell else None

        lines: list[Text] = []

        # ── Column headers ──────────────────────────────────────────────
        header = Text(idx_pad + " ", style=COLOR_INDEX)
        for c in range(cols):
            label = f"{c:^{CELL_W}}"
            header.append(label, style=f"bold {YELLOW}" if c == active_col else COLOR_INDEX)
            if c < cols - 1:
                header.append(" ", style=COLOR_INDEX)
        lines.append(header)

        pointer = Text(idx_pad + " ", style=COLOR_INDEX)
        for c in range(cols):
            marker = f"{'▼' if c == active_col else ' ':^{CELL_W}}"
            pointer.append(marker, style=f"bold {YELLOW}" if c == active_col else COLOR_INDEX)
            if c < cols - 1:
                pointer.append(" ", style=COLOR_INDEX)
        lines.append(pointer)

        # ── Top border ──────────────────────────────────────────────────
        top = Text(idx_pad + "┌", style=COLOR_INDEX)
        for c in range(cols):
            top.append(SEP, style=COLOR_INDEX)
            top.append("┬" if c < cols - 1 else "┐", style=COLOR_INDEX)
        lines.append(top)

        for r in range(rows):
            # ── Cell content row ────────────────────────────────────────
            row_text = Text()
            row_marker = "▶" if r == active_row else " "
            row_text.append(f"{row_marker}{r:>2}  │", style=f"bold {YELLOW}" if r == active_row else COLOR_INDEX)
            for c in range(cols):
                val = self._grid[r][c]
                state = "current" if self._current_cell == (r, c) else self._cell_states.get((r, c))
                is_arrow = arrow_cell == (r, c)
                arr = arrow_char if is_arrow else " "
                row_text.append_text(self._render_cell(val, state, arr))
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

        if self._context_lines:
            lines.append(Text(""))
            lines.append(Text("  grid context", style=f"bold {TEAL}"))
            lines.append(Text("  " + "─" * 28, style=COLOR_INDEX))
            for line in self._context_lines:
                style = f"bold {BLUE}" if line.startswith("Step") else TEXT
                lines.append(Text(f"  {line}", style=style))

        return Text("\n").join(lines)

    def _render_cell(self, val: int, state: str | None, arrow: str) -> Text:
        value = str(val)
        content = f" {value} {arrow} ".ljust(max(5, len(value) + 4))

        if state == "current":
            return Text(content, style=f"bold {COLOR_CURRENT} on {BG_CURRENT}")
        if state == "visited":
            return Text(content, style=f"{COLOR_VISITED} on {BG_VISITED}")
        if state == "checked_water":
            return Text(content, style=f"{COLOR_WATER_SEEN} on {BG_WATER_SEEN}")
        if val == 1:
            return Text(content, style=f"{COLOR_LAND} on {BG_CELL}")
        return Text(content, style=f"{COLOR_WATER} on {BG_CELL}")


# ---------------------------------------------------------------------------
# GridRenderer — logic layer (filter, compute, explain, variables, legend)
# ---------------------------------------------------------------------------


class GridRenderer:
    """Renderer logic for 2D grid problems."""

    def make_widget(self, input_data: list[list[int]]) -> GridWidget:
        return GridWidget(grid=input_data, cell_states={}, id="grid-widget")

    def update_widget(
        self,
        widget: GridWidget,
        input_data: list[list[int]],
        frame_states: dict,
    ) -> None:
        prev = frame_states.get("prev_cell")
        current = frame_states.get("current_cell")
        display_grid = frame_states.get("display_grid", input_data)
        context_lines = frame_states.get("context_lines", [])
        widget.update_grid(display_grid, frame_states.get("cell_states", {}),
                           prev_cell=prev, current_cell=current, context_lines=context_lines)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        """Replay frames up to index, return cell_states + prev/current cell."""
        states: dict[tuple[int, int], str] = {}
        prev_cell = None
        current_cell = None
        last_probe = None
        display_grid = None
        active_frame = frames[up_to] if frames else {}

        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            maybe_grid = self._extract_display_grid(frame)
            if maybe_grid is not None:
                display_grid = maybe_grid

            if ft in {"cell_probe", "cell_visit"}:
                r, c = frame["r"], frame["c"]
                prev_cell = last_probe
                last_probe = (r, c)
                current_cell = (r, c)
            elif ft == "cell_mark":
                r, c = frame["r"], frame["c"]
                states[(r, c)] = "visited"
                if current_cell == (r, c):
                    current_cell = None
            elif ft == "cell_water":
                r, c = frame["r"], frame["c"]
                states[(r, c)] = "checked_water"
                if current_cell == (r, c):
                    current_cell = None
            elif ft in {"count_update", "dfs_return", "traversal_complete"} and current_cell is not None:
                r, c = current_cell
                states.setdefault((r, c), "visited" if display_grid and display_grid[r][c] == 1 else "checked_water")
                current_cell = None

        return {
            "cell_states": states,
            "prev_cell": prev_cell,
            "current_cell": current_cell,
            "display_grid": display_grid,
            "context_lines": self._context_lines_for_frame(active_frame, current_cell, prev_cell),
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"cell_probe", "cell_visit", "cell_mark", "cell_water", "count_update", "traversal_complete"}
        result = []

        for f in frames:
            ft = f["type"]
            if ft in keep_types:
                result.append(f)
                continue
            if ft == "dfs_return":
                if f.get("dfs_depth", 1) == 0:
                    result.append(f)

        return result

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        locs = frame.get("locals", {})
        depth = frame.get("dfs_depth", 0)
        prefix = f"  [{step + 1}/{total}]  "

        if ft == "cell_visit":
            r, c = frame["r"], frame["c"]
            return f"{prefix}Visiting cell ({r},{c}) — checking if it's land and unvisited"
        if ft == "cell_probe":
            r, c = frame["r"], frame["c"]
            value = self._cell_value_from_frame(frame, r, c)
            return f"{prefix}Inspecting cell ({r},{c}) with value {value}"
        if ft == "cell_mark":
            r, c = frame["r"], frame["c"]
            return f"{prefix}Cell ({r},{c}) is part of the active solution path"
        if ft == "cell_water":
            r, c = frame["r"], frame["c"]
            value = self._cell_value_from_frame(frame, r, c)
            return f"{prefix}Cell ({r},{c}) stops traversal here — value {value} is not usable"
        if ft == "count_update":
            return f"{prefix}Primary metric updated — value is now {frame['count']}"
        if ft == "traversal_complete":
            return f"{prefix}Current traversal step is complete — state has settled"
        if ft == "dfs_return":
            if depth == 0:
                return f"{prefix}Recursive exploration is complete for this branch"
            return f"{prefix}Returning from a recursive branch"
        if ft == "line":
            fn = frame.get("fn", "")
            r_val = locs.get("r", "—")
            c_val = locs.get("c", "—")
            count = locs.get("count", "—")
            if fn == "dfs" and r_val != "—":
                return f"{prefix}DFS at ({r_val},{c_val}) depth={depth} — exploring neighbors"
            if r_val != "—" and c_val != "—":
                return f"{prefix}Scanning grid at ({r_val},{c_val}) — current metric={count}"
            return f"{prefix}Initializing grid state and traversal metadata"
        return f"{prefix}—"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass  # cell tracking is handled inside compute_states

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            ("#F7768E", "■", "currently visiting"),
            ("#9ECE6A", "■", "visited / in island"),
            ("#7AA2F7", "■", "checked water / blocked"),
            ("#73DACA", "■", "land (unvisited)"),
            ("#3D4566", "■", "water"),
            (YELLOW,    "→", "direction of travel"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locs = frame.get("locals", {})
        depth = frame.get("dfs_depth", 0)
        depth_bar = "█" * depth if depth else "·"
        entries: list[tuple[str, str, str]] = []

        active_row = locs.get("r", locs.get("row", "—"))
        active_col = locs.get("c", locs.get("col", "—"))
        next_row = locs.get("nr", "—")
        next_col = locs.get("nc", "—")
        rows = locs.get("rows", locs.get("m", "—"))
        cols = locs.get("cols", locs.get("n", "—"))
        count = locs.get("count", locs.get("result", locs.get("best", "—")))

        entries.append(("active cell", f"({active_row}, {active_col})", TEXT))
        if next_row != "—" and next_col != "—":
            entries.append(("neighbor cell", f"({next_row}, {next_col})", TEXT))
        entries.append(("grid size", f"{rows} x {cols}", DIM))
        entries.append(("result/count", str(count), f"bold {YELLOW}"))

        current_value = self._cell_value_from_frame(frame, locs.get("r"), locs.get("c"))
        if current_value != "—":
            entries.append(("cell value", str(current_value), TEXT))

        for label, key in (
            ("current area", "area"),
            ("best area", "max_area"),
            ("best score", "best"),
            ("distance", "dist"),
            ("steps", "steps"),
            ("perimeter", "perimeter"),
            ("paths", "paths"),
            ("queue size", "queue"),
            ("frontier size", "q"),
            ("answers", "ans"),
        ):
            if key not in locs:
                continue
            value = locs[key]
            if key in {"queue", "q"} and hasattr(value, "__len__"):
                value = len(value)
            entries.append((label, str(value), TEXT))

        entries.append(("call depth", f"{depth}  {depth_bar}", "#F7768E"))
        return entries

    def parse_input(self, raw: str) -> list[list[int]]:
        parsed = ast.literal_eval(raw.strip())
        if not isinstance(parsed, list) or not parsed:
            raise ValueError("Must be a non-empty list")
        if not isinstance(parsed[0], list):
            raise ValueError("Must be a 2D list")
        cols = len(parsed[0])
        for row in parsed:
            if not isinstance(row, list) or len(row) != cols:
                raise ValueError("All rows must have equal length")
            for cell in row:
                if not isinstance(cell, int):
                    raise ValueError("Cells must be integers")
        return parsed

    def serialize_input(self, input_data: list[list[int]]) -> str:
        return "[" + ",".join(
            "[" + ",".join(str(c) for c in row) + "]"
            for row in input_data
        ) + "]"

    @staticmethod
    def _extract_display_grid(frame: dict) -> list[list[int]] | None:
        locs = frame.get("locals", {})
        for key in ("grid", "board", "mat", "matrix", "rooms"):
            value = locs.get(key)
            if (
                isinstance(value, list)
                and value
                and isinstance(value[0], list)
            ):
                return value
        return None

    def _cell_value_from_frame(self, frame: dict, r: Any, c: Any) -> Any:
        if not isinstance(r, int) or not isinstance(c, int):
            return "—"
        grid = self._extract_display_grid(frame)
        if grid is None:
            return "—"
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            return grid[r][c]
        return "—"

    def _context_lines_for_frame(
        self,
        frame: dict,
        current_cell: tuple[int, int] | None,
        prev_cell: tuple[int, int] | None,
    ) -> list[str]:
        locs = frame.get("locals", {})
        ft = frame.get("type", "line")
        focus = current_cell
        if focus is None:
            r = locs.get("r")
            c = locs.get("c")
            if isinstance(r, int) and isinstance(c, int):
                focus = (r, c)

        movement = "idle"
        if prev_cell and focus and prev_cell != focus:
            dr = focus[0] - prev_cell[0]
            dc = focus[1] - prev_cell[1]
            movement = _ARROWS.get((dr, dc), "jump")

        lines = [f"Step: {self._step_label(ft, locs)}"]
        if focus is not None:
            value = self._cell_value_from_frame(frame, focus[0], focus[1])
            lines.append(f"Focus: r={focus[0]}, c={focus[1]}, value={value}")
        else:
            lines.append("Focus: waiting for the next active row/column pointer")

        if prev_cell and focus:
            lines.append(f"Move: {prev_cell} -> {focus} ({movement})")
        else:
            lines.append("Move: starting point or settled frame")

        count = locs.get("count", locs.get("max_area", locs.get("best", locs.get("steps", locs.get("perimeter", "—")))))
        lines.append(f"Metric: {count}")
        return lines

    @staticmethod
    def _step_label(ft: str, locs: dict) -> str:
        labels = {
            "cell_probe": "Inspect current cell before deciding",
            "cell_visit": "Enter a traversable cell",
            "cell_mark": "Lock this cell into the solution state",
            "cell_water": "Reject this cell and stop this branch",
            "count_update": "Update the main answer/metric",
            "dfs_return": "Return from the current recursive branch",
            "traversal_complete": "Finish this island or traversal phase",
            "line": "Advance algorithm control flow",
        }
        if ft == "line" and "r" in locs and "c" in locs:
            return "Advance the outer scan across the grid"
        return labels.get(ft, "Advance algorithm state")
