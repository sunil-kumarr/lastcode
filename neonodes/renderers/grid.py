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
