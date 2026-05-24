from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from lastcode.theme import SURFACE, BORDER, BLUE, RED, TEAL, DIM, SEL_BG


class ScrubberBar(Widget):
    """Step counter + play controls."""

    DEFAULT_CSS = f"""
    ScrubberBar {{
        background: {SURFACE};
        height: 3;
        padding: 0 2;
        layout: horizontal;
        align: center middle;
    }}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._step = 0
        self._total = 0
        self._playing = False
        self._speed = 1

    def update(self, step: int, total: int, playing: bool, speed: int = 1) -> None:
        self._step = step
        self._total = total
        self._playing = playing
        self._speed = speed
        self.refresh()

    def render(self) -> Text:
        result = Text()

        result.append("  [◀] ", style=f"bold {BLUE}")
        if self._playing:
            result.append("[⏸] ", style=f"bold {RED}")
        else:
            result.append("[▶] ", style=f"bold {BLUE}")
        result.append("[▶] ", style=f"bold {BLUE}")

        step_display = self._step + 1 if self._total > 0 else 0
        result.append(f"  step {step_display}/{self._total}  ", style=TEAL)
        result.append(f"{self._speed}x speed  ", style=DIM)

        if self._total > 0:
            bar_width = 20
            filled = int(bar_width * self._step / max(self._total - 1, 1))
            result.append("[", style=BORDER)
            result.append("█" * filled, style=BLUE)
            result.append("░" * (bar_width - filled), style=SEL_BG)
            result.append("]", style=BORDER)

        return result
