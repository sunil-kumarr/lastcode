from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from lastcode.theme import SURFACE, BORDER, TEAL, BLUE, TEXT, DIM


class VariablesPanel(Widget):
    """Shows current variable state driven by renderer-provided entries."""

    DEFAULT_CSS = f"""
    VariablesPanel {{
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
        self._entries: list[tuple[str, str, str]] = []  # (name, value, color)

    def update_entries(self, entries: list[tuple[str, str, str]]) -> None:
        self._entries = entries
        self.refresh()

    def render(self) -> Text:
        result = Text()
        result.append("  variables\n", style=f"bold {TEAL}")
        result.append("  " + "─" * 26 + "\n", style=BORDER)

        for name, value, color in self._entries:
            result.append(f"  {name:<14}", style=BLUE)
            result.append(f" = {value}\n", style=color or TEXT)

        return result
