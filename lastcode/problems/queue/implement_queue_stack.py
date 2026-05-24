"""Implement Queue using Stacks — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Implement Queue using Stacks'
CATEGORY = 'queue'
DIFFICULTY = 'easy'
RENDERER = 'queue'
DESCRIPTION = 'Implement a first-in-first-out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty).'
DEFAULT_INPUT = [("push", 1), ("push", 2), "pop", "peek"]

CODE_LINES = ['class MyQueue:', '    def __init__(self):', '        self.s1 = []; self.s2 = []', '    def push(self, val): self.s1.append(val)', '    def pop(self):', '        self.peek()', '        return self.s2.pop()', '    def peek(self):', '        if not self.s2:', '            while self.s1: self.s2.append(self.s1.pop())', '        return self.s2[-1]']
_LINE_MAP = {i: i for i in range(1, 12)}

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



def _implement_queue_stack_instrumented(ops):
    s1 = []
    s2 = []
    results = []
    for op in ops:
        if isinstance(op, tuple):
            action, val = op
        else:
            action, val = op, None
        if action == "push":
            s1.append(val)
            _viz_enqueue(val)
        elif action in ("pop", "peek"):
            if not s2:
                while s1:
                    popped = s1.pop()
                    _viz_dequeue(popped)
                    s2.append(popped)
            val = s2.pop() if action == "pop" else (s2[-1] if s2 else None)
            results.append(val)
    return results

def run(input_data):
    ops = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("val"), "locals": {"queue": locs.get("s1")}}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("popped"), "locals": {"queue": locs.get("s1")}}

    recorder = Recorder()
    return recorder.record(
        "_implement_queue_stack_instrumented",
        _implement_queue_stack_instrumented,
        ops,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
