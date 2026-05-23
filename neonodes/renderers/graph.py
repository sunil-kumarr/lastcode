"""
graph.py — Graph BFS renderer for Textual.
"""

from __future__ import annotations

import ast

from rich.text import Text
from textual.widget import Widget
from textual.app import RenderResult

from neonodes.theme import SURFACE, TEXT, DIM, YELLOW, TEAL, GREEN, RED

COLOR_CURRENT  = "#F7768E"
COLOR_IN_QUEUE = "#E0AF68"
COLOR_VISITED  = "#9ECE6A"
BG_CURRENT     = "#321820"
BG_IN_QUEUE    = "#2D2010"
BG_VISITED     = "#253320"
BG_NODE        = "#2D3250"


class GraphWidget(Widget):
    DEFAULT_CSS = f"""
    GraphWidget {{
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

    def update_graph(self, input_data, states: dict) -> None:
        self._input_data = input_data
        self._states = states
        self.refresh()

    def render(self) -> RenderResult:
        graph, start = self._input_data
        states = self._states
        visited: set[int] = states.get("visited", set())
        queue: list[int] = states.get("queue", [])
        current: int | None = states.get("current")
        active_edge = states.get("active_edge")

        import math
        from neonodes.renderers.canvas import TextCanvas

        # Left panel: Canvas for circular graph
        cw, ch = 40, 20
        canvas = TextCanvas(width=cw, height=ch)
        
        nodes_sorted = sorted(graph.keys())
        N = len(nodes_sorted)
        positions = {}
        cx, cy = 20, 10
        R_x, R_y = 16, 7  # 2:1 ratio for terminal fonts
        
        for i, node in enumerate(nodes_sorted):
            theta = 2 * math.pi * i / max(1, N) - math.pi / 2
            nx = cx + int(R_x * math.cos(theta))
            ny = cy + int(R_y * math.sin(theta))
            positions[node] = (nx, ny)

        # Draw edges
        for node in nodes_sorted:
            x0, y0 = positions[node]
            for nb in graph[node]:
                x1, y1 = positions[nb]
                canvas.draw_line(x0, y0, x1, y1, char="·", style=DIM)

        # Draw active edge on top
        if active_edge:
            u, v = active_edge
            if u in positions and v in positions:
                x0, y0 = positions[u]
                x1, y1 = positions[v]
                canvas.draw_directed_line(x0, y0, x1, y1, char="━", style=f"bold {YELLOW}", arrow_color=f"bold {YELLOW}")

        # Draw nodes
        for node in nodes_sorted:
            x, y = positions[node]
            node_style = self._node_style(node, visited, queue, current)
            canvas.draw_node(x, y, str(node), style=node_style)

        canvas_text = canvas.render()
        canvas_lines = canvas_text.split("\n")

        # Right panel content
        right_lines = []
        right_lines.append((f"  Traversal State", f"bold {DIM}"))
        right_lines.append((f"  " + "─" * 20, DIM))
        right_lines.append((f"  Queue:   ", DIM))
        right_lines.append((f"  {queue if queue else '[]'}", COLOR_IN_QUEUE))
        right_lines.append((f"  Visited: ", DIM))
        right_lines.append((f"  {sorted(visited) if visited else '{}'}", COLOR_VISITED))
        right_lines.append((f"  Current: ", DIM))
        right_lines.append((f"  {current if current is not None else '—'}", COLOR_CURRENT))
        right_lines.append((f" ", ""))
        right_lines.append((f"  Adjacency List", f"bold {DIM}"))
        right_lines.append((f"  " + "─" * 20, DIM))
        for node in nodes_sorted:
            right_lines.append((f"  {node} → {graph[node]}", DIM))

        result = Text()
        for i in range(max(ch, len(right_lines))):
            # left side
            if i < len(canvas_lines):
                result.append_text(canvas_lines[i])
            else:
                result.append(" " * cw)
            
            # right side
            if i < len(right_lines):
                text_val, style_val = right_lines[i]
                result.append(text_val, style=style_val)
            
            result.append("\n")

        return result

    def _node_style(self, node: int, visited: set, queue: list, current) -> str:
        if node == current:
            return f"bold {COLOR_CURRENT} on {BG_CURRENT}"
        if node in queue:
            return f"bold {COLOR_IN_QUEUE} on {BG_IN_QUEUE}"
        if node in visited:
            return f"{COLOR_VISITED} on {BG_VISITED}"
        return f"{TEXT} on {BG_NODE}"


# ---------------------------------------------------------------------------
# GraphRenderer
# ---------------------------------------------------------------------------


class GraphRenderer:

    def make_widget(self, input_data) -> GraphWidget:
        return GraphWidget(input_data=input_data, id="graph-widget")

    def update_widget(self, widget: GraphWidget, input_data, frame_states: dict) -> None:
        widget.update_graph(input_data, frame_states)

    def compute_states(self, frames: list[dict], up_to: int) -> dict:
        visited: set[int] = set()
        queue: list[int] = []
        current: int | None = None
        active_edge: tuple | None = None

        for frame in frames[:up_to + 1]:
            ft = frame.get("type")
            if ft == "enqueue":
                node = frame.get("node")
                from_node = frame.get("from_node")
                if from_node is not None:
                    active_edge = (from_node, node)
                if node not in queue:
                    queue.append(node)
            elif ft == "dequeue":
                node = frame.get("node")
                current = node
                active_edge = None
                if node in queue:
                    queue.remove(node)
            elif ft == "node_visit":
                node = frame.get("node")
                visited.add(node)
                active_edge = None

        return {"visited": visited, "queue": queue, "current": current, "active_edge": active_edge}

    def filter_frames(self, frames: list[dict]) -> list[dict]:
        keep_types = {"node_visit", "enqueue", "dequeue", "line"}
        return [f for f in frames if f.get("type") in keep_types]

    def explain_frame(self, frame: dict, step: int, total: int) -> str:
        ft = frame.get("type")
        prefix = f"  [{step + 1}/{total}]  "
        if ft == "enqueue":
            return f"{prefix}Enqueue node {frame.get('node')} — discovered unvisited neighbor"
        if ft == "dequeue":
            return f"{prefix}Dequeue node {frame.get('node')} — processing next in queue"
        if ft == "node_visit":
            return f"{prefix}Visit node {frame.get('node')} — exploring its neighbors"
        if ft == "line":
            return f"{prefix}Executing BFS traversal..."
        return f"{prefix}—"

    def apply_frame_extras(self, screen, frame: dict) -> None:
        pass

    def legend_entries(self) -> list[tuple[str, str, str]]:
        return [
            (COLOR_CURRENT,  "■", "currently processing"),
            (COLOR_IN_QUEUE, "■", "in queue"),
            (COLOR_VISITED,  "■", "visited"),
            (TEXT,           "■", "unvisited"),
        ]

    def variable_entries(self, frame: dict) -> list[tuple[str, str, str]]:
        node = frame.get("node", "—")
        queue = frame.get("queue", [])
        visited = frame.get("visited", set())
        return [
            ("node",    str(node),           f"bold {COLOR_CURRENT}"),
            ("queue",   str(queue),          COLOR_IN_QUEUE),
            ("visited", str(sorted(visited)), COLOR_VISITED),
        ]

    def parse_input(self, raw: str) -> tuple:
        raw = raw.strip()
        # Format: "{0:[1,2], 1:[0,3]}, 0"
        try:
            brace_end = raw.rindex("}")
            graph_part = raw[:brace_end + 1]
            rest = raw[brace_end + 1:].strip().lstrip(",").strip()
            graph = ast.literal_eval(graph_part)
            start = int(rest)
            if not isinstance(graph, dict):
                raise ValueError("expected dict")
            # Normalize keys/values to int
            graph = {int(k): [int(v) for v in vs] for k, vs in graph.items()}
            return (graph, start)
        except Exception as e:
            raise ValueError(f"Expected '{{0:[1,2], ...}}, start': {e}")

    def serialize_input(self, data: tuple) -> str:
        graph, start = data
        return f"{graph}, {start}"
