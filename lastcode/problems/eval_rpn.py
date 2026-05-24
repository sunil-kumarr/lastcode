"""Evaluate Reverse Polish Notation — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Evaluate Reverse Polish Notation'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = 'Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are +, -, *, and /.'
DEFAULT_INPUT = ["2", "1", "+", "3", "*"]

CODE_LINES = ['def eval_rpn(tokens):', '    stack = []', '    for token in tokens:', "        if token in ('+', '-', '*', '/'):", '            b = stack.pop(); a = stack.pop()', "            if token == '+': stack.append(a + b)", "            elif token == '-': stack.append(a - b)", "            elif token == '*': stack.append(a * b)", '            else: stack.append(int(a / b))', '        else: stack.append(int(token))', '    return stack[0]']
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



def _eval_rpn_instrumented(tokens):
    stack = []
    for i, token in enumerate(tokens):
        if token in ("+", "-", "*", "/"):
            b = stack.pop()
            _viz_pop(b)
            a = stack.pop()
            _viz_pop(a)
            if token == "+": res = a + b
            elif token == "-": res = a - b
            elif token == "*": res = a * b
            else: res = int(a / b)
            stack.append(res)
            _viz_push(res)
        else:
            val = int(token)
            stack.append(val)
            _viz_push(val)
    return stack[0] if stack else 0

def run(input_data):
    tokens = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("res", locs.get("val")), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("b") if "b" in locs else locs.get("a"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_eval_rpn_instrumented",
        _eval_rpn_instrumented,
        tokens,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
