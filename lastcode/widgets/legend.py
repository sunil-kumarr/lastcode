from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from lastcode.theme import SURFACE, BORDER, TEAL, TEXT


class LegendWidget(Widget):
    """Color legend driven by renderer-provided entries."""

    DEFAULT_CSS = f"""
    LegendWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: 100%;
        width: 1fr;
        border: solid {BORDER};
    }}
    """

    def __init__(self, entries: list[tuple[str, str, str]], **kwargs) -> None:
        super().__init__(**kwargs)
        self._entries = entries  # (color, icon, label)

    def render(self) -> Text:
        result = Text()
        result.append("  legend\n", style=f"bold {TEAL}")
        result.append("  " + "─" * 20 + "\n", style=BORDER)

        for color, icon, label in self._entries:
            result.append(f"  {icon} ", style=f"bold {color}")
            result.append(f"{label}\n", style=TEXT)

        return result
