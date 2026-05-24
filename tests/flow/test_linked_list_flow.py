import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lastcode.problems import reverse_linked_list, linked_list_cycle
from lastcode.renderers.linked_list import LinkedListRenderer

def test_reverse_linked_list_flow():
    print("Testing Reverse Linked List renderer flow...")
    input_data = [1, 2, 3, 4]
    
    frames = reverse_linked_list.run(input_data)
    renderer = LinkedListRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Verify nodes and pointers in a step in the middle
    state = renderer.compute_states(filtered, len(filtered) - 1)
    nodes = state.get("nodes", [])
    
    # We should have nodes matching our input_data list values
    node_vals = [n["val"] for n in nodes]
    for val in input_data:
        assert val in node_vals, f"Node({val}) should be tracked in nodes list"
        
    pointers = state.get("pointers", {})
    # Check that pointers contains head, curr, prev or similar pointer variables
    all_pointers = []
    for nid, plist in pointers.items():
        all_pointers.extend(plist)
    assert "prev" in all_pointers or "curr" in all_pointers or "head" in all_pointers

def test_linked_list_cycle_flow():
    print("Testing Linked List Cycle renderer flow...")
    # (arr, pos) representing a list with a cycle back to pos
    input_data = ([3, 2, 0, -4], 1)
    
    frames = linked_list_cycle.run(input_data)
    renderer = LinkedListRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    state = renderer.compute_states(filtered, len(filtered) - 1)
    nodes = state.get("nodes", [])
    assert len(nodes) > 0
