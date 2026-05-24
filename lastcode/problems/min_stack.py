"""Min Stack — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Min Stack'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = 'Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.'
DEFAULT_INPUT = [("push", -2), ("push", 0), ("push", -3), "getMin", "pop", "top", "getMin"]

CODE_LINES = ['class MinStack:', '    def __init__(self):', '        self.stack = []', '        self.min_stack = []', '    def push(self, val):', '        self.stack.append(val)', '        val = min(val, self.min_stack[-1] if self.min_stack else val)', '        self.min_stack.append(val)', '    def pop(self):', '        self.stack.pop(); self.min_stack.pop()', '    def top(self): return self.stack[-1]', '    def getMin(self): return self.min_stack[-1]']
_LINE_MAP = {i: i for i in range(1, 13)}

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



def _min_stack_instrumented(operations):
    stack = []
    min_stack = []
    results = []
    for i, op in enumerate(operations):
        if isinstance(op, tuple):
            action, val = op
        else:
            action, val = op, None

        if action == "push":
            stack.append(val)
            if not min_stack or val <= min_stack[-1]:
                min_stack.append(val)
            else:
                min_stack.append(min_stack[-1])
            _viz_push(val)
        elif action == "pop":
            if stack:
                val = stack.pop()
                min_stack.pop()
                _viz_pop(val)
        elif action in ("top", "getMin"):
            val = min_stack[-1] if action == "getMin" else (stack[-1] if stack else None)
            _viz_peek(val)
            results.append(val)
    return results

def run(input_data):
    operations = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("val"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("val"), "locals": locs}
    def handle_peek(locs: dict, depth: int) -> dict | None:
        return {"type": "peek", "val": locs.get("val"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_min_stack_instrumented",
        _min_stack_instrumented,
        operations,
        marker_fns={"_viz_push", "_viz_pop", "_viz_peek"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
            "_viz_peek": handle_peek,
        }
    )
