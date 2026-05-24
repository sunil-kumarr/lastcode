"""3Sum — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = '3Sum'
CATEGORY = 'two_pointer'
DIFFICULTY = 'medium'
RENDERER = 'two_pointer'
DESCRIPTION = 'Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.'
DEFAULT_INPUT = [-1, 0, 1, 2, -1, -4]

CODE_LINES = ['def three_sum(nums):', '    nums.sort()', '    res = []', '    for i in range(len(nums) - 2):', '        if i > 0 and nums[i] == nums[i-1]: continue', '        left, right = i + 1, len(nums) - 1', '        while left < right:', '            sum_val = nums[i] + nums[left] + nums[right]', '            if sum_val == 0:', '                res.append([nums[i], nums[left], nums[right]])', '                left += 1; right -= 1', '            elif sum_val < 0: left += 1', '            else: right -= 1', '    return res']
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



def _three_sum_instrumented(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
            sum_val = nums[i] + nums[left] + nums[right]
            _viz_compare(left, right)
            if sum_val == 0:
                res.append([nums[i], nums[left], nums[right]])
                _viz_found(left, right)
                left += 1; right -= 1
            elif sum_val < 0:
                left += 1
            else:
                right -= 1
            _viz_update(left, right)
    return res

def run(input_data):
    nums = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_compare", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_three_sum_instrumented",
        _three_sum_instrumented,
        nums,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
