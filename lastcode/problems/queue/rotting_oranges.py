"""Rotting Oranges (BFS) — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Rotting Oranges (BFS)'
CATEGORY = 'queue'
DIFFICULTY = 'medium'
RENDERER = 'queue'
DESCRIPTION = 'You are given an m x n grid where each cell can have one of three values: 0 empty, 1 fresh, or 2 rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange.'
DEFAULT_INPUT = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]

CODE_LINES = ['def oranges_rotting(grid):', '    q = []; fresh = 0', '    for r in range(len(grid)):', '        for c in range(len(grid[0])):', '            if grid[r][c] == 2: q.append((r, c))', '            elif grid[r][c] == 1: fresh += 1', '    minutes = 0', '    while q and fresh > 0:', '        minutes += 1', '        for _ in range(len(q)):', '            r, c = q.pop(0)', '            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:', '                nr, nc = r+dr, c+dc', '                if 0<=nr<len(grid) and 0<=nc<len(grid[0]) and grid[nr][nc] == 1:', '                    grid[nr][nc] = 2; fresh -= 1; q.append((nr, nc))', '    return minutes if fresh == 0 else -1']
_LINE_MAP = {i: i for i in range(1, 17)}

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



def _rotting_oranges_instrumented(grid):
    rows = len(grid)
    cols = len(grid[0])
    queue = []
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
                _viz_enqueue((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh > 0:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.pop(0)
            _viz_dequeue((r, c))
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
                    _viz_enqueue((nr, nc))
    return minutes if fresh == 0 else -1

def run(input_data):
    grid = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("nr", locs.get("r")), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("r"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_rotting_oranges_instrumented",
        _rotting_oranges_instrumented,
        grid,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
