"""Implement Stack using Queues — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Implement Stack using Queues'
CATEGORY = 'queue'
DIFFICULTY = 'easy'
RENDERER = 'queue'
DESCRIPTION = 'Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (push, top, pop, and empty).'
DEFAULT_INPUT = [("push", 1), ("push", 2), "pop", "top"]

CODE_LINES = ['class MyStack:', '    def __init__(self):', '        self.q = []', '    def push(self, val):', '        self.q.append(val)', '        for _ in range(len(self.q) - 1):', '            self.q.append(self.q.pop(0))', '    def pop(self): return self.q.pop(0)', '    def top(self): return self.q[0]']
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



def _implement_stack_queue_instrumented(ops):
    queue = []
    results = []
    for op in ops:
        if isinstance(op, tuple):
            action, val = op
        else:
            action, val = op, None
        if action == "push":
            queue.append(val)
            _viz_enqueue(val)
            for _ in range(len(queue) - 1):
                popped = queue.pop(0)
                _viz_dequeue(popped)
                queue.append(popped)
                _viz_enqueue(popped)
        elif action == "pop":
            if queue:
                val = queue.pop(0)
                _viz_dequeue(val)
                results.append(val)
        elif action == "top":
            val = queue[0] if queue else None
            results.append(val)
    return results

def run(input_data):
    ops = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("val", locs.get("popped")), "locals": locs}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("val", locs.get("popped")), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_implement_stack_queue_instrumented",
        _implement_stack_queue_instrumented,
        ops,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
