"""Online Stock Span — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Online Stock Span'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = "Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day."
DEFAULT_INPUT = [100, 80, 60, 70, 60, 75, 85]

CODE_LINES = ['class StockSpanner:', '    def __init__(self):', '        self.stack = []', '    def next(self, price):', '        span = 1', '        while self.stack and self.stack[-1][0] <= price:', '            span += self.stack.pop()[1]', '        self.stack.append((price, span))', '        return span']
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



def _online_stock_span_instrumented(prices):
    stack = []
    res = []
    for i, price in enumerate(prices):
        span = 1
        while stack and stack[-1][0] <= price:
            popped = stack.pop()
            _viz_pop(popped)
            span += popped[1]
        stack.append((price, span))
        _viz_push((price, span))
        res.append(span)
    return res

def run(input_data):
    prices = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("price"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_online_stock_span_instrumented",
        _online_stock_span_instrumented,
        prices,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
