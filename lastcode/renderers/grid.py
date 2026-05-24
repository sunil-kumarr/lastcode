"""
grid.py — Textual Widget that renders a 2D grid with per-cell color states.

Cell states:
  'visited'  — green
  'current'  — red/coral
  default    — unified dark bg, land vs water by text color only
"""

from __future__ import annotations

import ast
from typing import Any

from rich.text import Text

from textual.widget import Widget
from textual.app import RenderResult

from lastcode.theme import YELLOW, TEXT, DIM

# Unified background — same for all cells
BG_CELL    = "#1E2230"

# Text/highlight colors
COLOR_VISITED  = "#9ECE6A"   # green
COLOR_CURRENT  = "#F7768E"   # coral
BG_VISITED     = "#253320"   # subtle green tint
BG_CURRENT     = "#321820"   # subtle red tint
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
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._grid = grid
        self._cell_states: dict[tuple[int, int], str] = cell_states or {}
        self._prev_cell = prev_cell
        self._current_cell = current_cell

    def update_grid(
        self,
        grid: list[list[int]],
        cell_states: dict[tuple[int, int], str],
        prev_cell: tuple[int, int] | None = None,
        current_cell: tuple[int, int] | None = None,
    ) -> None:
        self._grid = grid
        self._cell_states = cell_states
        self._prev_cell = prev_cell
        self._current_cell = current_cell
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

        CELL_W = 5   # inner width of each cell (chars)
        SEP = "─" * CELL_W
        idx_pad = "     "   # 5 chars to align with row-index prefix

        lines: list[Text] = []

        # ── Column headers ──────────────────────────────────────────────
        header = Text(idx_pad + " ", style=COLOR_INDEX)
        for c in range(cols):
            header.append(f"  {c}  ", style=COLOR_INDEX)
            if c < cols - 1:
                header.append(" ", style=COLOR_INDEX)
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
            row_text.append(f" {r:2}  │", style=COLOR_INDEX)
            for c in range(cols):
                val = self._grid[r][c]
                state = self._cell_states.get((r, c))
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

        return Text("\n").join(lines)

    def _render_cell(self, val: int, state: str | None, arrow: str) -> Text:
        # Each cell: " V A " = space, value, space, arrow, space  (5 chars)
        content = f" {val} {arrow} "

        if state == "current":
            return Text(content, style=f"bold {COLOR_CURRENT} on {BG_CURRENT}")
        elif state == "visited":
            return Text(content, style=f"{COLOR_VISITED} on {BG_VISITED}")
        elif val == 1:
            return Text(content, style=f"{COLOR_LAND} on {BG_CELL}")
        else:
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
        widget.update_grid(input_data, frame_states.get("cell_states", {}),
                           prev_cell=prev, current_cell=current)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        """Replay frames up to index, return cell_states + prev/current cell."""
        states: dict[tuple[int, int], str] = {}
        prev_cell = None
        current_cell = None

        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            if ft == "cell_visit":
                r, c = frame["r"], frame["c"]
                for k in list(states):
                    if states[k] == "current":
                        states[k] = "visited"
                prev_cell = current_cell
                current_cell = (r, c)
                states[(r, c)] = "current"
            elif ft == "cell_mark":
                r, c = frame["r"], frame["c"]
                states[(r, c)] = "visited"

        return {
            "cell_states": states,
            "prev_cell": prev_cell,
            "current_cell": current_cell,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"cell_visit", "cell_mark", "count_update"}
        result = []
        seen: set[tuple] = set()

        for f in frames:
            ft = f["type"]
            if ft in keep_types:
                result.append(f)
                continue
            if ft == "dfs_return":
                if f.get("dfs_depth", 1) == 0:
                    result.append(f)
                continue
            if ft == "line":
                fn = f.get("fn", "")
                locs = f.get("locals", {})
                r, c = locs.get("r"), locs.get("c")
                if fn != "dfs" and r is not None and c is not None:
                    key = ("scan", r, c)
                    if key not in seen:
                        seen.add(key)
                        result.append(f)
                elif fn == "dfs" and r is not None and c is not None:
                    depth = f.get("dfs_depth", 0)
                    key = ("dfs", r, c, depth)
                    if key not in seen:
                        seen.add(key)
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
        if ft == "cell_mark":
            r, c = frame["r"], frame["c"]
            return f"{prefix}Marking ({r},{c}) as visited — won't revisit this cell"
        if ft == "count_update":
            return f"{prefix}Island fully explored — count is now {frame['count']}"
        if ft == "dfs_return":
            if depth == 0:
                return f"{prefix}DFS complete — returning from island traversal"
            return f"{prefix}Dead end — cell out of bounds, already visited, or water"
        if ft == "line":
            fn = frame.get("fn", "")
            r_val = locs.get("r", "—")
            c_val = locs.get("c", "—")
            count = locs.get("count", "—")
            if fn == "dfs" and r_val != "—":
                return f"{prefix}DFS at ({r_val},{c_val}) depth={depth} — exploring neighbors"
            if r_val != "—" and c_val != "—":
                return f"{prefix}Scanning grid at ({r_val},{c_val}) — count={count}"
            return f"{prefix}Initializing — setting up grid dimensions and count = 0"
        return f"{prefix}—"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass  # cell tracking is handled inside compute_states

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            ("#F7768E", "■", "currently visiting"),
            ("#9ECE6A", "■", "visited / in island"),
            ("#73DACA", "■", "land (unvisited)"),
            ("#3D4566", "■", "water"),
            (YELLOW,    "→", "direction of travel"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locs = frame.get("locals", {})
        depth = frame.get("dfs_depth", 0)
        depth_bar = "█" * depth if depth else "·"

        return [
            ("count",     str(locs.get("count", "—")), f"bold {YELLOW}"),
            ("r",         str(locs.get("r", "—")),     TEXT),
            ("c",         str(locs.get("c", "—")),     TEXT),
            ("rows",      str(locs.get("rows", "—")),  DIM),
            ("cols",      str(locs.get("cols", "—")),  DIM),
            ("dfs_depth", f"{depth}  {depth_bar}",     "#F7768E"),
        ]

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
                if cell not in (0, 1):
                    raise ValueError("Cells must be 0 or 1")
        return parsed

    def serialize_input(self, input_data: list[list[int]]) -> str:
        return "[" + ",".join(
            "[" + ",".join(str(c) for c in row) + "]"
            for row in input_data
        ) + "]"
