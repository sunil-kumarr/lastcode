"""Remove Duplicates from Sorted — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Remove Duplicates from Sorted'
CATEGORY = 'two_pointer'
DIFFICULTY = 'easy'
RENDERER = 'two_pointer'
DESCRIPTION = 'Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.'
DEFAULT_INPUT = [1, 1, 2]

CODE_LINES = ['def remove_duplicates(nums):', '    if not nums: return 0', '    left = 0', '    for right in range(1, len(nums)):', '        if nums[right] != nums[left]:', '            left += 1', '            nums[left] = nums[right]', '    return left + 1']
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



def _remove_duplicates_instrumented(nums):
    if not nums: return 0
    left = 0
    for right in range(1, len(nums)):
        _viz_compare(left, right)
        if nums[right] != nums[left]:
            left += 1
            nums[left] = nums[right]
            _viz_update(left, right)
    _viz_found(left, left)
    return left + 1

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
        "_remove_duplicates_instrumented",
        _remove_duplicates_instrumented,
        nums,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
