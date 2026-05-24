from lastcode.problems.dp.triangle import run


def test_triangle_frames_keep_constant_width():
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    frames = run(triangle)

    assert {frame["shape"] for frame in frames} == {"triangle"}
    widths = {len(frame["table"]) for frame in frames}
    row_widths = {tuple(len(row) for row in frame["table"]) for frame in frames}

    assert widths == {4}
    assert row_widths == {(1, 2, 3, 4)}


def test_triangle_final_value_is_minimum_total():
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    frames = run(triangle)

    assert "Final answer" in frames[-1]["note"]
    assert frames[-1]["result_value"] == 11
