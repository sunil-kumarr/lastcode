"""Walls and Gates (BFS) — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Walls and Gates (BFS)'
CATEGORY = 'queue'
DIFFICULTY = 'medium'
RENDERER = 'queue'
DESCRIPTION = 'Fill each empty cell in a grid with the distance to its nearest gate. If it is impossible, fill it with INF.'
DEFAULT_INPUT = [[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]]

CODE_LINES = ['def walls_and_gates(rooms):', '    q = []', '    for r in range(len(rooms)):', '        for c in range(len(rooms[0])):', '            if rooms[r][c] == 0: q.append((r, c))', '    while q:', '        r, c = q.pop(0)', '        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:', '            nr, nc = r + dr, c + dc', '            if 0<=nr<len(rooms) and 0<=nc<len(rooms[0]) and rooms[nr][nc] == 2147483647:', '                rooms[nr][nc] = rooms[r][c] + 1; q.append((nr, nc))']
_LINE_MAP = {i: i for i in range(1, 12)}

# Dummy visualization markers
def _viz_compare(*args, **kwargs): pass
def _viz_update(*args, **kwargs): pass
def _viz_found(*args, **kwargs): pass
def _viz_push(*args, **kwargs): pass
def _viz_pop(*args, **kwargs): pass
def _viz_peek(*args, **kwargs): pass
def _viz_enqueue(*args, **kwargs): pass
def _viz_dequeue(*args, **kwargs): pass
def _viz_link(*args, **kwargs): pass



def _walls_and_gates_instrumented(rooms):
    rows = len(rooms)
    cols = len(rooms[0])
    queue = []
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))
                _viz_enqueue((r, c))
    while queue:
        r, c = queue.pop(0)
        _viz_dequeue((r, c))
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
                _viz_enqueue((nr, nc))

def run(input_data):
    rooms = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("nr", locs.get("r")), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("r"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_walls_and_gates_instrumented",
        _walls_and_gates_instrumented,
        rooms,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
