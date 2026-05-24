"""Flow regression test — Minimum Size Subarray Sum."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import min_size_subarray_sum
from neonodes.renderers.sliding_window import SlidingWindowRenderer


def test_min_subarray_sum_flow():
    print("Testing Min Size Subarray Sum flow...")
    nums, target = [2, 3, 1, 2, 4, 3], 7
    input_data = (nums, target)

    frames = min_size_subarray_sum.run(input_data)
    r = SlidingWindowRenderer()
    filtered = r.filter_frames(frames)

    print(f"Total frames: {len(frames)}, Filtered: {len(filtered)}")
    assert len(filtered) > 0

    # Step 0
    state0 = r.compute_states(filtered, 0)
    entries0 = r.variable_entries(filtered[0])
    keys0 = [k for k, v, c in entries0]

    print("Step 0 — checking initial state...")
    assert state0["sequence"] == nums, "Sequence must be the nums array"
    assert "left" in keys0, "left must appear from start"
    assert "curr_sum" in keys0, "curr_sum must appear from start"
    assert "min_len" in keys0, "min_len must appear from start"

    # Check target is shown
    assert state0.get("sequence") is not None

    # Find a window_found frame
    found_frames = [f for f in filtered if f.get("type") == "window_found"]
    assert len(found_frames) > 0, "Must have at least one window_found frame"

    found_idx = filtered.index(found_frames[0])
    state_found = r.compute_states(filtered, found_idx)
    assert state_found["found"] is True, "found flag must be True at window_found frame"

    # Render the found state
    widget = r.make_widget(input_data)
    r.update_widget(widget, input_data, state_found)
    rendered = widget.render()
    text = rendered.plain
    assert "curr_sum" in text, "curr_sum must appear in window state"
    assert "target" in text, "target must appear in window state"
    assert "✓" in text, "Found indicator must appear at window_found"

    # Final result: min_len for [2,3,1,2,4,3] target=7 should be 2
    state_last = r.compute_states(filtered, len(filtered) - 1)
    entries_last = r.variable_entries(filtered[-1])
    min_len_entry = [v for k, v, c in entries_last if k == "min_len"]
    assert min_len_entry, "min_len must appear in last step variables"
    assert min_len_entry[0] == "2", f"Expected min_len=2, got {min_len_entry[0]}"

    print("ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_min_subarray_sum_flow()
