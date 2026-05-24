"""Trapping Rain Water — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Trapping Rain Water'
CATEGORY = 'two_pointer'
DIFFICULTY = 'hard'
RENDERER = 'two_pointer'
DESCRIPTION = 'Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.'
DEFAULT_INPUT = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

CODE_LINES = ['def trap(height):', '    if not height: return 0', '    left, right = 0, len(height) - 1', '    left_max, right_max = height[left], height[right]', '    water = 0', '    while left < right:', '        if height[left] < height[right]:', '            left += 1', '            left_max = max(left_max, height[left])', '            water += left_max - height[left]', '        else:', '            right -= 1', '            right_max = max(right_max, height[right])', '            water += right_max - height[right]', '    return water']
_LINE_MAP = {i: i for i in range(1, 16)}

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



def _trapping_rain_water_instrumented(height):
    if not height: return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    while left < right:
        _viz_compare(left, right)
        if height[left] < height[right]:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
        _viz_update(left, right)
    _viz_found(left, right)
    return water

def run(input_data):
    height = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_compare", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_trapping_rain_water_instrumented",
        _trapping_rain_water_instrumented,
        height,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
