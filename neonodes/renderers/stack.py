"""
stack.py — Renderer for Stack problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_TOP   = "#F7768E"      # Pinkish-red for top element
COLOR_STACK = "#7AA2F7"      # Blue for stack elements
COLOR_PUSH  = "#9ECE6A"      # Green for push operations
COLOR_POP   = "#F7768E"      # Red/pink for pop operations
BG_STACK    = "#1E2A3D"      # Dark blue background for stack elements
BG_TOP      = "#321820"      # Dark pink background for top
BG_CELL     = "#2D3250"      # Default cell background
BG_CURR     = "#1E3322"      # Dark green for current processing element
BG_POP      = "#321820"      # Dark pink/red background for pop/popped pointer cell


def get_pointer_color(name: str) -> str:
    name_lower = name.lower()
    if name_lower in ("i", "curr", "pos", "p", "ptr"):
        return YELLOW
    elif name_lower in ("idx", "popped", "pop_idx", "val", "char"):
        return COLOR_POP
    elif name_lower in ("left", "l", "slow", "start"):
        return COLOR_TOP
    elif name_lower in ("right", "r", "fast", "end"):
        return COLOR_STACK
    return TEXT


def get_cell_style(idx: int, pointers: dict) -> tuple[str, str]:
    # Returns (text_color, bg_color)
    cell_ptrs = [name for name, val in pointers.items() if val == idx]
    if not cell_ptrs:
        return TEXT, BG_CELL
    if len(cell_ptrs) > 1:
        if any(p in ("idx", "popped", "pop_idx") for p in cell_ptrs):
            return COLOR_POP, BG_POP
        return YELLOW, BG_CURR

    name = cell_ptrs[0]
    name_lower = name.lower()
    if name_lower in ("i", "curr", "pos", "p", "ptr"):
        return YELLOW, BG_CURR
    elif name_lower in ("idx", "popped", "pop_idx"):
        return COLOR_POP, BG_POP
    elif name_lower in ("left", "l", "slow", "start"):
        return COLOR_TOP, BG_TOP
    elif name_lower in ("right", "r", "fast", "end"):
        return COLOR_STACK, BG_STACK
    return TEXT, BG_CELL



class StackWidget(Widget):
    DEFAULT_CSS = f"""
    StackWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 12;
    }}
    """

    def get_content_height(self, container, viewport, width) -> int:
        return max(12, getattr(self, "_content_lines", 12))

    def __init__(self, input_data, **kwargs) -> None:
        super().__init__(**kwargs)
        self._input_data = input_data
        self._states: dict = {}
        self._content_lines = 12

    def update_state(self, input_data, states: dict) -> None:
        self._input_data = input_data
        self._states = states
        self.refresh()

    def render(self) -> RenderResult:
        data = self._input_data
        states = self._states

        # Unpack input
        if isinstance(data, tuple) and len(data) == 2:
            sequence, extra = data
        elif isinstance(data, list):
            sequence, extra = data, None
        elif isinstance(data, str):
            sequence, extra = list(data), None
        else:
            sequence, extra = data, None

        if states.get("sequence") is not None:
            sequence = states["sequence"]
        if isinstance(sequence, str):
            sequence = list(sequence)

        stack_list = states.get("stack", [])
        operation = states.get("operation", "")
        op_type = states.get("op_type", "")
        op_val = states.get("op_val", "")
        curr_idx = states.get("curr_idx")

        result = Text()
        # Determine dynamic cell width for sequence visualization
        max_val_len = max((len(str(val)) for val in sequence), default=4) if sequence else 4
        SEQ_CELL_W = max(6, max_val_len + 2)

        # ── Extra parameter display ────────────────────────────────────
        if extra is not None:
            result.append(f"  Parameter: ", style=f"bold {DIM}")
            result.append(f"{extra}\n\n", style=f"bold {YELLOW}")

        # ── Input array / string visualization ─────────────────────────
        if isinstance(sequence, (list, str)) and len(sequence) <= 20:
            pointers = states.get("pointers", {})
            TOP_POINTER_NAMES = {"i", "curr", "pos", "left", "l", "slow", "start"}

            # Collect top and bottom pointers per cell index
            top_pointers_by_cell = [[] for _ in range(len(sequence))]
            bottom_pointers_by_cell = [[] for _ in range(len(sequence))]

            for name, idx in pointers.items():
                if idx is not None and 0 <= idx < len(sequence):
                    if name in TOP_POINTER_NAMES:
                        top_pointers_by_cell[idx].append(name)
                    else:
                        bottom_pointers_by_cell[idx].append(name)

            # Determine maximum depth of top pointers
            max_top_depth = max((len(ptrs) for ptrs in top_pointers_by_cell), default=0)

            # Render Top Pointer Name Rows
            for d in range(max_top_depth):
                result.append("   ", style=DIM)  # 3 spaces prefix
                for idx in range(len(sequence)):
                    ptrs = top_pointers_by_cell[idx]
                    if d < len(ptrs):
                        name = ptrs[d]
                        result.append(f"{name:^{SEQ_CELL_W}} ", style=f"bold {get_pointer_color(name)}")
                    else:
                        result.append(" " * (SEQ_CELL_W + 1))
                result.append("\n")

            # Render Top Pointer Arrow Row (down arrows: ↓)
            if max_top_depth > 0:
                result.append("   ", style=DIM)  # 3 spaces prefix
                for idx in range(len(sequence)):
                    ptrs = top_pointers_by_cell[idx]
                    if ptrs:
                        arrow_color = YELLOW if len(ptrs) > 1 else get_pointer_color(ptrs[0])
                        result.append(f"{'↓':^{SEQ_CELL_W}} ", style=f"bold {arrow_color}")
                    else:
                        result.append(" " * (SEQ_CELL_W + 1))
                result.append("\n")

            # Index header
            result.append("   ", style=DIM)
            for idx in range(len(sequence)):
                result.append(f"{idx:^{SEQ_CELL_W}} ", style=DIM)
            result.append("\n")

            # Top border
            result.append("  ┌", style=DIM)
            for idx in range(len(sequence)):
                result.append("─" * SEQ_CELL_W, style=DIM)
                result.append("┬" if idx < len(sequence) - 1 else "┐", style=DIM)
            result.append("\n")

            # Values row
            result.append("  │", style=DIM)
            for idx, val in enumerate(sequence):
                label = f" {str(val):^{SEQ_CELL_W - 2}} "
                text_col, bg_col = get_cell_style(idx, pointers)
                result.append(label, style=f"bold {text_col} on {bg_col}" if text_col != TEXT else f"{text_col} on {bg_col}")
                result.append("│", style=DIM)
            result.append("\n")

            # Bottom border
            result.append("  └", style=DIM)
            for idx in range(len(sequence)):
                result.append("─" * SEQ_CELL_W, style=DIM)
                result.append("┴" if idx < len(sequence) - 1 else "┘", style=DIM)
            result.append("\n")

            # Determine maximum depth of bottom pointers
            max_bottom_depth = max((len(ptrs) for ptrs in bottom_pointers_by_cell), default=0)

            # Render Bottom Pointer Arrow Row (up arrows: ↑)
            if max_bottom_depth > 0:
                result.append("   ", style=DIM)  # 3 spaces prefix
                for idx in range(len(sequence)):
                    ptrs = bottom_pointers_by_cell[idx]
                    if ptrs:
                        arrow_color = YELLOW if len(ptrs) > 1 else get_pointer_color(ptrs[0])
                        result.append(f"{'↑':^{SEQ_CELL_W}} ", style=f"bold {arrow_color}")
                    else:
                        result.append(" " * (SEQ_CELL_W + 1))
                result.append("\n")

            # Render Bottom Pointer Name Rows
            for d in range(max_bottom_depth):
                result.append("   ", style=DIM)  # 3 spaces prefix
                for idx in range(len(sequence)):
                    ptrs = bottom_pointers_by_cell[idx]
                    if d < len(ptrs):
                        name = ptrs[d]
                        result.append(f"{name:^{SEQ_CELL_W}} ", style=f"bold {get_pointer_color(name)}")
                    else:
                        result.append(" " * (SEQ_CELL_W + 1))
                result.append("\n")

        # ── Operation indicator ────────────────────────────────────────
        if operation:
            result.append("\n")
            if op_type == "push":
                result.append(f"  ▼ PUSH  ", style=f"bold {COLOR_PUSH}")
                result.append(f"{op_val}", style=f"bold {TEXT}")
                result.append(f"  →  stack\n", style=f"bold {COLOR_PUSH}")
            elif op_type == "pop":
                result.append(f"  ▲ POP   ", style=f"bold {COLOR_POP}")
                result.append(f"{op_val}", style=f"bold {TEXT}")
                result.append(f"  ←  stack\n", style=f"bold {COLOR_POP}")
            elif op_type == "peek":
                result.append(f"  👁 PEEK  ", style=f"bold {YELLOW}")
                result.append(f"{op_val}", style=f"bold {TEXT}")
                result.append(f"  (top)\n", style=f"bold {YELLOW}")
            else:
                result.append(f"  {operation}\n", style=f"bold {YELLOW}")

        # ── Vertical stack visualization ───────────────────────────────
        result.append("\n")

        # Check if the stack contains indices of the sequence
        stack_are_indices = False
        if (
            isinstance(sequence, (list, str))
            and stack_list
            and all(isinstance(x, int) and 0 <= x < len(sequence) for x in stack_list)
        ):
            stack_are_indices = True

        # Determine stack cell width dynamically
        if stack_list:
            if stack_are_indices:
                max_len = max(len(f"idx {item}: {sequence[item]}") for item in stack_list)
            else:
                max_len = max(len(str(item)) for item in stack_list)
            width = max(12, max_len + 4)
        else:
            width = 12

        if not stack_list:
            result.append("   ┌" + "─" * width + "┐\n", style=DIM)
            result.append("   │" + " (empty) ".center(width) + "│\n", style=DIM)
            result.append("   └" + "─" * width + "┘\n", style=DIM)
        else:
            # Open top
            result.append("   │" + " " * width + "│\n", style=DIM)

            for idx, item in enumerate(reversed(stack_list)):
                is_top = (idx == 0)
                if stack_are_indices:
                    val_str = f"idx {item}: {sequence[item]}"
                else:
                    val_str = str(item)
                item_str = f"{val_str:^{width}}"

                # Separator
                result.append("   ├", style=DIM)
                result.append("─" * width, style=DIM)
                result.append("┤\n", style=DIM)

                # Value cell
                result.append("   │", style=DIM)
                if is_top:
                    result.append(item_str, style=f"bold {COLOR_TOP} on {BG_TOP}")
                    result.append("│", style=DIM)
                    result.append(f" ◄ TOP", style=f"bold {COLOR_TOP}")
                else:
                    result.append(item_str, style=f"{COLOR_STACK} on {BG_STACK}")
                    result.append("│", style=DIM)
                result.append("\n")

            # Bottom
            result.append("   └", style=DIM)
            result.append("─" * width, style=DIM)
            result.append("┘\n", style=DIM)

        # Stack size
        result.append(f"\n  size = {len(stack_list)}\n", style=f"bold {DIM}")

        # ── Result display ─────────────────────────────────────────────
        res_val = states.get("res_val")
        if res_val is not None:
            var_name, var_data = res_val
            result.append(f"\n  {var_name} = {var_data}\n", style=f"bold {GREEN}")

        # Count lines for get_content_height
        line_count = result.plain.count("\n") + 1
        if line_count != self._content_lines:
            self._content_lines = line_count
            self.call_after_refresh(self.refresh, layout=True)

        return result


class StackRenderer:

    def make_widget(self, input_data) -> StackWidget:
        return StackWidget(input_data=input_data, id="stack-widget")

    def update_widget(self, widget: StackWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        STACK_KEYS = {"stack", "st", "s", "m_stack"}
        POINTER_NAMES = {"i", "idx", "index", "j", "k", "pos", "p", "ptr", "curr", "popped", "left", "right", "l", "r", "slow", "fast", "start", "end"}

        stack = []
        operation = ""
        op_type = ""
        op_val = ""
        curr_idx = None
        res_val = None
        pointers = {}
        sequence = None

        # 1. Collect ALL variable names across all frames
        all_var_names: set[str] = set()
        for frame in frames:
            for k in frame.get("locals", {}):
                if not k.startswith("_"):
                    all_var_names.add(k)

        # 2. Accumulate locals up to current step
        accumulated_vars: dict = {}
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            locals_val = frame.get("locals", {})

            # Extract stack
            for key in STACK_KEYS:
                if key in locals_val and isinstance(locals_val[key], list):
                    stack = list(locals_val[key])
                    break

            # Extract current index
            for key in ("i", "idx", "index"):
                if key in locals_val and isinstance(locals_val[key], int):
                    curr_idx = locals_val[key]
                    break

            # Extract active sequence being traversed
            for key in ("parts", "nums2", "temperatures", "asteroids", "tokens", "operations", "prices", "path", "s", "num"):
                if key in locals_val:
                    if isinstance(locals_val[key], (list, tuple, str)):
                        sequence = locals_val[key]
                        break

            # Accumulate pointer positions
            for name in POINTER_NAMES:
                if name in locals_val:
                    val = locals_val[name]
                    if isinstance(val, int):
                        pointers[name] = val

            # Operation
            val = frame.get("val", "")
            if ft == "push":
                operation = f"PUSH {val}"
                op_type = "push"
                op_val = val
            elif ft == "pop":
                operation = f"POP {val}"
                op_type = "pop"
                op_val = val
            elif ft in ("peek", "top"):
                operation = f"PEEK {val}"
                op_type = "peek"
                op_val = val
            elif ft == "line":
                operation = ""
                op_type = ""
                op_val = ""

            # Result
            for rk in ("ans", "res", "result"):
                if rk in locals_val:
                    res_val = (rk, locals_val[rk])

            # Accumulate all vars
            for k, v in locals_val.items():
                if not k.startswith("_"):
                    accumulated_vars[k] = v

        # Attach metadata to frame for variable_entries
        current_frame = frames[up_to]
        current_frame["accumulated_locals"] = accumulated_vars
        current_frame["all_var_names"] = list(all_var_names)

        # Make sure legacy curr_idx is set if not already
        if curr_idx is None:
            curr_idx = pointers.get("i", pointers.get("idx", None))

        return {
            "stack": stack,
            "operation": operation,
            "op_type": op_type,
            "op_val": op_val,
            "curr_idx": curr_idx,
            "res_val": res_val,
            "pointers": pointers,
            "sequence": sequence,
            "accumulated_locals": accumulated_vars,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"push", "pop", "peek", "top"}
        filtered = []
        line_count = 0
        for f in frames:
            ft = f.get("type")
            if ft in keep_types:
                filtered.append(f)
            elif ft == "line" or f.get("event") == "line":
                if line_count < 3:
                    filtered.append(f)
                    line_count += 1
        return filtered

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        val = frame.get("val", "")
        locals_val = frame.get("locals", {})

        # Get current stack from locals
        stack = None
        for key in ("stack", "st", "s", "m_stack"):
            if key in locals_val and isinstance(locals_val[key], list):
                stack = locals_val[key]
                break

        stack_str = f"  →  stack = {stack}" if stack is not None else ""

        if ft == "push":
            return f"{prefix}▼ Pushing {val} onto stack{stack_str}"
        if ft == "pop":
            return f"{prefix}▲ Popping {val} from stack{stack_str}"
        if ft in ("peek", "top"):
            return f"{prefix}👁 Peeking at top: {val}"

        return f"{prefix}Initializing..."

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_TOP,   "■", "top — top element of the stack"),
            (COLOR_STACK, "■", "stack elements"),
            (COLOR_PUSH,  "▼", "push operation"),
            (COLOR_POP,   "▲", "pop operation"),
            (YELLOW,      "■", "current processing element"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        accumulated  = frame.get("accumulated_locals", frame.get("locals", {}))
        all_vars     = frame.get("all_var_names", list(accumulated.keys()))

        STACK_KEYS = {"stack", "st", "s", "m_stack"}
        RESULT_KEYS = {"ans", "res", "result"}
        POINTER_KEYS = ["i", "idx", "index", "j", "k", "pos", "p", "ptr", "curr", "popped", "pop_idx", "left", "right", "l", "r", "slow", "fast", "start", "end"]
        SKIP_KEYS = {"temperatures", "tokens", "asteroids", "num", "heights",
                      "prices", "parentheses", "chars"}

        entries = []

        # 1. Stack variable
        for k in ("stack", "st", "s", "m_stack"):
            if k in all_vars:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), COLOR_STACK))
                break

        # 2. Pointers
        for k in POINTER_KEYS:
            if k in all_vars and k not in SKIP_KEYS:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), get_pointer_color(k)))

        # 3. Current value being processed
        already = {e[0] for e in entries} | STACK_KEYS | SKIP_KEYS
        for k in ("val", "token", "char", "c", "digit", "ast", "temp", "x"):
            if k in all_vars and k not in already:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), COLOR_TOP))
                break

        # 4. Result variables
        for k in sorted(all_vars):
            if k in RESULT_KEYS:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), GREEN))

        # 5. Other scalar variables
        already = {e[0] for e in entries} | STACK_KEYS | RESULT_KEYS | set(POINTER_KEYS) | SKIP_KEYS
        for k in sorted(all_vars):
            if k not in already and k not in SKIP_KEYS and not k.startswith("_"):
                val = accumulated.get(k, "—")
                if not isinstance(val, (list, dict, set)):
                    entries.append((k, str(val), TEAL))

        return entries if entries else [("—", "—", DIM)]

    def parse_input(self, raw: str) -> object:
        raw = raw.strip()
        try:
            return ast.literal_eval(raw)
        except Exception:
            pass
        return raw

    def serialize_input(self, data) -> str:
        return str(data)
