"""
stack.py — Renderer for Stack problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_TOP = "#F7768E"      # Pinkish-red for top element
COLOR_STACK = "#7AA2F7"    # Blue for stack elements
BG_STACK = "#1E2A3D"       # Dark blue background for stack elements
BG_CELL = "#2D3250"


class StackWidget(Widget):
    DEFAULT_CSS = f"""
    StackWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 12;
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
        states = self._states
        stack_list = states.get("stack", [])
        operation = states.get("operation", "")

        result = Text()
        
        # 1. Renders operation notice at the top
        if operation:
            result.append(f"  Operation: {operation}\n\n", style=f"bold {YELLOW}")
        else:
            result.append("\n\n")

        # 2. Render stack elements vertically (from top of stack down to bottom)
        # We want to draw a vertical stack box
        # e.g.:
        #    │      │
        #    ├──────┤
        #    │  c   │ ◄ top
        #    ├──────┤
        #    │  b   │
        #    ├──────┤
        #    │  a   │
        #    └──────┘
        
        width = 10
        top_str = " " * width
        
        if not stack_list:
            result.append("   ┌──────────┐\n", style=DIM)
            result.append("   │  (empty) │\n", style=DIM)
            result.append("   └──────────┘\n", style=DIM)
        else:
            result.append("   │" + " " * width + "│\n", style=DIM)
            for idx, item in enumerate(reversed(stack_list)):
                is_top = (idx == 0)
                item_str = f"{str(item):^10}"
                
                result.append("   ├", style=DIM)
                result.append("─" * width, style=DIM)
                result.append("┤\n", style=DIM)
                
                result.append("   │", style=DIM)
                if is_top:
                    result.append(item_str, style=f"bold {COLOR_TOP} on {BG_STACK}")
                    result.append("│", style=DIM)
                    result.append(f" ◄ top (size {len(stack_list)})", style=f"bold {COLOR_TOP}")
                else:
                    result.append(item_str, style=f"{TEXT} on {BG_CELL}")
                    result.append("│", style=DIM)
                result.append("\n")
                
            result.append("   └", style=DIM)
            result.append("─" * width, style=DIM)
            result.append("┘\n", style=DIM)

        return result


class StackRenderer:

    def make_widget(self, input_data) -> StackWidget:
        return StackWidget(input_data=input_data, id="stack-widget")

    def update_widget(self, widget: StackWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        stack = []
        operation = ""
        
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            locals_val = frame.get("locals", {})
            
            # Look for stack or list variables named 'stack', 'st', etc.
            st_val = None
            for key in ("stack", "st", "s", "m_stack"):
                if key in locals_val and isinstance(locals_val[key], list):
                    st_val = locals_val[key]
                    break
            
            if st_val is not None:
                stack = list(st_val)
                
            if ft == "push":
                val = frame.get("val")
                operation = f"PUSH {val}"
            elif ft == "pop":
                val = frame.get("val")
                operation = f"POP {val}"
            elif ft == "peek" or ft == "top":
                val = frame.get("val")
                operation = f"TOP/PEEK {val}"
            elif ft == "line":
                # Clear operation text on standard lines
                operation = ""

        return {
            "stack": stack,
            "operation": operation,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"push", "pop", "peek", "top", "line"}
        return [f for f in frames if f.get("type") in keep_types or f.get("event") == "line"]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        val = frame.get("val", "")
        
        if ft == "push":
            return f"{prefix}Pushed '{val}' onto the stack"
        if ft == "pop":
            return f"{prefix}Popped '{val}' from the stack"
        if ft == "peek" or ft == "top":
            return f"{prefix}Checked top of stack: '{val}'"
            
        return f"{prefix}Executing stack operations..."

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_TOP, "■", "top of the stack"),
            (TEXT,      "■", "stack elements"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locals_val = frame.get("locals", {})
        entries = []
        
        # Display common variables
        for k in ("stack", "st", "s", "val", "x", "ans", "item", "c", "char"):
            if k in locals_val:
                val = locals_val[k]
                color = COLOR_TOP if k == "val" else COLOR_STACK
                entries.append((k, str(val), color))
                
        if not entries:
            return [("—", "—", DIM)]
        return entries

    def parse_input(self, raw: str) -> object:
        raw = raw.strip()
        try:
            return ast.literal_eval(raw)
        except Exception:
            pass
        return raw

    def serialize_input(self, data) -> str:
        return str(data)
