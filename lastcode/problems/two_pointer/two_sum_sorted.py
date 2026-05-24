"""Two Sum II - Sorted Array — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Two Sum II - Sorted Array'
CATEGORY = 'two_pointer'
DIFFICULTY = 'medium'
RENDERER = 'two_pointer'
DESCRIPTION = 'Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.'
DEFAULT_INPUT = ([2, 7, 11, 15], 9)

CODE_LINES = ['def two_sum(numbers, target):', '    left = 0', '    right = len(numbers) - 1', '    while left < right:', '        sum_val = numbers[left] + numbers[right]', '        if sum_val == target:', '            return [left + 1, right + 1]', '        elif sum_val < target:', '            left += 1', '        else:', '            right -= 1', '    return []']
_LINE_MAP = {i: i for i in range(1, 13)}

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



def _two_sum_sorted_instrumented(numbers, target):
    left = 0
    right = len(numbers) - 1
    while left < right:
        sum_val = numbers[left] + numbers[right]
        _viz_compare(left, right)
        if sum_val == target:
            _viz_found(left, right)
            return [left + 1, right + 1]
        elif sum_val < target:
            left += 1
        else:
            right -= 1
        _viz_update(left, right)
    return []

def run(input_data):
    numbers, target = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_compare", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_two_sum_sorted_instrumented",
        _two_sum_sorted_instrumented,
        numbers, target,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
