"""Flow regression test — Longest Substring Without Repeating Characters."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from neonodes.problems import longest_substring_no_repeat
from neonodes.renderers.sliding_window import SlidingWindowRenderer


def test_longest_substr_flow():
    print("Testing Longest Substring No Repeat flow...")
    input_data = "abcabcbb"

    frames = longest_substring_no_repeat.run(input_data)
    r = SlidingWindowRenderer()
    filtered = r.filter_frames(frames)

    print(f"Total frames: {len(frames)}, Filtered: {len(filtered)}")
    assert len(filtered) > 0, "Filtered frames should not be empty"

    # Step 0 — function signature / initialisation
    state0 = r.compute_states(filtered, 0)
    entries0 = r.variable_entries(filtered[0])
    keys0 = [k for k, v, c in entries0]

    print("Step 0 — checking initial state...")
    assert state0["sequence"] == list(input_data) or state0["sequence"] == input_data, \
        "Sequence should be the input string"
    assert "left" in keys0, "left must appear in variables panel from the start"
    assert "max_len" in keys0, "max_len must appear in variables panel from the start"

    # A middle step — window should be active
    mid = len(filtered) // 2
    state_mid = r.compute_states(filtered, mid)
    assert state_mid["pointers"].get("left") is not None, "left pointer must be present"
    assert state_mid["pointers"].get("right") is not None, "right pointer must be present"

    # Render must not crash and must have content
    widget = r.make_widget(input_data)
    r.update_widget(widget, input_data, state_mid)
    rendered = widget.render()
    text = rendered.plain
    assert len(text) > 0, "Rendered output must not be empty"
    # Window bracket must appear somewhere in the output
    assert "L" in text and "R" in text, "Bracket labels L and R must appear"

    # Last step — max_len should be 3 for "abcabcbb"
    state_last = r.compute_states(filtered, len(filtered) - 1)
    entries_last = r.variable_entries(filtered[-1])
    max_len_entry = [v for k, v, c in entries_last if k == "max_len"]
    assert max_len_entry, "max_len should be present in last step variables"
    assert max_len_entry[0] == "3", f"Expected max_len=3, got {max_len_entry[0]}"

    print("ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_longest_substr_flow()
