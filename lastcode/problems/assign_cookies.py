"""Assign Cookies — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Assign Cookies'
CATEGORY = 'two_pointer'
DIFFICULTY = 'easy'
RENDERER = 'two_pointer'
DESCRIPTION = 'Assume you are a awesome parent and want to give your cookies. But, you should give each child at most one cookie. Return the maximum number of children content.'
DEFAULT_INPUT = ([3, 1, 2], [1, 2])

CODE_LINES = ['def find_content_children(g, s):', '    g.sort(); s.sort()', '    left, right = 0, 0', '    while left < len(g) and right < len(s):', '        if s[right] >= g[left]:', '            left += 1', '        right += 1', '    return left']
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



def _assign_cookies_instrumented(g, s):
    g.sort(); s.sort()
    left, right = 0, 0
    while left < len(g) and right < len(s):
        _viz_compare(left, right)
        if s[right] >= g[left]:
            left += 1
        right += 1
        _viz_update(left, right)
    _viz_found(left, right)
    return left

def run(input_data):
    g, s = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_compare", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_assign_cookies_instrumented",
        _assign_cookies_instrumented,
        g, s,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
