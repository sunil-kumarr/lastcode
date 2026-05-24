"""
two_pointer.py — Renderer for Two Pointer problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from lastcode.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_L = "#F7768E"      # Pinkish-red for left/slow pointer
COLOR_R = "#7AA2F7"      # Blue for right/fast pointer
BG_L = "#321820"         # Dark pink background
BG_R = "#1E2A3D"         # Dark blue background
BG_CELL = "#2D3250"      # Default cell background
BG_T = "#122F2D"         # Dark teal background for third pointer
BG_OL = "#3D351E"        # Dark yellow background for overlapping pointers

def get_pointer_color(name: str) -> str:
    name_lower = name.lower()
    if name_lower in ("left", "l", "slow", "low", "p1", "start"):
        return COLOR_L
    elif name_lower in ("right", "r", "fast", "high", "p2", "end"):
        return COLOR_R
    elif name_lower in ("i", "j", "k", "curr", "mid", "p3"):
        return TEAL
    return TEXT

def get_cell_style(idx: int, sequence_len: int, pointers: dict) -> tuple[str, str]:
    # Returns (text_color, bg_color)
    cell_ptrs = [name for name, val in pointers.items() if val == idx]
    if not cell_ptrs:
        return TEXT, BG_CELL
    if len(cell_ptrs) > 1:
        return YELLOW, BG_OL
    
    name = cell_ptrs[0]
    name_lower = name.lower()
    if name_lower in ("left", "l", "slow", "low", "p1", "start"):
        return COLOR_L, BG_L
    elif name_lower in ("right", "r", "fast", "high", "p2", "end"):
        return COLOR_R, BG_R
    else:
        return TEAL, BG_T


class TwoPointerWidget(Widget):
    DEFAULT_CSS = f"""
    TwoPointerWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 12;
    }}
    """

    def get_content_height(self, container, viewport, width) -> int:
        """Tell Textual exactly how many rows we need so the widget is never clipped."""
        return max(12, getattr(self, "_content_lines", 12))

    def __init__(self, input_data, **kwargs) -> None:
        super().__init__(**kwargs)
        self._input_data = input_data
        self._states: dict = {}
        # Animation states
        self._anim_active = False
        self._anim_frame_idx = 0
        self._anim_frames = []
        self._anim_timer = None
        self._current_step_id = None
        self._content_lines = 12

    def update_state(self, input_data, states: dict) -> None:
        self._input_data = input_data
        self._states = states
        
        is_sorting = states.get("is_sorting", False)
        step_id = states.get("step")
        
        if is_sorting:
            if self._current_step_id != step_id:
                # Stop existing animation
                if self._anim_timer:
                    self._anim_timer.stop()
                    self._anim_timer = None
                
                # Determine the sequence to sort from states, or default to input_data
                seq = states.get("prev_sequence") or states.get("sequence")
                if seq is None:
                    if isinstance(input_data, tuple) and len(input_data) == 2:
                        seq = input_data[0]
                    else:
                        seq = input_data
                
                self._anim_frames = self._generate_animation_frames(seq)
                self._anim_active = True
                self._anim_frame_idx = 0
                self._current_step_id = step_id
                self._anim_timer = self.set_interval(0.15, self._tick_sort_animation)
        else:
            self._anim_active = False
            if self._anim_timer:
                self._anim_timer.stop()
                self._anim_timer = None
            self._current_step_id = step_id
            
        self.refresh()

    def _generate_animation_frames(self, seq) -> list:
        if not seq:
            return [[]]
        # Standardize representation (e.g. if it's a string, make it list of chars)
        arr = list(seq)
        frames = [list(arr)]
        n = len(arr)
        
        # We want to perform a bubble sort and record every swap state
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    frames.append(list(arr))
                    swapped = True
            if not swapped:
                break
                
        if arr not in frames:
            frames.append(list(arr))
            
        # Sample frames to limit visual duration
        if len(frames) > 8:
            sampled = []
            for idx in range(8):
                f_idx = int(idx * (len(frames) - 1) / 7)
                sampled.append(frames[f_idx])
            frames = sampled
            
        return frames

    def _tick_sort_animation(self) -> None:
        if not self._anim_active:
            if self._anim_timer:
                self._anim_timer.stop()
                self._anim_timer = None
            return
            
        self._anim_frame_idx += 1
        if self._anim_frame_idx >= len(self._anim_frames):
            self._anim_active = False
            if self._anim_timer:
                self._anim_timer.stop()
                self._anim_timer = None
        self.refresh()

    def render(self) -> RenderResult:
        data = self._input_data
        # Standardize data format (e.g. list/string vs tuple)
        if isinstance(data, tuple) and len(data) == 2:
            sequence, target = data
        else:
            sequence, target = data, None

        states = self._states
        sequence = states.get("sequence", sequence)
        
        # Use animated frame sequence if active
        if self._anim_active and self._anim_frames:
            sequence = self._anim_frames[self._anim_frame_idx]

        pointers = states.get("pointers", {})
        comparison = states.get("comparison", "")

        result = Text()
        CELL_W = 6
        SEP = "─" * CELL_W

        if target is not None:
            result.append(f"Target: {target}\n\n", style=f"bold {YELLOW}")

        TOP_POINTER_NAMES = {"i", "slow", "low", "curr", "p1", "start"}
        
        # Collect top and bottom pointers per cell index
        top_pointers_by_cell = [[] for _ in range(len(sequence))]
        bottom_pointers_by_cell = [[] for _ in range(len(sequence))]
        
        # Only render pointers if not sorting
        if not self._anim_active:
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
                    result.append(f"{name:^6} ", style=f"bold {get_pointer_color(name)}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")
            
        # Render Top Pointer Arrow Row (down arrows: ↓)
        if max_top_depth > 0:
            result.append("   ", style=DIM)  # 3 spaces prefix
            for idx in range(len(sequence)):
                ptrs = top_pointers_by_cell[idx]
                if ptrs:
                    arrow_color = YELLOW if len(ptrs) > 1 else get_pointer_color(ptrs[0])
                    result.append(f"{'↓':^6} ", style=f"bold {arrow_color}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")

        # Index header
        result.append("   ", style=DIM)  # 3 spaces prefix
        for idx in range(len(sequence)):
            result.append(f"{idx:^6} ", style=DIM)
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
            if self._anim_active:
                result.append(label, style=f"bold {YELLOW} on {BG_CELL}")
            else:
                text_col, bg_col = get_cell_style(idx, len(sequence), pointers)
                result.append(label, style=f"bold {text_col} on {bg_col}" if text_col != TEXT else f"{text_col} on {bg_col}")
            result.append("│", style=DIM)
        result.append("\n")

        # Bottom border
        result.append("  └", style=DIM)
        for idx in range(len(sequence)):
            result.append(SEP, style=DIM)
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
                    result.append(f"{'↑':^6} ", style=f"bold {arrow_color}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")
            
        # Render Bottom Pointer Name Rows
        for d in range(max_bottom_depth):
            result.append("   ", style=DIM)  # 3 spaces prefix
            for idx in range(len(sequence)):
                ptrs = bottom_pointers_by_cell[idx]
                if d < len(ptrs):
                    name = ptrs[d]
                    result.append(f"{name:^6} ", style=f"bold {get_pointer_color(name)}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")

        # Bar Chart for Container with most water and Trapping Rain Water
        sequence_key = states.get("sequence_key")
        accumulated_locals = states.get("accumulated_locals", {})
        
        is_container_water = (sequence_key == "height" and "max_area" in accumulated_locals)
        is_trapping_water = (sequence_key == "height" and "water" in accumulated_locals)
        
        if (is_container_water or is_trapping_water) and len(sequence) > 0:
            l_idx = pointers.get("left")
            r_idx = pointers.get("right")
            
            # Calculate water heights for each column
            water_heights = [0] * len(sequence)
            if l_idx is not None and r_idx is not None:
                if is_container_water:
                    h_bound = min(sequence[l_idx], sequence[r_idx])
                    for idx in range(l_idx + 1, r_idx):
                        water_heights[idx] = max(0, h_bound - sequence[idx])
                elif is_trapping_water:
                    # Prefix maxes up to left
                    left_maxes = []
                    curr_max = 0
                    for val in sequence:
                        curr_max = max(curr_max, val)
                        left_maxes.append(curr_max)
                    # Suffix maxes from right to end
                    right_maxes = [0] * len(sequence)
                    curr_max = 0
                    for i in range(len(sequence) - 1, -1, -1):
                        curr_max = max(curr_max, sequence[i])
                        right_maxes[i] = curr_max
                    
                    for idx in range(len(sequence)):
                        if idx <= l_idx:
                            water_heights[idx] = max(0, left_maxes[idx] - sequence[idx])
                        elif idx >= r_idx:
                            water_heights[idx] = max(0, right_maxes[idx] - sequence[idx])

            # Determine maximum value
            max_val = max(sequence) if sequence else 0
            
            # Compute blocks and styles for each column
            tower_blocks = []
            water_blocks = []
            col_styles = []
            
            for idx, val in enumerate(sequence):
                # Calculate tower block height
                if max_val == 0:
                    t_b = 0
                elif max_val <= 10:
                    t_b = val
                else:
                    t_b = max(1, int(round(val * 10 / max_val))) if val > 0 else 0
                tower_blocks.append(t_b)
                
                # Calculate total height (tower + water) and water block height
                w_val = water_heights[idx]
                if w_val == 0:
                    w_b = 0
                else:
                    if max_val <= 10:
                        total_b = val + w_val
                    else:
                        total_val = val + w_val
                        total_b = max(1, int(round(total_val * 10 / max_val))) if total_val > 0 else 0
                    w_b = max(0, total_b - t_b)
                water_blocks.append(w_b)
                
                # Determine styling
                ptr_color = TEXT
                cell_ptrs = []
                if idx == l_idx: cell_ptrs.append("left")
                if idx == r_idx: cell_ptrs.append("right")
                for name, v in pointers.items():
                    if v == idx and name not in cell_ptrs:
                        cell_ptrs.append(name)
                
                if cell_ptrs:
                    ptr_color = YELLOW if len(cell_ptrs) > 1 else get_pointer_color(cell_ptrs[0])
                    style_str = f"bold {ptr_color}"
                else:
                    style_str = TEXT
                col_styles.append(style_str)

            # grid_height = tallest column (pure blocks only — no label rows inside)
            grid_height = max((t_b + w_b for t_b, w_b in zip(tower_blocks, water_blocks)), default=0)

            if grid_height > 0:
                result.append("\n\n")  # Spacer before chart

                # --- Block rows ONLY (top to bottom) — no labels inside ---
                for h in range(grid_height, 0, -1):
                    result.append("   ", style=DIM)
                    for idx in range(len(sequence)):
                        t_b = tower_blocks[idx]
                        w_b = water_blocks[idx]
                        style_str = col_styles[idx]

                        if h <= t_b:
                            result.append(" ████ ", style=style_str)
                        elif h <= t_b + w_b:
                            result.append(" ░░░░ ", style=f"bold {BLUE}")
                        else:
                            result.append("      ")
                        result.append(" ")
                    result.append("\n")

                # Base line
                result.append("   " + "═" * (len(sequence) * 7 - 1) + "\n", style=DIM)

                # Height values below baseline (x-axis), styled per pointer
                result.append("   ", style=DIM)
                for idx, val in enumerate(sequence):
                    style_str = col_styles[idx]
                    s = str(val)
                    label = f" {s:^4} " if len(s) <= 4 else f"{s:^6}"
                    result.append(label, style=style_str)
                    result.append(" ")
                result.append("\n")

                # Index row below heights
                result.append("   ", style=DIM)
                for idx in range(len(sequence)):
                    result.append(f"{idx:^6} ", style=DIM)
                result.append("\n")

        # Comparison line
        if comparison:
            result.append(f"\n  {comparison}\n", style=f"bold {TEAL}")

        # Result display
        res_val = states.get("res_val")
        if res_val is not None:
            var_name, var_data = res_val
            result.append(f"\n  {var_name} = {var_data}\n", style=f"bold {GREEN}")

        # Count lines so get_content_height can return the correct value
        line_count = result.plain.count("\n") + 1
        if line_count != self._content_lines:
            self._content_lines = line_count
            # Schedule a layout refresh so the container re-allocates height
            self.call_after_refresh(self.refresh, layout=True)

        return result


class TwoPointerRenderer:

    def make_widget(self, input_data) -> TwoPointerWidget:
        return TwoPointerWidget(input_data=input_data, id="two-pointer-widget")

    def update_widget(self, widget: TwoPointerWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        POINTER_NAMES = {"left", "right", "l", "r", "slow", "fast", "i", "j", "k", "curr", "low", "mid", "high", "p1", "p2", "p3", "start", "end"}
        pointers = {}
        comparison = ""
        current_sequence = None
        prev_sequence = None
        res_val = None
        
        # 1. Collect all unique variable names across ALL frames
        all_var_names = set()
        for frame in frames:
            locals_val = frame.get("locals", {})
            for k in locals_val.keys():
                if not k.startswith("_"):
                    all_var_names.add(k)
                    
        # 2. Accumulate most recent variable values up to up_to
        accumulated_vars = {}
        for idx, frame in enumerate(frames[:up_to + 1]):
            ft = frame.get("type")
            locals_val = frame.get("locals", {})
            
            # Find the active sequence (list/string/tuple) from local variables
            for key in ("nums", "numbers", "height", "g", "arr", "s"):
                if key in locals_val:
                    sequence_key = key
                    # Keep track of previous sequence state before update
                    if current_sequence is not None and locals_val[key] != current_sequence:
                        prev_sequence = current_sequence
                    current_sequence = locals_val[key]
                    break
                    
            # Accumulate pointer positions
            for name in POINTER_NAMES:
                if name in locals_val:
                    val = locals_val[name]
                    if isinstance(val, int):
                        pointers[name] = val

            # Accumulate other variable values
            for k, v in locals_val.items():
                if not k.startswith("_"):
                    accumulated_vars[k] = v

            # Accumulate res value
            if "res" in locals_val:
                res_val = ("res", locals_val["res"])
            elif "ans" in locals_val:
                res_val = ("ans", locals_val["ans"])

            # Comparison and other message details
            if "sum" in locals_val:
                comparison = f"Current Sum = {locals_val['sum']}"
            elif "curr" in locals_val:
                comparison = f"Current Value = {locals_val['curr']}"
            elif ft == "pointer_compare":
                # Find which variables were compared
                l_val = locals_val.get("left", locals_val.get("l", locals_val.get("slow", locals_val.get("i"))))
                r_val = locals_val.get("right", locals_val.get("r", locals_val.get("fast", locals_val.get("j"))))
                if l_val is not None and r_val is not None:
                    comparison = f"Comparing index {l_val} and index {r_val}"

        # Attach to the current frame so variable_entries can access it
        current_frame = frames[up_to]
        current_frame["accumulated_locals"] = accumulated_vars
        current_frame["all_var_names"] = list(all_var_names)
        current_frame["sequence_key"] = sequence_key

        # Detect if we are on a sorting line
        is_sorting = False
        if current_frame.get("type") == "line" and "filename" in current_frame:
            import linecache
            line_content = linecache.getline(current_frame["filename"], current_frame["lineno"]).strip()
            if any(term in line_content for term in ("nums.sort()", "numbers.sort()", "arr.sort()", "g.sort()")):
                is_sorting = True

        if is_sorting and current_sequence is not None:
            prev_sequence = current_sequence
            if isinstance(current_sequence, str):
                current_sequence = "".join(sorted(current_sequence))
            else:
                current_sequence = sorted(current_sequence)

        return {
            "pointers": pointers,
            "sequence": current_sequence,
            "prev_sequence": prev_sequence,
            "comparison": comparison,
            "is_sorting": is_sorting,
            "step": up_to,
            "res_val": res_val,
            "sequence_key": sequence_key,
            "accumulated_locals": accumulated_vars,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"pointer_compare", "pointer_update", "pointer_found"}
        filtered = []
        line_count = 0
        for f in frames:
            ft = f.get("type")
            if ft in keep_types:
                filtered.append(f)
            elif ft == "line":
                if line_count < 3:
                    filtered.append(f)
                    line_count += 1
        return filtered

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
            (TEAL,    "■", "i / curr / mid pointer position"),
            (YELLOW,  "■", "pointers overlapping"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        accumulated = frame.get("accumulated_locals", frame.get("locals", {}))
        all_vars = frame.get("all_var_names", list(accumulated.keys()))
        sequence_key = frame.get("sequence_key")
        
        entries = []
        pointer_keys = ["i", "j", "k", "left", "right", "l", "r", "slow", "fast", "curr", "low", "mid", "high"]
        
        # Collect pointers first
        for k in pointer_keys:
            if (k in all_vars or k in accumulated) and k != sequence_key:
                val = accumulated.get(k, "—")
                entries.append((k, str(val), get_pointer_color(k)))
                
        # Then other variables (excluding the active sequence variable itself)
        other_keys = sorted([k for k in (all_vars + list(accumulated.keys())) 
                             if k not in pointer_keys and k != sequence_key])
        # Deduplicate other keys while preserving order
        seen = set()
        other_keys = [x for x in other_keys if not (x in seen or seen.add(x))]
        
        for k in other_keys:
            val = accumulated.get(k, "—")
            color = GREEN if k in ("res", "ans") else TEXT
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
