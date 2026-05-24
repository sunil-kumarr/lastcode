"""Longest Repeating Char Replace — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Longest Repeating Char Replace'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = 'Given a string s and an integer k, you can choose any character of the string and change it to any other uppercase English character. Return the length of the longest substring containing all repeating letters you can get after performing at most k operations.'
DEFAULT_INPUT = ("AABABBA", 1)

CODE_LINES = ['def character_replacement(s, k):', '    counts = {}', '    max_count = 0', '    left = 0', '    max_len = 0', '    for right in range(len(s)):', '        counts[s[right]] = counts.get(s[right], 0) + 1', '        max_count = max(max_count, counts[s[right]])', '        while (right - left + 1) - max_count > k:', '            counts[s[left]] -= 1', '            left += 1', '        max_len = max(max_len, right - left + 1)', '    return max_len']
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



def _longest_repeating_char_replace_instrumented(s, k):
    counts = {}
    max_count = 0
    left = 0
    max_len = 0
    for right in range(len(s)):
        counts[s[right]] = counts.get(s[right], 0) + 1
        max_count = max(max_count, counts[s[right]])
        _viz_compare(left, right)
        while (right - left + 1) - max_count > k:
            counts[s[left]] -= 1
            left += 1
            _viz_update(left, right)
        max_len = max(max_len, right - left + 1)
    return max_len

def run(input_data):
    s, k = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_longest_repeating_char_replace_instrumented",
        _longest_repeating_char_replace_instrumented,
        s, k,
        marker_fns={"_viz_compare", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
        }
    )
