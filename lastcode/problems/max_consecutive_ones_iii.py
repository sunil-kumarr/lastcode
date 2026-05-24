"""Max Consecutive Ones III — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Max Consecutive Ones III'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given a binary array nums and an integer k, return the maximum number of consecutive 1s in the array if you can flip at most k 0s.'
DEFAULT_INPUT = ([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2)

CODE_LINES = ['def longest_ones(nums, k):', '    left = 0', '    zeros = 0', '    max_len = 0', '    for right in range(len(nums)):', '        if nums[right] == 0:', '            zeros += 1', '        while zeros > k:', '            if nums[left] == 0:', '                zeros -= 1', '            left += 1', '        max_len = max(max_len, right - left + 1)', '    return max_len']
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



def _max_consecutive_ones_iii_instrumented(nums, k):
    left = 0
    zeros = 0
    max_len = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        _viz_compare(left, right)
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
            _viz_update(left, right)
        max_len = max(max_len, right - left + 1)
    return max_len

def run(input_data):
    nums, k = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_max_consecutive_ones_iii_instrumented",
        _max_consecutive_ones_iii_instrumented,
        nums, k,
        marker_fns={"_viz_compare", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
        }
    )
