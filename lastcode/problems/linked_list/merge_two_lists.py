"""Merge Two Sorted Lists — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Merge Two Sorted Lists'
CATEGORY = 'linked_list'
DIFFICULTY = 'easy'
RENDERER = 'linked_list'
DESCRIPTION = 'You are given the heads of two sorted linked lists list1 and list2. Merge the two lists in a one sorted list.'
DEFAULT_INPUT = ([1, 3, 5], [2, 4, 6])

CODE_LINES = ['def merge_two_lists(list1, list2):', '    dummy = ListNode(0)', '    curr = dummy', '    while list1 and list2:', '        if list1.val <= list2.val:', '            curr.next = list1; list1 = list1.next', '        else:', '            curr.next = list2; list2 = list2.next', '        curr = curr.next', '    curr.next = list1 or list2', '    return dummy.next']
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


def _merge_two_lists_instrumented(list1, list2):
    from lastcode.problems.base import ListNode
    dummy = ListNode(0)
    curr = dummy
    while list1 is not None and list2 is not None:
        _viz_compare(list1, list2)
        if list1.val <= list2.val:
            curr.next = list1
            _viz_link(curr, list1)
            list1 = list1.next
        else:
            curr.next = list2
            _viz_link(curr, list2)
            list2 = list2.next
        curr = curr.next
        _viz_update(curr, list1, list2)
    if list1 is not None:
        curr.next = list1
        _viz_link(curr, list1)
    elif list2 is not None:
        curr.next = list2
        _viz_link(curr, list2)
    return dummy.next

def run(input_data):
    list1 = build_list(input_data[0]); list2 = build_list(input_data[1])
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_link(locs: dict, depth: int) -> dict | None:
        return {"type": "link_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_merge_two_lists_instrumented",
        _merge_two_lists_instrumented,
        list1, list2,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
