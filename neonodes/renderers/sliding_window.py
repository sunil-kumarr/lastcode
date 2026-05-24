"""
sliding_window.py — Renderer for Sliding Window problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_L   = "#F7768E"   # Pinkish-red for left pointer
COLOR_R   = "#7AA2F7"   # Blue for right pointer
COLOR_WIN = "#9ECE6A"   # Green for window elements
BG_WIN    = "#1E3322"   # Deep green background inside window
BG_L      = "#321820"   # Dark pink background at left pointer
BG_R      = "#1E2A3D"   # Dark blue background at right pointer
BG_BOTH   = "#3D351E"   # Dark yellow when both pointers overlap
BG_CELL   = "#2D3250"   # Default cell background


def _format_window_state(locals_val: dict, sequence_key: str | None) -> str:
    """Build a concise, human-readable window-state string."""
    parts = []

    if "curr_sum" in locals_val:
        parts.append(f"curr_sum = {locals_val['curr_sum']}")
    if "target" in locals_val and locals_val.get("target") is not None:
        parts.append(f"target = {locals_val['target']}")
    if "min_len" in locals_val:
        v = locals_val["min_len"]
        parts.append(f"min_len = {'∞' if v == float('inf') else v}")
    if "max_len" in locals_val:
        parts.append(f"max_len = {locals_val['max_len']}")
    if "max_fruits" in locals_val:
        parts.append(f"max_fruits = {locals_val['max_fruits']}")
    if "max_count" in locals_val:
        parts.append(f"max_count = {locals_val['max_count']}")
    if "zeros" in locals_val:
        parts.append(f"zeros = {locals_val['zeros']}")
    if "formed" in locals_val:
        parts.append(f"formed = {locals_val['formed']}")
    if "required" in locals_val:
        parts.append(f"required = {locals_val['required']}")

    # Character-frequency maps — render as compact "a:2  b:1" format
    for key in ("char_map", "counts", "window_counts", "sc", "c2"):
        if key in locals_val and isinstance(locals_val[key], dict):
            d = {k: v for k, v in locals_val[key].items() if v != 0}
            if d:
                inner = "  ".join(f"{k}:{v}" for k, v in sorted(d.items()))
                parts.append(f"{key}{{ {inner} }}")
            break

    return "  │  ".join(parts)


class SlidingWindowWidget(Widget):
    DEFAULT_CSS = f"""
    SlidingWindowWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 10;
    }}
    """

    def get_content_height(self, container, viewport, width) -> int:
        """Tell Textual how many rows we need so the widget is never clipped."""
        return max(10, getattr(self, "_content_lines", 10))

    def __init__(self, input_data, **kwargs) -> None:
        super().__init__(**kwargs)
        self._input_data = input_data
        self._states: dict = {}
        self._content_lines = 10

    def update_state(self, input_data, states: dict) -> None:
        self._input_data = input_data
        self._states = states
        self.refresh()

    def render(self) -> RenderResult:
        data = self._input_data
        states = self._states

        # Unpack input: (sequence, target) or just sequence
        if isinstance(data, tuple) and len(data) == 2:
            raw_sequence, target = data
        else:
            raw_sequence, target = data, None

        # Use the sequence from accumulated states if available
        sequence_key = states.get("sequence_key")
        sequence = states.get("sequence", raw_sequence)
        secondary = states.get("secondary")  # e.g. pattern string for permutation

        # Pointer positions
        pointers = states.get("pointers", {})
        l_idx = pointers.get("left", pointers.get("l"))
        r_idx = pointers.get("right", pointers.get("r"))

        window_state_str = states.get("window_state", "")
        found = states.get("found", False)

        result = Text()
        CELL_W = 6
        SEP    = "─" * CELL_W
        n      = len(sequence)

        # ── Target / secondary string header ───────────────────────────
        if secondary is not None:
            result.append(f"  Pattern: ", style=f"bold {DIM}")
            result.append(f"{secondary}\n\n", style=f"bold {YELLOW}")
        elif target is not None:
            result.append(f"  Target: ", style=f"bold {DIM}")
            result.append(f"{target}\n\n", style=f"bold {YELLOW}")

        # ── Window bracket row above the array ─────────────────────────
        has_window = (l_idx is not None and r_idx is not None and l_idx <= r_idx)
        if has_window:
            result.append("   ", style=DIM)  # 3-char prefix
            for idx in range(n):
                if idx == l_idx and idx == r_idx:
                    result.append(f"{'[L=R]':^6} ", style=f"bold {YELLOW}")
                elif idx == l_idx:
                    result.append(f"{'L':^6} ", style=f"bold {COLOR_L}")
                elif idx == r_idx:
                    result.append(f"{'R':^6} ", style=f"bold {COLOR_R}")
                elif l_idx < idx < r_idx:
                    result.append(f"{'·':^6} ", style=f"bold {COLOR_WIN}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")

            # Bracket line: ┌──── ... ────┐
            result.append("   ", style=DIM)
            for idx in range(n):
                if idx == l_idx and idx == r_idx:
                    result.append(f"{'╞' + '═'*(CELL_W-2) + '╡'} ", style=f"bold {YELLOW}")
                elif idx == l_idx:
                    result.append(f"┌{'─'*(CELL_W-1)} ", style=f"bold {COLOR_L}")
                elif idx == r_idx:
                    result.append(f"{'─'*(CELL_W-1)}┐ ", style=f"bold {COLOR_R}")
                elif l_idx < idx < r_idx:
                    result.append(f"{'─'*CELL_W} ", style=f"bold {COLOR_WIN}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")

        # ── Index header ───────────────────────────────────────────────
        result.append("   ", style=DIM)
        for idx in range(n):
            result.append(f"{idx:^6} ", style=DIM)
        result.append("\n")

        # ── Top border ─────────────────────────────────────────────────
        result.append("  ┌", style=DIM)
        for idx in range(n):
            result.append(SEP, style=DIM)
            result.append("┬" if idx < n - 1 else "┐", style=DIM)
        result.append("\n")

        # ── Values row ─────────────────────────────────────────────────
        result.append("  │", style=DIM)
        for idx, val in enumerate(sequence):
            label = f" {str(val):^4} "
            is_l = (idx == l_idx)
            is_r = (idx == r_idx)
            in_win = has_window and (l_idx <= idx <= r_idx)

            if is_l and is_r:
                style = f"bold {YELLOW} on {BG_BOTH}"
            elif is_l:
                style = f"bold {COLOR_L} on {BG_L}"
            elif is_r:
                style = f"bold {COLOR_R} on {BG_R}"
            elif in_win:
                style = f"bold {COLOR_WIN} on {BG_WIN}"
            else:
                style = f"{TEXT} on {BG_CELL}"

            result.append(label, style=style)
            result.append("│", style=DIM)
        result.append("\n")

        # ── Bottom border ──────────────────────────────────────────────
        result.append("  └", style=DIM)
        for idx in range(n):
            result.append(SEP, style=DIM)
            result.append("┴" if idx < n - 1 else "┘", style=DIM)
        result.append("\n")

        # ── Closing bracket row below the array ────────────────────────
        if has_window:
            result.append("   ", style=DIM)
            for idx in range(n):
                if idx == l_idx and idx == r_idx:
                    result.append(f"{'╞' + '═'*(CELL_W-2) + '╡'} ", style=f"bold {YELLOW}")
                elif idx == l_idx:
                    result.append(f"└{'─'*(CELL_W-1)} ", style=f"bold {COLOR_L}")
                elif idx == r_idx:
                    result.append(f"{'─'*(CELL_W-1)}┘ ", style=f"bold {COLOR_R}")
                elif l_idx < idx < r_idx:
                    result.append(f"{'─'*CELL_W} ", style=f"bold {COLOR_WIN}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")

        # ── Pointer arrow row ──────────────────────────────────────────
        if l_idx is not None or r_idx is not None:
            result.append("   ", style=DIM)
            for idx in range(n):
                is_l = (idx == l_idx)
                is_r = (idx == r_idx)
                if is_l and is_r:
                    result.append(f"{'↑':^6} ", style=f"bold {YELLOW}")
                elif is_l:
                    result.append(f"{'↑':^6} ", style=f"bold {COLOR_L}")
                elif is_r:
                    result.append(f"{'↑':^6} ", style=f"bold {COLOR_R}")
                else:
                    result.append("       ", style=DIM)
            result.append("\n")

            # ── Pointer label rows (stacked if overlapping) ──────────
            labels_by_col = [[] for _ in range(n)]
            if l_idx is not None and 0 <= l_idx < n:
                labels_by_col[l_idx].append(("left", COLOR_L))
            if r_idx is not None and r_idx != l_idx and 0 <= r_idx < n:
                labels_by_col[r_idx].append(("right", COLOR_R))
            elif r_idx is not None and r_idx == l_idx and 0 <= r_idx < n:
                labels_by_col[r_idx] = [("left", COLOR_L), ("right", COLOR_R)]

            max_depth = max((len(v) for v in labels_by_col), default=0)
            for d in range(max_depth):
                result.append("   ", style=DIM)
                for idx in range(n):
                    entries = labels_by_col[idx]
                    if d < len(entries):
                        name, color = entries[d]
                        result.append(f"{name:^6} ", style=f"bold {color}")
                    else:
                        result.append("       ", style=DIM)
                result.append("\n")

        # ── Window state info line ─────────────────────────────────────
        if window_state_str:
            state_color = GREEN if found else TEAL
            result.append(f"\n  {'✓ ' if found else ''}Window  {window_state_str}\n",
                          style=f"bold {state_color}")

        # ── Result variable display ────────────────────────────────────
        res_val = states.get("res_val")
        if res_val is not None:
            var_name, var_data = res_val
            display = "∞" if var_data == float("inf") else str(var_data)
            result.append(f"\n  {var_name} = {display}\n", style=f"bold {GREEN}")

        # Count lines for get_content_height
        line_count = result.plain.count("\n") + 1
        if line_count != self._content_lines:
            self._content_lines = line_count
            self.call_after_refresh(self.refresh, layout=True)

        return result


class SlidingWindowRenderer:

    def make_widget(self, input_data) -> SlidingWindowWidget:
        return SlidingWindowWidget(input_data=input_data, id="sliding-window-widget")

    def update_widget(self, widget: SlidingWindowWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        POINTER_NAMES = {"left", "right", "l", "r"}

        pointers = {}
        window_state_str = ""
        current_sequence = None
        sequence_key = None
        secondary = None
        res_val = None
        found = False

        # 1. Collect ALL variable names across all frames
        all_var_names: set[str] = set()
        for frame in frames:
            for k in frame.get("locals", {}):
                if not k.startswith("_"):
                    all_var_names.add(k)

        # 2. Accumulate locals up to current step
        accumulated_vars: dict = {}
        for frame in frames[: up_to + 1]:
            locals_val = frame.get("locals", {})

            # Detect primary sequence
            for key in ("s", "s2", "nums", "arr", "fruits"):
                if key in locals_val and isinstance(locals_val[key], (str, list)):
                    if sequence_key is None or key in ("s2", "nums"):
                        sequence_key = key
                    current_sequence = locals_val[key]
                    break

            # Detect secondary (pattern) string — e.g. s1 in permutation_in_string
            for key in ("s1", "p", "t"):
                if key in locals_val and isinstance(locals_val[key], str):
                    secondary = locals_val[key]
                    break

            # Accumulate pointer positions
            for name in POINTER_NAMES:
                if name in locals_val and isinstance(locals_val[name], int):
                    pointers[name] = locals_val[name]

            # Accumulate result
            for rk in ("ans", "res", "max_len", "min_len", "max_fruits"):
                if rk in locals_val:
                    v = locals_val[rk]
                    if not isinstance(v, (dict, list)) or rk in ("res",):
                        res_val = (rk, v)

            # Window state string
            window_state_str = _format_window_state(locals_val, sequence_key)

            # found flag
            if frame.get("type") == "window_found":
                found = True
            elif frame.get("type") == "window_update":
                found = False

            # Accumulate all vars
            for k, v in locals_val.items():
                if not k.startswith("_"):
                    accumulated_vars[k] = v

        # Attach accumulated data to current frame for variable_entries
        current_frame = frames[up_to]
        current_frame["accumulated_locals"] = accumulated_vars
        current_frame["all_var_names"] = list(all_var_names)
        current_frame["sequence_key"] = sequence_key

        return {
            "pointers": pointers,
            "sequence": current_sequence,
            "sequence_key": sequence_key,
            "secondary": secondary,
            "window_state": window_state_str,
            "found": found,
            "res_val": res_val,
            "accumulated_locals": accumulated_vars,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"window_check", "window_update", "window_found"}
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
        ft   = frame.get("type")
        locs = frame.get("locals", {})
        prefix = f"  [{step + 1}/{total}]  "

        l = locs.get("left", locs.get("l", "—"))
        r = locs.get("right", locs.get("r", "—"))
        size = (r - l + 1) if isinstance(l, int) and isinstance(r, int) else "?"

        if ft == "window_check":
            return f"{prefix}Expanding →  right moves to {r}  |  window [{l}..{r}]  size={size}"
        if ft == "window_update":
            return f"{prefix}Shrinking ←  left moves to {l}  |  window [{l}..{r}]  size={size}"
        if ft == "window_found":
            return f"{prefix}✓ Valid window found!  [{l}..{r}]  size={size}"

        return f"{prefix}Initializing  (left={l}, right={r})"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_L,   "■", "left  — left window boundary"),
            (COLOR_R,   "■", "right — right window boundary"),
            (COLOR_WIN, "■", "elements inside the sliding window"),
            (GREEN,     "■", "result / answer variable"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        accumulated  = frame.get("accumulated_locals", frame.get("locals", {}))
        all_vars     = frame.get("all_var_names", list(accumulated.keys()))
        sequence_key = frame.get("sequence_key")

        POINTER_KEYS = {"left", "right", "l", "r"}
        RESULT_KEYS  = {"ans", "res", "max_len", "min_len", "max_fruits"}
        WINDOW_KEYS  = {"curr_sum", "char_map", "counts", "window_counts",
                        "max_count", "zeros", "formed", "required", "sc", "c2", "c1"}
        SKIP_KEYS    = {"s", "s1", "s2", "nums", "arr", "fruits", "p", "t",
                        sequence_key, "char", "i", "c"}

        entries = []

        # 1. Pointer variables
        for k in ("left", "right", "l", "r"):
            if k in all_vars and k not in SKIP_KEYS:
                val = accumulated.get(k, "—")
                color = COLOR_L if k in ("left", "l") else COLOR_R
                entries.append((k, str(val), color))

        # 2. Window state variables
        for k in sorted(all_vars):
            if k in WINDOW_KEYS and k not in SKIP_KEYS:
                val = accumulated.get(k, "—")
                if isinstance(val, dict):
                    clean = {kk: vv for kk, vv in val.items() if vv != 0}
                    val_str = "{ " + "  ".join(f"{kk}:{vv}" for kk, vv in sorted(clean.items())) + " }" if clean else "{}"
                else:
                    val_str = "∞" if val == float("inf") else str(val)
                entries.append((k, val_str, TEAL))

        # 3. Result variables
        for k in sorted(all_vars):
            if k in RESULT_KEYS and k not in SKIP_KEYS:
                val = accumulated.get(k, "—")
                val_str = "∞" if val == float("inf") else str(val)
                entries.append((k, val_str, GREEN))

        # 4. Target / other scalar variables
        already = {e[0] for e in entries} | SKIP_KEYS | POINTER_KEYS | RESULT_KEYS | WINDOW_KEYS
        for k in sorted(all_vars):
            if k not in already and not k.startswith("_"):
                val = accumulated.get(k, "—")
                if not isinstance(val, (list, dict, set)):
                    entries.append((k, str(val), YELLOW))

        return entries if entries else [("—", "—", DIM)]

    def parse_input(self, raw: str) -> object:
        raw = raw.strip()
        try:
            parsed = ast.literal_eval(raw)
            return parsed
        except Exception:
            pass
        return raw

    def serialize_input(self, data) -> str:
        if isinstance(data, str):
            return data
        return str(data)
