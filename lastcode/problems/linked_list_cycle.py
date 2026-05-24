"""Linked List Cycle — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Linked List Cycle'
CATEGORY = 'linked_list'
DIFFICULTY = 'easy'
RENDERER = 'linked_list'
DESCRIPTION = 'Given head, the head of a linked list, determine if the linked list has a cycle in it.'
DEFAULT_INPUT = ([1, 2, 3, 4], 1)

CODE_LINES = ['def has_cycle(head):', '    slow = head', '    fast = head', '    while fast and fast.next:', '        slow = slow.next', '        fast = fast.next.next', '        if slow == fast: return True', '    return False']
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


def build_list(arr):
    if not arr: return None
    from lastcode.problems.base import ListNode
    nodes = [ListNode(val) for val in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    return nodes[0]

def build_list_cycle(arr, pos):
    if not arr: return None
    from lastcode.problems.base import ListNode
    nodes = [ListNode(val) for val in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    if pos >= 0 and pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0]


def _linked_list_cycle_instrumented(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        _viz_compare(slow, fast)
        slow = slow.next
        fast = fast.next.next
        _viz_update(slow, fast)
        if slow == fast:
            _viz_found(slow)
            return True
    return False

def run(input_data):
    head = build_list_cycle(input_data[0], input_data[1])
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_linked_list_cycle_instrumented",
        _linked_list_cycle_instrumented,
        head,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
