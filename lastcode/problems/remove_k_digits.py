"""Remove K Digits — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Remove K Digits'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = 'Given string num representing a non-negative integer num, and an integer k, return the smallest possible integer after removing k digits from num.'
DEFAULT_INPUT = ("1432219", 3)

CODE_LINES = ['def remove_k_digits(num, k):', '    stack = []', '    for digit in num:', '        while k > 0 and stack and stack[-1] > digit:', '            stack.pop(); k -= 1', '        stack.append(digit)', '    while k > 0: stack.pop(); k -= 1', "    res = ''.join(stack).lstrip('0')", "    return res if res else '0'"]
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



def _remove_k_digits_instrumented(num, k):
    stack = []
    for i, digit in enumerate(num):
        while k > 0 and stack and stack[-1] > digit:
            popped = stack.pop()
            _viz_pop(popped)
            k -= 1
        stack.append(digit)
        _viz_push(digit)
    while k > 0:
        popped = stack.pop()
        _viz_pop(popped)
        k -= 1
    ans = "".join(stack).lstrip("0")
    return ans if ans else "0"

def run(input_data):
    num, k = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("digit"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_remove_k_digits_instrumented",
        _remove_k_digits_instrumented,
        num, k,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
