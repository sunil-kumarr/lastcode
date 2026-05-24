"""Subarrays with K Diff Ints — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Subarrays with K Diff Ints'
CATEGORY = 'sliding_window'
DIFFICULTY = 'hard'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given an integer array nums and an integer k, return the number of good subarrays of nums. A good subarray is an array where the number of different integers in that subarray is exactly k.'
DEFAULT_INPUT = ([1, 2, 1, 2, 3], 2)

CODE_LINES = ['def subarrays_with_k_distinct(nums, k):', '    def at_most(k_val):', '        count = {}', '        left = 0; ans = 0', '        for right in range(len(nums)):', '            count[nums[right]] = count.get(nums[right], 0) + 1', '            while len(count) > k_val:', '                count[nums[left]] -= 1', '                if count[nums[left]] == 0: del count[nums[left]]', '                left += 1', '            ans += right - left + 1', '        return ans', '    return at_most(k) - at_most(k-1)']
_LINE_MAP = {i: i for i in range(1, 14)}

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



def _subarrays_k_different_instrumented(nums, k):
    def at_most(k_val):
        count = {}
        left = 0; ans = 0
        for right in range(len(nums)):
            count[nums[right]] = count.get(nums[right], 0) + 1
            _viz_compare(left, right)
            while len(count) > k_val:
                count[nums[left]] -= 1
                if count[nums[left]] == 0: del count[nums[left]]
                left += 1
                _viz_update(left, right)
            ans += right - left + 1
        return ans
    return at_most(k) - at_most(k-1)

def run(input_data):
    nums, k = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_subarrays_k_different_instrumented",
        _subarrays_k_different_instrumented,
        nums, k,
        marker_fns={"_viz_compare", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
        }
    )
