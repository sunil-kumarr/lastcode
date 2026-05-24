"""Odd Even Linked List — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Odd Even Linked List'
CATEGORY = 'linked_list'
DIFFICULTY = 'medium'
RENDERER = 'linked_list'
DESCRIPTION = 'Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.'
DEFAULT_INPUT = [1, 2, 3, 4, 5]

CODE_LINES = ['def odd_even_list(head):', '    if not head: return None', '    odd = head; even = head.next; even_head = even', '    while even and even.next:', '        odd.next = even.next; odd = odd.next', '        even.next = odd.next; even = even.next', '    odd.next = even_head', '    return head']
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


def _odd_even_list_instrumented(head):
    if not head: return None
    odd = head
    even = head.next
    even_head = even
    while even and even.next:
        _viz_compare(odd, even)
        odd.next = even.next
        _viz_link(odd, even.next)
        odd = odd.next

        even.next = odd.next
        _viz_link(even, odd.next)
        even = even.next
        _viz_update(odd, even)
    odd.next = even_head
    _viz_link(odd, even_head)
    return head

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
        "_odd_even_list_instrumented",
        _odd_even_list_instrumented,
        head,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
