"""Move Zeroes — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Move Zeroes'
CATEGORY = 'two_pointer'
DIFFICULTY = 'easy'
RENDERER = 'two_pointer'
DESCRIPTION = "Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements."
DEFAULT_INPUT = [0, 1, 0, 3, 12]

CODE_LINES = ['def move_zeroes(nums):', '    left = 0', '    for right in range(len(nums)):', '        if nums[right] != 0:', '            nums[left], nums[right] = nums[right], nums[left]', '            left += 1']
_LINE_MAP = {i: i for i in range(1, 7)}

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



def _move_zeroes_instrumented(nums):
    left = 0
    for right in range(len(nums)):
        _viz_compare(left, right)
        if nums[right] != 0:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
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
        "_move_zeroes_instrumented",
        _move_zeroes_instrumented,
        nums,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
