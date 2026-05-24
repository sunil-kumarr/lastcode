import importlib

import pytest

from lastcode.problems.registry import PROBLEMS, PROBLEM_MAP


DP_PROBLEM_IDS = [p["id"] for p in PROBLEMS if p.get("available") and p.get("renderer") == "dp"]


@pytest.mark.parametrize("problem_id", DP_PROBLEM_IDS)
def test_dp_problems_end_with_final_answer(problem_id: str) -> None:
    module = importlib.import_module(PROBLEM_MAP[problem_id])
    input_data = getattr(module, "DEFAULT_INPUT", getattr(module, "DEFAULT_GRID", None))

    frames = module.run(input_data)

    assert frames, f"{problem_id} returned no frames"
    assert frames[-1]["note"].startswith("Final answer:"), problem_id
