"""Intersection of Two Lists — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Intersection of Two Lists'
CATEGORY = 'linked_list'
DIFFICULTY = 'easy'
RENDERER = 'linked_list'
DESCRIPTION = 'Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.'
DEFAULT_INPUT = ([4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3)

CODE_LINES = ['def get_intersection_node(headA, headB):', '    pA = headA; pB = headB', '    while pA != pB:', '        pA = pA.next if pA else headB', '        pB = pB.next if pB else headA', '    return pA']
_LINE_MAP = {i: i for i in range(1, 7)}

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


def build_intersect_lists(arrA, arrB, skipA, skipB):
    if not arrA or not arrB: return None, None
    from lastcode.problems.base import ListNode
    nodesA = [ListNode(val) for val in arrA[:skipA]]
    nodesB = [ListNode(val) for val in arrB[:skipB]]
    nodesCommon = [ListNode(val) for val in arrA[skipA:]]
    
    for i in range(len(nodesA) - 1): nodesA[i].next = nodesA[i+1]
    for i in range(len(nodesB) - 1): nodesB[i].next = nodesB[i+1]
    for i in range(len(nodesCommon) - 1): nodesCommon[i].next = nodesCommon[i+1]
    
    if nodesCommon:
        if nodesA: nodesA[-1].next = nodesCommon[0]
        else: nodesA = nodesCommon
        if nodesB: nodesB[-1].next = nodesCommon[0]
        else: nodesB = nodesCommon
    return nodesA[0] if nodesA else None, nodesB[0] if nodesB else None


def _intersection_two_lists_instrumented(headA, headB):
    pA = headA
    pB = headB
    while pA != pB:
        _viz_compare(pA, pB)
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA
        _viz_update(pA, pB)
    _viz_found(pA)
    return pA

def run(input_data):
    headA, headB = build_intersect_lists(input_data[0], input_data[1], input_data[2], input_data[3])
    def handle_compare(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_update(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}
    def handle_found(locs: dict, depth: int) -> dict | None:
        return {"type": "pointer_update", "locals": locs}

    recorder = Recorder()
    return recorder.record(
        "_intersection_two_lists_instrumented",
        _intersection_two_lists_instrumented,
        headA, headB,
        marker_fns={"_viz_compare", "_viz_update", "_viz_found"},
        nested_fns=set(),
        marker_handlers={
            "_viz_compare": handle_compare,
            "_viz_update": handle_update,
            "_viz_found": handle_found,
        }
    )
