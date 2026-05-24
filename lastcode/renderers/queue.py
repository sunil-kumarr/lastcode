"""
queue.py — Renderer for Queue problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from lastcode.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_FRONT = "#F7768E"      # Pinkish-red for front of the queue
COLOR_REAR = "#7AA2F7"       # Blue for rear of the queue
COLOR_ENQUEUE = "#9ECE6A"    # Green for enqueue operations
COLOR_DEQUEUE = "#F7768E"    # Red/pink for dequeue operations
BG_QUEUE = "#1E2A3D"         # Dark blue background for queue elements
BG_FRONT = "#321820"         # Dark pink background
BG_REAR = "#1E2A3D"          # Dark blue background
BG_CELL = "#2D3250"          # Default cell background
BG_CURR = "#1E3322"          # Dark green for current processing element
BG_POP = "#321820"           # Dark pink/red background for popped pointer cell


def get_pointer_color(name: str) -> str:
    name_lower = name.lower()
    if name_lower in ("i", "curr", "pos", "p", "ptr"):
        return YELLOW
    elif name_lower in ("idx", "val", "char", "item", "x"):
        return COLOR_FRONT
    return TEXT


def get_cell_style(idx: int, pointers: dict) -> tuple[str, str]:
    cell_ptrs = [name for name, val in pointers.items() if val == idx]
    if not cell_ptrs:
        return TEXT, BG_CELL
    if len(cell_ptrs) > 1:
        if any(p in ("idx", "val", "char", "item", "x") for p in cell_ptrs):
            return COLOR_FRONT, BG_FRONT
        return YELLOW, BG_CURR
    name = cell_ptrs[0]
    name_lower = name.lower()
    if name_lower in ("i", "curr", "pos", "p", "ptr"):
        return YELLOW, BG_CURR
    elif name_lower in ("idx", "val", "char", "item", "x"):
        return COLOR_FRONT, BG_FRONT
    return TEXT, BG_CELL


class QueueWidget(Widget):
    DEFAULT_CSS = f"""
    QueueWidget {{
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

        queue_list = states.get("queue", [])
        operation = states.get("operation", "")
        op_type = states.get("op_type", "")
        op_val = states.get("op_val", "")

        result = Text()

        # ── Compute dynamic cell widths ─────────────────────────────────
        # For the input sequence: wide enough to show any value without overflow
        if isinstance(sequence, (list, str)) and len(sequence) > 0:
            max_seq_val_len = max(len(str(v)) for v in sequence)
            SEQ_CELL_W = max(6, max_seq_val_len + 2)
        else:
            SEQ_CELL_W = 6

        # For the queue itself: wide enough to show any queued value
        if queue_list:
            max_q_val_len = max(len(str(v)) for v in queue_list)
            Q_CELL_W = max(6, max_q_val_len + 2)
        else:
            Q_CELL_W = 6

        # ── Extra parameter display ────────────────────────────────────
        if extra is not None:
            result.append(f"  Parameter: ", style=f"bold {DIM}")
            result.append(f"{extra}\n\n", style=f"bold {YELLOW}")

        # ── Input array / stream visualization ─────────────────────────
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
                result.append("   ", style=DIM)
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
                result.append("   ", style=DIM)
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

            # Values row — value padded to exactly SEQ_CELL_W - 2 inner chars + 1 space each side
            result.append("  │", style=DIM)
            for idx, val in enumerate(sequence):
                inner_w = SEQ_CELL_W - 2
                val_str = str(val)
                # Truncate if somehow still too long (safety)
                if len(val_str) > inner_w:
                    val_str = val_str[:inner_w - 1] + "…"
                label = f" {val_str:^{inner_w}} "
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
                result.append("   ", style=DIM)
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
                result.append("   ", style=DIM)
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
            if op_type == "enqueue":
                result.append(f"  ► ENQUEUE  ", style=f"bold {COLOR_ENQUEUE}")
                result.append(f"{op_val}", style=f"bold {TEXT}")
                result.append(f"  →  rear\n", style=f"bold {COLOR_ENQUEUE}")
            elif op_type == "dequeue":
                result.append(f"  ◄ DEQUEUE  ", style=f"bold {COLOR_DEQUEUE}")
                result.append(f"{op_val}", style=f"bold {TEXT}")
                result.append(f"  ←  front\n", style=f"bold {COLOR_DEQUEUE}")
            elif op_type == "peek":
                result.append(f"  👁 PEEK     ", style=f"bold {YELLOW}")
                result.append(f"{op_val}", style=f"bold {TEXT}")
                result.append(f"  (front)\n", style=f"bold {YELLOW}")
            else:
                result.append(f"  {operation}\n", style=f"bold {YELLOW}")

        # ── Horizontal Queue visualization ──────────────────────────────
        result.append("\n")
        
        if not queue_list:
            result.append("              ┌───────────┐\n", style=DIM)
            result.append("  ◄──  front  │  (empty)  │  rear  ──◄\n", style=DIM)
            result.append("              └───────────┘\n", style=DIM)
        else:
            SEP = "─" * Q_CELL_W
            num_cells = len(queue_list)
            q_inner_w = Q_CELL_W - 2  # inner padding area

            # Top border
            result.append("              ┌", style=DIM)
            for idx in range(num_cells):
                result.append(SEP, style=DIM)
                result.append("┬" if idx < num_cells - 1 else "┐", style=DIM)
            result.append("\n")

            # Values
            result.append("  ◄──  front  │", style=DIM)
            for idx, val in enumerate(queue_list):
                val_str = str(val)
                if len(val_str) > q_inner_w:
                    val_str = val_str[:q_inner_w - 1] + "…"
                label = f" {val_str:^{q_inner_w}} "

                is_front = (idx == 0)
                is_rear = (idx == num_cells - 1)

                if is_front:
                    result.append(label, style=f"bold {COLOR_FRONT} on {BG_FRONT}")
                elif is_rear:
                    result.append(label, style=f"bold {COLOR_REAR} on {BG_REAR}")
                else:
                    result.append(label, style=f"{TEAL} on {BG_QUEUE}")
                result.append("│", style=DIM)
            result.append("  rear  ──◄\n", style=DIM)

            # Bottom border
            result.append("              └", style=DIM)
            for idx in range(num_cells):
                result.append(SEP, style=DIM)
                result.append("┴" if idx < num_cells - 1 else "┘", style=DIM)
            result.append("\n")

            # Metrics
            front_val = queue_list[0]
            rear_val = queue_list[-1]
            result.append(f"\n  size = {len(queue_list)}  │  front = {front_val}  │  rear = {rear_val}\n", style=f"bold {DIM}")

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


class QueueRenderer:

    def make_widget(self, input_data) -> QueueWidget:
        return QueueWidget(input_data=input_data, id="queue-widget")

    def update_widget(self, widget: QueueWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        QUEUE_KEYS = {"queue", "q", "deque", "dq", "tasks"}
        POINTER_NAMES = {"i", "idx", "index", "j", "k", "pos", "p", "ptr", "curr", "val", "x", "item"}

        queue = []
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

            # Extract queue
            for key in QUEUE_KEYS:
                if key in locals_val:
                    q_val = locals_val[key]
                    if isinstance(q_val, list) or "deque" in str(type(q_val)):
                        queue = list(q_val)
                        break

            # Extract current index
            for key in ("i", "idx", "index"):
                if key in locals_val and isinstance(locals_val[key], int):
                    curr_idx = locals_val[key]
                    break

            # Extract active sequence being traversed
            for key in ("val_list", "t_list", "ops", "prices", "operations", "tasks", "s", "num", "nums", "arr", "input_data"):
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
            if ft == "enqueue":
                operation = f"ENQUEUE {val}"
                op_type = "enqueue"
                op_val = val
            elif ft == "dequeue":
                operation = f"DEQUEUE {val}"
                op_type = "dequeue"
                op_val = val
            elif ft == "peek":
                operation = f"PEEK {val}"
                op_type = "peek"
                op_val = val
            elif ft == "line":
                operation = ""
                op_type = ""
                op_val = ""

            # Result
            for rk in ("ans", "res", "result", "avg"):
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

        if curr_idx is None:
            curr_idx = pointers.get("i", pointers.get("idx", None))

        return {
            "queue": queue,
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
        keep_types = {"enqueue", "dequeue", "peek", "line"}
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

        if ft == "enqueue":
            return f"{prefix}Enqueued '{val}' into the queue"
        if ft == "dequeue":
            return f"{prefix}Dequeued '{val}' from the queue"
        if ft == "peek":
            return f"{prefix}Peeked at front element '{val}'"

        return f"{prefix}Executing queue operations..."

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_FRONT, "■", "front of queue (dequeue/peek end)"),
            (COLOR_REAR,  "■", "rear of queue (enqueue end)"),
            (YELLOW,      "■", "current processing pointer"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        accumulated  = frame.get("accumulated_locals", frame.get("locals", {}))
        all_vars     = frame.get("all_var_names", list(accumulated.keys()))

        QUEUE_KEYS = {"queue", "q", "deque", "dq", "tasks"}
        RESULT_KEYS = {"ans", "res", "result", "avg"}
        POINTER_KEYS = ["i", "idx", "index", "j", "k", "pos", "p", "ptr", "curr"]
        SKIP_KEYS = {"prices", "operations", "tasks", "s", "num", "nums", "arr", "input_data"}

        entries = []

        # 1. Queue variable
        for k in ("queue", "q", "deque", "dq", "tasks"):
            if k in all_vars:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), COLOR_REAR))
                break

        # 2. Pointers
        for k in POINTER_KEYS:
            if k in all_vars and k not in SKIP_KEYS:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), get_pointer_color(k)))

        # 3. Current value being processed
        already = {e[0] for e in entries} | QUEUE_KEYS | SKIP_KEYS
        for k in ("val", "token", "char", "c", "digit", "ast", "temp", "x", "item"):
            if k in all_vars and k not in already:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), COLOR_FRONT))
                break

        # 4. Result variables
        for k in sorted(all_vars):
            if k in RESULT_KEYS:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), GREEN))

        # 5. Other scalar variables
        already = {e[0] for e in entries} | QUEUE_KEYS | RESULT_KEYS | set(POINTER_KEYS) | SKIP_KEYS
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
