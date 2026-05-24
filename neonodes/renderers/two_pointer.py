"""
two_pointer.py — Renderer for Two Pointer problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_L = "#F7768E"      # Pinkish-red for left/slow pointer
COLOR_R = "#7AA2F7"      # Blue for right/fast pointer
BG_L = "#321820"         # Dark pink background
BG_R = "#1E2A3D"         # Dark blue background
BG_CELL = "#2D3250"      # Default cell background


class TwoPointerWidget(Widget):
    DEFAULT_CSS = f"""
    TwoPointerWidget {{
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
        # Standardize data format (e.g. list/string vs tuple)
        if isinstance(data, tuple) and len(data) == 2:
            sequence, target = data
        else:
            sequence, target = data, None

        states = self._states
        l_idx = states.get("left")
        r_idx = states.get("right")
        comparison = states.get("comparison", "")

        result = Text()
        CELL_W = 6
        SEP = "─" * CELL_W

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
            is_l = (idx == l_idx)
            is_r = (idx == r_idx)
            
            if is_l and is_r:
                result.append(label, style=f"bold {YELLOW} on {BG_L}")
            elif is_l:
                result.append(label, style=f"bold {COLOR_L} on {BG_L}")
            elif is_r:
                result.append(label, style=f"bold {COLOR_R} on {BG_R}")
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

        # Comparison line
        if comparison:
            result.append(f"\n  {comparison}\n", style=f"bold {TEAL}")

        return result


class TwoPointerRenderer:

    def make_widget(self, input_data) -> TwoPointerWidget:
        return TwoPointerWidget(input_data=input_data, id="two-pointer-widget")

    def update_widget(self, widget: TwoPointerWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        left = None
        right = None
        comparison = ""
        
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            if ft in ("pointer_compare", "pointer_update", "pointer_found", "line"):
                locals_val = frame.get("locals", {})
                
                # Check for left/right or slow/fast patterns
                l_val = locals_val.get("left", locals_val.get("l", locals_val.get("slow", locals_val.get("i"))))
                r_val = locals_val.get("right", locals_val.get("r", locals_val.get("fast", locals_val.get("j"))))
                
                if l_val is not None:
                    left = l_val
                if r_val is not None:
                    right = r_val
                
                # Comparison details
                if "sum" in locals_val:
                    comparison = f"Current Sum = {locals_val['sum']}"
                elif "curr" in locals_val:
                    comparison = f"Current Value = {locals_val['curr']}"
                elif ft == "pointer_compare" and l_val is not None and r_val is not None:
                    comparison = f"Comparing index {l_val} and index {r_val}"

        return {
            "left": left,
            "right": right,
            "comparison": comparison,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"pointer_compare", "pointer_update", "pointer_found", "line"}
        return [f for f in frames if f.get("type") in keep_types or f.get("event") == "line"]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        locals_val = frame.get("locals", {})
        l = locals_val.get("left", locals_val.get("l", locals_val.get("slow", locals_val.get("i", "—"))))
        r = locals_val.get("right", locals_val.get("r", locals_val.get("fast", locals_val.get("j", "—"))))
        
        if ft == "pointer_compare":
            return f"{prefix}Comparing values at left ({l}) and right ({r})"
        if ft == "pointer_update":
            return f"{prefix}Updating pointers (moving left/right: left={l}, right={r})"
        if ft == "pointer_found":
            return f"{prefix}Condition satisfied with pointers left={l}, right={r}!"
            
        return f"{prefix}Traversing (left={l}, right={r})"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_L, "■", "left / slow pointer position"),
            (COLOR_R, "■", "right / fast pointer position"),
            (YELLOW,  "■", "pointers overlapping"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locals_val = frame.get("locals", {})
        entries = []
        for k in ("l", "left", "slow", "i", "r", "right", "fast", "j", "target", "sum", "ans"):
            if k in locals_val:
                val = locals_val[k]
                color = COLOR_L if k in ("l", "left", "slow", "i") else (COLOR_R if k in ("r", "right", "fast", "j") else YELLOW)
                entries.append((k, str(val), color))
        if not entries:
            return [("—", "—", DIM)]
        return entries

    def parse_input(self, raw: str) -> object:
        raw = raw.strip()
        try:
            parsed = ast.literal_eval(raw)
            return parsed
        except Exception:
            pass
        return raw

    def serialize_input(self, data) -> str:
        return str(data)
