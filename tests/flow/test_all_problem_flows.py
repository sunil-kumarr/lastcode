from __future__ import annotations

import importlib

import pytest

from lastcode.app import _load_renderer
from lastcode.problems.registry import PROBLEMS, PROBLEM_MAP


ALL_PROBLEM_IDS = [p["id"] for p in PROBLEMS if p.get("available")]


@pytest.mark.parametrize("problem_id", ALL_PROBLEM_IDS)
def test_problem_flow_renders(problem_id: str) -> None:
    problem_meta = next(p for p in PROBLEMS if p["id"] == problem_id)
    module = importlib.import_module(PROBLEM_MAP[problem_id])

    input_data = getattr(module, "DEFAULT_INPUT", getattr(module, "DEFAULT_GRID", None))
    assert input_data is not None, f"{problem_id} is missing default input"

    frames = module.run(input_data)
    assert frames, f"{problem_id} returned no frames"

    renderer = _load_renderer(problem_meta["renderer"])
    filtered = renderer.filter_frames(frames)
    assert filtered, f"{problem_id} has no user-facing frames after filtering"

    state = renderer.compute_states(filtered, len(filtered) - 1)
    widget = renderer.make_widget(input_data)
    renderer.update_widget(widget, input_data, state)
    rendered = widget.render()

    assert getattr(rendered, "plain", str(rendered)).strip(), f"{problem_id} rendered empty output"
