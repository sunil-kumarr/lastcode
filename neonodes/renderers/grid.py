"""
grid.py — Textual Widget that renders a 2D grid with per-cell color states.

Cell states:
  'visited'  — green
  'current'  — red/coral
  default    — unified dark bg, land vs water by text color only
"""

from __future__ import annotations

from rich.text import Text

from textual.widget import Widget
from textual.app import RenderResult

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

        # Compute arrow: direction from prev_cell to current_cell
        arrow_cell: tuple[int, int] | None = None
        arrow_char = "·"
        if self._prev_cell and self._current_cell:
            pr, pc = self._prev_cell
            cr, cc = self._current_cell
            delta = (cr - pr, cc - pc)
            if delta in _ARROWS:
                arrow_cell = self._prev_cell
                arrow_char = _ARROWS[delta]

        lines: list[Text] = []

        # Column index header
        header = Text("      ", style=COLOR_INDEX)
        for c in range(cols):
            header.append(f"  {c}  ", style=COLOR_INDEX)
        lines.append(header)

        lines.append(Text("─" * (6 + cols * 5), style=COLOR_INDEX))

        for r in range(rows):
            row_text = Text()
            row_text.append(f" {r:2} │ ", style=COLOR_INDEX)

            for c in range(cols):
                val = self._grid[r][c]
                state = self._cell_states.get((r, c))
                is_arrow = arrow_cell == (r, c)
                row_text.append_text(self._render_cell(val, state, is_arrow, arrow_char))
                row_text.append("  ")

            lines.append(row_text)

        return Text("\n").join(lines)

    def _render_cell(self, val: int, state: str | None, is_arrow: bool, arrow_char: str) -> Text:
        suffix = f" {arrow_char}" if is_arrow else "  "

        if state == "current":
            return Text(f" {val}{suffix}", style=f"bold {COLOR_CURRENT} on {BG_CURRENT}")
        elif state == "visited":
            return Text(f" {val}{suffix}", style=f"{COLOR_VISITED} on {BG_VISITED}")
        elif val == 1:
            return Text(f" {val}{suffix}", style=f"{COLOR_LAND} on {BG_CELL}")
        else:
            return Text(f" {val}{suffix}", style=f"{COLOR_WATER} on {BG_CELL}")
