import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import container_water
from neonodes.renderers.two_pointer import TwoPointerRenderer

def test_container_water_flow():
    print("Testing Container With Most Water step-by-step visualizer flow and variables...")
    input_data = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    original_input = list(input_data)
    
    # Run problem recorder
    frames = container_water.run(input_data)
    
    renderer = TwoPointerRenderer()
    filtered = renderer.filter_frames(frames)
    
    print(f"Original frames: {len(frames)}, Filtered frames: {len(filtered)}")
    
    # 1. Step 0: Function Signature (Line 1)
    state_0 = renderer.compute_states(filtered, 0)
    entries_0 = renderer.variable_entries(filtered[0])
    keys_0 = [name for name, val, col in entries_0]
    
    print("Verifying Step 0 (Function Signature)...")
    assert state_0["sequence"] == original_input, "Step 0 must show original height input"
    assert "left" in keys_0, "'left' variable must be present in variables panel from the start"
    assert "right" in keys_0, "'right' variable must be present in variables panel from the start"
    assert "max_area" in keys_0, "'max_area' variable must be present in variables panel from the start"
    
    # 2. Step 3 (First comparison frame)
    state_3 = renderer.compute_states(filtered, 3)
    entries_3 = renderer.variable_entries(filtered[3])
    print("Verifying Step 3 (First Pointer Comparison)...")
    
    left_val_3 = [val for name, val, col in entries_3 if name == "left"][0]
    assert left_val_3 == "0", f"Expected left to be '0', got {left_val_3}"
    
    right_val_3 = [val for name, val, col in entries_3 if name == "right"][0]
    assert right_val_3 == "8", f"Expected right to be '8', got {right_val_3}"
    
    max_area_val_3 = [val for name, val, col in entries_3 if name == "max_area"][0]
    assert max_area_val_3 == "8", f"Expected max_area to be '8', got {max_area_val_3}"

    print("ALL TESTS PASSED SUCCESSFULLY!")

def test_container_water_big_numbers():
    print("Testing Container With Most Water with big numbers ratio scaling...")
    input_data = [100, 800, 600, 200, 500, 400, 800, 300, 700]
    
    # Run problem recorder
    frames = container_water.run(input_data)
    
    renderer = TwoPointerRenderer()
    filtered = renderer.filter_frames(frames)
    
    # Render a state to make sure it doesn't raise any formatting/rendering exception
    state_3 = renderer.compute_states(filtered, 3)
    widget = renderer.make_widget(input_data)
    renderer.update_widget(widget, input_data, state_3)
    rendered_text = widget.render()
    assert len(rendered_text.plain) > 0, "Rendered output should not be empty"
    print("Big numbers test passed!")

if __name__ == "__main__":
    test_container_water_flow()
    test_container_water_big_numbers()
