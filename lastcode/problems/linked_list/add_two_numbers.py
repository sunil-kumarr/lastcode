"""Add Two Numbers — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Add Two Numbers'
CATEGORY = 'linked_list'
DIFFICULTY = 'medium'
RENDERER = 'linked_list'
DESCRIPTION = 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.'
DEFAULT_INPUT = ([2, 4, 3], [5, 6, 4])

CODE_LINES = ['def add_two_numbers(l1, l2):', '    dummy = ListNode(0)', '    curr = dummy; carry = 0', '    while l1 or l2 or carry:', '        v1 = l1.val if l1 else 0', '        v2 = l2.val if l2 else 0', '        total = v1 + v2 + carry', '        carry = total // 10', '        curr.next = ListNode(total % 10)', '        curr = curr.next', '        if l1: l1 = l1.next', '        if l2: l2 = l2.next', '    return dummy.next']
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


def _add_two_numbers_instrumented(l1, l2):
    from lastcode.problems.base import ListNode
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    while l1 is not None or l2 is not None or carry > 0:
        _viz_compare(l1, l2)
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry = total // 10
        new_node = ListNode(total % 10)
        curr.next = new_node
        _viz_link(curr, new_node)
        curr = new_node
        if l1: l1 = l1.next
        if l2: l2 = l2.next
        _viz_update(curr, l1, l2)
    return dummy.next

def run(input_data):
    l1 = build_list(input_data[0]); l2 = build_list(input_data[1])
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_link(locs: dict, depth: int) -> dict | None:
        return {"type": "link_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_add_two_numbers_instrumented",
        _add_two_numbers_instrumented,
        l1, l2,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
