"""Basic Calculator — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Basic Calculator'
CATEGORY = 'stack'
DIFFICULTY = 'hard'
RENDERER = 'stack'
DESCRIPTION = 'Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.'
DEFAULT_INPUT = "(1+(4+5+2)-3)+(6+8)"

CODE_LINES = ['def calculate(s):', '    stack = []; res = 0; sign = 1; op = 0', '    for ch in s:', '        if ch.isdigit(): op = op * 10 + int(ch)', "        elif ch == '+': res += sign * op; op = 0; sign = 1", "        elif ch == '-': res += sign * op; op = 0; sign = -1", "        elif ch == '(': stack.append(res); stack.append(sign); res = 0; sign = 1", "        elif ch == ')':: res += sign * op; op = 0; res = stack.pop() * res + stack.pop()", '    return res + sign * op']
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



def _basic_calculator_instrumented(s):
    stack = []
    operand = 0
    res = 0
    sign = 1
    for i, ch in enumerate(s):
        if ch.isdigit():
            operand = operand * 10 + int(ch)
        elif ch == '+':
            res += sign * operand
            operand = 0
            sign = 1
        elif ch == '-':
            res += sign * operand
            operand = 0
            sign = -1
        elif ch == '(':
            stack.append(res)
            _viz_push(res)
            stack.append(sign)
            _viz_push(sign)
            res = 0
            sign = 1
        elif ch == ')':
            res += sign * operand
            operand = 0
            p_sign = stack.pop()
            _viz_pop(p_sign)
            p_res = stack.pop()
            _viz_pop(p_res)
            res = p_res + p_sign * res
    res += sign * operand
    return res

def run(input_data):
    s = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("res", locs.get("sign")), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("p_sign", locs.get("p_res")), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_basic_calculator_instrumented",
        _basic_calculator_instrumented,
        s,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
