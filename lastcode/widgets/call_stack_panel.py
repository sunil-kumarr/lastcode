from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from lastcode.theme import SURFACE, BORDER, TEAL, BLUE, YELLOW, TEXT, DIM, RED


class CallStackPanel(Widget):
    """Shows recursive call stack entries for tree problems."""

    DEFAULT_CSS = f"""
    CallStackPanel {{
        background: {SURFACE};
        padding: 1 2;
        height: 100%;
        width: 1fr;
        overflow-y: auto;
        border: solid {BORDER};
    }}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._entries: list[dict] = []
        self._edge_note: str = ""

    def update_entries(self, entries: list[dict], edge_note: str = "") -> None:
        self._entries = entries
        self._edge_note = edge_note
        self.refresh()

    def render(self) -> Text:
        result = Text()
        result.append("  call stack\n", style=f"bold {TEAL}")
        result.append("  " + "─" * 26 + "\n", style=BORDER)

        if self._edge_note:
            result.append("  edge ", style=BLUE)
            result.append(f"{self._edge_note}\n", style=f"bold {YELLOW}")

        if not self._entries:
            result.append("  (no recursive stack)\n", style=DIM)
            return result

        for idx, entry in enumerate(self._entries):
            prefix = "▶" if entry.get("current") else " "
            depth = entry.get("depth", idx)
            label = entry.get("label", "—")
            result.append(f"  {prefix} {depth:<2} ", style=RED if entry.get("current") else BLUE)
            result.append(f"{label}\n", style=f"bold {TEXT}" if entry.get("current") else TEXT)

        return result
