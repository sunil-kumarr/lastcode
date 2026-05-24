"""Backspace String Compare — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Backspace String Compare'
CATEGORY = 'two_pointer'
DIFFICULTY = 'easy'
RENDERER = 'two_pointer'
DESCRIPTION = "Given two strings s and t, return true if they are equal when both are typed into empty text editors. '#' means a backspace character."
DEFAULT_INPUT = ("ab#c", "ad#c")

CODE_LINES = ['def backspace_compare(s, t):', '    def next_valid(string, index):', '        backspaces = 0', '        while index >= 0:', "            if string[index] == '#': backspaces += 1", '            elif backspaces > 0: backspaces -= 1', '            else: break', '            index -= 1', '        return index', '    i, j = len(s) - 1, len(t) - 1', '    while i >= 0 or j >= 0:', '        i = next_valid(s, i); j = next_valid(t, j)', '        if i >= 0 and j >= 0 and s[i] != t[j]: return False', '        if (i >= 0) != (j >= 0): return False', '        i -= 1; j -= 1', '    return True']
_LINE_MAP = {i: i for i in range(1, 17)}

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



def _backspace_compare_instrumented(s, t):
    def next_valid(string, index):
        backspaces = 0
        while index >= 0:
            if string[index] == '#': backspaces += 1
            elif backspaces > 0: backspaces -= 1
            else: break
            index -= 1
        return index
    i, j = len(s) - 1, len(t) - 1
    while i >= 0 or j >= 0:
        _viz_compare(i, j)
        i = next_valid(s, i); j = next_valid(t, j)
        if i >= 0 and j >= 0 and s[i] != t[j]: return False
        if (i >= 0) != (j >= 0): return False
        i -= 1; j -= 1
        _viz_update(i, j)
    _viz_found(i, j)
    return True

def run(input_data):
    s, t = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_compare", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_backspace_compare_instrumented",
        _backspace_compare_instrumented,
        s, t,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
