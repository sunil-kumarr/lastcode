"""Palindrome Linked List — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Palindrome Linked List'
CATEGORY = 'linked_list'
DIFFICULTY = 'easy'
RENDERER = 'linked_list'
DESCRIPTION = 'Given the head of a singly linked list, return true if it is a palindrome or false otherwise.'
DEFAULT_INPUT = [1, 2, 2, 1]

CODE_LINES = ['def is_palindrome(head):', '    vals = []', '    curr = head', '    while curr:', '        vals.append(curr.val)', '        curr = curr.next', '    return vals == vals[::-1]']
_LINE_MAP = {i: i for i in range(1, 8)}

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


def _palindrome_linked_list_instrumented(head):
    vals = []
    curr = head
    while curr:
        _viz_compare(curr)
        vals.append(curr.val)
        curr = curr.next
    return vals == vals[::-1]

def run(input_data):
    head = build_list(input_data)
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_palindrome_linked_list_instrumented",
        _palindrome_linked_list_instrumented,
        head,
        marker_fns={"_viz_compare"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
        }
    )
