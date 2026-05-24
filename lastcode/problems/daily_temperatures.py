"""Daily Temperatures — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Daily Temperatures'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = 'Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the i-th day to get a warmer temperature.'
DEFAULT_INPUT = [73, 74, 75, 71, 69, 72, 76, 73]

CODE_LINES = ['def daily_temperatures(temperatures):', '    ans = [0] * len(temperatures)', '    stack = []', '    for i, temp in enumerate(temperatures):', '        while stack and temperatures[stack[-1]] < temp:', '            idx = stack.pop()', '            ans[idx] = i - idx', '        stack.append(i)', '    return ans']
_LINE_MAP = {i: i for i in range(1, 10)}

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



def _daily_temperatures_instrumented(temperatures):
    ans = [0] * len(temperatures)
    stack = []
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            idx = stack.pop()
            _viz_pop(idx)
            ans[idx] = i - idx
        stack.append(i)
        _viz_push(i)
    return ans

def run(input_data):
    temperatures = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("i"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("idx"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_daily_temperatures_instrumented",
        _daily_temperatures_instrumented,
        temperatures,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
