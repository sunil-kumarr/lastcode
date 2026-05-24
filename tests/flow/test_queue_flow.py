import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import moving_average, recent_calls
from neonodes.renderers.queue import QueueRenderer

def test_moving_average_flow():
    print("Testing Moving Average queue renderer flow...")
    input_data = ([1, 10, 3, 5], 3)
    
    frames = moving_average.run(input_data)
    renderer = QueueRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    # Verify sequence detection and pointer tracking
    state = renderer.compute_states(filtered, len(filtered) - 1)
    assert state.get("sequence") == input_data[0], "Should detect val_list as sequence"
    assert "i" in state.get("pointers", {}), "'i' pointer should be tracked for moving_average"
    assert len(state.get("queue", [])) > 0, "Queue should not be empty"

def test_recent_calls_flow():
    print("Testing Recent Calls queue renderer flow...")
    input_data = [1, 100, 3001, 3002]
    
    frames = recent_calls.run(input_data)
    renderer = QueueRenderer()
    filtered = renderer.filter_frames(frames)
    
    assert len(filtered) > 0, "Should have filtered frames"
    
    state = renderer.compute_states(filtered, len(filtered) - 1)
    assert state.get("sequence") == input_data, "Should detect t_list as sequence"
    assert "i" in state.get("pointers", {}), "'i' pointer should be tracked for recent_calls"
