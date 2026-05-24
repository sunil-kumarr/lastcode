from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from lastcode.theme import SURFACE, BORDER, DIM, BLUE, RED, TEXT, SEL_BG


class CodePane(Widget):
    """Read-only code display with highlighted current line."""

    DEFAULT_CSS = f"""
    CodePane {{
        background: {SURFACE};
        padding: 1 2;
        width: 100%;
        height: 1fr;
        overflow-y: auto;
    }}
    """

    def __init__(self, code_lines: list[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self._code_lines = code_lines
        self._highlighted_lineno: int | None = None

    def highlight_line(self, lineno: int | None) -> None:
        self._highlighted_lineno = lineno
        self.refresh()

    def render(self) -> Text:
        result = Text()
        max_len = max(1, (self.size.width or 80) - 8)

        for display_idx, line in enumerate(self._code_lines, start=1):
            is_current = (
                self._highlighted_lineno is not None
                and display_idx == self._highlighted_lineno
            )
            truncated = line[:max_len]
            line_no_text = f"{display_idx:3} "

            if is_current:
                result.append(line_no_text, style=f"bold {BLUE}")
                result.append("▶ ", style=f"bold {RED}")
                result.append(truncated + "\n", style=f"bold {TEXT} on {SEL_BG}")
            else:
                result.append(line_no_text, style=DIM)
                result.append("  ")
                stripped = line.strip()
                if stripped.startswith("#") or stripped == "":
                    result.append(truncated + "\n", style=DIM)
                elif stripped.startswith("def "):
                    result.append(truncated + "\n", style="#C792EA")
                elif stripped.startswith("return"):
                    result.append(truncated + "\n", style=RED)
                elif stripped.startswith("if ") or stripped.startswith("for "):
                    result.append(truncated + "\n", style="#89B4FA")
                else:
                    result.append(truncated + "\n", style=TEXT)

        return result
