"""
sliding_window.py — Renderer for Sliding Window problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_L = "#F7768E"      # Pinkish-red for left pointer
COLOR_R = "#7AA2F7"      # Blue for right pointer
COLOR_WIN = "#9ECE6A"    # Green for window elements
BG_WIN = "#253320"       # Dark green background for window range
BG_CELL = "#2D3250"      # Default cell background


class SlidingWindowWidget(Widget):
    DEFAULT_CSS = f"""
    SlidingWindowWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 10;
    }}
    """

    def __init__(self, input_data, **kwargs) -> None:
        super().__init__(**kwargs)
        self._input_data = input_data
        self._states: dict = {}

    def update_state(self, input_data, states: dict) -> None:
        self._input_data = input_data
        self._states = states
        self.refresh()

    def render(self) -> RenderResult:
        data = self._input_data
        # If input_data is a tuple (e.g. (arr, target)), unpack it
        if isinstance(data, tuple) and len(data) == 2:
            sequence, target = data
        else:
            sequence, target = data, None

        states = self._states
        l_idx = states.get("left")
        r_idx = states.get("right")
        window_state = states.get("window_state", "")

        result = Text()
        CELL_W = 6
        SEP = "─" * CELL_W

        # Header / title
        if target is not None:
            result.append(f"Target: {target}\n\n", style=f"bold {YELLOW}")

        # Index header
        result.append("  ", style=DIM)
        for idx in range(len(sequence)):
            result.append(f"  {idx:<4}", style=DIM)
        result.append("\n")

        # Top border
        result.append("  ┌", style=DIM)
        for idx in range(len(sequence)):
            result.append(SEP, style=DIM)
            result.append("┬" if idx < len(sequence) - 1 else "┐", style=DIM)
        result.append("\n")

        # Values row
        result.append("  │", style=DIM)
        for idx, val in enumerate(sequence):
            label = f" {str(val):^4} "
            in_window = False
            if l_idx is not None and r_idx is not None:
                in_window = (l_idx <= idx <= r_idx)
            
            if in_window:
                result.append(label, style=f"bold {COLOR_WIN} on {BG_WIN}")
            else:
                result.append(label, style=f"{TEXT} on {BG_CELL}")
            result.append("│", style=DIM)
        result.append("\n")

        # Bottom border
        result.append("  └", style=DIM)
        for idx in range(len(sequence)):
            result.append(SEP, style=DIM)
            result.append("┴" if idx < len(sequence) - 1 else "┘", style=DIM)
        result.append("\n")

        # Pointer row
        result.append("  ", style=DIM)
        for idx in range(len(sequence)):
            is_l = (idx == l_idx)
            is_r = (idx == r_idx)
            if is_l and is_r:
                result.append(f" {'↑LR':^4} ", style=f"bold {YELLOW}")
            elif is_l:
                result.append(f" {'↑L':^4} ", style=f"bold {COLOR_L}")
            elif is_r:
                result.append(f" {'↑R':^4} ", style=f"bold {COLOR_R}")
            else:
                result.append(" " * CELL_W, style=DIM)
        result.append("\n")

        # Window state details
        if window_state:
            result.append(f"\n  Window State: {window_state}\n", style=f"bold {TEAL}")

        return result


class SlidingWindowRenderer:

    def make_widget(self, input_data) -> SlidingWindowWidget:
        return SlidingWindowWidget(input_data=input_data, id="sliding-window-widget")

    def update_widget(self, widget: SlidingWindowWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        left = None
        right = None
        window_state = ""
        
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            if ft in ("window_check", "window_update", "window_found", "line"):
                locals_val = frame.get("locals", {})
                if "left" in locals_val or "l" in locals_val:
                    left = locals_val.get("left", locals_val.get("l"))
                if "right" in locals_val or "r" in locals_val:
                    right = locals_val.get("right", locals_val.get("r"))
                
                # Try to extract window state representation
                if "window" in locals_val:
                    window_state = str(locals_val["window"])
                elif "char_map" in locals_val:
                    window_state = str({k: v for k, v in locals_val["char_map"].items() if v > 0})
                elif "counts" in locals_val:
                    window_state = str(locals_val["counts"])
                elif "curr_sum" in locals_val:
                    window_state = f"Sum = {locals_val['curr_sum']}"
                elif "s" in locals_val and isinstance(locals_val["s"], int):
                    window_state = f"Sum = {locals_val['s']}"

        return {
            "left": left,
            "right": right,
            "window_state": window_state,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        # Keep window operations and lines
        keep_types = {"window_check", "window_update", "window_found", "line"}
        return [f for f in frames if f.get("type") in keep_types or f.get("event") == "line"]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        locals_val = frame.get("locals", {})
        l = locals_val.get("left", locals_val.get("l", "—"))
        r = locals_val.get("right", locals_val.get("r", "—"))
        
        if ft == "window_check":
            return f"{prefix}Checking window [{l}, {r}]"
        if ft == "window_update":
            return f"{prefix}Updating window constraints (adjusting pointers: L={l}, R={r})"
        if ft == "window_found":
            return f"{prefix}Valid window state found for range [{l}, {r}]"
            
        return f"{prefix}Processing index R={r}"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_L,   "↑L", "left boundary pointer"),
            (COLOR_R,   "↑R", "right boundary pointer"),
            (COLOR_WIN, "■",  "elements inside sliding window"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locals_val = frame.get("locals", {})
        entries = []
        for k in ("l", "left", "r", "right", "ans", "max_len", "curr_sum", "min_len", "k"):
            if k in locals_val:
                val = locals_val[k]
                color = COLOR_L if "l" in k else (COLOR_R if "r" in k else YELLOW)
                entries.append((k, str(val), color))
        if not entries:
            return [("—", "—", DIM)]
        return entries

    def parse_input(self, raw: str) -> object:
        raw = raw.strip()
        try:
            parsed = ast.literal_eval(raw)
            if isinstance(parsed, tuple) and len(parsed) == 2:
                return parsed
            if isinstance(parsed, list):
                return parsed
            if isinstance(parsed, str):
                return parsed
        except Exception:
            pass
        # Fallback to returning string directly
        return raw

    def serialize_input(self, data) -> str:
        if isinstance(data, str):
            return data
        return str(data)
