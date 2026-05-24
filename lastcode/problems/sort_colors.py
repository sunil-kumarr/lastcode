"""Sort Colors — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Sort Colors'
CATEGORY = 'two_pointer'
DIFFICULTY = 'medium'
RENDERER = 'two_pointer'
DESCRIPTION = 'Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue (0, 1, and 2).'
DEFAULT_INPUT = [2, 0, 2, 1, 1, 0]

CODE_LINES = ['def sort_colors(nums):', '    left = 0', '    curr = 0', '    right = len(nums) - 1', '    while curr <= right:', '        if nums[curr] == 0:', '            nums[left], nums[curr] = nums[curr], nums[left]', '            left += 1; curr += 1', '        elif nums[curr] == 2:', '            nums[right], nums[curr] = nums[curr], nums[right]', '            right -= 1', '        else:', '            curr += 1']
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



def _sort_colors_instrumented(nums):
    left = 0
    curr = 0
    right = len(nums) - 1
    while curr <= right:
        _viz_compare(curr, right)
        if nums[curr] == 0:
            nums[left], nums[curr] = nums[curr], nums[left]
            left += 1; curr += 1
        elif nums[curr] == 2:
            nums[right], nums[curr] = nums[curr], nums[right]
            right -= 1
        else:
            curr += 1
        _viz_update(left, right)
    _viz_found(left, right)

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
        "_sort_colors_instrumented",
        _sort_colors_instrumented,
        nums,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
