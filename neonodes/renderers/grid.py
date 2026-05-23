"""
grid.py — Textual Widget that renders a 2D grid with per-cell color states.

Cell states:
  'visited'  — green  (#9ECE6A)
  'current'  — red    (#F7768E)
  'start'    — yellow (#E0AF68)
  default    — dark panel bg, value determines land/water styling
"""

from __future__ import annotations

from rich.text import Text

from textual.widget import Widget
from textual.app import RenderResult


# Colour palette
COLOR_VISITED  = "#9ECE6A"   # green text
BG_VISITED     = "#1A2814"   # dark green bg
COLOR_CURRENT  = "#F7768E"   # red/coral text
BG_CURRENT     = "#2A1420"   # dark red bg
COLOR_LAND     = "#73DACA"   # teal text
BG_LAND        = "#142028"   # dark teal bg
COLOR_WATER    = "#565F89"   # muted text
BG_WATER       = "#1A1A2E"   # dark bg
COLOR_INDEX    = "#3D4566"   # dim index numbers


class GridWidget(Widget):
    """Renders a 2D grid with optional per-cell highlight states."""

    DEFAULT_CSS = """
    GridWidget {
        border: solid #3D4566;
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
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._grid = grid
        self._cell_states: dict[tuple[int, int], str] = cell_states or {}

    def update_grid(
        self,
        grid: list[list[int]],
        cell_states: dict[tuple[int, int], str],
    ) -> None:
        self._grid = grid
        self._cell_states = cell_states
        self.refresh()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> RenderResult:
        if not self._grid or not self._grid[0]:
            return Text("  (empty grid)", style="dim")

        rows = len(self._grid)
        cols = len(self._grid[0])

        lines: list[Text] = []

        # Column index header
        header = Text("     ", style=COLOR_INDEX)
        for c in range(cols):
            header.append(f" {c:2} ", style=COLOR_INDEX)
        lines.append(header)

        # Separator
        sep_len = 5 + cols * 4
        lines.append(Text("─" * sep_len, style=COLOR_INDEX))

        for r in range(rows):
            row_text = Text()
            # Row index
            row_text.append(f" {r:2} │", style=COLOR_INDEX)

            for c in range(cols):
                val = self._grid[r][c]
                state = self._cell_states.get((r, c))
                row_text.append(" ")
                row_text.append_text(self._render_cell(val, state))
                row_text.append(" ")

            lines.append(row_text)

        result = Text("\n").join(lines)
        return result

    def _render_cell(self, val: int, state: str | None) -> Text:
        label = str(val)

        if state == "current":
            return Text(f" {label} ", style=f"bold {COLOR_CURRENT} on {BG_CURRENT}")
        elif state == "visited":
            return Text(f" {label} ", style=f"bold {COLOR_VISITED} on {BG_VISITED}")
        elif val == 1:
            return Text(f" {label} ", style=f"{COLOR_LAND} on {BG_LAND}")
        else:
            return Text(f" {label} ", style=f"{COLOR_WATER} on {BG_WATER}")
