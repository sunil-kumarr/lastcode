import sys
import os

# Add project root to sys.path if running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import three_sum
from neonodes.renderers.two_pointer import TwoPointerRenderer

def test_three_sum_flow():
    print("Testing 3Sum step-by-step visualizer flow and variables...")
    input_data = [-1, 0, 1, 2, -1, -4]
    original_input = list(input_data)
    
    # Run problem recorder
    frames = three_sum.run(list(input_data))
    
    renderer = TwoPointerRenderer()
    filtered = renderer.filter_frames(frames)
    
    # 1. Verify frame filtering (consecutive duplicates and loop line frames removed)
    print(f"Original frames: {len(frames)}, Filtered frames: {len(filtered)}")
    assert len(filtered) == 19, f"Expected exactly 19 filtered steps, got {len(filtered)}"
    
    # 2. Step 0: Function Signature (Line 1)
    state_0 = renderer.compute_states(filtered, 0)
    entries_0 = renderer.variable_entries(filtered[0])
    keys_0 = [name for name, val, col in entries_0]
    
    print("Verifying Step 0 (Function Signature)...")
    assert state_0["sequence"] == original_input, "Step 0 must show original unsorted input"
    assert not state_0["is_sorting"], "Step 0 must not be in sorting state"
    assert "res" in keys_0, "'res' variable must be present in variables panel from the start"
    assert "sum_val" in keys_0, "'sum_val' variable must be present in variables panel from the start"
    assert "i" in keys_0, "'i' variable must be present in variables panel from the start"
    
    res_val_0 = [val for name, val, col in entries_0 if name == "res"][0]
    assert res_val_0 == "—", f"Expected res to be uninitialized ('—'), got {res_val_0}"

    # 3. Step 1: Sorting statement (Line 2: nums.sort())
    state_1 = renderer.compute_states(filtered, 1)
    print("Verifying Step 1 (Sorting Statement)...")
    assert state_1["is_sorting"], "Step 1 must trigger sorting state"
    assert state_1["prev_sequence"] == original_input, "Step 1 prev_sequence must be unsorted sequence"
    assert state_1["sequence"] == sorted(original_input), "Step 1 sequence must settle on sorted sequence"

    # 4. Step 2: res = [] assignment (Line 3)
    state_2 = renderer.compute_states(filtered, 2)
    entries_2 = renderer.variable_entries(filtered[2])
    print("Verifying Step 2 (res = [] assignment)...")
    assert state_2["sequence"] == sorted(original_input), "Step 2 sequence must be sorted sequence"
    res_val_2 = [val for name, val, col in entries_2 if name == "res"][0]
    assert res_val_2 == "—", "Step 2 res variable is highlighted but not yet executed (value should be uninitialized)"

    # 5. Step 3: First Pointer Comparison (Line 8)
    state_3 = renderer.compute_states(filtered, 3)
    entries_3 = renderer.variable_entries(filtered[3])
    print("Verifying Step 3 (First Pointer Comparison)...")
    
    res_val_3 = [val for name, val, col in entries_3 if name == "res"][0]
    assert res_val_3 == "[]", f"Expected res to be initialized to '[]', got {res_val_3}"
    
    i_val_3 = [val for name, val, col in entries_3 if name == "i"][0]
    assert i_val_3 == "0", f"Expected i to be '0', got {i_val_3}"
    
    left_val_3 = [val for name, val, col in entries_3 if name == "left"][0]
    assert left_val_3 == "1", f"Expected left to be '1', got {left_val_3}"
    
    right_val_3 = [val for name, val, col in entries_3 if name == "right"][0]
    assert right_val_3 == "5", f"Expected right to be '5', got {right_val_3}"
    
    sum_val_3 = [val for name, val, col in entries_3 if name == "sum_val"][0]
    assert sum_val_3 == "-3", f"Expected sum_val to be '-3', got {sum_val_3}"

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_three_sum_flow()
