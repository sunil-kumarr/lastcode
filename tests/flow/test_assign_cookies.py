import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import assign_cookies
from neonodes.renderers.two_pointer import TwoPointerRenderer

def test_assign_cookies_flow():
    print("Testing Assign Cookies step-by-step visualizer flow and variables...")
    input_data = ([3, 1, 2], [1, 2])
    original_g = list(input_data[0])
    original_s = list(input_data[1])
    
    # Run problem recorder
    frames = assign_cookies.run(input_data)
    
    renderer = TwoPointerRenderer()
    filtered = renderer.filter_frames(frames)
    
    print(f"Original frames: {len(frames)}, Filtered frames: {len(filtered)}")
    
    # 1. Step 0: Function Signature (Line 1)
    state_0 = renderer.compute_states(filtered, 0)
    entries_0 = renderer.variable_entries(filtered[0])
    keys_0 = [name for name, val, col in entries_0]
    
    print("Verifying Step 0 (Function Signature)...")
    assert state_0["sequence"] == original_g, "Step 0 must show original unsorted input g"
    assert not state_0["is_sorting"], "Step 0 must not be in sorting state"
    assert "s" in keys_0, "'s' variable must be present in variables panel from the start"
    assert "left" in keys_0, "'left' variable must be present in variables panel from the start"
    assert "right" in keys_0, "'right' variable must be present in variables panel from the start"
    
    s_val_0 = [val for name, val, col in entries_0 if name == "s"][0]
    assert s_val_0 == str(original_s), f"Expected s to be {original_s}, got {s_val_0}"

    # 2. Step 1: Sorting statement (Line 2: g.sort(); s.sort())
    state_1 = renderer.compute_states(filtered, 1)
    print("Verifying Step 1 (Sorting Statement)...")
    assert state_1["is_sorting"], "Step 1 must trigger sorting state"
    assert state_1["prev_sequence"] == original_g, "Step 1 prev_sequence must be unsorted sequence g"
    assert state_1["sequence"] == sorted(original_g), "Step 1 sequence must settle on sorted sequence g"

    # 3. Step 2: pointers assignment (Line 3)
    state_2 = renderer.compute_states(filtered, 2)
    entries_2 = renderer.variable_entries(filtered[2])
    print("Verifying Step 2 (Pointers assignment)...")
    assert state_2["sequence"] == sorted(original_g), "Step 2 sequence must be sorted sequence g"
    left_val_2 = [val for name, val, col in entries_2 if name == "left"][0]
    assert left_val_2 == "—", "Step 2 left variable is highlighted but not yet executed (value should be uninitialized)"

    # 4. Step 3: First Pointer Comparison (Line 5)
    state_3 = renderer.compute_states(filtered, 3)
    entries_3 = renderer.variable_entries(filtered[3])
    print("Verifying Step 3 (First Pointer Comparison)...")
    
    left_val_3 = [val for name, val, col in entries_3 if name == "left"][0]
    assert left_val_3 == "0", f"Expected left to be '0', got {left_val_3}"
    
    right_val_3 = [val for name, val, col in entries_3 if name == "right"][0]
    assert right_val_3 == "0", f"Expected right to be '0', got {right_val_3}"
    
    s_val_3 = [val for name, val, col in entries_3 if name == "s"][0]
    assert s_val_3 == str(original_s), f"Expected s to be {original_s}, got {s_val_3}"

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_assign_cookies_flow()
