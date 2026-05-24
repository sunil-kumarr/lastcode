"""Minimum Window Substring — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Minimum Window Substring'
CATEGORY = 'sliding_window'
DIFFICULTY = 'hard'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given two strings s and t, return the minimum window substring of s such that every character in t (including duplicates) is included in the window.'
DEFAULT_INPUT = ("ADOBECODEBANC", "ABC")

CODE_LINES = ['def min_window(s, t):', "    if not s or not t: return ''", '    dict_t = {}', '    for c in t: dict_t[c] = dict_t.get(c, 0) + 1', '    required = len(dict_t)', '    left = 0; formed = 0', '    window_counts = {}', "    ans = (float('inf'), None, None)", '    for right in range(len(s)):', '        char = s[right]', '        window_counts[char] = window_counts.get(char, 0) + 1', '        if char in dict_t and window_counts[char] == dict_t[char]:', '            formed += 1', '        while left <= right and formed == required:', '            if right - left + 1 < ans[0]:', '                ans = (right - left + 1, left, right)', '            char = s[left]', '            window_counts[char] -= 1', '            if char in dict_t and window_counts[char] < dict_t[char]:', '                formed -= 1', '            left += 1', "    return '' if ans[0] == float('inf') else s[ans[1]:ans[2]+1]"]
_LINE_MAP = {i: i for i in range(1, 23)}

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



def _min_window_substring_instrumented(s, t):
    if not s or not t: return ""
    dict_t = {}
    for c in t: dict_t[c] = dict_t.get(c, 0) + 1
    required = len(dict_t)
    left = 0; formed = 0
    window_counts = {}
    ans = (float('inf'), None, None)
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
        _viz_compare(left, right)
        while left <= right and formed == required:
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
                _viz_found(left, right)
            char = s[left]
            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
            left += 1
            _viz_update(left, right)
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]

def run(input_data):
    s, t = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "window_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_min_window_substring_instrumented",
        _min_window_substring_instrumented,
        s, t,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
