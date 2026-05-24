"""Longest Substring No Repeat — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Longest Substring No Repeat'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given a string s, find the length of the longest substring without repeating characters.'
DEFAULT_INPUT = "abcabcbb"

CODE_LINES = ['def longest_substring(s):', '    char_map = {}', '    left = 0', '    max_len = 0', '    for right in range(len(s)):', '        char = s[right]', '        if char in char_map and char_map[char] >= left:', '            left = char_map[char] + 1', '        char_map[char] = right', '        max_len = max(max_len, right - left + 1)', '    return max_len']
_LINE_MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11}

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



def _longest_substring_no_repeat_instrumented(s):
    char_map = {}
    left = 0
    max_len = 0
    for right in range(len(s)):
        char = s[right]
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
            _viz_update(left, right)
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
        _viz_compare(left, right)
    return max_len

def run(input_data):
    s = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_longest_substring_no_repeat_instrumented",
        _longest_substring_no_repeat_instrumented,
        s,
        marker_fns={"_viz_compare", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
        }
    )
