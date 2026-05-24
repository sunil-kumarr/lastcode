import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import daily_temperatures, eval_rpn, asteroid_collision, next_greater_element, simplify_path
from neonodes.renderers.stack import StackRenderer

def test_daily_temperatures_flow():
    print("Testing Daily Temperatures stack renderer flow...")
    input_data = [73, 74, 75, 71, 69, 72, 76, 73]
    
    # Run problem recorder
    frames = daily_temperatures.run(list(input_data))
    
    renderer = StackRenderer()
    filtered = renderer.filter_frames(frames)
    
    # Verify we got some steps
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Compute states for a step in the middle (e.g. step where we pop and compare)
    # Let's find a step with 'pop' operation
    pop_step_idx = None
    for idx, f in enumerate(filtered):
        state = renderer.compute_states(filtered, idx)
        if state.get("op_type") == "pop":
            pop_step_idx = idx
            break
            
    assert pop_step_idx is not None, "Should find at least one pop operation in Daily Temperatures flow"
    
    state = renderer.compute_states(filtered, pop_step_idx)
    # Verify pointers are tracked
    pointers = state.get("pointers", {})
    assert "i" in pointers, "'i' pointer should be tracked"
    assert "idx" in pointers or "idx" in state.get("accumulated_locals", {}), "idx should be tracked"
    
    # Verify variable entries style pointers
    entries = renderer.variable_entries(filtered[pop_step_idx])
    keys = [name for name, val, col in entries]
    assert "stack" in keys, "stack should be in variable entries"
    assert "i" in keys, "i pointer should be in variable entries"

def test_eval_rpn_flow():
    print("Testing Eval RPN stack renderer flow...")
    input_data = ["2", "1", "+", "3", "*"]
    
    frames = eval_rpn.run(list(input_data))
    renderer = StackRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Find a push step
    push_step_idx = None
    for idx, f in enumerate(filtered):
        state = renderer.compute_states(filtered, idx)
        if state.get("op_type") == "push":
            push_step_idx = idx
            break
            
    assert push_step_idx is not None, "Should find at least one push operation"
    
    state = renderer.compute_states(filtered, push_step_idx)
    assert len(state.get("stack", [])) > 0, "Stack should not be empty after a push"
    assert "i" in state.get("pointers", {}), "'i' pointer should be tracked for eval_rpn"

def test_asteroid_collision_flow():
    print("Testing Asteroid Collision stack renderer flow...")
    input_data = [5, 10, -5]
    
    frames = asteroid_collision.run(list(input_data))
    renderer = StackRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Verify sequence detection and pointer tracking
    state = renderer.compute_states(filtered, len(filtered) - 1)
    assert state.get("sequence") == input_data, "Should detect asteroids as sequence"
    assert "i" in state.get("pointers", {}), "'i' pointer should be tracked for asteroid_collision"

def test_next_greater_element_flow():
    print("Testing Next Greater Element I stack renderer flow...")
    input_data = ([4, 1, 2], [1, 3, 4, 2])
    
    frames = next_greater_element.run(input_data)
    renderer = StackRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Verify sequence detection (nums2 is traversed) and pointer tracking
    state = renderer.compute_states(filtered, len(filtered) - 1)
    assert state.get("sequence") == input_data[1], "Should detect nums2 as sequence"
    assert "i" in state.get("pointers", {}), "'i' pointer should be tracked for next_greater_element"

def test_simplify_path_flow():
    print("Testing Simplify Path stack renderer flow...")
    input_data = "/home//foo/"
    
    frames = simplify_path.run(input_data)
    renderer = StackRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Verify sequence detection (split parts) and pointer tracking
    state = renderer.compute_states(filtered, len(filtered) - 1)
    assert state.get("sequence") == ["", "home", "", "foo", ""], "Should detect parts as sequence"
    assert "i" in state.get("pointers", {}), "'i' pointer should be tracked for simplify_path"

