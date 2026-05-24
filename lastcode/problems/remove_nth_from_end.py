"""Remove Nth Node From End — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Remove Nth Node From End'
CATEGORY = 'linked_list'
DIFFICULTY = 'medium'
RENDERER = 'linked_list'
DESCRIPTION = 'Given the head of a linked list, remove the nth node from the end of the list and return its head.'
DEFAULT_INPUT = ([1, 2, 3, 4, 5], 2)

CODE_LINES = ['def remove_nth_from_end(head, n):', '    dummy = ListNode(0, head)', '    slow = dummy; fast = dummy', '    for _ in range(n + 1): fast = fast.next', '    while fast is not None:', '        slow = slow.next; fast = fast.next', '    slow.next = slow.next.next', '    return dummy.next']
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


def _remove_nth_from_end_instrumented(head, n):
    from lastcode.problems.base import ListNode
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    for _ in range(n + 1):
        if fast: fast = fast.next
    _viz_update(slow, fast)
    while fast is not None:
        _viz_compare(slow, fast)
        slow = slow.next
        fast = fast.next
        _viz_update(slow, fast)
    to_delete = slow.next
    if to_delete:
        slow.next = to_delete.next
        _viz_link(slow, to_delete.next)
    return dummy.next

def run(input_data):
    head = build_list(input_data[0]); n = input_data[1]
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_link(locs: dict, depth: int) -> dict | None:
        return {"type": "link_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_remove_nth_from_end_instrumented",
        _remove_nth_from_end_instrumented,
        head, n,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
