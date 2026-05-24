"""Sliding Window Max (Deque) — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Sliding Window Max (Deque)'
CATEGORY = 'queue'
DIFFICULTY = 'hard'
RENDERER = 'queue'
DESCRIPTION = 'Given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. Return the max sliding window.'
DEFAULT_INPUT = ([1, 3, -1, -3, 5, 3, 6, 7], 3)

CODE_LINES = ['def max_sliding_window(nums, k):', '    q = []', '    res = []', '    for i, num in enumerate(nums):', '        while q and nums[q[-1]] < num: q.pop()', '        q.append(i)', '        if q[0] == i - k: q.pop(0)', '        if i >= k - 1: res.append(nums[q[0]])', '    return res']
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



def _max_sliding_window_queue_instrumented(nums, k):
    queue = []
    res = []
    for i, num in enumerate(nums):
        while queue and nums[queue[-1]] < num:
            queue.pop()
        queue.append(i)
        _viz_enqueue(i)
        if queue[0] == i - k:
            popped = queue.pop(0)
            _viz_dequeue(popped)
        if i >= k - 1:
            res.append(nums[queue[0]])
    return res

def run(input_data):
    nums, k = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("i"), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_max_sliding_window_queue_instrumented",
        _max_sliding_window_queue_instrumented,
        nums, k,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
