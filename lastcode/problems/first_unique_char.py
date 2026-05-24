"""First Unique Char in String — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'First Unique Char in String'
CATEGORY = 'queue'
DIFFICULTY = 'easy'
RENDERER = 'queue'
DESCRIPTION = 'Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.'
DEFAULT_INPUT = "loveleetcode"

CODE_LINES = ['def first_uniq_char(s):', '    counts = {}; q = []', '    for i, c in enumerate(s):', '        counts[c] = counts.get(c, 0) + 1', '        q.append((c, i))', '        while q and counts[q[0][0]] > 1:', '            q.pop(0)', '    return q[0][1] if q else -1']
_LINE_MAP = {i: i for i in range(1, 9)}

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



def _first_unique_char_instrumented(s):
    counts = {}
    queue = []
    for i, char in enumerate(s):
        counts[char] = counts.get(char, 0) + 1
        queue.append((char, i))
        _viz_enqueue(char)
        while queue and counts[queue[0][0]] > 1:
            popped = queue.pop(0)
            _viz_dequeue(popped[0])
    return queue[0][1] if queue else -1

def run(input_data):
    s = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("char"), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("popped")[0] if locs.get("popped") else "", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_first_unique_char_instrumented",
        _first_unique_char_instrumented,
        s,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
