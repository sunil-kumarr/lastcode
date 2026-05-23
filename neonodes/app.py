"""
app.py — Textual App for neonodes algorithm visualizer.

Layout:
  ┌─────────────┬──────────────────┐
  │  Code Pane  │   Grid Widget    │
  │  (left)     ├──────────────────┤
  │             │  Variables Panel │
  ├─────────────┴──────────────────┤
  │  Scrubber + Input Bar          │
  └────────────────────────────────┘
"""

from __future__ import annotations

import ast
import copy
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import (
    Footer,
    Input,
    Label,
)
from rich.text import Text

from neonodes.renderers.grid import GridWidget

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


# ---------------------------------------------------------------------------
# Code Pane
# ---------------------------------------------------------------------------


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
        """Highlight the 1-based lineno (matching frame lineno)."""
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

            # Truncate long lines to prevent wrapping
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


# ---------------------------------------------------------------------------
# Legend Widget
# ---------------------------------------------------------------------------


class LegendWidget(Widget):
    """Color legend for grid cell states."""

    DEFAULT_CSS = f"""
    LegendWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: 10;
        border: solid {BORDER};
    }}
    """

    def render(self) -> Text:
        result = Text()
        result.append("  legend\n", style=f"bold {TEAL}")
        result.append("  " + "─" * 20 + "\n", style=BORDER)

        entries = [
            ("current",  COLOR_CURRENT,  "■", "currently visiting"),
            ("visited",  COLOR_VISITED,  "■", "visited / in island"),
            ("land",     "#73DACA",      "■", "land (unvisited)"),
            ("water",    "#3D4566",      "■", "water"),
            ("arrow",    "#E0AF68",      "→", "direction of travel"),
        ]
        for _, color, icon, label in entries:
            result.append(f"  {icon} ", style=f"bold {color}")
            result.append(f"{label}\n", style=TEXT)

        return result


# ---------------------------------------------------------------------------
# Variables Panel
# ---------------------------------------------------------------------------


class VariablesPanel(Widget):
    """Shows current variable state: count, r, c, dfs_depth."""

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
        self._vars: dict = {}
        self._dfs_depth: int = 0
        self._frame_type: str = ""

    def update_vars(self, frame: dict) -> None:
        self._vars = frame.get("locals", {})
        self._dfs_depth = frame.get("dfs_depth", 0)
        self._frame_type = frame.get("type", "")
        self.refresh()

    def render(self) -> Text:
        result = Text()
        result.append("  variables\n", style=f"bold {TEAL}")
        result.append("  " + "─" * 26 + "\n", style=BORDER)

        def var_line(name: str, val, style: str = TEXT) -> None:
            padded = f"  {name:<14}"
            result.append(padded, style=BLUE)
            result.append(f" = {val}\n", style=style)

        locs = self._vars

        count = locs.get("count", "—")
        var_line("count", count, style=f"bold {YELLOW}")

        r_val = locs.get("r", "—")
        c_val = locs.get("c", "—")
        var_line("r", r_val)
        var_line("c", c_val)

        rows_val = locs.get("rows", "—")
        cols_val = locs.get("cols", "—")
        var_line("rows", rows_val, style=DIM)
        var_line("cols", cols_val, style=DIM)

        depth_bar = "█" * self._dfs_depth if self._dfs_depth else "·"
        var_line("dfs_depth", f"{self._dfs_depth}  {depth_bar}", style=RED)

        result.append("\n")
        type_colors = {
            "cell_visit":   RED,
            "cell_mark":    TEAL,
            "count_update": YELLOW,
            "dfs_return":   "#C792EA",
            "line":         DIM,
        }
        ft = self._frame_type
        color = type_colors.get(ft, BORDER)
        result.append("  frame type: ", style=DIM)
        result.append(f"{ft}\n", style=f"bold {color}")

        return result


# ---------------------------------------------------------------------------
# Scrubber / bottom bar
# ---------------------------------------------------------------------------


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
            bar_filled = "█" * filled
            bar_empty = "░" * (bar_width - filled)
            result.append("[", style=BORDER)
            result.append(bar_filled, style=BLUE)
            result.append(bar_empty, style=SEL_BG)
            result.append("]", style=BORDER)

        return result


