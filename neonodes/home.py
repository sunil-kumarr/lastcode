"""
home.py — Home screen for neonodes: topic/difficulty filters + problem list.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.screen import Screen
from textual.widget import Widget
from rich.text import Text

from neonodes.problems.registry import TOPICS, DIFFICULTIES, PROBLEMS

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

BG      = "#252836"
SURFACE = "#1E2230"
BORDER  = "#3D4566"
TEXT    = "#C0CAE4"
DIM     = "#565F89"
BLUE    = "#7AA2F7"
GREEN   = "#9ECE6A"
YELLOW  = "#E0AF68"
RED     = "#F7768E"
TEAL    = "#73DACA"
SEL_BG  = "#2D3250"

DIFF_COLORS = {
    "easy":   GREEN,
    "medium": YELLOW,
    "hard":   RED,
}


# ---------------------------------------------------------------------------
# HomeWidget
# ---------------------------------------------------------------------------


class HomeWidget(Widget):
    """Full-screen home widget with topic/difficulty filters and problem list."""

    can_focus = True

    VISIBLE_ROWS = 8  # max rows before scrolling

    class ProblemSelected(Message):
        """Emitted when the user presses Enter on an available problem."""

        def __init__(self, problem_id: str) -> None:
            super().__init__()
            self.problem_id = problem_id

    DEFAULT_CSS = f"""
    HomeWidget {{
        background: {BG};
        width: 100%;
        height: 100%;
        padding: 0;
    }}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._topic: str = "all"
        self._difficulty: str = "all"
        self._selected: int = 0
        self._scroll_offset: int = 0

    def on_mount(self) -> None:
        self.focus()

    def _filtered(self) -> list[dict]:
        result = []
        for p in PROBLEMS:
            if self._topic != "all" and p["topic"] != self._topic:
                continue
            if self._difficulty != "all" and p["difficulty"] != self._difficulty:
                continue
            result.append(p)
        return result

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> Text:
        result = Text()
        width = self.size.width or 80

        # --- Header ---
        result.append("\n\n")
        title = "neonodes"
        result.append(title.center(width) + "\n", style=f"bold {BLUE}")
        subtitle = "algorithm visualizer"
        result.append(subtitle.center(width) + "\n", style=DIM)
        result.append("\n")

        # --- Divider ---
        result.append("  " + "─" * (width - 4) + "\n", style=BORDER)
        result.append("\n")

        # --- Topic filter ---
        result.append("  topic      ", style=DIM)
        for t in TOPICS:
            if t == self._topic:
                result.append(f" {t} ", style=f"bold {BLUE} on {SEL_BG}")
            else:
                result.append(f" {t} ", style=DIM)
            result.append(" ")
        result.append("\n")

        # --- Difficulty filter ---
        result.append("  difficulty ", style=DIM)
        for d in DIFFICULTIES:
            if d == self._difficulty:
                active_color = DIFF_COLORS.get(d, BLUE)
                result.append(f" {d} ", style=f"bold {active_color} on {SEL_BG}")
            else:
                result.append(f" {d} ", style=DIM)
            result.append(" ")
        result.append("\n")

        result.append("\n")

        # --- Divider ---
        result.append("  " + "─" * (width - 4) + "\n", style=BORDER)
        result.append("\n")

        # --- Problem list ---
        filtered = self._filtered()
        if not filtered:
            result.append("  no problems match the current filters\n", style=DIM)
        else:
            # Clamp selected index
            sel = max(0, min(self._selected, len(filtered) - 1))
            visible_rows = self.VISIBLE_ROWS
            scroll = self._scroll_offset

            # Ensure selected is visible
            if sel < scroll:
                scroll = sel
            if sel >= scroll + visible_rows:
                scroll = sel - visible_rows + 1
            self._scroll_offset = scroll

            visible = filtered[scroll: scroll + visible_rows]

            for idx_rel, problem in enumerate(visible):
                idx_abs = idx_rel + scroll
                is_selected = (idx_abs == sel)
                available = problem.get("available", False)

                diff = problem["difficulty"]
                diff_color = DIFF_COLORS.get(diff, TEXT)
                topic_str = f"{problem['topic']:<8}"
                diff_str = f"{diff:<8}"
                title_str = f"{problem['title']:<36}"

                if is_selected:
                    # Selected row
                    result.append("  ", style=f"on {SEL_BG}")
                    result.append("▶  ", style=f"bold {BLUE} on {SEL_BG}")
                    if available:
                        result.append(title_str, style=f"bold {TEXT} on {SEL_BG}")
                    else:
                        result.append(title_str + "· · · ", style=f"{DIM} on {SEL_BG}")
                    result.append(f"  {topic_str}", style=f"{TEAL} on {SEL_BG}")
                    result.append(f"  {diff_str}", style=f"{diff_color} on {SEL_BG}")
                    result.append("\n")
                else:
                    result.append("     ")
                    if available:
                        result.append(title_str, style=TEXT)
                    else:
                        result.append(title_str + "· · · ", style=DIM)
                    result.append(f"  {topic_str}", style=TEAL)
                    result.append(f"  {diff_str}", style=diff_color)
                    result.append("\n")

        result.append("\n")

        # --- Divider ---
        result.append("  " + "─" * (width - 4) + "\n", style=BORDER)

        # --- Key hints ---
        hints = [
            ("[↑↓]", "navigate"),
            ("[t]",   "topic"),
            ("[d]",   "difficulty"),
            ("[enter]", "launch"),
            ("[q]",   "quit"),
        ]
        result.append("  ")
        for key, label in hints:
            result.append(key, style=f"bold {BLUE}")
            result.append(f" {label}  ", style=DIM)
        result.append("\n")

        return result

    # ------------------------------------------------------------------
    # Key handling
    # ------------------------------------------------------------------

    def on_key(self, event) -> None:
        filtered = self._filtered()
        total = len(filtered)

        if event.key == "up":
            if total > 0:
                self._selected = max(0, self._selected - 1)
            self.refresh()

        elif event.key == "down":
            if total > 0:
                self._selected = min(total - 1, self._selected + 1)
            self.refresh()

        elif event.key == "t":
            cur_idx = TOPICS.index(self._topic)
            self._topic = TOPICS[(cur_idx + 1) % len(TOPICS)]
            self._selected = 0
            self._scroll_offset = 0
            self.refresh()

        elif event.key == "d":
            cur_idx = DIFFICULTIES.index(self._difficulty)
            self._difficulty = DIFFICULTIES[(cur_idx + 1) % len(DIFFICULTIES)]
            self._selected = 0
            self._scroll_offset = 0
            self.refresh()

        elif event.key == "enter":
            if total > 0:
                sel = max(0, min(self._selected, total - 1))
                problem = filtered[sel]
                if problem.get("available", False):
                    self.post_message(HomeWidget.ProblemSelected(problem["id"]))
                else:
                    # Coming soon — stay, just refresh (no navigation)
                    self.refresh()


# ---------------------------------------------------------------------------
# HomeScreen
# ---------------------------------------------------------------------------


class HomeScreen(Screen):
    """Home screen with problem browser."""

    CSS = f"Screen {{ background: {BG}; }}"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield HomeWidget(id="home-widget")

    def on_home_widget_problem_selected(self, event: HomeWidget.ProblemSelected) -> None:
        self.app.launch_problem(event.problem_id)

    def action_quit(self) -> None:
        self.app.exit()
