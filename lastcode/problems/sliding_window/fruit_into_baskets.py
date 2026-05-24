"""Fruit Into Baskets — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Fruit Into Baskets'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = 'You are visiting a farm that has a single row of fruit trees arranged from left to right. You have two baskets, and each basket can only hold a single type of fruit. Return the maximum number of fruits you can collect.'
DEFAULT_INPUT = [1, 2, 1, 2, 3]

CODE_LINES = ['def total_fruit(fruits):', '    counts = {}', '    left = 0', '    max_fruits = 0', '    for right in range(len(fruits)):', '        counts[fruits[right]] = counts.get(fruits[right], 0) + 1', '        while len(counts) > 2:', '            counts[fruits[left]] -= 1', '            if counts[fruits[left]] == 0: del counts[fruits[left]]', '            left += 1', '        max_fruits = max(max_fruits, right - left + 1)', '    return max_fruits']
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



def _fruit_into_baskets_instrumented(fruits):
    counts = {}
    left = 0
    max_fruits = 0
    for right in range(len(fruits)):
        counts[fruits[right]] = counts.get(fruits[right], 0) + 1
        _viz_compare(left, right)
        while len(counts) > 2:
            counts[fruits[left]] -= 1
            if counts[fruits[left]] == 0: del counts[fruits[left]]
            left += 1
            _viz_update(left, right)
        max_fruits = max(max_fruits, right - left + 1)
    return max_fruits

def run(input_data):
    fruits = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_fruit_into_baskets_instrumented",
        _fruit_into_baskets_instrumented,
        fruits,
        marker_fns={"_viz_compare", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
        }
    )
