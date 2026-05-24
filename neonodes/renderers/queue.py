"""
queue.py — Renderer for Queue problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_FRONT = "#F7768E"      # Pinkish-red for front of the queue
COLOR_REAR = "#7AA2F7"       # Blue for rear of the queue
BG_QUEUE = "#2D3250"


class QueueWidget(Widget):
    DEFAULT_CSS = f"""
    QueueWidget {{
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
        states = self._states
        queue_list = states.get("queue", [])
        operation = states.get("operation", "")

        result = Text()

        # 1. Operations Notice
        if operation:
            result.append(f"  Operation: {operation}\n\n", style=f"bold {YELLOW}")
        else:
            result.append("\n\n")

        # 2. Horizontal Queue rendering
        # e.g.:
        #      ┌───┬───┬───┐
        #   ◄  │ 1 │ 2 │ 3 │ ◄
        #      └───┴───┴───┘
        #        ▲       ▲
        #      front   rear
        
        if not queue_list:
            result.append("     ┌───────────┐\n", style=DIM)
            result.append("  ◄  │  (empty)  │  ◄\n", style=DIM)
            result.append("     └───────────┘\n", style=DIM)
        else:
            CELL_W = 6
            SEP = "─" * CELL_W
            num_cells = len(queue_list)

            # Top border
            result.append("     ┌", style=DIM)
            for idx in range(num_cells):
                result.append(SEP, style=DIM)
                result.append("┬" if idx < num_cells - 1 else "┐", style=DIM)
            result.append("\n")

            # Values
            result.append("  ◄  │", style=DIM)
            for idx, val in enumerate(queue_list):
                label = f" {str(val):^4} "
                
                is_front = (idx == 0)
                is_rear = (idx == num_cells - 1)
                
                if is_front:
                    result.append(label, style=f"bold {COLOR_FRONT} on #253320")
                elif is_rear:
                    result.append(label, style=f"bold {COLOR_REAR} on #1E2A3D")
                else:
                    result.append(label, style=f"{TEXT} on {BG_QUEUE}")
                result.append("│", style=DIM)
            result.append("  ◄\n", style=DIM)

            # Bottom border
            result.append("     └", style=DIM)
            for idx in range(num_cells):
                result.append(SEP, style=DIM)
                result.append("┴" if idx < num_cells - 1 else "┘", style=DIM)
            result.append("\n")

            # Pointer labels
            result.append("     ", style=DIM)
            for idx in range(num_cells):
                is_front = (idx == 0)
                is_rear = (idx == num_cells - 1)
                
                if is_front and is_rear:
                    result.append(f" {'↑F,R':^4} ", style=f"bold {YELLOW}")
                elif is_front:
                    result.append(f" {'↑Frnt':^4} ", style=f"bold {COLOR_FRONT}")
                elif is_rear:
                    result.append(f" {'↑Rear':^4} ", style=f"bold {COLOR_REAR}")
                else:
                    result.append(" " * CELL_W, style=DIM)
                result.append(" " if idx < num_cells - 1 else "", style=DIM)
            result.append("\n")

        return result


class QueueRenderer:

    def make_widget(self, input_data) -> QueueWidget:
        return QueueWidget(input_data=input_data, id="queue-widget")

    def update_widget(self, widget: QueueWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        queue = []
        operation = ""
        
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            locals_val = frame.get("locals", {})
            
            # Identify any list representing the queue
            q_val = None
            for key in ("queue", "q", "deque", "dq", "tasks"):
                if key in locals_val and (isinstance(locals_val[key], list) or "deque" in str(type(locals_val[key]))):
                    q_val = list(locals_val[key])
                    break
            
            if q_val is not None:
                queue = q_val
                
            if ft == "enqueue":
                val = frame.get("val")
                operation = f"ENQUEUE {val}"
            elif ft == "dequeue":
                val = frame.get("val")
                operation = f"DEQUEUE {val}"
            elif ft == "line":
                operation = ""

        return {
            "queue": queue,
            "operation": operation,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"enqueue", "dequeue", "line"}
        return [f for f in frames if f.get("type") in keep_types or f.get("event") == "line"]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        val = frame.get("val", "")
        
        if ft == "enqueue":
            return f"{prefix}Enqueued '{val}' into the queue"
        if ft == "dequeue":
            return f"{prefix}Dequeued '{val}' from the queue"
            
        return f"{prefix}Executing queue operations..."

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_FRONT, "■", "front of queue (dequeue/peek end)"),
            (COLOR_REAR,  "■", "rear of queue (enqueue end)"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locals_val = frame.get("locals", {})
        entries = []
        
        for k in ("queue", "q", "deque", "dq", "val", "x", "ans", "item"):
            if k in locals_val:
                val = locals_val[k]
                color = COLOR_FRONT if k == "val" else COLOR_REAR
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
