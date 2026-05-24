"""Design Circular Queue — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Design Circular Queue'
CATEGORY = 'queue'
DIFFICULTY = 'medium'
RENDERER = 'queue'
DESCRIPTION = 'Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the first position to make a circle.'
DEFAULT_INPUT = (3, [('enq', 1), ('enq', 2), 'deq', ('enq', 3)])

CODE_LINES = ['class MyCircularQueue:', '    def __init__(self, k):', '        self.q = [None] * k; self.head = -1; self.tail = -1; self.size = k', '    def enQueue(self, val):', '        if (self.tail + 1) % self.size == self.head: return False', '        if self.head == -1: self.head = 0', '        self.tail = (self.tail + 1) % self.size', '        self.q[self.tail] = val; return True', '    def deQueue(self):', '        if self.head == -1: return False', '        if self.head == self.tail: self.head = -1; self.tail = -1', '        else: self.head = (self.head + 1) % self.size', '        return True']
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



def _circular_queue_instrumented(size, ops):
    queue = [None] * size
    head = -1; tail = -1
    res = []
    for i, op in enumerate(ops):
        if isinstance(op, tuple):
            action, val = op
        else:
            action, val = op, None
        if action == "enq":
            if (tail + 1) % size == head:
                res.append(False)
            else:
                if head == -1: head = 0
                tail = (tail + 1) % size
                queue[tail] = val
                _viz_enqueue(val)
                res.append(True)
        elif action == "deq":
            if head == -1:
                res.append(False)
            else:
                val = queue[head]
                queue[head] = None
                _viz_dequeue(val)
                if head == tail:
                    head = -1; tail = -1
                else:
                    head = (head + 1) % size
                res.append(True)
    return res

def run(input_data):
    size, ops = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("val"), "locals": {"queue": [x for x in locs.get("queue", []) if x is not None]}}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("val"), "locals": {"queue": [x for x in locs.get("queue", []) if x is not None]}}

    recorder = Recorder()
    return recorder.record(
        "_circular_queue_instrumented",
        _circular_queue_instrumented,
        size, ops,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
