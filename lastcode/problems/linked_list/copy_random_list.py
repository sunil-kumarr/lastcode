"""Copy List with Random Pointer — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Copy List with Random Pointer'
CATEGORY = 'linked_list'
DIFFICULTY = 'medium'
RENDERER = 'linked_list'
DESCRIPTION = 'A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null. Construct a deep copy of the list.'
DEFAULT_INPUT = [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]

CODE_LINES = ['def copy_random_list(head):', '    if not head: return None', '    curr = head; mapping = {}', '    while curr:', '        mapping[curr] = ListNode(curr.val)', '        curr = curr.next', '    curr = head', '    while curr:', '        node = mapping[curr]', '        if curr.next: node.next = mapping[curr.next]', '        if curr.random: node.random = mapping[curr.random]', '        curr = curr.next', '    return mapping[head]']
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


def build_list_random(arr):
    if not arr: return None
    from lastcode.problems.base import ListNode
    nodes = [ListNode(val[0]) for val in arr]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    for i, val in enumerate(arr):
        rnd_idx = val[1]
        if rnd_idx is not None and rnd_idx >= 0 and rnd_idx < len(nodes):
            nodes[i].random = nodes[rnd_idx]
    return nodes[0]


def _copy_random_list_instrumented(head):
    if not head: return None
    from lastcode.problems.base import ListNode
    curr = head
    mapping = {}
    while curr:
        new_node = ListNode(curr.val)
        mapping[id(curr)] = new_node
        _viz_compare(curr)
        curr = curr.next

    curr = head
    while curr:
        new_node = mapping[id(curr)]
        nxt = curr.next
        rnd = curr.random
        if nxt: new_node.next = mapping[id(nxt)]
        if rnd: new_node.random = mapping[id(rnd)]
        _viz_link(new_node, new_node.next)
        curr = curr.next
        _viz_update(new_node)
    return mapping[id(head)]

def run(input_data):
    head = build_list_random(input_data)
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_link(locs: dict, depth: int) -> dict | None:
        return {"type": "link_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_copy_random_list_instrumented",
        _copy_random_list_instrumented,
        head,
        marker_fns={"_viz_compare", "_viz_link", "_viz_update"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_link": handle_link,
            "_viz_update": handle_update,
        }
    )
