"""Minimum Size Subarray Sum — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Minimum Size Subarray Sum'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target.'
DEFAULT_INPUT = ([2, 3, 1, 2, 4, 3], 7)

CODE_LINES = ['def min_subarray_len(nums, target):', '    left = 0', '    curr_sum = 0', "    min_len = float('inf')", '    for right in range(len(nums)):', '        curr_sum += nums[right]', '        while curr_sum >= target:', '            min_len = min(min_len, right - left + 1)', '            curr_sum -= nums[left]', '            left += 1', "    return min_len if min_len != float('inf') else 0"]
_LINE_MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11}

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



def _min_size_subarray_sum_instrumented(nums, target):
    left = 0
    curr_sum = 0
    min_len = float('inf')
    for right in range(len(nums)):
        curr_sum += nums[right]
        _viz_compare(left, right)
        while curr_sum >= target:
            min_len = min(min_len, right - left + 1)
            _viz_found(left, right)
            curr_sum -= nums[left]
            left += 1
            _viz_update(left, right)
    return min_len if min_len != float('inf') else 0

def run(input_data):
    nums, target = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "window_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_min_size_subarray_sum_instrumented",
        _min_size_subarray_sum_instrumented,
        nums, target,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
