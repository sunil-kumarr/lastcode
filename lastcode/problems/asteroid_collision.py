"""Asteroid Collision — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Asteroid Collision'
CATEGORY = 'stack'
DIFFICULTY = 'medium'
RENDERER = 'stack'
DESCRIPTION = 'We are given an array asteroids of integers representing asteroids in a row. Find out the state of the asteroids after all collisions.'
DEFAULT_INPUT = [5, 10, -5]

CODE_LINES = ['def asteroid_collision(asteroids):', '    stack = []', '    for ast in asteroids:', '        while stack and ast < 0 < stack[-1]:', '            if stack[-1] < -ast: stack.pop(); continue', '            elif stack[-1] == -ast: stack.pop()', '            break', '        else: stack.append(ast)', '    return stack']
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



def _asteroid_collision_instrumented(asteroids):
    stack = []
    for i, ast in enumerate(asteroids):
        while stack and ast < 0 < stack[-1]:
            if stack[-1] < -ast:
                popped = stack.pop()
                _viz_pop(popped)
                continue
            elif stack[-1] == -ast:
                popped = stack.pop()
                _viz_pop(popped)
            break
        else:
            stack.append(ast)
            _viz_push(ast)
    return stack

def run(input_data):
    asteroids = input_data
    def handle_push(locs: dict, depth: int) -> dict | None:
        return {"type": "push", "val": locs.get("ast"), "locals": locs}
    def handle_pop(locs: dict, depth: int) -> dict | None:
        return {"type": "pop", "val": locs.get("popped"), "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_asteroid_collision_instrumented",
        _asteroid_collision_instrumented,
        asteroids,
        marker_fns={"_viz_push", "_viz_pop"},
        nested_fns=set(),
        marker_handlers={
            "_viz_push": handle_push,
            "_viz_pop": handle_pop,
        }
    )
