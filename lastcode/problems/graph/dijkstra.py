"""Dijkstra Shortest Path — full implementation with visualization tracing."""

from __future__ import annotations

import heapq
from lastcode.recorder import Recorder

TITLE      = "Dijkstra Shortest Path"
CATEGORY   = "graph"
DIFFICULTY = "medium"
RENDERER   = "graph"
DESCRIPTION = (
    "Given a weighted undirected graph and a start node, "
    "compute the shortest distance from the start node to all other nodes using Dijkstra's algorithm."
)

DEFAULT_INPUT = ({0: [(1, 4), (2, 1)], 1: [(0, 4), (3, 1)], 2: [(0, 1), (1, 2), (3, 5)], 3: [(1, 1), (2, 5)]}, 0)

CODE_LINES = [
    "import heapq",
    "",
    "def dijkstra(graph, start):",
    "    pq = [(0, start)]",
    "    dist = {node: float('inf') for node in graph}",
    "    dist[start] = 0",
    "    visited = set()",
    "    while pq:",
    "        d, u = heapq.heappop(pq)",
    "        if u in visited:",
    "            continue",
    "        visited.add(u)",
    "        for v, weight in graph[u]:",
    "            if v not in visited:",
    "                new_dist = dist[u] + weight",
    "                if new_dist < dist[v]:",
    "                    dist[v] = new_dist",
    "                    heapq.heappush(pq, (new_dist, v))",
    "    return dist",
]

_LINE_MAP = {
    1: 1,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    17: 17,
    18: 18,
    19: 19
}


# ---------------------------------------------------------------------------
# Marker stubs
# ---------------------------------------------------------------------------

def _viz_visit(node: int) -> None:  # noqa: ARG001
    pass

def _viz_dequeue(node: int) -> None:  # noqa: ARG001
    pass

def _viz_pq(pq: list) -> None:  # noqa: ARG001
    pass

def _viz_dist(dist: dict) -> None:  # noqa: ARG001
    pass

def _viz_edge_check(u: int, v: int) -> None:  # noqa: ARG001
    pass


# ---------------------------------------------------------------------------
# Instrumented algorithm
# ---------------------------------------------------------------------------

def _dijkstra_instrumented(graph: dict, start: int) -> dict:
    import heapq
    pq = [(0, start)]
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    visited = set()
    
    _viz_dist(dist)
    _viz_pq(pq)

    while pq:
        d, u = heapq.heappop(pq)
        _viz_dequeue(u)
        
        if u in visited:
            continue
        visited.add(u)
        _viz_visit(u)
        
        for v, weight in graph[u]:
            if v not in visited:
                _viz_edge_check(u, v)
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
                    _viz_dist(dist)
                    _viz_pq(pq)
    return dist


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(input_data: tuple) -> list[dict]:
    graph, start = input_data
    pq_snapshot: list = []
    dist_snapshot: dict = {}

    def handle_pq(locs: dict, depth: int) -> dict | None:
        nonlocal pq_snapshot
        pq_snapshot = list(locs.get("pq", []))
        return {
            "type": "pq_update",
            "pq": pq_snapshot,
            "distances": dict(dist_snapshot),
        }

    def handle_dist(locs: dict, depth: int) -> dict | None:
        nonlocal dist_snapshot
        dist_snapshot = dict(locs.get("dist", {}))
        return {
            "type": "dist_update",
            "pq": list(pq_snapshot),
            "distances": dist_snapshot,
        }

    def handle_visit(locs: dict, depth: int) -> dict | None:
        node = locs.get("u")
        return {
            "type": "node_visit",
            "node": node,
            "pq": list(pq_snapshot),
            "distances": dict(dist_snapshot),
        }

    def handle_dequeue(locs: dict, depth: int) -> dict | None:
        node = locs.get("u")
        return {
            "type": "dequeue",
            "node": node,
            "pq": list(pq_snapshot),
            "distances": dict(dist_snapshot),
        }

    def handle_edge_check(locs: dict, depth: int) -> dict | None:
        u = locs.get("u")
        v = locs.get("v")
        return {
            "type": "edge_check",
            "u": u,
            "v": v,
            "pq": list(pq_snapshot),
            "distances": dict(dist_snapshot),
        }

    recorder = Recorder()
    return recorder.record(
        "_dijkstra_instrumented",
        _dijkstra_instrumented,
        graph,
        start,
        marker_fns={"_viz_pq", "_viz_dist", "_viz_visit", "_viz_dequeue", "_viz_edge_check"},
        nested_fns=set(),
        marker_handlers={
            "_viz_pq": handle_pq,
            "_viz_dist": handle_dist,
            "_viz_visit": handle_visit,
            "_viz_dequeue": handle_dequeue,
            "_viz_edge_check": handle_edge_check,
        },
    )
