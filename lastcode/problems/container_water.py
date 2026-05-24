"""Container With Most Water — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Container With Most Water'
CATEGORY = 'two_pointer'
DIFFICULTY = 'medium'
RENDERER = 'two_pointer'
DESCRIPTION = 'You are given an integer array height of length n. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.'
DEFAULT_INPUT = [1, 8, 6, 2, 5, 4, 8, 3, 7]

CODE_LINES = ['def max_area(height):', '    left = 0', '    right = len(height) - 1', '    max_area = 0', '    while left < right:', '        width = right - left', '        h = min(height[left], height[right])', '        max_area = max(max_area, width * h)', '        if height[left] < height[right]:', '            left += 1', '        else:', '            right -= 1', '    return max_area']
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



def _container_water_instrumented(height):
    left = 0
    right = len(height) - 1
    max_area = 0
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_area = max(max_area, width * h)
        _viz_compare(left, right)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
        _viz_update(left, right)
    _viz_found(left, right)
    return max_area

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
        "_container_water_instrumented",
        _container_water_instrumented,
        height,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
