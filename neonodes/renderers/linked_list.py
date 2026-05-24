"""
linked_list.py — Renderer for Linked List problems.
"""

from __future__ import annotations

import ast
from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, BLUE, GREEN, YELLOW, TEAL, RED
from neonodes.renderers.canvas import TextCanvas

COLOR_CURR = "#F7768E"     # Pinkish-red for current pointer node
COLOR_HEAD = "#7AA2F7"     # Blue for head node
COLOR_NODE = "#9ECE6A"     # Green for other nodes
BG_NODE = "#253320"
BG_CELL = "#2D3250"


class LinkedListWidget(Widget):
    DEFAULT_CSS = f"""
    LinkedListWidget {{
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
        nodes = states.get("nodes", [])       # List of dicts: {"id":..., "val":..., "is_curr":..., "is_head":...}
        edges = states.get("edges", [])       # List of tuples: (from_id, to_id, is_random)
        pointers = states.get("pointers", {})  # Dict: node_id -> list of pointer names (e.g., ["curr", "prev"])
        
        if not nodes:
            return Text("  (empty list)", style="dim")

        # Set up canvas
        # Node width is 5, spacing between nodes is 8
        cw = max(80, len(nodes) * 13 + 10)
        ch = 14
        canvas = TextCanvas(width=cw, height=ch)

        # Position nodes
        # If there are multiple distinct list heads, we can group them into layers (e.g. List 1 at cy=4, List 2 at cy=10)
        # To determine layers, let's group nodes by their source chain or index
        positions = {}
        node_by_id = {n["id"]: n for n in nodes}
        
        # Simple heuristic: if we have more than 1 head, layout List 1 at cy=3 and List 2 at cy=9
        has_multiple_chains = any(n.get("chain_idx", 0) > 0 for n in nodes)
        
        for idx, node in enumerate(nodes):
            chain = node.get("chain_idx", 0)
            node_seq = node.get("seq_idx", idx)
            cx = node_seq * 13 + 6
            cy = 9 if (has_multiple_chains and chain > 0) else 4
            positions[node["id"]] = (cx, cy)

        # Draw edges
        for from_id, to_id, is_random in edges:
            if from_id in positions and to_id in positions:
                px, py = positions[from_id]
                cx, cy = positions[to_id]
                
                style = COLOR_NODE
                if is_random:
                    style = RED
                
                # If it's a backward edge (cycle)
                if cx <= px:
                    # Draw a loop: drop down, go back, go up
                    # We can use canvas.draw_line
                    canvas.draw_line(px, py + 1.5, px, py + 3, style=style)
                    canvas.draw_line(px, py + 3, cx, py + 3, style=style)
                    canvas.draw_line(cx, py + 3, cx, cy + 1.5, style=style)
                    # Draw arrowhead
                    canvas.draw_text(cx, cy + 2, "^", style=style)
                else:
                    # Standard forward arrow
                    canvas.draw_directed_line(px + 2, py, cx - 2, cy, style=style, arrow_color=style)
            elif from_id in positions and to_id is None:
                # Points to NULL
                px, py = positions[from_id]
                canvas.draw_text(px + 3, py, "──>", style=DIM)
                canvas.draw_text(px + 7, py, "NULL", style=RED)

        # Draw nodes
        for node in nodes:
            nid = node["id"]
            if nid in positions:
                cx, cy = positions[nid]
                
                # Node styling
                if node.get("is_curr"):
                    style = f"bold {COLOR_CURR} on {BG_NODE}"
                elif node.get("is_head"):
                    style = f"bold {COLOR_HEAD} on {BG_NODE}"
                else:
                    style = f"bold {TEXT} on {BG_CELL}"
                
                canvas.draw_node(cx, cy, str(node["val"]), style=style)
                
                # Draw pointer names underneath node
                pt_list = pointers.get(nid, [])
                if pt_list:
                    pt_text = ", ".join(pt_list)
                    canvas.draw_text(cx - len(pt_text)//2, cy + 2, pt_text, style=f"bold {YELLOW}")

        return canvas.render()


class LinkedListRenderer:

    def make_widget(self, input_data) -> LinkedListWidget:
        return LinkedListWidget(input_data=input_data, id="linked-list-widget")

    def update_widget(self, widget: LinkedListWidget, input_data, frame_states: dict) -> None:
        widget.update_state(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        nodes_info = []
        edges_info = []
        pointers_map = {}
        
        # We will parse the last frame to reconstruct the state of nodes and links
        if not frames or up_to >= len(frames):
            return {}
            
        frame = frames[up_to]
        locals_val = frame.get("locals", {})
        
        # 1. Discover all active list nodes in local variables
        node_objs = {}  # id -> python node object dict
        ptr_names = {}  # id -> list of pointer names
        
        # We also want to locate standard pointer names like 'curr', 'prev', 'head', 'slow', 'fast'
        for k, v in locals_val.items():
            if v is not None and (hasattr(v, "val") or (isinstance(v, dict) and "val" in v)):
                nid = id(v) if not isinstance(v, dict) else v.get("node_id", id(v))
                if isinstance(v, dict):
                    node_objs[nid] = v
                else:
                    node_objs[nid] = {"node_id": nid, "val": getattr(v, "val"), "next": getattr(v, "next", None), "random": getattr(v, "random", None)}
                
                if k not in ptr_names:
                    ptr_names[nid] = []
                ptr_names[nid].append(k)

        # 2. Traverse lists starting from heads or other pointer nodes to build ordering
        visited = set()
        ordered_nodes = []
        edges = []
        
        # Find potential heads (pointers containing 'head' or just start traversing from all known nodes)
        heads = []
        for nid, ptrs in ptr_names.items():
            if any("head" in p for p in ptrs):
                heads.append(nid)
                
        # If no explicit heads, sort other node pointers to start from the earliest
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
                    # Cycle detected in traversal!
                    break
                    
                visited.add(curr_id)
                node_data = node_objs[curr_id]
                
                # Check properties
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
                
                # Check next pointer
                nxt = node_data.get("next")
                if nxt is not None:
                    nxt_id = id(nxt) if not isinstance(nxt, dict) else nxt.get("node_id", id(nxt))
                    
                    # Ensure next node is in node_objs
                    if nxt_id not in node_objs:
                        if isinstance(nxt, dict):
                            node_objs[nxt_id] = nxt
                        else:
                            node_objs[nxt_id] = {"node_id": nxt_id, "val": getattr(nxt, "val"), "next": getattr(nxt, "next", None), "random": getattr(nxt, "random", None)}
                            
                    edges.append((curr_id, nxt_id, False))
                    curr_id = nxt_id
                else:
                    edges.append((curr_id, None, False))
                    curr_id = None
                
                # Check random pointer
                rnd = node_data.get("random")
                if rnd is not None:
                    rnd_id = id(rnd) if not isinstance(rnd, dict) else rnd.get("node_id", id(rnd))
                    if rnd_id not in node_objs:
                        if isinstance(rnd, dict):
                            node_objs[rnd_id] = rnd
                        else:
                            node_objs[rnd_id] = {"node_id": rnd_id, "val": getattr(rnd, "val"), "next": getattr(rnd, "next", None), "random": getattr(rnd, "random", None)}
                    edges.append((curr_id, rnd_id, True))
                    
                seq_idx += 1
            chain_idx += 1

        # Build pointer names mapping for widget rendering
        pointers_display = {}
        for nid, names in ptr_names.items():
            # Exclude internal variables that aren't useful pointer labels
            clean_names = [n for n in names if n not in ("self", "node_data", "nxt", "nxt_id", "v")]
            if clean_names:
                pointers_display[nid] = clean_names

        return {
            "nodes": ordered_nodes,
            "edges": edges,
            "pointers": pointers_display,
        }

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"link_update", "pointer_update", "line"}
        return [f for f in frames if f.get("type") in keep_types or f.get("event") == "line"]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        
        if ft == "link_update":
            return f"{prefix}Updating pointer links / connections"
        if ft == "pointer_update":
            return f"{prefix}Advancing pointer references"
            
        return f"{prefix}Traversing linked list nodes"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURR, "■", "current node under inspection"),
            (COLOR_HEAD, "■", "head / start node"),
            (COLOR_NODE, "■", "standard list node"),
            (RED,        "■", "random pointer edge"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        locals_val = frame.get("locals", {})
        entries = []
        
        for k, v in locals_val.items():
            if v is not None and (hasattr(v, "val") or (isinstance(v, dict) and "val" in v)):
                val = getattr(v, "val") if not isinstance(v, dict) else v.get("val")
                entries.append((k, f"Node({val})", COLOR_HEAD if "head" in k else (COLOR_CURR if k == "curr" else YELLOW)))
            elif isinstance(v, (int, str, bool)):
                entries.append((k, str(v), TEAL))
                
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
