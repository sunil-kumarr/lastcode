"""
tree.py — ASCII binary tree renderer for Textual.
"""

from __future__ import annotations

import ast

from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, YELLOW, TEAL, BLUE

COLOR_CURRENT  = "#F7768E"
COLOR_VISITED  = "#9ECE6A"
BG_CURRENT     = "#321820"
BG_VISITED     = "#253320"
BG_NODE        = "#2D3250"


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

        visited: set[int] = self._states.get("visited", set())
        current: int | None = self._states.get("current")

        nodes: dict[int, int] = {}  # node_id (1-based) -> val
        for i, v in enumerate(arr):
            if v is not None:
                nodes[i + 1] = v

        if not nodes:
            return Text("  (empty tree)", style="dim")

        from neonodes.renderers.canvas import TextCanvas

        max_depth = max((nid.bit_length() - 1) for nid in nodes)
        
        # Allocate canvas
        slot_w = 8
        cw = (2 ** max_depth) * slot_w
        ch = (max_depth + 1) * 6
        
        canvas = TextCanvas(width=cw, height=ch)
        
        positions = {}
        for depth in range(max_depth + 1):
            first_id = 2 ** depth
            slots = 2 ** depth
            gap = (2 ** max_depth) / slots
            
            for pos in range(slots):
                nid = first_id + pos
                if nid in nodes:
                    cx = int((pos + 0.5) * gap * slot_w)
                    cy = depth * 5 + 2
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
                else:
                    canvas.draw_orthogonal_edge(px, py + 2, cx, cy - 2, arrow=None, style=DIM)

        # Draw nodes
        for nid, val in nodes.items():
            cx, cy = positions[nid]
            if nid == current:
                node_style = f"bold {COLOR_CURRENT} on {BG_CURRENT}"
            elif nid in visited:
                node_style = f"bold {COLOR_VISITED} on {BG_VISITED}"
            else:
                node_style = f"bold {TEXT} on {BG_NODE}"
                
            canvas.draw_node(cx, cy, str(val), style=node_style)

        result = canvas.render()

        result_list = self._states.get("result", [])
        if result_list:
            result.append("\n  result:  ", style=DIM)
            result.append(" → ".join(str(v) for v in result_list), style=f"bold {YELLOW}")
            result.append("\n")

        return result


# ---------------------------------------------------------------------------
# TreeRenderer
# ---------------------------------------------------------------------------


class TreeRenderer:

    def make_widget(self, input_data: list) -> TreeWidget:
        return TreeWidget(input_data=input_data, id="tree-widget")

    def update_widget(self, widget: TreeWidget, input_data: list, frame_states: dict) -> None:
        widget.update_tree(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        visited: set[int] = set()
        result: list[int] = []
        temp_current = None

        active_node_id = "—"
        active_node_val = "—"

        # 1. Compute visited set and output result list cumulatively
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            if ft == "node_visit":
                nid = frame["node_id"]
                if temp_current is not None and nid != temp_current:
                    visited.add(temp_current)
                temp_current = nid
                active_node_id = frame["node_id"]
                active_node_val = frame["val"]
            elif ft == "append_result":
                result.append(frame["val"])
                if temp_current is not None:
                    visited.add(temp_current)
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

        # 2. Simulate call stack to track the exact active path, edge, and direction
        stacks = []
        active_stack = []
        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            depth = frame.get("dfs_depth", frame.get("depth", 0))
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

        self._last_state = {
            "visited": visited,
            "current": current,
            "result": result,
            "active_edge": active_edge,
            "direction": direction,
            "active_node_id": active_node_id,
            "active_node_val": active_node_val
        }
        return self._last_state

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        candidate_frames = [f for f in frames if f.get("type") in {"node_visit", "append_result", "line"}]

        states = []
        visited = set()
        result = []
        temp_current = None

        stacks = []
        active_stack = []
        for frame in candidate_frames:
            ft = frame.get("type")
            depth = frame.get("dfs_depth", frame.get("depth", 0))
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

        return filtered

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        if ft == "node_visit":
            return f"{prefix}Visiting node {frame['val']} — process left subtree first (inorder)"
        if ft == "append_result":
            return f"{prefix}Appended {frame['val']} to result"
        if ft == "line":
            depth = frame.get("dfs_depth", 0)
            return f"{prefix}traverse() at recursion depth {depth}"
        return f"{prefix}—"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURRENT, "■", "currently visiting"),
            (COLOR_VISITED, "■", "visited"),
            (TEXT,          "■", "unvisited"),
            (YELLOW,        "━", "traversing down"),
            (BLUE,          "━", "backtracking up"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        state = getattr(self, "_last_state", {})
        active_id = state.get("active_node_id", "—")
        active_val = state.get("active_node_val", "—")

        # Format the accumulated result list
        result_list = state.get("result", [])
        result_str = str(result_list) if result_list else "[]"

        depth = frame.get("dfs_depth", frame.get("depth", "—"))

        return [
            ("node",   str(active_val),  f"bold {COLOR_CURRENT}" if active_val != "None" else DIM),
            ("id",     str(active_id),   TEAL),
            ("depth",  str(depth),       DIM),
            ("result", result_str,       f"bold {YELLOW}" if result_list else DIM),
        ]

    def parse_input(self, raw: str) -> list:
        parsed = ast.literal_eval(raw.strip())
        if not isinstance(parsed, list):
            raise ValueError("Must be a list (level-order)")
        if len(parsed) > 15:
            raise ValueError("Max 15 nodes")
        for v in parsed:
            if v is not None and not isinstance(v, int):
                raise ValueError("Values must be integers or None")
        return parsed

    def serialize_input(self, data: list) -> str:
        return str(data)
