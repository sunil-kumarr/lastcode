import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lastcode.problems import trapping_rain_water
from lastcode.renderers.two_pointer import TwoPointerRenderer

def test_trapping_water_flow():
    print("Testing Trapping Rain Water step-by-step visualizer flow and variables...")
    input_data = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    original_input = list(input_data)
    
    # Run problem recorder
    frames = trapping_rain_water.run(input_data)
    
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
    assert "water" in keys_0, "'water' variable must be present in variables panel from the start"
    
    # 2. Step 3 (First comparison frame)
    state_3 = renderer.compute_states(filtered, 3)
    entries_3 = renderer.variable_entries(filtered[3])
    print("Verifying Step 3 (First Pointer Comparison)...")
    
    left_val_3 = [val for name, val, col in entries_3 if name == "left"][0]
    assert left_val_3 == "0", f"Expected left to be '0', got {left_val_3}"
    
    right_val_3 = [val for name, val, col in entries_3 if name == "right"][0]
    assert right_val_3 == "11", f"Expected right to be '11', got {right_val_3}"
    
    water_val_3 = [val for name, val, col in entries_3 if name == "water"][0]
    assert water_val_3 == "0", f"Expected water to be '0', got {water_val_3}"

    # Render a state to make sure it doesn't raise any formatting/rendering exception
    widget = renderer.make_widget(input_data)
    renderer.update_widget(widget, input_data, state_3)
    rendered_text = widget.render()
    assert len(rendered_text.plain) > 0, "Rendered output should not be empty"

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_trapping_water_flow()
