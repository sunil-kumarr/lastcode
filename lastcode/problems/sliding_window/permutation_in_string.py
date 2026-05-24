"""Permutation in String — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Permutation in String'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.'
DEFAULT_INPUT = ("ab", "eidbaooo")

CODE_LINES = ['def check_inclusion(s1, s2):', '    if len(s1) > len(s2): return False', '    c1 = {}; c2 = {}', '    for c in s1: c1[c] = c1.get(c, 0) + 1', '    for i in range(len(s1)): c2[s2[i]] = c2.get(s2[i], 0) + 1', '    if c1 == c2: return True', '    left = 0', '    for right in range(len(s1), len(s2)):', '        c2[s2[right]] = c2.get(s2[right], 0) + 1', '        c2[s2[left]] -= 1', '        if c2[s2[left]] == 0: del c2[s2[left]]', '        left += 1', '        if c1 == c2: return True', '    return False']
_LINE_MAP = {i: i for i in range(1, 15)}

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



def _permutation_in_string_instrumented(s1, s2):
    if len(s1) > len(s2): return False
    c1 = {}; c2 = {}
    for c in s1: c1[c] = c1.get(c, 0) + 1
    for i in range(len(s1)): c2[s2[i]] = c2.get(s2[i], 0) + 1

    left = 0
    _viz_compare(left, len(s1) - 1)
    if c1 == c2: return True

    for right in range(len(s1), len(s2)):
        c2[s2[right]] = c2.get(s2[right], 0) + 1
        c2[s2[left]] -= 1
        if c2[s2[left]] == 0: del c2[s2[left]]
        left += 1
        _viz_update(left, right)
        if c1 == c2:
            _viz_found(left, right)
            return True
    return False

def run(input_data):
    s1, s2 = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "window_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_permutation_in_string_instrumented",
        _permutation_in_string_instrumented,
        s1, s2,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
