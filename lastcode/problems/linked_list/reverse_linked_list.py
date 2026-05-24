"""Reverse Linked List — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Reverse Linked List'
CATEGORY = 'linked_list'
DIFFICULTY = 'easy'
RENDERER = 'linked_list'
DESCRIPTION = 'Given the head of a singly linked list, reverse the list, and return the reversed list.'
DEFAULT_INPUT = [1, 2, 3, 4]

CODE_LINES = ['def reverse_list(head):', '    prev = None', '    curr = head', '    while curr is not None:', '        nxt = curr.next', '        curr.next = prev', '        prev = curr', '        curr = nxt', '    return prev']
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


def _reverse_linked_list_instrumented(head):
    prev = None
    curr = head
    while curr is not None:
        _viz_compare(curr)
        nxt = curr.next
        curr.next = prev
        _viz_link(curr, prev)
        prev = curr
        curr = nxt
        _viz_update(prev, curr)
    return prev

def run(input_data):
    head = build_list(input_data)
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_link(locs: dict, depth: int) -> dict | None:
        return {"type": "link_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_reverse_linked_list_instrumented",
        _reverse_linked_list_instrumented,
        head,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
