"""Sliding Window Maximum — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Sliding Window Maximum'
CATEGORY = 'sliding_window'
DIFFICULTY = 'hard'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. Return the max sliding window.'
DEFAULT_INPUT = ([1, 3, -1, -3, 5, 3, 6, 7], 3)

CODE_LINES = ['def max_sliding_window(nums, k):', '    res = []', '    q = []', '    left = 0', '    for right in range(len(nums)):', '        while q and nums[q[-1]] < nums[right]:', '            q.pop()', '        q.append(right)', '        if left > q[0]:', '            q.pop(0)', '        if right >= k - 1:', '            res.append(nums[q[0]])', '            left += 1', '    return res']
_LINE_MAP = {i: i for i in range(1, 15)}

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



def _sliding_window_maximum_instrumented(nums, k):
    res = []
    q = []
    left = 0
    for right in range(len(nums)):
        while q and nums[q[-1]] < nums[right]:
            q.pop()
        q.append(right)
        _viz_compare(left, right)
        if left > q[0]:
            q.pop(0)
        if right >= k - 1:
            res.append(nums[q[0]])
            _viz_found(left, right)
            left += 1
            _viz_update(left, right)
    return res

def run(input_data):
    nums, k = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "window_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_sliding_window_maximum_instrumented",
        _sliding_window_maximum_instrumented,
        nums, k,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
