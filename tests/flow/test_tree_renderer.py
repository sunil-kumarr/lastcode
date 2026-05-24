from __future__ import annotations

import importlib

from lastcode.app import _load_renderer


def _tree_render(problem_id: str):
    module = importlib.import_module(f"lastcode.problems.tree.{problem_id}")
    input_data = getattr(module, "DEFAULT_INPUT")
    frames = module.run(input_data)
    renderer = _load_renderer("tree")
    filtered = renderer.filter_frames(frames)
    state = renderer.compute_states(filtered, len(filtered) - 1)
    return renderer, filtered, state


def test_tree_renderer_keeps_backtracking_frames_and_motion_trail() -> None:
    renderer, filtered, state = _tree_render("bt_max_depth")

    assert any(frame["type"] == "dfs_return" for frame in filtered)
    assert state["motion_trail"]
    assert state["current"] is None
    assert renderer.explain_frame(filtered[-1], len(filtered) - 1, len(filtered)).endswith("maximum depth = 4")
    assert state["call_stack_entries"]
    assert state["edge_note"]


def test_tree_renderer_uses_short_prompt_labels_for_path_sum() -> None:
    renderer, filtered, _ = _tree_render("path_sum_ii")

    node_step = next(frame for frame in filtered if frame["type"] == "node_visit")
    labels = [name for name, _, _ in renderer.variable_entries(node_step)]

    assert labels[:5] == ["n", "lvl", "sum", "target", "path"]


def test_tree_renderer_shows_final_answers_for_traversals() -> None:
    renderer, filtered, state = _tree_render("right_side_view")
    module = importlib.import_module("lastcode.problems.tree.right_side_view")
    widget = renderer.make_widget(module.DEFAULT_INPUT)
    renderer.update_widget(widget, module.DEFAULT_INPUT, state)
    rendered = widget.render()

    assert state["final_answer"] == [1, 3, 6, 10]
    assert "Final answer" in renderer.explain_frame(filtered[-1], len(filtered) - 1, len(filtered))
    assert "step:" in getattr(rendered, "plain", str(rendered))


def test_tree_edge_labels_render_on_top_of_nodes() -> None:
    module = importlib.import_module("lastcode.problems.tree.bt_max_depth")
    frames = module.run(module.DEFAULT_INPUT)
    renderer = _load_renderer("tree")
    filtered = renderer.filter_frames(frames)

    for step in range(len(filtered)):
        state = renderer.compute_states(filtered, step)
        if not state.get("edge_note"):
            continue
        widget = renderer.make_widget(module.DEFAULT_INPUT)
        renderer.update_widget(widget, module.DEFAULT_INPUT, state)
        rendered = getattr(widget.render(), "plain", str(widget.render()))
        assert state["edge_note"] in rendered
        break
    else:
        raise AssertionError("expected at least one edge note for bt_max_depth")


def test_tree_transition_notes_cover_bfs_and_flatten_flows() -> None:
    renderer, filtered, _ = _tree_render("bt_level_order")
    state = renderer.compute_states(filtered, 3)
    assert state["transition_note"]

    renderer, filtered, _ = _tree_render("zigzag_level_order")
    state = renderer.compute_states(filtered, 3)
    assert state["transition_note"]

    renderer, filtered, _ = _tree_render("flatten_tree")
    state = renderer.compute_states(filtered, 3)
    assert state["transition_note"]


def test_tree_first_step_does_not_pre_highlight_solution_path() -> None:
    renderer, filtered, _ = _tree_render("invert_tree")
    first_state = renderer.compute_states(filtered, 0)
    assert first_state["active_path"] == []
    assert first_state["current"] is None

    renderer, filtered, _ = _tree_render("flatten_tree")
    first_state = renderer.compute_states(filtered, 0)
    assert first_state["active_path"] == []
    assert first_state["current"] is None


def test_symmetric_tree_starts_from_root() -> None:
    renderer, filtered, _ = _tree_render("symmetric_tree")
    first_visit = next(frame for frame in filtered if frame["type"] == "node_visit")
    assert first_visit["val"] == 1
    assert renderer.explain_frame(first_visit, 1, len(filtered)).startswith("  [2/")


def test_lca_bst_call_stack_shows_current_targets() -> None:
    renderer, filtered, state = _tree_render("lca_bst")
    labels = [entry["label"] for entry in state["call_stack_entries"]]

    assert any("p=" in label and "q=" in label for label in labels)
    assert any(label.startswith("node ") or label.startswith("visit ") for label in labels)
    assert state["visit_path"][:2] == [1, 2]
    assert state["edge_note"]


def test_tree_return_labels_show_returned_values() -> None:
    renderer, filtered, _ = _tree_render("bt_max_depth")
    return_step = next(frame for frame in filtered if frame["type"] == "dfs_return")
    labels = [name for name, _, _ in renderer.variable_entries(return_step)]

    assert "ans" in labels or "res" in labels


def test_tree_zoom_changes_render_width() -> None:
    renderer, filtered, _ = _tree_render("bt_max_depth")
    module = importlib.import_module("lastcode.problems.tree.bt_max_depth")

    state_small = renderer.compute_states(filtered, 6)
    state_small["zoom"] = 0.6
    widget = renderer.make_widget(module.DEFAULT_INPUT)
    renderer.update_widget(widget, module.DEFAULT_INPUT, state_small)
    small_width = max(len(line) for line in getattr(widget.render(), "plain", str(widget.render())).splitlines())

    state_large = renderer.compute_states(filtered, 6)
    state_large["zoom"] = 1.6
    widget = renderer.make_widget(module.DEFAULT_INPUT)
    renderer.update_widget(widget, module.DEFAULT_INPUT, state_large)
    large_width = max(len(line) for line in getattr(widget.render(), "plain", str(widget.render())).splitlines())

    assert large_width > small_width


def test_tree_zoom_in_action_increases_zoom() -> None:
    from lastcode.app import VisualizerScreen

    module = importlib.import_module("lastcode.problems.tree.bt_max_depth")
    screen = VisualizerScreen(module)

    start_zoom = screen._zoom
    screen._set_zoom(screen._zoom + 0.2)
    assert screen._zoom > start_zoom
