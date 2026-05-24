"""
home.py — Home screen for neonodes: topic/difficulty filters, search, and problem list.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.screen import Screen
from textual.widget import Widget
from rich.text import Text

from neonodes.problems.registry import TOPICS, DIFFICULTIES, PROBLEMS
from neonodes.theme import THEMES


def format_topic(topic: str) -> str:
    """Format snake_case topics as space-separated capitalized words (e.g. DP, Binary Tree)."""
    words = topic.replace("_", " ").split()
    capitalized = []
    for w in words:
        if w.lower() == "dp":
            capitalized.append("DP")
        else:
            capitalized.append(w.capitalize())
    return " ".join(capitalized)


class HomeWidget(Widget):
    """Full-screen home widget with topic/difficulty filters and problem list."""

    can_focus = True

    class ProblemSelected(Message):
        """Emitted when the user presses Enter on an available problem."""

        def __init__(self, problem_id: str) -> None:
            super().__init__()
            self.problem_id = problem_id

    DEFAULT_CSS = """
    HomeWidget {
        width: 100%;
        height: 100%;
        padding: 0;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._search_query: str = ""
        self._mode: str = "NORMAL"  # "NORMAL" or "SEARCH"
        self._topic: str = "all"
        self._difficulty: str = "all"
        self._sort_key: str = "Name"  # Default sorting: "Name". Options: "Name", "Topic", "Difficulty"
        self._theme_name: str = "Midnight"  # Start with Midnight to match screenshot
        self._selected: int = 0
        self._scroll_offset: int = 0

    @property
    def theme(self) -> dict:
        return THEMES.get(self._theme_name, THEMES["Midnight"])

    def apply_theme(self) -> None:
        t = self.theme
        self.styles.background = t["bg"]
        self.styles.color = t["text"]
        if self.screen:
            self.screen.styles.background = t["bg"]

    def on_mount(self) -> None:
        self.focus()
        self.apply_theme()

    def _filtered_and_sorted(self) -> list[dict]:
        # 1. Filter
        result = []
        for p in PROBLEMS:
            # Search filter
            if self._search_query:
                if self._search_query.lower() not in p["title"].lower():
                    continue
            # Topic filter
            if self._topic != "all" and p["topic"] != self._topic:
                continue
            # Difficulty filter
            if self._difficulty != "all" and p["difficulty"] != self._difficulty:
                continue
            result.append(p)

        # 2. Sort
        if self._sort_key == "Name":
            result.sort(key=lambda x: x["title"].lower())
        elif self._sort_key == "Topic":
            result.sort(key=lambda x: x["topic"].lower())
        elif self._sort_key == "Difficulty":
            diff_order = {"easy": 0, "medium": 1, "hard": 2}
            result.sort(key=lambda x: diff_order.get(x["difficulty"], 3))

        return result

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_top_boxes(self, width: int, theme: dict) -> Text:
        t_border = theme["border"]
        t_text = theme["text"]
        t_blue = theme["blue"]
        t_green = theme["green"]
        t_yellow = theme["yellow"]

        # Select boxes based on terminal width to prevent wrap-around
        if width >= 77:
            display_boxes = [
                ("topic", "Topic [t]", 11, lambda: format_topic(self._topic), t_green if self._topic == "all" else t_yellow),
                ("difficulty", "Difficulty [d]", 16, lambda: self._difficulty.upper(), t_green if self._difficulty == "all" else t_yellow),
                ("sort", "Sort [s]", 13, lambda: self._sort_key + " ⬆", t_blue),
                ("theme", "Theme [c]", 11, lambda: self._theme_name, t_blue),
            ]
        elif width >= 63:
            display_boxes = [
                ("topic", "Topic [t]", 11, lambda: format_topic(self._topic), t_green if self._topic == "all" else t_yellow),
                ("difficulty", "Difficulty [d]", 16, lambda: self._difficulty.upper(), t_green if self._difficulty == "all" else t_yellow),
                ("sort", "Sort [s]", 13, lambda: self._sort_key + " ⬆", t_blue),
            ]
        elif width >= 47:
            display_boxes = [
                ("topic", "Topic [t]", 11, lambda: format_topic(self._topic), t_green if self._topic == "all" else t_yellow),
                ("difficulty", "Difficulty [d]", 16, lambda: self._difficulty.upper(), t_green if self._difficulty == "all" else t_yellow),
            ]
        else:
            display_boxes = [
                ("topic", "Topic [t]", 11, lambda: format_topic(self._topic), t_green if self._topic == "all" else t_yellow),
            ]

        fixed_w = sum(box[2] for box in display_boxes)
        num_boxes = len(display_boxes)
        # Solve for search_inner_w so that the total line width matches 'width'
        search_inner_w = max(10, width - fixed_w - 3 * num_boxes - 4)

        top_line = Text()
        search_lbl = " Search "
        search_border_r = search_inner_w + 2 - len(search_lbl)
        top_line.append("┌", style=t_border)
        top_line.append("─", style=t_border)
        top_line.append(search_lbl, style=f"bold {t_text}")
        top_line.append("─" * max(0, search_border_r - 1), style=t_border)

        for name, label, inner_w, val_func, color in display_boxes:
            top_line.append("┬", style=t_border)
            top_line.append("─", style=t_border)
            top_line.append(label, style=f"bold {t_text}")
            extra_dashes = max(0, inner_w - len(label))
            top_line.append("─" * extra_dashes, style=t_border)
            top_line.append("─", style=t_border)

        top_line.append("┐\n", style=t_border)

        mid_line = Text()
        mid_line.append("│", style=t_border)
        search_val = self._search_query
        if self._mode == "SEARCH":
            search_val += "█"
        search_disp = f" {search_val}"
        search_disp = search_disp[:search_inner_w+2].ljust(search_inner_w+2)
        mid_line.append(search_disp, style=t_text)

        for name, label, inner_w, val_func, color in display_boxes:
            mid_line.append("│", style=t_border)
            val = val_func()
            val_disp = f" {val}"
            val_disp = val_disp[:inner_w+2].ljust(inner_w+2)
            mid_line.append(val_disp, style=f"bold {color}")

        mid_line.append("│\n", style=t_border)

        bot_line = Text()
        bot_line.append("└", style=t_border)
        bot_line.append("─" * (search_inner_w + 2), style=t_border)
        for name, label, inner_w, val_func, color in display_boxes:
            bot_line.append("┴", style=t_border)
            bot_line.append("─" * (inner_w + 2), style=t_border)
        bot_line.append("┘\n", style=t_border)

        result = Text()
        result.append(top_line)
        result.append(mid_line)
        result.append(bot_line)
        return result

    def render(self) -> Text:
        result = Text()
        width = self.size.width or 80
        height = self.size.height or 24
        t = self.theme

        t_text = t["text"]
        t_dim = t["dim"]
        t_blue = t["blue"]
        t_green = t["green"]
        t_yellow = t["yellow"]
        t_red = t["red"]
        t_teal = t["teal"]
        t_sel_bg = t["sel_bg"]

        # Apply themes to screen in case size or screen state changed
        self.apply_theme()

        # 1. Top Search/Filter Boxes
        result.append(self.render_top_boxes(width, t))
        result.append("\n")

        # 2. Table Column Definition
        columns = [
            ("#", 4, lambda p, i: f"{i:2d} ", lambda p: t_dim),
            ("Name", 42, lambda p, i: p["title"], lambda p: t_text if p["available"] else t_dim),
            ("Topic", 12, lambda p, i: format_topic(p["topic"]), lambda p: t_teal),
            ("Difficulty", 12, lambda p, i: p["difficulty"], lambda p: t_red if p["difficulty"] == "hard" else (t_yellow if p["difficulty"] == "medium" else t_green)),
            ("Status", 14, lambda p, i: " • Available" if p["available"] else " • Coming Soon", lambda p: t_green if p["available"] else t_dim),
        ]

        # Calculate dynamic Name column width (accounting for 2-space gaps and left margin)
        other_w = sum(w for col, w, _, _ in columns if col != "Name")
        # 5 columns -> 4 gaps of 2 spaces = 8 spaces. Plus 2 spaces left margin = 10 spaces.
        name_w = max(20, width - other_w - 10)

        # 3. Render Table Title
        filtered = self._filtered_and_sorted()
        result.append(f"Problems ({len(filtered)}/{len(PROBLEMS)})\n", style=f"bold {t_text}")

        # 4. Render Table Header Row
        header_line = Text()
        header_line.append("  ")
        for col_idx, (col, w, _, _) in enumerate(columns):
            col_name = col
            if col == "Name" and self._sort_key == "Name":
                col_name += "▲"
            elif col == "Topic" and self._sort_key == "Topic":
                col_name += "▲"
            elif col == "Difficulty" and self._sort_key == "Difficulty":
                col_name += "▲"

            disp_w = name_w if col == "Name" else w
            header_line.append(col_name.ljust(disp_w), style=f"bold {t_text}")
            if col_idx < len(columns) - 1:
                header_line.append("  ")
        header_line.append("\n")
        result.append(header_line)

        # 5. Render Problem Rows
        if not filtered:
            result.append("\n  no problems match filters / search query\n", style=t_dim)
        else:
            # Handle scroll offsets
            sel = max(0, min(self._selected, len(filtered) - 1))
            # Dynamic height allocation
            # Top boxes (3) + Spacer (1) + Table Title (1) + Table Header (1) + Details (2) + Status (1) + Margin (4) = 13 lines reserved
            visible_rows = max(5, height - 13)

            scroll = self._scroll_offset
            if sel < scroll:
                scroll = sel
            if sel >= scroll + visible_rows:
                scroll = sel - visible_rows + 1
            self._scroll_offset = scroll

            visible = filtered[scroll: scroll + visible_rows]

            for idx_rel, problem in enumerate(visible):
                idx_abs = idx_rel + scroll
                is_sel = (idx_abs == sel)
                bg = t_sel_bg if is_sel else ""

                row_text = Text()
                if is_sel:
                    row_text.append("▶ ")
                else:
                    row_text.append("  ")

                for col_idx, (col, w, val_func, color_func) in enumerate(columns):
                    val = val_func(problem, idx_abs + 1)
                    disp_w = name_w if col == "Name" else w
                    val_str = val[:disp_w].ljust(disp_w)

                    if is_sel:
                        c = "bold #FFFFFF"
                    else:
                        c = color_func(problem)

                    row_text.append(val_str, style=c)
                    if col_idx < len(columns) - 1:
                        row_text.append("  ", style=f"on {bg}" if is_sel else "")

                if is_sel:
                    row_text.stylize(f"on {bg}")

                row_text.append("\n")
                result.append(row_text)

        # Fill in remaining empty space to keep details aligned at bottom if small dataset
        actual_rows = len(filtered[scroll: scroll + visible_rows]) if filtered else 0
        fill_lines = max(0, visible_rows - actual_rows)
        result.append("\n" * fill_lines)

        # 6. Selected Problem Details Bar
        result.append("\n")
        if filtered:
            sel_problem = filtered[max(0, min(self._selected, len(filtered) - 1))]
            title = sel_problem["title"]
            diff = sel_problem["difficulty"].upper()
            topic = format_topic(sel_problem["topic"]).upper()
            
            result.append("▶ ", style=f"bold {t_blue}")
            result.append(f"{title}  ", style=f"bold {t_text}")
            diff_color = t_green if diff == "EASY" else (t_yellow if diff == "MEDIUM" else t_red)
            result.append(f"{diff}  ", style=diff_color)
            result.append(f"{topic}", style=f"bold {t_teal}")
        result.append("\n")

        # 7. Bottom Status Bar
        status = Text()
        if self._mode == "SEARCH":
            status.append("Type to search...   ", style=t_dim)
            status.append("Esc", style=f"bold {t_yellow}")
            status.append(" or ", style=t_dim)
            status.append("Enter", style=f"bold {t_yellow}")
            status.append(" to return to navigation", style=t_dim)
        else:
            hints = [
                ("Enter", "detail"), ("/", "search"), ("t", "topic"), ("d", "difficulty"),
                ("s", "sort"), ("c", "theme"), ("r", "reset"), ("q", "quit")
            ]
            for idx, (key, label) in enumerate(hints):
                if idx > 0:
                    status.append("   ")
                status.append(key, style=f"bold {t_blue}")
                status.append(f":{label}", style=t_dim)

        result.append(status)
        return result

    # ------------------------------------------------------------------
    # Key handling
    # ------------------------------------------------------------------

    def on_key(self, event) -> None:
        filtered = self._filtered_and_sorted()
        total = len(filtered)

        if self._mode == "SEARCH":
            # Prevent default bubbling (like screen shortcuts) when typing
            event.prevent_default()
            event.stop()

            if event.key == "backspace":
                self._search_query = self._search_query[:-1]
                self._selected = 0
                self._scroll_offset = 0
                self.refresh()
            elif event.key in ("escape", "enter"):
                self._mode = "NORMAL"
                self.refresh()
            elif event.key == "space":
                self._search_query += " "
                self._selected = 0
                self._scroll_offset = 0
                self.refresh()
            elif len(event.key) == 1 and event.key.isprintable():
                self._search_query += event.key
                self._selected = 0
                self._scroll_offset = 0
                self.refresh()
            return

        # NORMAL MODE
        if event.key == "up":
            if total > 0:
                self._selected = max(0, self._selected - 1)
            self.refresh()

        elif event.key == "down":
            if total > 0:
                self._selected = min(total - 1, self._selected + 1)
            self.refresh()

        elif event.key == "slash":  # enter search mode
            self._mode = "SEARCH"
            self.refresh()

        elif event.key == "t":  # cycle Topic
            cur_idx = TOPICS.index(self._topic)
            self._topic = TOPICS[(cur_idx + 1) % len(TOPICS)]
            self._selected = 0
            self._scroll_offset = 0
            self.refresh()

        elif event.key == "d":  # cycle Difficulty
            cur_idx = DIFFICULTIES.index(self._difficulty)
            self._difficulty = DIFFICULTIES[(cur_idx + 1) % len(DIFFICULTIES)]
            self._selected = 0
            self._scroll_offset = 0
            self.refresh()

        elif event.key == "s":  # cycle Sort
            SORT_KEYS = ["Name", "Topic", "Difficulty"]
            cur_idx = SORT_KEYS.index(self._sort_key)
            self._sort_key = SORT_KEYS[(cur_idx + 1) % len(SORT_KEYS)]
            self.refresh()

        elif event.key == "c":  # cycle Theme (Color Scheme)
            names = list(THEMES.keys())
            cur_idx = names.index(self._theme_name)
            self._theme_name = names[(cur_idx + 1) % len(names)]
            self.apply_theme()
            self.refresh()

        elif event.key == "r":  # Reset filters
            self._search_query = ""
            self._topic = "all"
            self._difficulty = "all"
            self._sort_key = "Name"
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
                    self.notify(f"'{problem['title']}' is coming soon!")


# ---------------------------------------------------------------------------
# HomeScreen
# ---------------------------------------------------------------------------


class HomeScreen(Screen):
    """Home screen with problem browser."""

    CSS = "Screen { background: transparent; }"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield HomeWidget(id="home-widget")

    def on_home_widget_problem_selected(self, event: HomeWidget.ProblemSelected) -> None:
        self.app.launch_problem(event.problem_id)

    def action_quit(self) -> None:
        self.app.exit()
