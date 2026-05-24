"""Generate Parentheses — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Generate Parentheses'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = 'Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.'
DEFAULT_INPUT = 3

CODE_LINES = ['def generate_parentheses(n):', '    ans = []', '    stack = []', '    def backtrack(op, cl):', "        if op == cl == n: ans.append(''.join(stack)); return", '        if op < n:', "            stack.append('(')", '            backtrack(op + 1, cl)', '            stack.pop()', '        if cl < op:', "            stack.append(')')", '            backtrack(op, cl + 1)', '            stack.pop()']
_LINE_MAP = {i: i for i in range(1, 16)}

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



def _generate_parentheses_instrumented(n):
    ans = []
    stack = []
    def backtrack(open_c: int, close_c: int):
        if open_c == close_c == n:
            ans.append("".join(stack))
            _viz_peek("".join(stack))
            return
        if open_c < n:
            stack.append("(")
            _viz_push("(")
            backtrack(open_c + 1, close_c)
            stack.pop()
            _viz_pop("(")
        if close_c < open_c:
            stack.append(")")
            _viz_push(")")
            backtrack(open_c, close_c + 1)
            stack.pop()
            _viz_pop(")")
    backtrack(0, 0)
    return ans

def run(input_data):
    n = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": "(", "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": ")", "locals": locs}
    def handle_peek(locs: dict, depth: int) -> dict | None:
        return {"type": "peek", "val": locs.get("ans")[-1] if locs.get("ans") else "", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_generate_parentheses_instrumented",
        _generate_parentheses_instrumented,
        n,
        marker_fns={"_viz_push", "_viz_pop", "_viz_peek"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
            "_viz_peek": handle_peek,
        }
    )
