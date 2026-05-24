"""Next Greater Element I — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Next Greater Element I'
CATEGORY = 'stack'
DIFFICULTY = 'easy'
RENDERER = 'stack'
DESCRIPTION = 'The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.'
DEFAULT_INPUT = ([4, 1, 2], [1, 3, 4, 2])

CODE_LINES = ['def next_greater(nums1, nums2):', '    mapping = {}; stack = []', '    for num in nums2:', '        while stack and stack[-1] < num:', '            popped = stack.pop()', '            mapping[popped] = num', '        stack.append(num)', '    return [mapping.get(n, -1) for n in nums1]']
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



def _next_greater_element_instrumented(nums1, nums2):
    mapping = {}
    stack = []
    for i, num in enumerate(nums2):
        while stack and stack[-1] < num:
            popped = stack.pop()
            _viz_pop(popped)
            mapping[popped] = num
        stack.append(num)
        _viz_push(num)
    res = [mapping.get(n, -1) for n in nums1]
    return res

def run(input_data):
    nums1, nums2 = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("num"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_next_greater_element_instrumented",
        _next_greater_element_instrumented,
        nums1, nums2,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
