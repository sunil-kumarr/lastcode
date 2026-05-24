"""Find All Anagrams in String — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Find All Anagrams in String'
CATEGORY = 'sliding_window'
DIFFICULTY = 'medium'
RENDERER = 'sliding_window'
DESCRIPTION = "Given two strings s and p, return an array of all the start indices of p's anagrams in s."
DEFAULT_INPUT = ("cbaebabacd", "abc")

CODE_LINES = ['def find_anagrams(s, p):', '    res = []', '    if len(p) > len(s): return res', '    pc = {}; sc = {}', '    for char in p: pc[char] = pc.get(char, 0) + 1', '    for i in range(len(p)): sc[s[i]] = sc.get(s[i], 0) + 1', '    if sc == pc: res.append(0)', '    left = 0', '    for right in range(len(p), len(s)):', '        sc[s[right]] = sc.get(s[right], 0) + 1', '        sc[s[left]] -= 1', '        if sc[s[left]] == 0: del sc[s[left]]', '        left += 1', '        if sc == pc: res.append(left)', '    return res']
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



def _find_all_anagrams_instrumented(s, p):
    res = []
    if len(p) > len(s): return res
    pc = {}; sc = {}
    for char in p: pc[char] = pc.get(char, 0) + 1
    for i in range(len(p)): sc[s[i]] = sc.get(s[i], 0) + 1

    left = 0
    _viz_compare(left, len(p) - 1)
    if sc == pc: res.append(0)

    for right in range(len(p), len(s)):
        sc[s[right]] = sc.get(s[right], 0) + 1
        sc[s[left]] -= 1
        if sc[s[left]] == 0: del sc[s[left]]
        left += 1
        _viz_update(left, right)
        if sc == pc:
            _viz_found(left, right)
            res.append(left)
    return res

def run(input_data):
    s, p = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "window_check", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "window_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "window_found", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_find_all_anagrams_instrumented",
        _find_all_anagrams_instrumented,
        s, p,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
