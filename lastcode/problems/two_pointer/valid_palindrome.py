"""Valid Palindrome — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Valid Palindrome'
CATEGORY = 'two_pointer'
DIFFICULTY = 'easy'
RENDERER = 'two_pointer'
DESCRIPTION = 'A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.'
DEFAULT_INPUT = "A man, a plan, a canal: Panama"

CODE_LINES = ['def is_palindrome(s):', "    clean_s = ''.join(c.lower() for c in s if c.isalnum())", '    left, right = 0, len(clean_s) - 1', '    while left < right:', '        if clean_s[left] != clean_s[right]:', '            return False', '        left += 1; right -= 1', '    return True']
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



def _valid_palindrome_instrumented(s):
    clean_s = "".join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(clean_s) - 1
    while left < right:
        _viz_compare(left, right)
        if clean_s[left] != clean_s[right]:
            return False
        left += 1; right -= 1
        _viz_update(left, right)
    _viz_found(left, right)
    return True

def run(input_data):
    s = input_data
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_compare", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_found", "locals": locs}

    recorder = Recorder()
    clean_s = "".join(c.lower() for c in s if c.isalnum())
    return recorder.record(
        "_valid_palindrome_instrumented",
        _valid_palindrome_instrumented,
        clean_s,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
