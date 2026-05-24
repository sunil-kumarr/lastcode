"""app.py — VisualizerScreen + lastcodeApp."""

from __future__ import annotations

import copy
import importlib
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Footer, Input, Label, Static

from lastcode.theme import BG, SURFACE, BORDER, TEXT, DIM, BLUE, YELLOW, RED, SEL_BG
from lastcode.widgets import CodePane, ScrubberBar, VariablesPanel, LegendWidget, CallStackPanel
from lastcode.renderers.grid import GridWidget


def _load_renderer(renderer_name: str):
    """Instantiate a renderer by dotted class path from RENDERER_MAP."""
    from lastcode.problems.registry import RENDERER_MAP
    dotted = RENDERER_MAP.get(renderer_name)
    if not dotted:
        raise ValueError(f"Unknown renderer: {renderer_name!r}")
    module_path, cls_name = dotted.rsplit(".", 1)
    mod = importlib.import_module(module_path)
    return getattr(mod, cls_name)()


def _load_problem(problem_id: str):
    """Import a problem module by id from PROBLEM_MAP."""
    from lastcode.problems.registry import PROBLEM_MAP
    dotted = PROBLEM_MAP.get(problem_id)
    if not dotted:
        raise ValueError(f"Unknown problem: {problem_id!r}")
    return importlib.import_module(dotted)


# ---------------------------------------------------------------------------
# VisualizerScreen
# ---------------------------------------------------------------------------


