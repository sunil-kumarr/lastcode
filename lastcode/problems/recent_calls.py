"""Number of Recent Calls — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Number of Recent Calls'
CATEGORY = 'queue'
DIFFICULTY = 'easy'
RENDERER = 'queue'
DESCRIPTION = 'You have a RecentCounter class which counts the number of recent requests within a certain time frame.'
DEFAULT_INPUT = [1, 100, 3001, 3002]

CODE_LINES = ['class RecentCounter:', '    def __init__(self):', '        self.q = []', '    def ping(self, t):', '        self.q.append(t)', '        while self.q[0] < t - 3000:', '            self.q.pop(0)', '        return len(self.q)']
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



def _recent_calls_instrumented(t_list):
    queue = []
    res = []
    for i, t in enumerate(t_list):
        queue.append(t)
        _viz_enqueue(t)
        while queue and queue[0] < t - 3000:
            popped = queue.pop(0)
            _viz_dequeue(popped)
        res.append(len(queue))
    return res

def run(input_data):
    t_list = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("t"), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_recent_calls_instrumented",
        _recent_calls_instrumented,
        t_list,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
