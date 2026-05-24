"""
linked_list.py — Renderer for Linked List problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED

COLOR_CURR = "#F7768E"     # Pinkish-red for current pointer node
COLOR_HEAD = "#7AA2F7"     # Blue for head node
COLOR_NODE = "#9ECE6A"     # Green for standard nodes
BG_NODE = "#321820"        # Dark pink/red background
BG_CELL = "#2D3250"        # Default cell background


class RichCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[" "] * width for _ in range(height)]
        self.styles = [[TEXT] * width for _ in range(height)]

    def set(self, x: int, y: int, char: str, style: str = TEXT):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = char
            self.styles[y][x] = style

    def write_string(self, x: int, y: int, s: str, style: str = TEXT):
        for i, char in enumerate(s):
            self.set(x + i, y, char, style)

    def render(self) -> Text:
        result = Text()
        for y in range(self.height):
            line_text = Text()
            # Trim trailing spaces
            row_len = self.width
            while row_len > 0 and self.grid[y][row_len - 1] == " ":
                row_len -= 1
            
            curr_style = None
            span_start = 0
            for x in range(row_len):
                char = self.grid[y][x]
                style = self.styles[y][x]
                if style != curr_style:
                    if x > span_start:
                        span_str = "".join(self.grid[y][span_start:x])
                        line_text.append(span_str, style=curr_style)
                    curr_style = style
                    span_start = x
            if row_len > span_start:
                span_str = "".join(self.grid[y][span_start:row_len])
                line_text.append(span_str, style=curr_style)
            
            result.append(line_text)
            result.append("\n")
        return result


class LinkedListWidget(Widget):
    DEFAULT_CSS = f"""
    LinkedListWidget {{
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
        states = self._states
        nodes = states.get("nodes", [])       # List of dicts: {"id":..., "val":..., "is_curr":..., "is_head":...}
        edges = states.get("edges", [])       # List of tuples: (from_id, to_id, is_random)
        pointers = states.get("pointers", {})  # Dict: node_id -> list of pointer names
        operation = states.get("operation", "")

        result = Text()

        # 1. Operation Notice
        if operation:
            result.append(f"  Operation: {operation}\n\n", style=f"bold {YELLOW}")
        else:
            result.append("\n")

        if not nodes:
            result.append("  (empty list)", style="dim")
            return result

        # Group nodes by chain index
        chains = {}
        for node in nodes:
            c_idx = node.get("chain_idx", 0)
            if c_idx not in chains:
                chains[c_idx] = []
            chains[c_idx].append(node)

        # Sort nodes within each chain
        for c_idx in chains:
            chains[c_idx].sort(key=lambda n: n.get("seq_idx", 0))

        # Max width & height calculation
        max_width = max(100, max(len(nodes) * 11 + 15 for nodes in chains.values()))
        max_height = len(chains) * 8

        canvas = RichCanvas(width=max_width, height=max_height)

        for c_idx, chain_nodes in sorted(chains.items()):
            base_y = c_idx * 8
            
            # Header label for multiple chains
            if len(chains) > 1:
                canvas.write_string(0, base_y + 1, f"List {c_idx + 1}:", style=f"bold {BLUE}")
                start_x = 10
            else:
                start_x = 2

            cycle_detected = None
            visited_nids = set()

            for idx, node in enumerate(chain_nodes):
                nid = node["id"]
                node_x = start_x + idx * 9
                
                # Check for cycle next link
                next_nid = None
                for from_id, to_id, is_random in edges:
                    if from_id == nid and not is_random:
                        next_nid = to_id
                        break
                
                # Render node box
                if node.get("is_curr"):
                    box_style = f"bold {COLOR_CURR}"
                    bg_style = f"on {BG_NODE}"
                elif node.get("is_head"):
                    box_style = f"bold {COLOR_HEAD}"
                    bg_style = f"on {BG_NODE}"
                else:
                    box_style = f"bold {TEXT}"
                    bg_style = f"on {BG_CELL}"

                # Draw node box borders & value
                canvas.write_string(node_x, base_y, "┌───┐", style=DIM)
                val_str = f"{str(node['val']):^3}"
                canvas.set(node_x, base_y + 1, "│", style=DIM)
                canvas.write_string(node_x + 1, base_y + 1, val_str, style=f"{box_style} {bg_style}")
                canvas.set(node_x + 4, base_y + 1, "│", style=DIM)
                canvas.write_string(node_x, base_y + 2, "└───┘", style=DIM)

                # Draw pointer labels under this node
                pt_list = pointers.get(nid, [])
                if pt_list:
                    clean_names = [n for n in pt_list if n not in ("self", "node_data", "nxt", "nxt_id", "v")]
                    if clean_names:
                        pt_text = ", ".join(clean_names)
                        ptr_x = node_x + 2 - len(pt_text) // 2
                        if ptr_x < 0: ptr_x = 0
                        canvas.set(node_x + 2, base_y + 3, "↑", style=f"bold {YELLOW}")
                        canvas.write_string(ptr_x, base_y + 4, pt_text, style=f"bold {YELLOW}")

                visited_nids.add(nid)

                # Render next link
                if next_nid is not None:
                    if next_nid in visited_nids:
                        target_idx = -1
                        for t_i, t_node in enumerate(chain_nodes):
                            if t_node["id"] == next_nid:
                                target_idx = t_i
                                break
                        if target_idx != -1:
                            cycle_detected = (idx, target_idx)
                        break
                    else:
                        canvas.write_string(node_x + 5, base_y + 1, "──→ ", style=COLOR_NODE)
                else:
                    canvas.write_string(node_x + 5, base_y + 1, "──→ NULL", style=f"bold {RED}")

            if cycle_detected is not None:
                from_idx, to_idx = cycle_detected
                from_col = start_x + from_idx * 9 + 2
                to_col = start_x + to_idx * 9 + 2
                
                arrow_y = base_y + 5
                line_y = base_y + 6
                
                canvas.set(to_col, arrow_y, "▲", style=f"bold {RED}")
                canvas.set(from_col, arrow_y, "│", style=f"bold {RED}")
                
                canvas.set(to_col, line_y, "└", style=f"bold {RED}")
                canvas.set(from_col, line_y, "┘", style=f"bold {RED}")
                for col in range(to_col + 1, from_col):
                    canvas.set(col, line_y, "─", style=f"bold {RED}")
                canvas.write_string(from_col + 2, line_y, " (cycle)", style=f"bold {RED}")

        result.append(canvas.render())

        # Render random edges if any (Copy Random List)
        random_edges = [edge for edge in edges if edge[2]]
        if random_edges:
            result.append("\n  Random Pointers:\n", style=f"bold {DIM}")
            for from_id, to_id, _ in random_edges:
                from_val = "None"
                to_val = "None"
                for node in nodes:
                    if node["id"] == from_id:
                        from_val = str(node["val"])
                    if node["id"] == to_id:
                        to_val = str(node["val"])
                result.append(f"    Node({from_val}) ", style=COLOR_CURR)
                result.append("──random──→ ", style=RED)
                result.append(f"Node({to_val})\n", style=COLOR_HEAD)

        # Count lines for get_content_height
        line_count = result.plain.count("\n") + 1
        if line_count != self._content_lines:
            self._content_lines = line_count
            self.call_after_refresh(self.refresh, layout=True)

        return result


class LinkedListRenderer:

    def make_widget(self, input_data) -> LinkedListWidget:
        return LinkedListWidget(input_data=input_data, id="linked-list-widget")

    def update_widget(self, widget: LinkedListWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        if not frames or up_to >= len(frames):
            return {}

        # 1. Collect ALL variable names across all frames
        all_var_names: set[str] = set()
        for frame in frames:
            for k in frame.get("locals", {}):
                if not k.startswith("_"):
                    all_var_names.add(k)

        # 2. Accumulate locals up to current step
        accumulated_vars: dict = {}
        for frame in frames[:up_to + 1]:
            locals_val = frame.get("locals", {})
            for k, v in locals_val.items():
                if not k.startswith("_"):
                    accumulated_vars[k] = v

        current_frame = frames[up_to]
        current_frame["accumulated_locals"] = accumulated_vars
        current_frame["all_var_names"] = list(all_var_names)

        # Reconstruct nodes and edges from the accumulated locals
        node_objs = {}
        ptr_names = {}

        for k, v in accumulated_vars.items():
            if v is not None and (hasattr(v, "val") or (isinstance(v, dict) and "val" in v)):
                nid = id(v) if not isinstance(v, dict) else v.get("node_id", id(v))
                if isinstance(v, dict):
                    node_objs[nid] = v
                else:
                    node_objs[nid] = {
                        "node_id": nid,
                        "val": getattr(v, "val"),
                        "next": getattr(v, "next", None),
                        "random": getattr(v, "random", None)
                    }
                
                if nid not in ptr_names:
                    ptr_names[nid] = []
                ptr_names[nid].append(k)

        visited = set()
        ordered_nodes = []
        edges = []

        # Find potential heads
        heads = []
        for nid, ptrs in ptr_names.items():
            if any("head" in p for p in ptrs):
                heads.append(nid)

        other_ptrs = [nid for nid in node_objs if nid not in heads]
        start_nodes = heads + other_ptrs

        chain_idx = 0
        for start_id in start_nodes:
            if start_id in visited:
                continue

            curr_id = start_id
            seq_idx = 0
            while curr_id is not None and curr_id in node_objs:
                if curr_id in visited:
                    break

                visited.add(curr_id)
                node_data = node_objs[curr_id]

                is_curr = any(p in ("curr", "current", "node") for p in ptr_names.get(curr_id, []))
                is_head = any("head" in p for p in ptr_names.get(curr_id, []))

                ordered_nodes.append({
                    "id": curr_id,
                    "val": node_data["val"],
                    "is_curr": is_curr,
                    "is_head": is_head,
                    "chain_idx": chain_idx,
                    "seq_idx": seq_idx,
                })

                nxt = node_data.get("next")
                if nxt is not None:
                    nxt_id = id(nxt) if not isinstance(nxt, dict) else nxt.get("node_id", id(nxt))
                    if nxt_id not in node_objs:
                        if isinstance(nxt, dict):
                            node_objs[nxt_id] = nxt
                        else:
                            node_objs[nxt_id] = {
                                "node_id": nxt_id,
                                "val": getattr(nxt, "val"),
                                "next": getattr(nxt, "next", None),
                                "random": getattr(nxt, "random", None)
                            }
                    edges.append((curr_id, nxt_id, False))
                    curr_id = nxt_id
                else:
                    edges.append((curr_id, None, False))
                    curr_id = None

                rnd = node_data.get("random")
                if rnd is not None:
                    rnd_id = id(rnd) if not isinstance(rnd, dict) else rnd.get("node_id", id(rnd))
                    if rnd_id not in node_objs:
                        if isinstance(rnd, dict):
                            node_objs[rnd_id] = rnd
                        else:
                            node_objs[rnd_id] = {
                                "node_id": rnd_id,
                                "val": getattr(rnd, "val"),
                                "next": getattr(rnd, "next", None),
                                "random": getattr(rnd, "random", None)
                            }
                    edges.append((curr_id, rnd_id, True))

                seq_idx += 1
            chain_idx += 1

        pointers_display = {}
        for nid, names in ptr_names.items():
            clean_names = [n for n in names if n not in ("self", "node_data", "nxt", "nxt_id", "v")]
            if clean_names:
                pointers_display[nid] = clean_names

        operation = ""
        ft = current_frame.get("type")
        val = current_frame.get("val", "")
        if ft == "link_update":
            operation = f"LINK UPDATE: {val}" if val else "LINK UPDATE"
        elif ft == "pointer_update":
            operation = f"POINTER UPDATE: {val}" if val else "POINTER UPDATE"

        return {
            "nodes": ordered_nodes,
            "edges": edges,
            "pointers": pointers_display,
            "operation": operation,
            "accumulated_locals": accumulated_vars,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"link_update", "pointer_update", "line"}
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

        if ft == "link_update":
            return f"{prefix}Updating links/connections: {val}" if val else f"{prefix}Updating pointer links / connections"
        if ft == "pointer_update":
            return f"{prefix}Advancing pointers: {val}" if val else f"{prefix}Advancing pointer references"

        return f"{prefix}Traversing linked list nodes"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURR, "■", "current node under inspection"),
            (COLOR_HEAD, "■", "head / start node"),
            (COLOR_NODE, "■", "standard list node"),
            (RED,        "■", "random pointer edge or cycle link"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        accumulated  = frame.get("accumulated_locals", frame.get("locals", {}))
        all_vars     = frame.get("all_var_names", list(accumulated.keys()))

        entries = []

        # Sort variables to ensure consistent display order
        for k in sorted(all_vars):
            if k.startswith("_"):
                continue
            val = accumulated.get(k)
            if val is None:
                continue

            if hasattr(val, "val") or (isinstance(val, dict) and "val" in val):
                node_val = getattr(val, "val") if not isinstance(val, dict) else val.get("val")
                if "head" in k:
                    color = COLOR_HEAD
                elif k in ("curr", "current"):
                    color = COLOR_CURR
                elif k == "prev":
                    color = YELLOW
                else:
                    color = TEAL
                entries.append((k, f"Node({node_val})", color))
            elif isinstance(val, (int, str, bool)):
                entries.append((k, str(val), GREEN))

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
