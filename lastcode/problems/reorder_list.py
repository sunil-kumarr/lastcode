"""Reorder List — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Reorder List'
CATEGORY = 'linked_list'
DIFFICULTY = 'medium'
RENDERER = 'linked_list'
DESCRIPTION = 'You are given the head of a singly linked-list. Reorder the list to be on the form L0 -> Ln -> L1 -> Ln-1 -> ...'
DEFAULT_INPUT = [1, 2, 3, 4]

CODE_LINES = ['def reorder_list(head):', '    if not head: return', '    slow = head; fast = head', '    while fast and fast.next:', '        slow = slow.next; fast = fast.next.next', '    prev = None; curr = slow.next; slow.next = None', '    while curr:', '        nxt = curr.next; curr.next = prev; prev = curr; curr = nxt', '    l1, l2 = head, prev', '    while l1 and l2:', '        nxt1, nxt2 = l1.next, l2.next', '        l1.next = l2; l2.next = nxt1', '        l1, l2 = nxt1, nxt2']
_LINE_MAP = {i: i for i in range(1, 14)}

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


def _reorder_list_instrumented(head):
    if not head: return
    slow = head; fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    prev = None
    curr = slow.next
    slow.next = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    l1 = head
    l2 = prev
    while l1 and l2:
        _viz_compare(l1, l2)
        nxt1 = l1.next
        nxt2 = l2.next

        l1.next = l2
        _viz_link(l1, l2)
        l2.next = nxt1
        _viz_link(l2, nxt1)

        l1 = nxt1
        l2 = nxt2
        _viz_update(l1, l2)

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
        "_reorder_list_instrumented",
        _reorder_list_instrumented,
        head,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
