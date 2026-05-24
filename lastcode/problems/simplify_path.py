"""Simplify Path — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Simplify Path'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = "Given a string path, which is an absolute path (starting with a slash '/') to a file or directory in a Unix-style file system, convert it to the simplified canonical path."
DEFAULT_INPUT = "/home//foo/"

CODE_LINES = ['def simplify_path(path):', '    stack = []', "    for part in path.split('/'):", "        if part == '..':", '            if stack: stack.pop()', "        elif part and part != '.':", '            stack.append(part)', "    return '/' + '/'.join(stack)"]
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



def _simplify_path_instrumented(path):
    stack = []
    parts = path.split("/")
    for i, part in enumerate(parts):
        if part == "..":
            if stack:
                popped = stack.pop()
                _viz_pop(popped)
        elif part and part != ".":
            stack.append(part)
            _viz_push(part)
    return "/" + "/".join(stack)

def run(input_data):
    path = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("part"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_simplify_path_instrumented",
        _simplify_path_instrumented,
        path,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
