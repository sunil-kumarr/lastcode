"""
tree.py — ASCII binary tree renderer for Textual.
"""

from __future__ import annotations

import ast

from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from lastcode.theme import SURFACE, TEXT, DIM, YELLOW, TEAL, BLUE

COLOR_CURRENT  = "#F7768E"
COLOR_VISITED  = "#A6E3A1"
BG_CURRENT     = "#36202A"
BG_VISITED     = "#1F3428"
BG_NODE        = "#27314A"

COLOR_PATH     = "#CBA6F7"
BG_PATH        = "#2A2040"
BG_TRAIL       = "#13313A"
COLOR_RETURN   = "#FAB387"


# ---------------------------------------------------------------------------
# TreeWidget
# ---------------------------------------------------------------------------


class TreeWidget(Widget):
    DEFAULT_CSS = f"""
    TreeWidget {{
        background: {SURFACE};
        padding: 1 2;
        height: auto;
        min-height: 10;
    }}
    """

    def __init__(self, input_data: list, **kwargs) -> None:
        super().__init__(**kwargs)
        self._input_data = input_data
        self._states: dict = {}

    def update_tree(self, input_data: list, states: dict) -> None:
        self._input_data = input_data
        self._states = states
        self.refresh()

    def render(self) -> RenderResult:
        arr = self._input_data
        if not arr:
            return Text("  (empty tree)", style="dim")

        zoom = float(self._states.get("zoom", 1.0) or 1.0)
        zoom = max(0.6, min(1.8, zoom))
        visited: set[int] = self._states.get("visited", set())
        current: int | None = self._states.get("current")
        motion_trail: list[int] = self._states.get("motion_trail", [])
        trail_set = set(motion_trail)
        edge_note = self._states.get("edge_note", "")
        edge_direction = self._states.get("edge_direction")

        nodes: dict[int, int] = {}  # node_id (1-based) -> val
        for i, v in enumerate(arr):
            if v is not None:
                nodes[i + 1] = v

        if not nodes:
            return Text("  (empty tree)", style="dim")

        from lastcode.renderers.canvas import TextCanvas

        max_depth = max((nid.bit_length() - 1) for nid in nodes)
        
        # Allocate canvas
        slot_w = max(8, int(10 * zoom))
        margin_left = max(12, int(12 * zoom))
        cw = (2 ** max_depth) * slot_w + margin_left
        row_h = max(7, int(10 * zoom))
        ch = (max_depth + 1) * row_h
        
        canvas = TextCanvas(width=cw, height=ch)
        edge_labels: list[tuple[int, int, str]] = []

        transition_note = self._states.get("transition_note")
        if transition_note:
            canvas.draw_text(2, 0, transition_note, style=f"bold {TEAL}")
        
        # Draw the vertical level indicator line on the left side
        for y in range(1, ch - 1):
            canvas.draw_char(9, y, "│", style=DIM)
            
        # Draw horizontal ticks and Level labels for each level
        for depth in range(max_depth + 1):
            cy = depth * row_h + 2
            canvas.draw_char(9, cy, "┤", style=DIM)
            canvas.draw_char(8, cy, "─", style=DIM)
            canvas.draw_char(7, cy, "─", style=DIM)
            canvas.draw_text(2, cy, f"L{depth}" if max_depth >= 3 else f"Level {depth}", style=TEAL)
        
        positions = {}
        for depth in range(max_depth + 1):
            first_id = 2 ** depth
            slots = 2 ** depth
            gap = (2 ** max_depth) / slots
            
            for pos in range(slots):
                nid = first_id + pos
                if nid in nodes:
                    cx = int((pos + 0.5) * gap * slot_w) + margin_left
                    cy = depth * row_h + 2
                    positions[nid] = (cx, cy)

        # Draw edges
        for nid in nodes:
            if nid == 1:
                continue
            parent = nid // 2
            if parent in positions:
                px, py = positions[parent]
                cx, cy = positions[nid]
                
                # Check if this edge is active
                active_edge = self._states.get("active_edge")
                direction = self._states.get("direction")
                is_active = (active_edge is not None) and (
                    active_edge[0] == parent and active_edge[1] == nid
                )

                # Check if this edge is part of the current active path
                active_path = self._states.get("active_path", [])
                problem_type = self._states.get("problem_type", "traversal")
                is_in_path = (problem_type in {"path_exists", "path_sum_paths"}) and (parent in active_path) and (nid in active_path)

                if is_active:
                    if direction == "down":
                        canvas.draw_orthogonal_edge(
                            px, py + 2, cx, cy - 2,
                            arrow="v",
                            style=f"bold {YELLOW}",
                            arrow_color=f"bold {YELLOW}"
                        )
                    else:  # direction == "up"
                        canvas.draw_orthogonal_edge(
                            px, py + 2, cx, cy - 2,
                            arrow="^",
                            style=f"bold {BLUE}",
                            arrow_color=f"bold {BLUE}"
                        )
                elif is_in_path:
                    canvas.draw_orthogonal_edge(
                        px, py + 2, cx, cy - 2,
                        arrow=None,
                        style=f"bold {COLOR_PATH}"
                    )
                elif parent in trail_set and nid in trail_set:
                    canvas.draw_orthogonal_edge(
                        px, py + 2, cx, cy - 2,
                        arrow=None,
                        style=f"bold {TEAL}"
                    )
                else:
                    canvas.draw_orthogonal_edge(px, py + 2, cx, cy - 2, arrow=None, style=DIM)

                if active_edge == (parent, nid) and edge_note:
                    mid_x = (px + cx) // 2
                    mid_y = (py + cy) // 2
                    label_y = mid_y - max(1, row_h // 5) if edge_direction == "down" else mid_y + max(1, row_h // 5)
                    label_x = max(0, min(mid_x - len(edge_note) // 2, cw - len(edge_note) - 1))
                    edge_labels.append((label_x, label_y, edge_note))

        # Draw nodes
        active_path = self._states.get("active_path", [])
        problem_type = self._states.get("problem_type", "traversal")
        for nid, val in nodes.items():
            cx, cy = positions[nid]
            is_in_path = (problem_type in {"path_exists", "path_sum_paths"}) and (nid in active_path)

            if nid == current:
                node_style = f"bold {COLOR_CURRENT} on {BG_CURRENT}"
            elif is_in_path:
                node_style = f"bold {COLOR_PATH} on {BG_PATH}"
            elif nid in trail_set:
                node_style = f"bold {TEAL} on {BG_TRAIL}"
            elif nid in visited:
                node_style = f"bold {COLOR_VISITED} on {BG_VISITED}"
            else:
                node_style = f"bold {TEXT} on {BG_NODE}"

            canvas.draw_node(cx, cy, str(val), style=node_style)

        for label_x, label_y, note in edge_labels:
            canvas.draw_text(label_x, label_y, note, style=f"bold {COLOR_RETURN}")

        result = canvas.render()

        result_list = self._states.get("result", [])
        if result_list:
            result.append("\n  result:  ", style=DIM)
            result.append(" → ".join(str(v) for v in result_list), style=f"bold {YELLOW}")
            result.append("\n")

        step_prompt = self._states.get("step_prompt")
        if step_prompt:
            result.append("  step:  ", style=DIM)
            result.append(step_prompt, style=f"bold {TEAL}")
            result.append("\n")

        return result


# ---------------------------------------------------------------------------
# TreeRenderer
# ---------------------------------------------------------------------------


class TreeRenderer:

    def _problem_kind_from_frame(self, frame: dict) -> str:
        source = f"{frame.get('filename', '')}:{frame.get('fn', '')}".lower()
        kind_map = [
            ("bt_preorder", "preorder"),
            ("bt_inorder", "inorder"),
            ("bt_postorder", "postorder"),
            ("bt_level_order", "level_order"),
            ("zigzag_level_order", "zigzag"),
            ("right_side_view", "right_view"),
            ("invert_tree", "invert"),
            ("flatten_tree", "flatten"),
            ("validate_bst", "validate_bst"),
            ("symmetric_tree", "symmetric"),
            ("lca_bst", "lca"),
            ("lca_bt", "lca"),
            ("bt_max_depth", "max_depth"),
            ("bt_path_sum", "path_exists"),
            ("path_sum_ii", "path_sum_paths"),
            ("sum_numbers", "sum_numbers"),
            ("diameter_bt", "diameter"),
            ("max_path_sum", "max_path_sum"),
            ("kth_smallest_bst", "kth_smallest"),
        ]
        for needle, kind in kind_map:
            if needle in source:
                return kind
        return "traversal"

    def _summarize_value(self, value, *, limit: int = 4) -> str:
        if value is None:
            return "None"
        if hasattr(value, "node_id") and hasattr(value, "val"):
            return str(getattr(value, "val"))
        if isinstance(value, dict):
            if "val" in value and "node_id" in value:
                return str(value["val"])
            return "{" + ", ".join(f"{k}: {self._summarize_value(v, limit=limit)}" for k, v in list(value.items())[:limit]) + ("…" if len(value) > limit else "") + "}"
        if isinstance(value, list):
            if not value:
                return "[]"
            inner = ", ".join(self._summarize_value(v, limit=limit) for v in value[:limit])
            suffix = "…" if len(value) > limit else ""
            return f"[{inner}{', ' if suffix else ''}{suffix}]"
        if isinstance(value, tuple):
            return "(" + ", ".join(self._summarize_value(v, limit=limit) for v in value) + ")"
        return str(value)

    def _frame_summary(self, frame: dict) -> str:
        fn = frame.get("fn", "call")
        locals_val = frame.get("locals", {})
        parts: list[str] = []

        node = locals_val.get("node", locals_val.get("root"))
        if node is not None:
            parts.append(f"node={self._summarize_value(node)}")

        if "curr_sum" in locals_val:
            parts.append(f"sum={self._summarize_value(locals_val['curr_sum'])}")
        if "curr_num" in locals_val:
            parts.append(f"num={self._summarize_value(locals_val['curr_num'])}")
        if "target_sum" in locals_val:
            parts.append(f"target={self._summarize_value(locals_val['target_sum'])}")
        if "k" in locals_val:
            parts.append(f"k={self._summarize_value(locals_val['k'])}")
        if "p" in locals_val:
            parts.append(f"p={self._summarize_value(locals_val['p'])}")
        if "q" in locals_val:
            parts.append(f"q={self._summarize_value(locals_val['q'])}")
        if "depth" in locals_val and fn != "dfs":
            parts.append(f"depth={self._summarize_value(locals_val['depth'])}")
        if "path" in locals_val:
            parts.append(f"path={self._summarize_value(locals_val['path'])}")
        if "low" in locals_val:
            parts.append(f"low={self._summarize_value(locals_val['low'])}")
        if "high" in locals_val:
            parts.append(f"high={self._summarize_value(locals_val['high'])}")
        if "left" in locals_val and isinstance(locals_val.get("left"), (int, float)):
            parts.append(f"L={self._summarize_value(locals_val['left'])}")
        if "right" in locals_val and isinstance(locals_val.get("right"), (int, float)):
            parts.append(f"R={self._summarize_value(locals_val['right'])}")

        if not parts:
            return fn
        return f"{fn}(" + ", ".join(parts) + ")"

    def _frame_return_summary(self, frame: dict, kind: str) -> str:
        locals_val = frame.get("locals", {})
        if kind == "max_depth":
            left = locals_val.get("left")
            right = locals_val.get("right")
            node = locals_val.get("node")
            if node is None:
                return "return 0"
            if left is not None or right is not None:
                return f"return {1 + max(left or 0, right or 0)}"
        for key in ("result", "res", "valid", "is_valid", "found", "answer", "ans", "diameter", "max_sum", "kth", "lca"):
            if key in locals_val:
                return f"return {self._summarize_value(locals_val[key])}"
        if kind in {"preorder", "inorder", "postorder", "level_order", "zigzag", "right_view"}:
            if "node" in locals_val and locals_val["node"] is not None:
                return f"return {self._summarize_value(locals_val['node'])}"
        if kind == "path_exists":
            if "curr_sum" in locals_val and "target_sum" in locals_val:
                return f"return {str(locals_val['curr_sum'] == locals_val['target_sum']).lower()}"
        if kind == "path_sum_paths":
            if "result" in locals_val:
                return f"return {self._summarize_value(locals_val['result'])}"
        if kind == "sum_numbers":
            if "curr_num" in locals_val:
                return f"return {self._summarize_value(locals_val['curr_num'])}"
        if kind == "max_path_sum":
            if "node" in locals_val and locals_val.get("node") is None:
                return "return 0"
            left_gain = locals_val.get("left_gain")
            right_gain = locals_val.get("right_gain")
            node = locals_val.get("node")
            if node is not None and (left_gain is not None or right_gain is not None):
                left_gain = left_gain or 0
                right_gain = right_gain or 0
                if hasattr(node, "val"):
                    return f"return {node.val + max(left_gain, right_gain)}"
        if "curr_num" in locals_val:
            return f"return {self._summarize_value(locals_val['curr_num'])}"
        if "curr_sum" in locals_val:
            return f"return {self._summarize_value(locals_val['curr_sum'])}"
        if "path" in locals_val:
            return f"return {self._summarize_value(locals_val['path'])}"
        if "left" in locals_val and "right" in locals_val:
            return f"return L={self._summarize_value(locals_val['left'])}, R={self._summarize_value(locals_val['right'])}"
        return "return"

    def _frame_stack_entries(self, frames: list[dict], up_to: int, kind: str) -> list[dict]:
        stack_frames: list[dict | None] = []
        stack_meta: list[dict | None] = []
        stack_context = getattr(self, "_stack_context", {})

        for frame in frames[:up_to + 1]:
            depth = max(1, frame.get("dfs_depth", frame.get("depth", 0)))
            stack_frames = stack_frames[:depth]
            stack_meta = stack_meta[:depth]

            if frame.get("type") in {"line", "dfs_return"}:
                locals_val = frame.get("locals", {})
                node = locals_val.get("node", locals_val.get("root"))
                if node is not None:
                    if hasattr(node, "val"):
                        node_val = node.val
                    elif isinstance(node, dict):
                        node_val = node.get("val")
                    else:
                        node_val = node
                    entry = {
                        "depth": depth - 1,
                        "label": self._frame_return_summary(frame, kind) if frame.get("type") == "dfs_return" else self._frame_summary(frame),
                        "node": node_val,
                        "current": False,
                    }
                    if len(stack_meta) < depth:
                        stack_meta.append(entry)
                    else:
                        stack_meta[depth - 1] = entry
            elif frame.get("type") == "node_visit":
                suffix = ""
                if kind == "lca" and (stack_context.get("p") is not None or stack_context.get("q") is not None):
                    suffix = f" (p={stack_context.get('p')}, q={stack_context.get('q')})"
                entry = {
                    "depth": depth - 1,
                    "label": (self._transition_note(frame, kind) or self._frame_summary(frame)) + suffix,
                    "node": frame.get("val"),
                    "current": False,
                }
                if len(stack_meta) < depth:
                    stack_meta.append(entry)
                else:
                    stack_meta[depth - 1] = entry

            stack_frames.append(list(stack_meta))

        current_stack = stack_frames[-1] if stack_frames else []
        for idx, entry in enumerate(current_stack):
            if entry is not None:
                entry["current"] = idx == len(current_stack) - 1
        return [entry for entry in current_stack if entry is not None]

    def _edge_note(self, frame: dict, kind: str, direction: str | None) -> str:
        if not direction:
            if frame.get("type") == "dfs_return":
                return self._frame_return_summary(frame, kind)
            return ""
        if direction == "down":
            if frame.get("type") == "node_visit":
                return self._frame_summary(frame)
            return self._frame_summary(frame)
        if frame.get("type") == "dfs_return":
            return self._frame_return_summary(frame, kind)
        return self._frame_return_summary(frame, kind)

    def _transition_note(self, frame: dict, kind: str) -> str:
        ft = frame.get("type")
        if ft == "node_visit":
            val = self._summarize_value(frame.get("val"))
            if kind in {"level_order", "zigzag"}:
                return f"visit {val}"
            if kind == "flatten":
                return f"touch {val}"
            return f"node {val}"
        if ft == "append_result":
            val = self._summarize_value(frame.get("val"))
            if kind in {"level_order", "zigzag"}:
                return f"append {val} to level"
            return f"append {val}"
        if ft == "dfs_return":
            return self._frame_return_summary(frame, kind)
        locals_val = frame.get("locals", {})
        if kind == "level_order":
            queue = self._summarize_value(locals_val.get("queue"))
            return f"queue {queue}"
        if kind == "zigzag":
            queue = self._summarize_value(locals_val.get("queue"))
            direction = "ltr" if locals_val.get("left_to_right", True) else "rtl"
            return f"{direction} queue {queue}"
        if kind == "flatten":
            curr = self._summarize_value(locals_val.get("curr"))
            prev = self._summarize_value(locals_val.get("prev"))
            return f"rewire curr={curr} prev={prev}"
        if kind == "invert":
            left = self._summarize_value(locals_val.get("left"))
            right = self._summarize_value(locals_val.get("right"))
            return f"swap left={left} right={right}"
        if kind == "path_exists":
            curr_sum = self._summarize_value(locals_val.get("curr_sum"))
            target = self._summarize_value(locals_val.get("target_sum"))
            return f"sum {curr_sum}/{target}"
        if kind == "path_sum_paths":
            curr_sum = self._summarize_value(locals_val.get("curr_sum"))
            target = self._summarize_value(locals_val.get("target_sum"))
            return f"path sum {curr_sum}/{target}"
        return self._frame_summary(frame)

    def _latest_node_label(self, frame: dict) -> str:
        locals_val = frame.get("locals", {})
        node = locals_val.get("node") or locals_val.get("root")
        if hasattr(node, "val"):
            return str(node.val)
        if isinstance(node, dict) and "val" in node:
            return str(node["val"])
        state = getattr(self, "_last_state", {})
        active_val = state.get("active_node_val", "—")
        return "—" if active_val in ("—", None) else str(active_val)

    def _final_answer_text(self, kind: str, frame: dict, state: dict) -> str:
        locals_val = frame.get("locals", {})
        result = state.get("final_answer")
        if result is None:
            for key in ("result", "res", "valid", "is_valid", "found", "answer", "ans", "diameter", "max_sum", "kth", "lca"):
                if key in locals_val:
                    result = locals_val[key]
                    break

        if kind == "invert":
            return f"Final answer: tree inverted"
        if kind == "flatten":
            return f"Final answer: tree flattened into a right-only chain"
        if kind == "validate_bst":
            return f"Final answer: BST valid = {self._summarize_value(result)}"
        if kind == "symmetric":
            return f"Final answer: symmetric = {self._summarize_value(result)}"
        if kind == "path_exists":
            return f"Final answer: path exists = {self._summarize_value(result)}"
        if kind == "max_depth":
            if result is None:
                result = state.get("max_depth_val")
            return f"Final answer: maximum depth = {self._summarize_value(result)}"
        if kind == "diameter":
            return f"Final answer: diameter = {self._summarize_value(result)}"
        if kind == "max_path_sum":
            return f"Final answer: max path sum = {self._summarize_value(result)}"
        if kind == "sum_numbers":
            return f"Final answer: total = {self._summarize_value(result)}"
        if kind == "kth_smallest":
            return f"Final answer: kth smallest = {self._summarize_value(result)}"
        if kind == "lca":
            return f"Final answer: ancestor = {self._summarize_value(result)}"
        return f"Final answer: {self._summarize_value(result)}"

    def make_widget(self, input_data: list | tuple) -> TreeWidget:
        arr = input_data[0] if isinstance(input_data, tuple) else input_data
        return TreeWidget(input_data=arr, id="tree-widget")

    def update_widget(self, widget: TreeWidget, input_data: list | tuple, frame_states: dict) -> None:
        arr = input_data[0] if isinstance(input_data, tuple) else input_data
        widget.update_tree(arr, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        visited: set[int] = set()
        result: list[int] = []
        temp_current = None
        recent_visits: list[int] = []

        active_node_id = "—"
        active_node_val = "—"

        problem_type = self._problem_kind_from_frame(frames[0]) if frames else "traversal"
        left_h = "—"
        right_h = "—"
        curr_sum = "—"
        target_sum = "—"
        max_depth_val = 0
        final_answer = None
        step_prompt = ""
        call_stack_entries: list[dict] = []
        edge_note = ""
        edge_direction = None
        lca_p = None
        lca_q = None
        visit_path: list[int] = []

        # 1. Compute visited set and output result list cumulatively
        current_frames = frames[:up_to + 1]
        for idx, frame in enumerate(current_frames):
            ft = frame.get("type")

            depth_val = frame.get("dfs_depth", frame.get("depth", 0))
            if depth_val > max_depth_val:
                max_depth_val = depth_val

            if ft == "node_visit":
                nid = frame["node_id"]
                if temp_current is not None and nid != temp_current:
                    visited.add(temp_current)
                prev_visit = visit_path[-1] if visit_path else None
                if not visit_path:
                    visit_path = [nid]
                else:
                    prev_parent = prev_visit // 2 if prev_visit else None
                    if prev_visit is not None and nid // 2 == prev_visit:
                        visit_path.append(nid)
                    elif prev_visit is not None and prev_visit // 2 == nid:
                        visit_path[-1] = nid
                    elif prev_parent is not None and nid == prev_parent:
                        visit_path[-1] = nid
                    else:
                        visit_path.append(nid)
                temp_current = nid
                if nid in recent_visits:
                    recent_visits.remove(nid)
                recent_visits.append(nid)
                recent_visits[:] = recent_visits[-4:]
                active_node_id = frame["node_id"]
                active_node_val = frame["val"]
            elif ft == "append_result":
                result.append(frame["val"])
                if temp_current is not None:
                    visited.add(temp_current)
                if temp_current is not None and temp_current in recent_visits:
                    recent_visits.remove(temp_current)
                if temp_current is not None:
                    recent_visits.append(temp_current)
                    recent_visits[:] = recent_visits[-4:]
            elif ft in ("line", "dfs_return"):
                locals_val = frame.get("locals", {})
                if "node" in locals_val:
                    node_var = locals_val["node"]
                    if node_var is not None:
                        if hasattr(node_var, "node_id"):
                            active_node_id = node_var.node_id
                            active_node_val = node_var.val
                        elif isinstance(node_var, dict):
                            active_node_id = node_var.get("node_id")
                            active_node_val = node_var.get("val")
                    else:
                        active_node_id = "—"
                        active_node_val = "None"

                if "left" in locals_val:
                    left_h = locals_val["left"]
                if "right" in locals_val:
                    right_h = locals_val["right"]
                if "curr_sum" in locals_val:
                    curr_sum = locals_val["curr_sum"]
                if "target_sum" in locals_val:
                    target_sum = locals_val["target_sum"]
                if problem_type == "lca":
                    if "p" in locals_val:
                        lca_p = locals_val["p"].val if hasattr(locals_val["p"], "val") else locals_val["p"]
                    if "q" in locals_val:
                        lca_q = locals_val["q"].val if hasattr(locals_val["q"], "val") else locals_val["q"]
            if idx == len(current_frames) - 1:
                locals_val = frame.get("locals", {})
                for key in ("result", "res", "valid", "is_valid", "found", "answer", "ans", "diameter", "max_sum", "kth", "lca"):
                    if key in locals_val:
                        final_answer = locals_val[key]
                        break

        if temp_current is not None:
            visited.add(temp_current)

        if final_answer is None and problem_type == "max_depth":
            final_answer = max_depth_val

        if current_frames:
            step_prompt = self.explain_frame(current_frames[-1], up_to, len(frames))

        # 2. Simulate call stack to track the exact active path, edge, and direction
        stacks = []
        active_stack = []
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            depth = frame.get("dfs_depth", frame.get("depth", 0))
            depth = max(1, depth)
            active_stack = active_stack[:depth]

            if ft in ("line", "dfs_return"):
                locals_val = frame.get("locals", {})
                if "node" in locals_val:
                    node_var = locals_val["node"]
                    nid = None
                    if node_var is not None:
                        if hasattr(node_var, "node_id"):
                            nid = node_var.node_id
                        elif isinstance(node_var, dict):
                            nid = node_var.get("node_id")
                    if len(active_stack) < depth:
                        active_stack.append(nid)
                    else:
                        active_stack[depth - 1] = nid
            elif ft == "node_visit":
                nid = frame.get("node_id")
                if len(active_stack) < depth:
                    active_stack.append(nid)
                else:
                    active_stack[depth - 1] = nid

            clean = [x for x in active_stack if x is not None]
            stacks.append(clean)

        curr_stack = stacks[-1] if stacks else []
        prev_stack = stacks[-2] if len(stacks) >= 2 else []

        current = curr_stack[-1] if curr_stack else None
        active_edge = None
        direction = None

        if len(curr_stack) > len(prev_stack):
            current = curr_stack[-1]
            if len(curr_stack) >= 2:
                active_edge = (curr_stack[-2], curr_stack[-1])
                direction = "down"
        elif len(curr_stack) < len(prev_stack):
            current = curr_stack[-1] if curr_stack else None
            if curr_stack and len(prev_stack) > len(curr_stack):
                active_edge = (curr_stack[-1], prev_stack[len(curr_stack)])
                direction = "up"
        else:
            current = curr_stack[-1] if curr_stack else None
            if len(curr_stack) >= 2:
                active_edge = (curr_stack[-2], curr_stack[-1])
                direction = "down"

        if not active_edge and len(visit_path) >= 2:
            active_edge = (visit_path[-2], visit_path[-1])
            direction = "down"
            if current is None:
                current = visit_path[-1]

        if up_to == len(frames) - 1:
            current = None

        self._stack_context = {"p": lca_p, "q": lca_q}
        call_stack_entries = self._frame_stack_entries(frames, up_to, problem_type)
        edge_direction = direction
        edge_source = current_frames[-1] if current_frames else None
        if (
            edge_source
            and up_to == len(frames) - 1
            and edge_source.get("type") == "line"
            and len(current_frames) >= 2
            and current_frames[-2].get("type") == "dfs_return"
        ):
            edge_source = current_frames[-2]
        edge_note = self._edge_note(edge_source, problem_type, direction) if edge_source else ""
        if not edge_note and problem_type == "lca" and len(visit_path) >= 2:
            edge_note = self._transition_note(current_frames[-1], problem_type)
        transition_note = self._transition_note(current_frames[-1], problem_type) if current_frames else ""

        # Reconstruct node_id -> val from frames to extract path values
        node_id_to_val = {}
        for frame in frames:
            if frame.get("type") == "node_visit":
                node_id_to_val[frame["node_id"]] = frame["val"]

        success_path = getattr(self, "_success_path", [])
        active_path = curr_stack
        if not active_path and problem_type in {"path_exists", "path_sum_paths"}:
            active_path = success_path
        path_vals = [node_id_to_val[nid] for nid in active_path if nid in node_id_to_val]

        self._last_state = {
            "visited": visited,
            "current": current,
            "result": result,
            "active_edge": active_edge,
            "direction": direction,
            "active_node_id": active_node_id,
            "active_node_val": active_node_val,
            "problem_type": problem_type,
            "left_h": left_h,
            "right_h": right_h,
            "curr_sum": curr_sum,
            "target_sum": target_sum,
            "max_depth_val": max_depth_val,
            "active_path": active_path,
            "path_vals": path_vals,
            "motion_trail": recent_visits,
            "final_answer": final_answer,
            "step_prompt": step_prompt,
            "terminal_step": up_to == len(frames) - 1,
            "call_stack_entries": call_stack_entries,
            "edge_note": edge_note,
            "edge_direction": edge_direction,
            "transition_note": transition_note,
            "visit_path": visit_path,
        }
        return self._last_state

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        candidate_frames = [f for f in frames if f.get("type") in {"node_visit", "append_result", "line", "dfs_return"}]

        # Extract target_sum from raw frames
        target_sum = None
        for frame in candidate_frames:
            locals_val = frame.get("locals", {})
            if "target_sum" in locals_val:
                target_sum = locals_val["target_sum"]
                break

        states = []
        visited = set()
        result = []
        temp_current = None
        success_path = []

        stacks = []
        active_stack = []
        for frame in candidate_frames:
            ft = frame.get("type")
            depth = frame.get("dfs_depth", frame.get("depth", 0))
            depth = max(1, depth)
            active_stack = active_stack[:depth]

            if ft in ("line", "dfs_return"):
                locals_val = frame.get("locals", {})
                if "node" in locals_val:
                    node_var = locals_val["node"]
                    nid = None
                    if node_var is not None:
                        if hasattr(node_var, "node_id"):
                            nid = node_var.node_id
                        elif isinstance(node_var, dict):
                            nid = node_var.get("node_id")
                    if len(active_stack) < depth:
                        active_stack.append(nid)
                    else:
                        active_stack[depth - 1] = nid
            elif ft == "node_visit":
                nid = frame.get("node_id")
                if len(active_stack) < depth:
                    active_stack.append(nid)
                else:
                    active_stack[depth - 1] = nid

            clean = [x for x in active_stack if x is not None]
            stacks.append(clean)

            # Track success path when target sum is reached in raw frames
            if target_sum is not None:
                locals_val = frame.get("locals", {})
                c_sum = locals_val.get("curr_sum")
                if c_sum is not None and c_sum == target_sum:
                    success_path = list(clean)

            if ft == "node_visit":
                nid = frame["node_id"]
                if temp_current is not None and nid != temp_current:
                    visited.add(temp_current)
                temp_current = nid
            elif ft == "append_result":
                result.append(frame["val"])
                if temp_current is not None:
                    visited.add(temp_current)

            curr_stack = clean
            prev_stack = stacks[-2] if len(stacks) >= 2 else []

            current = curr_stack[-1] if curr_stack else None
            active_edge = None
            direction = None

            if len(curr_stack) > len(prev_stack):
                current = curr_stack[-1]
                if len(curr_stack) >= 2:
                    active_edge = (curr_stack[-2], curr_stack[-1])
                    direction = "down"
            elif len(curr_stack) < len(prev_stack):
                current = curr_stack[-1] if curr_stack else None
                if curr_stack and len(prev_stack) > len(curr_stack):
                    active_edge = (curr_stack[-1], prev_stack[len(curr_stack)])
                    direction = "up"
            else:
                current = curr_stack[-1] if curr_stack else None
                if len(curr_stack) >= 2:
                    active_edge = (curr_stack[-2], curr_stack[-1])
                    direction = "down"

            states.append((
                frozenset(visited),
                current,
                tuple(result),
                active_edge,
                direction
            ))

        filtered = []
        last_state = None
        for f, state in zip(candidate_frames, states):
            ft = f.get("type")
            if ft in ("node_visit", "append_result"):
                filtered.append(f)
                last_state = state
            else:
                if last_state is None or state != last_state:
                    filtered.append(f)
                    last_state = state

        self._success_path = success_path if target_sum is not None else []
        return filtered

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        state = getattr(self, "_last_state", {})
        kind = state.get("problem_type", "traversal")
        prefix = f"  [{step + 1}/{total}]  "
        if step == total - 1:
            return f"{prefix}{self._final_answer_text(kind, frame, state)}"
        if ft == "node_visit":
            node_val = frame["val"]
            if kind == "preorder":
                return f"{prefix}Enter node {node_val}, record it before children"
            if kind == "inorder":
                return f"{prefix}Go through node {node_val} after the left subtree"
            if kind == "postorder":
                return f"{prefix}Defer node {node_val} until both children are done"
            if kind == "level_order":
                return f"{prefix}Visit node {node_val} at the current BFS level"
            if kind == "zigzag":
                return f"{prefix}Visit node {node_val} and alternate the level direction"
            if kind == "right_view":
                return f"{prefix}Check node {node_val} as the next visible value from the right"
            if kind == "invert":
                return f"{prefix}Swap the children of node {node_val}"
            if kind == "flatten":
                return f"{prefix}Splice node {node_val} into the flattened right chain"
            if kind == "path_exists":
                return f"{prefix}Track running sum through node {node_val}"
            if kind == "path_sum_paths":
                return f"{prefix}Extend the root-to-leaf path with node {node_val}"
            if kind == "max_depth":
                return f"{prefix}Measure the height of node {node_val}'s subtree"
            if kind == "diameter":
                return f"{prefix}Combine the left and right depths through node {node_val}"
            if kind == "max_path_sum":
                return f"{prefix}Combine gains through node {node_val}"
            if kind == "sum_numbers":
                return f"{prefix}Append node {node_val} to the current number"
            if kind == "validate_bst":
                return f"{prefix}Validate node {node_val} against BST bounds"
            if kind == "symmetric":
                return f"{prefix}Compare node {node_val} with its mirror pair"
            if kind == "lca":
                return f"{prefix}Search node {node_val} for the two targets"
            if kind == "kth_smallest":
                return f"{prefix}Inorder visit node {node_val} and count it"
            return f"{prefix}Visiting node {node_val}"
        if ft == "append_result":
            node_val = frame["val"]
            if kind == "right_view":
                return f"{prefix}Recorded {node_val} as the visible value for this level"
            if kind in {"level_order", "zigzag"}:
                return f"{prefix}Added {node_val} to the current level output"
            if kind == "path_sum_paths":
                return f"{prefix}Captured one root-to-leaf path ending at {node_val}"
            if kind == "kth_smallest":
                return f"{prefix}Recorded the kth smallest value {node_val}"
            return f"{prefix}Appended {node_val} to result"
        if ft == "dfs_return":
            locals_val = frame.get("locals", {})
            node_val = self._summarize_value(locals_val.get("node"))
            if kind == "max_depth":
                left_h = self._summarize_value(locals_val.get("left"))
                right_h = self._summarize_value(locals_val.get("right"))
                return f"{prefix}Return height for node {node_val}: left={left_h}, right={right_h}"
            if kind == "max_path_sum":
                left_gain = self._summarize_value(locals_val.get("left_gain"))
                right_gain = self._summarize_value(locals_val.get("right_gain"))
                return f"{prefix}Return best gain for node {node_val}: left={left_gain}, right={right_gain}"
            return f"{prefix}Return from node {node_val}"
        if ft == "line":
            depth = frame.get("dfs_depth", 0)
            level = max(0, depth - 1) if depth > 0 else "—"
            locals_val = frame.get("locals", {})
            if kind == "level_order":
                queue = self._summarize_value(locals_val.get("queue"))
                level_size = locals_val.get("level_size", "—")
                return f"{prefix}Process BFS level {level} with queue {queue} (size {level_size})"
            if kind == "zigzag":
                direction = "left-to-right" if locals_val.get("left_to_right", True) else "right-to-left"
                queue = self._summarize_value(locals_val.get("queue"))
                return f"{prefix}Process zigzag level {level} going {direction}, queue {queue}"
            if kind == "right_view":
                result = self._summarize_value(locals_val.get("result"))
                return f"{prefix}Check whether level {level} already has a visible value: {result}"
            if kind == "invert":
                left = self._summarize_value(locals_val.get("left"))
                right = self._summarize_value(locals_val.get("right"))
                return f"{prefix}Swap left={left} and right={right}"
            if kind == "flatten":
                curr = self._summarize_value(locals_val.get("curr"))
                prev = self._summarize_value(locals_val.get("prev"))
                return f"{prefix}Rewire curr={curr} after prev={prev}"
            if kind == "validate_bst":
                low = self._summarize_value(locals_val.get("low"))
                high = self._summarize_value(locals_val.get("high"))
                return f"{prefix}Check BST bounds low={low}, high={high}"
            if kind == "symmetric":
                left = self._summarize_value(locals_val.get("left"))
                right = self._summarize_value(locals_val.get("right"))
                return f"{prefix}Compare mirror nodes left={left}, right={right}"
            if kind == "lca":
                left = self._summarize_value(locals_val.get("left"))
                right = self._summarize_value(locals_val.get("right"))
                return f"{prefix}Combine subtree results left={left}, right={right}"
            if kind == "max_depth":
                left = self._summarize_value(locals_val.get("left"))
                right = self._summarize_value(locals_val.get("right"))
                return f"{prefix}Compute height from left={left} and right={right}"
            if kind == "path_exists":
                curr_sum = self._summarize_value(locals_val.get("curr_sum"))
                target = self._summarize_value(locals_val.get("target_sum"))
                return f"{prefix}Update running sum {curr_sum} against target {target}"
            if kind == "path_sum_paths":
                curr_sum = self._summarize_value(locals_val.get("curr_sum"))
                target = self._summarize_value(locals_val.get("target_sum"))
                path = self._summarize_value(locals_val.get("path"))
                return f"{prefix}Track path {path} with sum {curr_sum} toward target {target}"
            if kind == "diameter":
                left = self._summarize_value(locals_val.get("left"))
                right = self._summarize_value(locals_val.get("right"))
                return f"{prefix}Update diameter from left={left} and right={right}"
            if kind == "max_path_sum":
                left_gain = self._summarize_value(locals_val.get("left_gain"))
                right_gain = self._summarize_value(locals_val.get("right_gain"))
                max_sum = self._summarize_value(locals_val.get("max_sum"))
                return f"{prefix}Combine gains left={left_gain}, right={right_gain}, best={max_sum}"
            if kind == "sum_numbers":
                curr_num = self._summarize_value(locals_val.get("curr_num"))
                return f"{prefix}Build the current number {curr_num}"
            if kind == "kth_smallest":
                count = self._summarize_value(locals_val.get("count"))
                res = self._summarize_value(locals_val.get("res"))
                return f"{prefix}Count inorder visits {count}, candidate {res}"
            return f"{prefix}Traverse at recursion level {level}"
        return f"{prefix}—"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURRENT, "■", "currently visiting"),
            (TEAL,          "━", "recent motion"),
            (COLOR_VISITED, "■", "visited"),
            (TEXT,          "■", "unvisited"),
            (YELLOW,        "━", "traversing down"),
            (BLUE,          "━", "backtracking up"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        state = getattr(self, "_last_state", {})
        active_val = state.get("active_node_val", "—")
        raw_depth = frame.get("dfs_depth", frame.get("depth", "—"))
        if raw_depth == "—" or raw_depth == 0:
            level_val = "—"
        else:
            try:
                level_val = str(int(raw_depth) - 1)
            except (ValueError, TypeError):
                level_val = "—"

        entries = [
            ("n",   self._summarize_value(active_val),  f"bold {COLOR_CURRENT}" if active_val != "None" and active_val != "—" else DIM),
            ("lvl",  str(level_val),   DIM if level_val == "—" else TEXT),
        ]

        problem_type = state.get("problem_type", "traversal")

        if problem_type == "max_depth":
            left_h = state.get("left_h", "—")
            right_h = state.get("right_h", "—")
            max_depth_val = state.get("max_depth_val", 0)
            entries.append(("Lh", str(left_h), DIM if left_h == "—" else TEXT))
            entries.append(("Rh", str(right_h), DIM if right_h == "—" else TEXT))
            entries.append(("ans", str(max_depth_val), f"bold {YELLOW}"))
        elif problem_type in {"path_exists", "path_sum_paths"}:
            curr_sum = state.get("curr_sum", "—")
            target_sum = state.get("target_sum", "—")
            path_vals = state.get("path_vals", [])
            entries.append(("sum", str(curr_sum), f"bold {YELLOW}" if curr_sum != "—" else DIM))
            entries.append(("target", str(target_sum), TEAL))
            entries.append(("path", self._summarize_value(path_vals), f"bold {COLOR_PATH}" if path_vals else DIM))
        else:
            result_list = state.get("result", [])
            result_str = self._summarize_value(result_list) if result_list else "[]"
            entries.append(("res", result_str, f"bold {YELLOW}" if result_list else DIM))

        final_answer = state.get("final_answer")
        if final_answer is not None:
            entries.append(("ans", self._summarize_value(final_answer), f"bold {TEAL}"))

        return entries

    def parse_input(self, raw: str) -> list | tuple[list, int]:
        parsed = ast.literal_eval(raw.strip())
        if isinstance(parsed, tuple) and len(parsed) == 2 and isinstance(parsed[0], list) and isinstance(parsed[1], int):
            arr, target = parsed
            if len(arr) > 31:
                raise ValueError("Max 31 nodes")
            for v in arr:
                if v is not None and not isinstance(v, int):
                    raise ValueError("Values must be integers or None")
            return parsed

        if not isinstance(parsed, list):
            raise ValueError("Must be a list (level-order) or (list, target) tuple")
        if len(parsed) > 31:
            raise ValueError("Max 31 nodes")
        for v in parsed:
            if v is not None and not isinstance(v, int):
                raise ValueError("Values must be integers or None")
        return parsed

    def serialize_input(self, data: list) -> str:
        return str(data)