class VisualizerScreen(Screen):
    """Full-screen visualizer — renderer-agnostic."""

    AUTO_FOCUS = ""

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("left",   "prev_frame",    "◀ Prev",      show=True),
        Binding("right",  "next_frame",    "Next ▶",      show=True),
        Binding("space",  "toggle_play",   "Play/Pause",  show=True),
        Binding("minus",  "zoom_out",      "Zoom Out",    show=True),
        Binding("+", "zoom_in",      "Zoom In", show=True),
        Binding("equal",  "zoom_in",       "Zoom In",     show=False),
        Binding("0",      "zoom_reset",    "Reset Zoom",  show=True),
        Binding("tab",    "toggle_tab",    "Toggle View", show=True),
        Binding("i",      "focus_input",   "Edit Input",  show=True),
        Binding("q",      "quit",          "Quit",        show=True),
        Binding("escape", "escape_action", "Home/Cancel", show=True),
        Binding("h",      "prev_frame",    "Prev",        show=False),
        Binding("l",      "next_frame",    "Next",        show=False),
        Binding("enter",  "submit_input",  "Submit",      show=True),
    ]

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

    #problem-panel {{
        height: 16;
        background: {SURFACE};
        border: solid {BORDER};
        layout: vertical;
    }}

    #solution-panel {{
        height: 1fr;
        background: {SURFACE};
        border: solid {BORDER};
        layout: vertical;
    }}

    #problem-desc {{
        padding: 1 2;
        overflow-y: auto;
        height: 1fr;
        color: {TEXT};
        background: {SURFACE};
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
        height: 20;
        layout: horizontal;
    }}

    #zoom-controls {{
        height: 1;
        color: {DIM};
        padding: 0 2;
    }}

    #legend {{
        width: 1fr;
        height: 100%;
    }}

    #call-stack-panel {{
        width: 1fr;
        height: 100%;
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
        height: 6;
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
        height: 3;
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
        self._renderer = _load_renderer(getattr(problem_module, "RENDERER", "grid"))

        input_data = copy.deepcopy(
            getattr(problem_module, "DEFAULT_INPUT",
                    getattr(problem_module, "DEFAULT_GRID", None))
        )
        self._input_data = input_data
        self._frames: list[dict] = []
        self._step: int = 0
        self._playing: bool = False
        self._play_timer: Timer | None = None
        self._frame_states: dict = {}
        self._play_speed: int = 1
        self._zoom: float = 1.0
        self._lineno_map: dict[int, int] = {}
        self._input_focused: bool = False

        raw_frames = problem_module.run(input_data)
        self._frames = self._renderer.filter_frames(raw_frames)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def compose(self) -> ComposeResult:
        viz_widget = self._renderer.make_widget(self._input_data)
        is_tree = getattr(self._problem, "RENDERER", "") == "tree"

        with Container(id="main-container"):
            with Vertical(id="left-panel"):
                with Container(id="problem-panel"):
                    yield Label(
                        f"  {self._problem.TITLE}  [{self._problem.DIFFICULTY.upper()}]",
                        id="problem-title",
                    )
                    yield Static(self._problem.DESCRIPTION, id="problem-desc")
                with Container(id="solution-panel"):
                    yield CodePane(self._problem.CODE_LINES, id="code-pane")

            with Vertical(id="right-panel"):
                with Container(id="grid-container"):
                    yield viz_widget
                yield Label("", id="step-explanation")
                yield Label("zoom: [-] 100% [+]   [0] reset", id="zoom-controls")
                with Horizontal(id="info-row"):
                    yield VariablesPanel(id="vars-panel")
                    if is_tree:
                        yield CallStackPanel(id="call-stack-panel")
                    yield LegendWidget(
                        entries=self._renderer.legend_entries(),
                        id="legend",
                    )

        with Container(id="input-bar"):
            with Horizontal(id="input-row"):
                yield Label("input ▶", id="input-label")
                yield Input(
                    value=self._renderer.serialize_input(self._input_data),
                    placeholder="edit input...",
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
        self.set_focus(None)

        self.query_one("#left-panel").border_title = "problem + solution"
        self.query_one("#problem-panel").border_title = "problem statement"
        self.query_one("#solution-panel").border_title = "solution"
        self.query_one("#grid-container").border_title = "visualization"
        self.query_one("#vars-panel").border_title = "variables"
        if getattr(self._problem, "RENDERER", "") == "tree":
            self.query_one("#call-stack-panel").border_title = "call stack"
        self.query_one("#legend").border_title = "legend"
        self.query_one("#step-explanation").border_title = "step explanation"
        self.query_one("#input-bar").border_title = "input"
        self.query_one("#bottom-bar").border_title = "playback"

    # ------------------------------------------------------------------
    # Frame navigation
    # ------------------------------------------------------------------

    def _apply_frame(self, step: int) -> None:
        if not self._frames:
            return

        step = max(0, min(step, len(self._frames) - 1))
        self._step = step
        frame = self._frames[step]

        # Let renderer compute visual state
        self._frame_states = self._renderer.compute_states(self._frames, step)
        if getattr(self._problem, "RENDERER", "") == "tree":
            self._frame_states["zoom"] = self._zoom

        # Update visualization widget
        viz = self.query_one("#grid-container").children[0]
        self._renderer.update_widget(viz, self._input_data, self._frame_states)

        # Update code pane
        code_pane = self.query_one("#code-pane", CodePane)
        
        active_display_line = None
        for i in range(step, -1, -1):
            if "display_line" in self._frames[i]:
                active_display_line = self._frames[i]["display_line"]
                break
            if "lineno" in self._frames[i]:
                active_display_line = self._abs_lineno_to_display(self._frames[i]["lineno"])
                break

        if active_display_line is not None:
            code_pane.highlight_line(active_display_line)
        else:
            code_pane.highlight_line(None)

        # Update variables
        vars_panel = self.query_one("#vars-panel", VariablesPanel)
        vars_panel.update_entries(self._renderer.variable_entries(frame))

        if getattr(self._problem, "RENDERER", "") == "tree":
            stack_panel = self.query_one("#call-stack-panel", CallStackPanel)
            stack_panel.update_entries(
                self._frame_states.get("call_stack_entries", []),
                self._frame_states.get("edge_note", ""),
            )

        # Update step explanation
        self.query_one("#step-explanation", Label).update(
            self._renderer.explain_frame(frame, step, len(self._frames))
        )
        self.query_one("#zoom-controls", Label).update(
            f"zoom: [-] {int(self._zoom * 100)}% [+]   [0] reset"
        )

        # Update scrubber
        self.query_one("#scrubber", ScrubberBar).update(
            step, len(self._frames), self._playing, self._play_speed
        )

    def _build_lineno_map(self) -> dict[int, int]:
        """Map absolute source line numbers to 1-based CODE_LINES display indices."""
        import inspect
        mapping: dict[int, int] = {}

        # Find the instrumented function in the problem module
        instrumented = None
        for name in dir(self._problem):
            if name.startswith("_") and "instrumented" in name:
                instrumented = getattr(self._problem, name)
                break
        if instrumented is None:
            return mapping

        try:
            source_lines, start_line = inspect.getsourcelines(instrumented)
        except Exception:
            return mapping

        # If the problem file defines _LINE_MAP or LINE_MAP, use it directly (relative -> display)
        custom_map = getattr(self._problem, "LINE_MAP", None) or getattr(self._problem, "_LINE_MAP", None)
        if custom_map:
            for rel_line, display_line in custom_map.items():
                mapping[start_line + rel_line - 1] = display_line
            return mapping

        code_display_idx = 0
        for src_offset, src_line in enumerate(source_lines):
            abs_lineno = start_line + src_offset
            stripped_src = src_line.strip()
            if (
                not stripped_src
                or stripped_src.startswith('"""')
                or stripped_src.startswith("#")
                or "_viz_" in stripped_src
            ):
                continue
            while code_display_idx < len(self._problem.CODE_LINES):
                if self._problem.CODE_LINES[code_display_idx].strip():
                    break
                code_display_idx += 1
            if code_display_idx < len(self._problem.CODE_LINES):
                mapping[abs_lineno] = code_display_idx + 1
                code_display_idx += 1

        return mapping

    def _abs_lineno_to_display(self, lineno: int) -> int | None:
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

    def action_toggle_tab(self) -> None:
        return

    def _set_zoom(self, value: float) -> None:
        self._zoom = max(0.6, min(1.8, round(value, 2)))
        if self._frames and self.query("#grid-container"):
            self._apply_frame(self._step)

    def action_zoom_in(self) -> None:
        if getattr(self._problem, "RENDERER", "") != "tree":
            return
        self._set_zoom(self._zoom + 0.2)

    def action_zoom_out(self) -> None:
        if getattr(self._problem, "RENDERER", "") != "tree":
            return
        self._set_zoom(self._zoom - 0.2)

    def action_zoom_reset(self) -> None:
        if getattr(self._problem, "RENDERER", "") != "tree":
            return
        self._set_zoom(1.0)

    def action_focus_input(self) -> None:
        self.query_one("#grid-input", Input).focus()

    def action_escape_action(self) -> None:
        if self._input_focused:
            inp = self.query_one("#grid-input", Input)
            inp.value = self._renderer.serialize_input(self._input_data)
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
    # Input focus/blur → swap footer bindings
    # ------------------------------------------------------------------

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
        normal_only = {"prev_frame", "next_frame", "toggle_play", "focus_input", "quit", "toggle_tab"}
        input_only  = {"submit_input"}
        if self._input_focused and action in normal_only:
            return False
        if not self._input_focused and action in input_only:
            return False
        return True

    # ------------------------------------------------------------------
    # Play timer
    # ------------------------------------------------------------------

    def _start_play(self) -> None:
        if self._step >= len(self._frames) - 1:
            self._apply_frame(0)
        self._playing = True
        self._play_timer = self.set_interval(1.0 / self._play_speed, self._tick_play)
        self.query_one("#scrubber", ScrubberBar).update(
            self._step, len(self._frames), self._playing, self._play_speed
        )

    def _stop_play(self) -> None:
        self._playing = False
        if self._play_timer:
            self._play_timer.stop()
            self._play_timer = None
        self.query_one("#scrubber", ScrubberBar).update(
            self._step, len(self._frames), self._playing, self._play_speed
        )

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
        try:
            parsed = self._renderer.parse_input(raw)
        except Exception as exc:
            error_label.update(f"  parse error: {exc}")
            return

        error_label.update("")
        self._input_data = parsed
        raw_frames = self._problem.run(parsed)
        self._frames = self._renderer.filter_frames(raw_frames)
        self._step = 0
        self._frame_states = {}
        self._stop_play()

        self.query_one("#grid-input", Input).value = self._renderer.serialize_input(parsed)
        self._apply_frame(0)


# ---------------------------------------------------------------------------
# lastcodeApp
# ---------------------------------------------------------------------------


class lastcodeApp(App):
    CSS = f"Screen {{ background: {BG}; }}"

    def on_mount(self) -> None:
        from lastcode.home import HomeScreen
        self.push_screen(HomeScreen())

    def launch_problem(self, problem_id: str) -> None:
        try:
            mod = _load_problem(problem_id)
        except Exception:
            return
        self.push_screen(VisualizerScreen(problem_module=mod))
