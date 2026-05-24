"""Moving Average from Stream — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Moving Average from Stream'
CATEGORY = 'queue'
DIFFICULTY = 'easy'
RENDERER = 'queue'
DESCRIPTION = 'Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.'
DEFAULT_INPUT = ([1, 10, 3, 5], 3)

CODE_LINES = ['class MovingAverage:', '    def __init__(self, size):', '        self.q = []; self.size = size; self.sum = 0', '    def next(self, val):', '        if len(self.q) == self.size:', '            self.sum -= self.q.pop(0)', '        self.q.append(val)', '        self.sum += val', '        return self.sum / len(self.q)']
_LINE_MAP = {i: i for i in range(1, 10)}

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



def _moving_average_instrumented(val_list, size):
    queue = []
    curr_sum = 0
    res = []
    for i, val in enumerate(val_list):
        if len(queue) == size:
            popped = queue.pop(0)
            _viz_dequeue(popped)
            curr_sum -= popped
        queue.append(val)
        _viz_enqueue(val)
        curr_sum += val
        res.append(curr_sum / len(queue))
    return res

def run(input_data):
    val_list, size = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("val"), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_moving_average_instrumented",
        _moving_average_instrumented,
        val_list, size,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