# ---------------------------------------------------------------------------
# VisualizerScreen
# ---------------------------------------------------------------------------


class VisualizerScreen(Screen):
    """Full-screen visualizer for a single algorithm problem."""

    BINDINGS: ClassVar[list[Binding]] = [
        # Normal mode
        Binding("left",   "prev_frame",   "◀ Prev",     show=True),
        Binding("right",  "next_frame",   "Next ▶",     show=True),
        Binding("space",  "toggle_play",  "Play/Pause", show=True),
        Binding("i",      "focus_input",  "Edit Input", show=True),
        Binding("q",      "quit",         "Quit",       show=True),
        Binding("h",      "prev_frame",   "Prev",       show=False),
        Binding("l",      "next_frame",   "Next",       show=False),
        # escape routes to go_home or cancel_input depending on mode
        Binding("escape", "escape_action", "Home/Cancel", show=True),
        # Input mode only
        Binding("enter",  "submit_input", "Submit",     show=True),
    ]

    _input_focused: bool = False

    CSS = f"""
    Screen {{ background: {BG}; }}

    #main-container {{
        layout: horizontal;
        height: 1fr;
    }}

    #left-panel {{
        width: 40%;
        height: 100%;
        layout: vertical;
        border: solid {BORDER};
    }}

    #right-panel {{
        width: 60%;
        height: 100%;
        layout: vertical;
    }}

    #grid-container {{
        height: 1fr;
        background: {SURFACE};
        padding: 1 2;
        overflow: auto auto;
        border: solid {BORDER};
    }}

    #info-row {{
        height: 12;
        layout: horizontal;
    }}

    #step-explanation {{
        height: 3;
        width: 100%;
        background: {BG};
        padding: 0 2;
        color: {BLUE};
        content-align: left middle;
        border: solid {BORDER};
        border-title-color: {DIM};
    }}

    #input-bar {{
        height: 5;
        background: {BG};
        border: solid {BORDER};
        layout: vertical;
        padding: 0 1;
    }}

    #input-row {{
        height: 3;
        layout: horizontal;
        align: center middle;
    }}

    #input-label {{
        width: 8;
        color: {DIM};
        padding: 0 1;
    }}

    #grid-input {{
        width: 1fr;
        background: {SURFACE};
        border: solid {BORDER};
        color: {TEXT};
    }}

    #grid-input:focus {{
        border: solid {BLUE};
    }}

    #parse-error {{
        color: {RED};
        height: 1;
        padding: 0 1;
    }}

    #bottom-bar {{
        height: 3;
        background: {BG};
        border: solid {BORDER};
        layout: vertical;
        padding: 0 1;
    }}

    Label#problem-title {{
        color: {YELLOW};
        text-style: bold;
        padding: 0 2;
        width: 100%;
        border-bottom: solid {BORDER};
    }}

    Footer {{
        background: {SURFACE};
        color: {DIM};
    }}

    Footer > .footer--key {{
        background: {SEL_BG};
        color: {BLUE};
    }}
    """

    def __init__(self, problem_module, **kwargs) -> None:
        super().__init__(**kwargs)
        self._problem = problem_module
        self._grid = copy.deepcopy(problem_module.DEFAULT_GRID)
        self._frames: list[dict] = []
        self._step: int = 0
        self._playing: bool = False
        self._play_timer: Timer | None = None
        self._cell_states: dict[tuple[int, int], str] = {}
        self._play_speed: int = 1
        self._lineno_map: dict[int, int] = {}

        self._prev_cell: tuple[int, int] | None = None
        self._current_cell: tuple[int, int] | None = None
        self._frames = self._filter_frames(problem_module.run(self._grid))

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            with Vertical(id="left-panel"):
                yield Label(
                    f"  {self._problem.TITLE}  [{self._problem.DIFFICULTY.upper()}]",
                    id="problem-title",
                )
                yield CodePane(self._problem.CODE_LINES, id="code-pane")

            with Vertical(id="right-panel"):
                with Container(id="grid-container"):
                    yield GridWidget(
                        grid=self._grid,
                        cell_states={},
                        id="grid-widget",
                    )
                with Horizontal(id="info-row"):
                    yield VariablesPanel(id="vars-panel")
                    yield LegendWidget(id="legend")

        yield Label("", id="step-explanation")

        with Container(id="input-bar"):
            with Horizontal(id="input-row"):
                yield Label("grid ▶", id="input-label")
                yield Input(
                    value=self._grid_to_str(self._grid),
                    placeholder="[[1,0,1],[0,1,0]]",
                    id="grid-input",
                )
            yield Label("", id="parse-error")

        with Container(id="bottom-bar"):
            yield ScrubberBar(id="scrubber")

        yield Footer()

    def on_mount(self) -> None:
        self._lineno_map = self._build_lineno_map()
        self._apply_frame(0)
        self.query_one("#grid-input", Input).blur()

        # Set border titles on containers
        self.query_one("#left-panel").border_title = "code"
        self.query_one("#grid-container").border_title = "visualization"
        self.query_one("#vars-panel").border_title = "variables"
        self.query_one("#legend").border_title = "legend"
        self.query_one("#step-explanation").border_title = "step explanation"
        self.query_one("#input-bar").border_title = "input"
        self.query_one("#bottom-bar").border_title = "playback"

    # ------------------------------------------------------------------
    # Frame navigation
    # ------------------------------------------------------------------

    def _apply_frame(self, step: int) -> None:
        """Apply frame at `step` index to all widgets."""
        if not self._frames:
            return

        step = max(0, min(step, len(self._frames) - 1))
        self._step = step
        frame = self._frames[step]

        self._cell_states = self._compute_cell_states(step)

        # Track prev → current cell for arrow rendering
        if frame.get("type") == "cell_visit":
            self._prev_cell = self._current_cell
            self._current_cell = (frame["r"], frame["c"])

        grid_w = self.query_one("#grid-widget", GridWidget)
        grid_w.update_grid(self._grid, self._cell_states,
                           prev_cell=self._prev_cell,
                           current_cell=self._current_cell)

        code_pane = self.query_one("#code-pane", CodePane)
        if frame.get("type") == "line":
            display_lineno = self._abs_lineno_to_display(frame["lineno"])
            code_pane.highlight_line(display_lineno)
        else:
            code_pane.highlight_line(None)

        vars_panel = self.query_one("#vars-panel", VariablesPanel)
        vars_panel.update_vars(frame)

        explanation = self.query_one("#step-explanation", Label)
        explanation.update(self._explain_frame(frame, step))

        scrubber = self.query_one("#scrubber", ScrubberBar)
        scrubber.update(step, len(self._frames), self._playing, self._play_speed)

    def _compute_cell_states(self, up_to: int) -> dict[tuple[int, int], str]:
        """Replay all frames up to `up_to`, building cell state dict."""
        states: dict[tuple[int, int], str] = {}
        for i, frame in enumerate(self._frames[: up_to + 1]):
            ft = frame.get("type")
            if ft == "cell_visit":
                r, c = frame["r"], frame["c"]
                for k in list(states.keys()):
                    if states[k] == "current":
                        states[k] = "visited"
                states[(r, c)] = "current"
            elif ft == "cell_mark":
                r, c = frame["r"], frame["c"]
                states[(r, c)] = "visited"
        return states

    def _explain_frame(self, frame: dict, step: int) -> str:
        ft = frame.get("type")
        locs = frame.get("locals", {})
        depth = frame.get("dfs_depth", 0)
        prefix = f"  [{step + 1}/{len(self._frames)}]  "

        if ft == "cell_visit":
            r, c = frame["r"], frame["c"]
            return f"{prefix}Visiting cell ({r},{c}) — checking if it's land and unvisited"
        if ft == "cell_mark":
            r, c = frame["r"], frame["c"]
            return f"{prefix}Marking ({r},{c}) as visited — won't revisit this cell"
        if ft == "count_update":
            return f"{prefix}Island fully explored — count is now {frame['count']}"
        if ft == "dfs_return":
            if depth == 0:
                return f"{prefix}DFS complete — returning from island traversal"
            return f"{prefix}Dead end — cell out of bounds, already visited, or water"
        if ft == "line":
            fn = frame.get("fn", "")
            lineno = frame.get("lineno", 0)
            display = self._abs_lineno_to_display(lineno)
            count = locs.get("count", "—")
            r_val = locs.get("r", "—")
            c_val = locs.get("c", "—")
            if display is not None and display <= 4:
                return f"{prefix}Initializing — setting up grid dimensions and count = 0"
            if fn == "dfs" and r_val != "—":
                return f"{prefix}DFS at ({r_val},{c_val}) depth={depth} — exploring neighbors"
            if r_val != "—" and c_val != "—":
                return f"{prefix}Scanning grid at ({r_val},{c_val}) — count={count}"
            return f"{prefix}Executing line {display or lineno}"
        return f"{prefix}—"

    def _build_lineno_map(self) -> dict[int, int]:
        """
        Build a mapping from absolute source line numbers of
        _count_islands_instrumented to 1-based CODE_LINES display indices.
        """
        import inspect
        import neonodes.problems.count_islands as mod
        mapping: dict[int, int] = {}
        try:
            source_lines, start_line = inspect.getsourcelines(
                mod._count_islands_instrumented
            )
        except Exception:
            return mapping

        code_display_idx = 0
        for src_offset, src_line in enumerate(source_lines):
            abs_lineno = start_line + src_offset
            stripped_src = src_line.strip()

            if not stripped_src:
                continue
            if stripped_src.startswith('"""'):
                continue

            while code_display_idx < len(self._problem.CODE_LINES):
                cl = self._problem.CODE_LINES[code_display_idx].strip()
                if cl:
                    break
                code_display_idx += 1

            if code_display_idx < len(self._problem.CODE_LINES):
                mapping[abs_lineno] = code_display_idx + 1  # 1-based
                code_display_idx += 1

        return mapping

    def _abs_lineno_to_display(self, lineno: int) -> int | None:
        """Map an absolute source lineno to a 1-based CODE_LINES display index."""
        return self._lineno_map.get(lineno)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def action_prev_frame(self) -> None:
        self._apply_frame(self._step - 1)
        if self._playing:
            self._stop_play()

    def action_next_frame(self) -> None:
        self._apply_frame(self._step + 1)
        if self._step >= len(self._frames) - 1 and self._playing:
            self._stop_play()

    def action_toggle_play(self) -> None:
        if self._playing:
            self._stop_play()
        else:
            self._start_play()

    def action_focus_input(self) -> None:
        self.query_one("#grid-input", Input).focus()

    def on_input_focus(self, event: Input.Focus) -> None:
        if event.input.id != "grid-input":
            return
        self._input_focused = True
        self.refresh_bindings()

    def on_input_blur(self, event: Input.Blur) -> None:
        if event.input.id != "grid-input":
            return
        self._input_focused = False
        self.refresh_bindings()

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        normal_only = {"prev_frame", "next_frame", "toggle_play", "focus_input", "quit"}
        input_only  = {"submit_input"}
        if self._input_focused:
            if action in normal_only:
                return False
        else:
            if action in input_only:
                return False
        return True

    def action_escape_action(self) -> None:
        if self._input_focused:
            inp = self.query_one("#grid-input", Input)
            inp.value = self._grid_to_str(self._grid)
            inp.blur()
        else:
            self.app.pop_screen()

    def action_submit_input(self) -> None:
        inp = self.query_one("#grid-input", Input)
        self._parse_and_reload(inp.value)
        inp.blur()

    def action_quit(self) -> None:
        self.app.exit()

    # ------------------------------------------------------------------
    # Play timer
    # ------------------------------------------------------------------

    def _start_play(self) -> None:
        if self._step >= len(self._frames) - 1:
            self._apply_frame(0)
        self._playing = True
        interval = 1.0 / self._play_speed
        self._play_timer = self.set_interval(interval, self._tick_play)
        scrubber = self.query_one("#scrubber", ScrubberBar)
        scrubber.update(self._step, len(self._frames), self._playing, self._play_speed)

    def _stop_play(self) -> None:
        self._playing = False
        if self._play_timer:
            self._play_timer.stop()
            self._play_timer = None
        scrubber = self.query_one("#scrubber", ScrubberBar)
        scrubber.update(self._step, len(self._frames), self._playing, self._play_speed)

    def _tick_play(self) -> None:
        if self._step >= len(self._frames) - 1:
            self._stop_play()
            return
        self._apply_frame(self._step + 1)

    # ------------------------------------------------------------------
    # Input handler
    # ------------------------------------------------------------------

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "grid-input":
            return
        self._parse_and_reload(event.value)
        event.input.blur()

    def _parse_and_reload(self, raw: str) -> None:
        error_label = self.query_one("#parse-error", Label)
        raw = raw.strip()
        try:
            parsed = ast.literal_eval(raw)
            if not isinstance(parsed, list) or not parsed:
                raise ValueError("Must be a non-empty list")
            if not isinstance(parsed[0], list):
                raise ValueError("Must be a 2D list")
            cols = len(parsed[0])
            for row in parsed:
                if not isinstance(row, list) or len(row) != cols:
                    raise ValueError("All rows must have equal length")
                for cell in row:
                    if cell not in (0, 1):
                        raise ValueError("Cells must be 0 or 1")
        except Exception as exc:
            error_label.update(f"  parse error: {exc}")
            return

        error_label.update("")
        self._grid = parsed
        self._frames = self._filter_frames(self._problem.run(self._grid))
        self._step = 0
        self._cell_states = {}
        self._prev_cell = None
        self._current_cell = None
        self._stop_play()

        self.query_one("#grid-input", Input).value = self._grid_to_str(parsed)
        self._apply_frame(0)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _filter_frames(frames: list[dict]) -> list[dict]:
        """Keep only logically meaningful frames, drop noisy line events."""
        keep_types = {"cell_visit", "cell_mark", "count_update"}
        # For line frames: keep only the first entry into each (fn, r, c) combo
        # and the outer scan loop entries (fn=_count_islands_instrumented with r,c defined)
        result = []
        seen_scan: set[tuple] = set()

        for f in frames:
            ft = f["type"]
            if ft in keep_types:
                result.append(f)
                continue
            if ft == "dfs_return":
                # Only keep returns at depth 0 (island fully done)
                if f.get("dfs_depth", 1) == 0:
                    result.append(f)
                continue
            if ft == "line":
                fn = f.get("fn", "")
                locs = f.get("locals", {})
                r, c = locs.get("r"), locs.get("c")
                # Keep outer scan: first time we see each (r, c) in the main loop
                if fn == "_count_islands_instrumented" and r is not None and c is not None:
                    key = ("scan", r, c)
                    if key not in seen_scan:
                        seen_scan.add(key)
                        result.append(f)
                # Keep dfs entry: first line of dfs for each (r, c) at each depth
                elif fn == "dfs" and r is not None and c is not None:
                    depth = f.get("dfs_depth", 0)
                    key = ("dfs", r, c, depth)
                    if key not in seen_scan:
                        seen_scan.add(key)
                        result.append(f)

        return result

    @staticmethod
    def _grid_to_str(grid: list[list[int]]) -> str:
        return "[" + ",".join("[" + ",".join(str(c) for c in row) + "]" for row in grid) + "]"


# ---------------------------------------------------------------------------
# NeonodesApp
# ---------------------------------------------------------------------------


class NeonodesApp(App):
    """Main Textual application — starts on the home screen."""

    CSS = f"Screen {{ background: {BG}; }}"

    def on_mount(self) -> None:
        from neonodes.home import HomeScreen
        self.push_screen(HomeScreen())

    def launch_problem(self, problem_id: str) -> None:
        from neonodes.problems import count_islands
        from neonodes.problems.registry import PROBLEMS

        problem_map = {"count_islands": count_islands}
        mod = problem_map.get(problem_id)
        if mod is None:
            return  # coming soon — do nothing
        self.push_screen(VisualizerScreen(problem_module=mod))
