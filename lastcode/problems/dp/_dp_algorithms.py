from __future__ import annotations

import copy
import inspect
from functools import wraps
import re
import textwrap


def _snippet(*lines: str) -> list[str]:
    return [line.rstrip() for line in lines]


def _append_final_answer_frame(frames: list[dict]) -> list[dict]:
    if not frames:
        return frames

    last = frames[-1]
    note = str(last.get("note", ""))
    if note.startswith("Final answer:"):
        return frames

    final_frame = copy.deepcopy(last)
    result_label = final_frame.get("result_label", "result")
    result_value = final_frame.get("result_value", "—")
    final_frame["note"] = f"Final answer: {result_label} = {result_value}"
    final_frame["display_line"] = last.get("display_line", final_frame.get("display_line", 1))
    final_frame["shape"] = last.get("shape", final_frame.get("shape"))
    final_frame["compare_cells"] = []
    final_frame["trace_cells"] = []
    final_frame["solved_cells"] = copy.deepcopy(last.get("solved_cells", []))
    final_frame["locals"] = copy.deepcopy(last.get("locals", {}))
    final_frame["state_formula"] = "Return the computed result"
    frames.append(final_frame)
    return frames


def _with_final_answer(builder):
    @wraps(builder)
    def wrapped(*args, **kwargs):
        return _append_final_answer_frame(builder(*args, **kwargs))

    return wrapped


_DP_INTERVIEW_CODE: dict[str, list[str]] = {
    "build_climbing_stairs_frames": _snippet(
        "def climbing_stairs(n):",
        "    if n <= 2:",
        "        return n",
        "",
        "    dp = [0] * (n + 1)",
        "    dp[1], dp[2] = 1, 2",
        "    for i in range(3, n + 1):",
        "        dp[i] = dp[i - 1] + dp[i - 2]",
        "    return dp[n]",
    ),
    "build_min_cost_climbing_stairs_frames": _snippet(
        "def min_cost_climbing_stairs(cost):",
        "    n = len(cost)",
        "    dp = [0] * (n + 1)",
        "    for i in range(2, n + 1):",
        "        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])",
        "    return dp[n]",
    ),
    "build_house_robber_frames": _snippet(
        "def house_robber(nums):",
        "    if not nums:",
        "        return 0",
        "    if len(nums) == 1:",
        "        return nums[0]",
        "    dp = [0] * len(nums)",
        "    dp[0] = nums[0]",
        "    dp[1] = max(nums[0], nums[1])",
        "    for i in range(2, len(nums)):",
        "        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])",
        "    return dp[-1]",
    ),
    "build_house_robber_ii_frames": _snippet(
        "def house_robber_ii(nums):",
        "    if len(nums) == 1:",
        "        return nums[0]",
        "",
        "    def rob_linear(arr):",
        "        prev2 = prev1 = 0",
        "        for value in arr:",
        "            prev2, prev1 = prev1, max(prev1, prev2 + value)",
        "        return prev1",
        "",
        "    best_excl_last = rob_linear(nums[:-1])",
        "    best_excl_first = rob_linear(nums[1:])",
        "    return max(best_excl_last, best_excl_first)",
    ),
    "build_coin_change_frames": _snippet(
        "def coin_change(coins, amount):",
        "    dp = [amount + 1] * (amount + 1)",
        "    dp[0] = 0",
        "    for coin in coins:",
        "        for current in range(coin, amount + 1):",
        "            dp[current] = min(dp[current], dp[current - coin] + 1)",
        "    return dp[amount] if dp[amount] != amount + 1 else -1",
    ),
    "build_coin_change_ii_frames": _snippet(
        "def coin_change_ii(amount, coins):",
        "    dp = [0] * (amount + 1)",
        "    dp[0] = 1",
        "    for coin in coins:",
        "        for current in range(coin, amount + 1):",
        "            dp[current] += dp[current - coin]",
        "    return dp[amount]",
    ),
    "build_lis_frames": _snippet(
        "def length_of_lis(nums):",
        "    if not nums:",
        "        return 0",
        "    dp = [1] * len(nums)",
        "    best = 1",
        "    for current in range(len(nums)):",
        "        for candidate in range(current):",
        "            if nums[candidate] < nums[current] and dp[candidate] + 1 > dp[current]:",
        "                dp[current] = dp[candidate] + 1",
        "                best = max(best, dp[current])",
        "    return best",
    ),
    "build_partition_equal_subset_sum_frames": _snippet(
        "def can_partition(nums):",
        "    total = sum(nums)",
        "    if total % 2:",
        "        return False",
        "    target = total // 2",
        "    dp = [False] * (target + 1)",
        "    dp[0] = True",
        "    for num in nums:",
        "        for current in range(target, num - 1, -1):",
        "            if dp[current - num]:",
        "                dp[current] = True",
        "    return dp[target]",
    ),
    "build_target_sum_frames": _snippet(
        "def find_target_sum_ways(nums, target):",
        "    offset = sum(nums)",
        "    width = 2 * offset + 1",
        "    dp = [0] * width",
        "    dp[offset] = 1",
        "    for num in nums:",
        "        nxt = [0] * width",
        "        for current in range(width):",
        "            if dp[current]:",
        "                nxt[current + num] += dp[current]",
        "                nxt[current - num] += dp[current]",
        "        dp = nxt",
        "    return dp[offset + target] if 0 <= offset + target < width else 0",
    ),
    "build_word_break_frames": _snippet(
        "def word_break(source, dictionary):",
        "    word_set = set(dictionary)",
        "    dp = [False] * (len(source) + 1)",
        "    dp[0] = True",
        "    for end in range(1, len(source) + 1):",
        "        for start in range(end):",
        "            if dp[start] and source[start:end] in word_set:",
        "                dp[end] = True",
        "                break",
        "    return dp[-1]",
    ),
    "build_decode_ways_frames": _snippet(
        "def num_decodings(s):",
        "    if not s or s[0] == '0':",
        "        return 0",
        "    dp = [0] * (len(s) + 1)",
        "    dp[0] = dp[1] = 1",
        "    for i in range(2, len(s) + 1):",
        "        if s[i - 1] != '0':",
        "            dp[i] += dp[i - 1]",
        "        if 10 <= int(s[i - 2:i]) <= 26:",
        "            dp[i] += dp[i - 2]",
        "    return dp[-1]",
    ),
    "build_unique_paths_frames": _snippet(
        "def unique_paths(m, n):",
        "    dp = [[1] * n for _ in range(m)]",
        "    for row in range(1, m):",
        "        for col in range(1, n):",
        "            dp[row][col] = dp[row - 1][col] + dp[row][col - 1]",
        "    return dp[-1][-1]",
    ),
    "build_min_path_sum_frames": _snippet(
        "def min_path_sum(grid):",
        "    rows, cols = len(grid), len(grid[0])",
        "    dp = [[0] * cols for _ in range(rows)]",
        "    for row in range(rows):",
        "        for col in range(cols):",
        "            if row == 0 and col == 0:",
        "                dp[row][col] = grid[row][col]",
        "            elif row == 0:",
        "                dp[row][col] = dp[row][col - 1] + grid[row][col]",
        "            elif col == 0:",
        "                dp[row][col] = dp[row - 1][col] + grid[row][col]",
        "            else:",
        "                dp[row][col] = min(dp[row - 1][col], dp[row][col - 1]) + grid[row][col]",
        "    return dp[-1][-1]",
    ),
    "build_triangle_frames": _snippet(
        "def minimum_total(triangle):",
        "    dp = triangle[-1][:]",
        "    for row in range(len(triangle) - 2, -1, -1):",
        "        for col in range(len(triangle[row])):",
        "            dp[col] = triangle[row][col] + min(dp[col], dp[col + 1])",
        "    return min(dp)",
    ),
    "build_edit_distance_frames": _snippet(
        "def edit_distance(word1, word2):",
        "    rows, cols = len(word2) + 1, len(word1) + 1",
        "    dp = [[0] * cols for _ in range(rows)]",
        "    for row in range(rows):",
        "        dp[row][0] = row",
        "    for col in range(cols):",
        "        dp[0][col] = col",
        "    for row in range(1, rows):",
        "        for col in range(1, cols):",
        "            if word2[row - 1] == word1[col - 1]:",
        "                dp[row][col] = dp[row - 1][col - 1]",
        "            else:",
        "                dp[row][col] = 1 + min(dp[row - 1][col], dp[row][col - 1], dp[row - 1][col - 1])",
        "    return dp[-1][-1]",
    ),
    "build_interleaving_string_frames": _snippet(
        "def is_interleave(first, second, third):",
        "    if len(first) + len(second) != len(third):",
        "        return False",
        "    dp = [[False] * (len(first) + 1) for _ in range(len(second) + 1)]",
        "    dp[0][0] = True",
        "    for row in range(len(second) + 1):",
        "        for col in range(len(first) + 1):",
        "            if row == 0 and col == 0:",
        "                continue",
        "            idx = row + col - 1",
        "            if col > 0 and first[col - 1] == third[idx]:",
        "                dp[row][col] |= dp[row][col - 1]",
        "            if row > 0 and second[row - 1] == third[idx]:",
        "                dp[row][col] |= dp[row - 1][col]",
        "    return dp[-1][-1]",
    ),
    "build_distinct_subsequences_frames": _snippet(
        "def num_distinct(s, t):",
        "    dp = [[0] * (len(s) + 1) for _ in range(len(t) + 1)]",
        "    for col in range(len(s) + 1):",
        "        dp[0][col] = 1",
        "    for row in range(1, len(t) + 1):",
        "        for col in range(1, len(s) + 1):",
        "            dp[row][col] = dp[row][col - 1]",
        "            if t[row - 1] == s[col - 1]:",
        "                dp[row][col] += dp[row - 1][col - 1]",
        "    return dp[-1][-1]",
    ),
    "build_lps_frames": _snippet(
        "def longest_palindromic_subsequence(s):",
        "    n = len(s)",
        "    dp = [[0] * n for _ in range(n)]",
        "    for i in range(n):",
        "        dp[i][i] = 1",
        "    for length in range(2, n + 1):",
        "        for i in range(n - length + 1):",
        "            j = i + length - 1",
        "            if s[i] == s[j]:",
        "                dp[i][j] = 2 + (dp[i + 1][j - 1] if length > 2 else 0)",
        "            else:",
        "                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])",
        "    return dp[0][-1] if s else 0",
    ),
    "build_palindromic_substrings_frames": _snippet(
        "def count_palindromic_substrings(s):",
        "    n = len(s)",
        "    dp = [[False] * n for _ in range(n)]",
        "    count = 0",
        "    for length in range(1, n + 1):",
        "        for i in range(n - length + 1):",
        "            j = i + length - 1",
        "            if s[i] == s[j] and (length <= 2 or dp[i + 1][j - 1]):",
        "                dp[i][j] = True",
        "                count += 1",
        "    return count",
    ),
    "build_lcs_frames": _snippet(
        "def longest_common_subsequence(first, second):",
        "    rows, cols = len(second) + 1, len(first) + 1",
        "    dp = [[0] * cols for _ in range(rows)]",
        "    for row in range(1, rows):",
        "        for col in range(1, cols):",
        "            if second[row - 1] == first[col - 1]:",
        "                dp[row][col] = dp[row - 1][col - 1] + 1",
        "            else:",
        "                dp[row][col] = max(dp[row - 1][col], dp[row][col - 1])",
        "    return dp[-1][-1]",
    ),
}


def code_lines_for(func) -> list[str]:
    target = inspect.unwrap(func)
    interview_lines = _DP_INTERVIEW_CODE.get(target.__name__)
    if interview_lines is not None:
        return interview_lines

    source = textwrap.dedent(inspect.getsource(target)).splitlines()
    signature = inspect.signature(target)
    clean_name = target.__name__.removeprefix("build_").removesuffix("_frames")
    params = ", ".join(signature.parameters.keys())
    lines: list[str] = []
    for line in source:
        stripped = line.strip()
        if (
            stripped.startswith("frames = []")
            or stripped == "return frames"
            or stripped.startswith("_emit(")
            or stripped.startswith("#")
        ):
            continue
        if stripped.startswith("def "):
            line = f"def {clean_name}({params}):"
        line = _prettify_code_line(line)
        lines.append(line)
    return [line.rstrip() for line in lines if line.strip()]


def _emit(
    frames: list[dict],
    *,
    table,
    note: str,
    display_line: int,
    active_cells: list[tuple[int, int]] | None = None,
    compare_cells: list[tuple[int, int]] | None = None,
    solved_cells: list[tuple[int, int]] | None = None,
    trace_cells: list[tuple[int, int]] | None = None,
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
    result_label: str = "result",
    result_value=None,
    locals: dict | None = None,
    state_formula: str | None = None,
    column_pointers: list[dict] | None = None,
    row_pointers: list[dict] | None = None,
    variable_labels: dict[str, str] | None = None,
    shape: str | None = None,
) -> None:
    safe_locals = copy.deepcopy(locals or {})
    pretty_labels = _variable_label_map()
    merged_labels = {**pretty_labels, **(variable_labels or {})}
    inferred_column_pointers, inferred_row_pointers = _infer_pointers(
        safe_locals,
        active_cells or [],
        compare_cells or [],
        merged_labels,
    )
    frames.append(
        {
            "type": "dp_step",
            "table": copy.deepcopy(table),
            "note": note,
            "display_line": 1 if not frames else display_line,
            "active_cells": active_cells or [],
            "compare_cells": compare_cells or [],
            "solved_cells": solved_cells or [],
            "trace_cells": trace_cells or [],
            "row_labels": row_labels,
            "col_labels": col_labels,
            "result_label": result_label,
            "result_value": result_value,
            "locals": safe_locals,
            "state_formula": state_formula,
            "column_pointers": copy.deepcopy(column_pointers or inferred_column_pointers),
            "row_pointers": copy.deepcopy(row_pointers or inferred_row_pointers),
            "variable_labels": copy.deepcopy(merged_labels),
            "shape": shape,
        }
    )


def _range_labels(size: int, prefix: str = "") -> list[str]:
    return [f"{prefix}{i}" for i in range(size)]


def _blue(name: str, col: int) -> dict:
    return {"name": name, "col": col, "color": "#7AA2F7"}


def _pink(name: str, col: int) -> dict:
    return {"name": name, "col": col, "color": "#F7768E"}


def _yellow(name: str, col: int) -> dict:
    return {"name": name, "col": col, "color": "#E0AF68"}


def _row_pointer(name: str, row: int) -> dict:
    return {"name": name, "row": row, "color": "#7AA2F7"}


def _variable_label_map() -> dict[str, str]:
    return {
        "n": "step_count",
        "m": "row_count",
        "rows": "row_count",
        "cols": "col_count",
        "i": "current_index",
        "j": "candidate_index",
        "r": "row_index",
        "c": "col_index",
        "s": "source_string",
        "t": "target_string",
        "s1": "first_string",
        "s2": "second_string",
        "s3": "third_string",
        "nums": "number_values",
        "cost": "cost_values",
        "coins": "coin_values",
        "amount": "target_amount",
        "target": "target_total",
        "word1": "source_word",
        "word2": "target_word",
        "dp": "dp_state",
        "total": "current_amount",
        "coin": "coin_value",
        "num": "current_value",
        "length": "window_length",
        "idx": "current_index",
    }


def _prettify_code_line(line: str) -> str:
    replacements = _variable_label_map()
    for old, new in sorted(replacements.items(), key=lambda item: -len(item[0])):
        line = re.sub(rf"\b{re.escape(old)}\b", new, line)
    line = line.replace("input_data", "problem_input")
    return line


def _infer_pointers(
    locals_val: dict,
    active_cells: list[tuple[int, int]],
    compare_cells: list[tuple[int, int]],
    labels: dict[str, str],
) -> tuple[list[dict], list[dict]]:
    column_pointers: list[dict] = []
    row_pointers: list[dict] = []

    if active_cells:
        active_row, active_col = active_cells[0]
        for key in ("col_index", "amount_index", "target_sum_index", "source_index", "target_index", "house_index", "stair_index", "current_index", "c", "i", "idx"):
            if key in locals_val:
                column_pointers.append(_pink(labels.get(key, key), active_col))
                break
        for key in ("row_index", "r"):
            if key in locals_val:
                row_pointers.append(_row_pointer(labels.get(key, key), active_row))
                break

    if compare_cells:
        candidate_row, candidate_col = compare_cells[0]
        for key in ("candidate_col_index", "candidate_amount_index", "candidate_index", "left_index", "j"):
            if key in locals_val:
                column_pointers.append(_blue(labels.get(key, key), candidate_col))
                break
        else:
            column_pointers.append(_blue("candidate", candidate_col))
        for key in ("candidate_row_index", "row_index", "r"):
            if key in locals_val and all(pointer["row"] != candidate_row for pointer in row_pointers):
                row_pointers.append(_row_pointer(labels.get(key, key), candidate_row))
                break

    return column_pointers, row_pointers


def build_climbing_stairs_frames(n: int) -> list[dict]:
    frames = []
    if n <= 2:
        _emit(frames, table=[1, 2][:max(n, 1)], note="Base case already gives the answer", display_line=2, solved_cells=[(0, max(n - 1, 0))], col_labels=_range_labels(max(n, 1)), result_label="ways", result_value=n, locals={"n": n})
        return frames
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    _emit(frames, table=dp[1:], note="Seed the first two stair counts", display_line=5, solved_cells=[(0, 0), (0, 1)], col_labels=_range_labels(n), result_label="ways", result_value=2, locals={"n": n})
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        _emit(frames, table=dp[1:], note=f"Ways to reach stair {i} = previous two stairs", display_line=8, active_cells=[(0, i - 1)], compare_cells=[(0, i - 2), (0, i - 3)], solved_cells=[(0, i - 1)], col_labels=_range_labels(n), result_label="ways", result_value=dp[i], locals={"n": n, "i": i})
    return frames


def build_min_cost_climbing_stairs_frames(cost: list[int]) -> list[dict]:
    frames = []
    n = len(cost)
    dp = [0] * (n + 1)
    _emit(frames, table=dp, note="Start with zero cost before the staircase", display_line=3, solved_cells=[(0, 0)], col_labels=_range_labels(n + 1), result_label="min_cost", result_value=0, locals={"n": n})
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
        _emit(frames, table=dp, note=f"Choose the cheaper jump into step {i}", display_line=5, active_cells=[(0, i)], compare_cells=[(0, i - 1), (0, i - 2)], solved_cells=[(0, i)], col_labels=_range_labels(n + 1), result_label="min_cost", result_value=dp[i], locals={"n": n, "i": i})
    return frames


def build_house_robber_frames(nums: list[int]) -> list[dict]:
    frames = []
    if not nums:
        return frames
    dp = [0] * len(nums)
    dp[0] = nums[0]
    _emit(frames, table=dp, note="First house defines the starting best loot", display_line=7, solved_cells=[(0, 0)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=dp[0], locals={"i": 0})
    if len(nums) == 1:
        return frames
    dp[1] = max(nums[0], nums[1])
    _emit(frames, table=dp, note="Choose the better of the first two houses", display_line=8, active_cells=[(0, 1)], compare_cells=[(0, 0)], solved_cells=[(0, 1)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=dp[1], locals={"i": 1})
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        _emit(frames, table=dp, note=f"Skip or rob house {i}", display_line=10, active_cells=[(0, i)], compare_cells=[(0, i - 1), (0, i - 2)], solved_cells=[(0, i)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=dp[i], locals={"i": i})
    return frames


def build_house_robber_ii_frames(nums: list[int]) -> list[dict]:
    def rob_linear(arr: list[int], offset: int, frames: list[dict], line_no: int) -> int:
        prev2 = 0
        prev1 = 0
        table = [0] * len(nums)
        for idx, value in enumerate(arr):
            best = max(prev1, prev2 + value)
            prev2, prev1 = prev1, best
            table[offset + idx] = best
            _emit(frames, table=table, note=f"Best circular loot considering house {offset + idx}", display_line=line_no, active_cells=[(0, offset + idx)], compare_cells=[(0, max(offset + idx - 1, 0))], solved_cells=[(0, offset + idx)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=best, locals={"i": offset + idx})
        return prev1

    frames = []
    if len(nums) == 1:
        _emit(frames, table=nums, note="Only one house exists in the circle", display_line=2, solved_cells=[(0, 0)], col_labels=_range_labels(1), result_label="loot", result_value=nums[0], locals={"i": 0})
        return frames
    best_excl_last = rob_linear(nums[:-1], 0, frames, 7)
    best_excl_first = rob_linear(nums[1:], 1, frames, 7)
    _emit(frames, table=[best_excl_last, best_excl_first], note="Take the better of the two linear passes", display_line=13, active_cells=[(0, 0), (0, 1)], solved_cells=[(0, 0), (0, 1)], col_labels=["skip last", "skip first"], result_label="loot", result_value=max(best_excl_last, best_excl_first), locals={})
    return frames


def build_coin_change_frames(input_data: tuple[list[int], int]) -> list[dict]:
    coin_values, target_amount = input_data
    frames = []
    dp_state = [target_amount + 1] * (target_amount + 1)
    dp_state[0] = 0
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: every amount starts unreachable except amount 0",
        display_line=4,
        solved_cells=[(0, 0)],
        col_labels=_range_labels(target_amount + 1),
        result_label="min_coins",
        result_value=0,
        locals={"target_amount": target_amount, "coin_values": coin_values},
        state_formula="dp_state[amount] = target_amount + 1, and dp_state[0] = 0",
    )
    for coin_index, coin_value in enumerate(coin_values):
        for amount_index in range(coin_value, target_amount + 1):
            candidate_amount_index = amount_index - coin_value
            candidate_coin_count = dp_state[candidate_amount_index] + 1
            current_coin_count = dp_state[amount_index]
            if candidate_coin_count < current_coin_count:
                dp_state[amount_index] = candidate_coin_count
                _emit(
                    frames,
                    table=dp_state,
                    note=f"Use coin {coin_value} to improve amount {amount_index}",
                    display_line=6,
                    active_cells=[(0, amount_index)],
                    compare_cells=[(0, candidate_amount_index)],
                    solved_cells=[(0, amount_index)],
                    col_labels=_range_labels(target_amount + 1),
                    result_label="min_coins",
                    result_value=dp_state[amount_index],
                    locals={
                        "target_amount": target_amount,
                        "coin_values": coin_values,
                        "coin_index": coin_index,
                        "coin_value": coin_value,
                        "amount_index": amount_index,
                        "candidate_amount_index": candidate_amount_index,
                    },
                    state_formula=f"dp_state[{amount_index}] = min({current_coin_count}, dp_state[{candidate_amount_index}] + 1 = {candidate_coin_count})",
                    column_pointers=[
                        _pink("amount_index", amount_index),
                        _blue("candidate_amount_index", candidate_amount_index),
                    ],
                )
    return frames


def build_coin_change_ii_frames(input_data: tuple[int, list[int]]) -> list[dict]:
    target_amount, coin_values = input_data
    frames = []
    dp_state = [0] * (target_amount + 1)
    dp_state[0] = 1
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: there is exactly one way to make amount 0",
        display_line=4,
        solved_cells=[(0, 0)],
        col_labels=_range_labels(target_amount + 1),
        result_label="ways",
        result_value=1,
        locals={"target_amount": target_amount, "coin_values": coin_values},
        state_formula="dp_state[0] = 1 and every other amount starts at 0 ways",
    )
    for coin_index, coin_value in enumerate(coin_values):
        for amount_index in range(coin_value, target_amount + 1):
            candidate_amount_index = amount_index - coin_value
            previous_way_count = dp_state[amount_index]
            dp_state[amount_index] += dp_state[candidate_amount_index]
            _emit(
                frames,
                table=dp_state,
                note=f"Add combinations that end with coin {coin_value}",
                display_line=6,
                active_cells=[(0, amount_index)],
                compare_cells=[(0, candidate_amount_index)],
                solved_cells=[(0, amount_index)],
                col_labels=_range_labels(target_amount + 1),
                result_label="ways",
                result_value=dp_state[amount_index],
                locals={
                    "target_amount": target_amount,
                    "coin_values": coin_values,
                    "coin_index": coin_index,
                    "coin_value": coin_value,
                    "amount_index": amount_index,
                    "candidate_amount_index": candidate_amount_index,
                },
                state_formula=f"dp_state[{amount_index}] = {previous_way_count} + dp_state[{candidate_amount_index}] = {dp_state[amount_index]}",
                column_pointers=[
                    _pink("amount_index", amount_index),
                    _blue("candidate_amount_index", candidate_amount_index),
                ],
            )
    return frames


def build_lis_frames(nums: list[int]) -> list[dict]:
    frames = []
    if not nums:
        return frames
    number_values = nums
    dp_state = [1] * len(number_values)
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: every value starts with LIS length 1",
        display_line=2,
        solved_cells=[(0, idx) for idx in range(len(number_values))],
        col_labels=_range_labels(len(number_values)),
        result_label="lis",
        result_value=1,
        locals={"number_values": number_values},
        state_formula="dp_state[index] = 1 before checking smaller previous values",
    )
    best_length = 1
    for current_index in range(len(number_values)):
        for candidate_index in range(current_index):
            if number_values[candidate_index] < number_values[current_index] and dp_state[candidate_index] + 1 > dp_state[current_index]:
                dp_state[current_index] = dp_state[candidate_index] + 1
                best_length = max(best_length, dp_state[current_index])
                _emit(
                    frames,
                    table=dp_state,
                    note=f"Extend the subsequence at index {candidate_index} into index {current_index}",
                    display_line=9,
                    active_cells=[(0, current_index)],
                    compare_cells=[(0, candidate_index)],
                    solved_cells=[(0, current_index)],
                    col_labels=_range_labels(len(number_values)),
                    result_label="lis",
                    result_value=best_length,
                    locals={
                        "number_values": number_values,
                        "current_index": current_index,
                        "candidate_index": candidate_index,
                    },
                    state_formula=f"dp_state[{current_index}] = dp_state[{candidate_index}] + 1 = {dp_state[current_index]}",
                    column_pointers=[
                        _pink("current_index", current_index),
                        _blue("candidate_index", candidate_index),
                    ],
                )
    return frames


def build_partition_equal_subset_sum_frames(nums: list[int]) -> list[dict]:
    total = sum(nums)
    frames = []
    if total % 2:
        _emit(frames, table=[total], note="Odd total means equal partition is impossible", display_line=3, solved_cells=[(0, 0)], col_labels=["sum"], result_label="possible", result_value=False, locals={})
        return frames
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    _emit(frames, table=dp, note="Subset sum 0 is always achievable", display_line=7, solved_cells=[(0, 0)], col_labels=_range_labels(target + 1), result_label="possible", result_value=True, locals={"target": target})
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
                _emit(frames, table=dp, note=f"Use value {num} to reach subset sum {s}", display_line=11, active_cells=[(0, s)], compare_cells=[(0, s - num)], solved_cells=[(0, s)], col_labels=_range_labels(target + 1), result_label="possible", result_value=dp[target], locals={"i": s, "target": target})
    return frames


def build_target_sum_frames(input_data: tuple[list[int], int]) -> list[dict]:
    nums, target = input_data
    offset = sum(nums)
    width = 2 * offset + 1
    dp = [0] * width
    dp[offset] = 1
    frames = []
    _emit(frames, table=dp, note="Offset zero sum into the center of the table", display_line=5, solved_cells=[(0, offset)], col_labels=_range_labels(width), result_label="ways", result_value=1, locals={"target": target})
    for idx, num in enumerate(nums):
        nxt = [0] * width
        for s in range(width):
            if dp[s]:
                nxt[s + num] += dp[s]
                nxt[s - num] += dp[s]
        dp = nxt
        _emit(frames, table=dp, note=f"After number {num}, distribute ways to plus/minus sums", display_line=12, active_cells=[(0, offset + target)] if 0 <= offset + target < width else [], solved_cells=[(0, pos) for pos, value in enumerate(dp) if value], col_labels=_range_labels(width), result_label="ways", result_value=dp[offset + target] if 0 <= offset + target < width else 0, locals={"i": idx, "target": target})
    return frames


def build_word_break_frames(input_data: tuple[str, list[str]]) -> list[dict]:
    source_string, dictionary_words = input_data
    word_set = set(dictionary_words)
    dp_state = [False] * (len(source_string) + 1)
    dp_state[0] = True
    frames = []
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: the empty prefix is always segmentable",
        display_line=4,
        solved_cells=[(0, 0)],
        col_labels=_range_labels(len(source_string) + 1),
        result_label="segmentable",
        result_value=True,
        locals={"source_string": source_string, "dictionary_words": dictionary_words},
        state_formula="dp_state[end_index] is True when some earlier split and current word both work",
    )
    for target_index in range(1, len(source_string) + 1):
        for candidate_index in range(target_index):
            if dp_state[candidate_index] and source_string[candidate_index:target_index] in word_set:
                dp_state[target_index] = True
                word_piece = source_string[candidate_index:target_index]
                _emit(
                    frames,
                    table=dp_state,
                    note=f'Split "{source_string[:target_index]}" at {candidate_index} using "{word_piece}"',
                    display_line=7,
                    active_cells=[(0, target_index)],
                    compare_cells=[(0, candidate_index)],
                    solved_cells=[(0, target_index)],
                    col_labels=_range_labels(len(source_string) + 1),
                    result_label="segmentable",
                    result_value=dp_state[target_index],
                    locals={
                        "source_string": source_string,
                        "dictionary_words": dictionary_words,
                        "target_index": target_index,
                        "candidate_index": candidate_index,
                    },
                    state_formula=f"dp_state[{target_index}] = dp_state[{candidate_index}] and '{word_piece}' in dictionary",
                    column_pointers=[
                        _pink("target_index", target_index),
                        _blue("candidate_index", candidate_index),
                    ],
                )
                break
    return frames


def build_decode_ways_frames(s: str) -> list[dict]:
    frames = []
    source_string = s
    if not source_string or source_string[0] == "0":
        _emit(frames, table=[0], note="A leading zero cannot be decoded", display_line=2, solved_cells=[(0, 0)], col_labels=["0"], result_label="ways", result_value=0, locals={"source_string": source_string}, state_formula="A valid decoding cannot start with 0")
        return frames
    dp_state = [0] * (len(source_string) + 1)
    dp_state[0] = dp_state[1] = 1
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: empty and first valid digit both have one decoding",
        display_line=4,
        solved_cells=[(0, 0), (0, 1)],
        col_labels=_range_labels(len(source_string) + 1),
        result_label="ways",
        result_value=1,
        locals={"source_string": source_string},
        state_formula="dp_state[index] collects one-digit and two-digit decode counts",
    )
    for target_index in range(2, len(source_string) + 1):
        build_parts: list[str] = []
        if source_string[target_index - 1] != "0":
            dp_state[target_index] += dp_state[target_index - 1]
            build_parts.append(f"dp_state[{target_index - 1}]")
        if 10 <= int(source_string[target_index - 2:target_index]) <= 26:
            dp_state[target_index] += dp_state[target_index - 2]
            build_parts.append(f"dp_state[{target_index - 2}]")
        _emit(
            frames,
            table=dp_state,
            note=f"Count one-digit and two-digit decodes ending at position {target_index}",
            display_line=8,
            active_cells=[(0, target_index)],
            compare_cells=[(0, target_index - 1), (0, target_index - 2)],
            solved_cells=[(0, target_index)],
            col_labels=_range_labels(len(source_string) + 1),
            result_label="ways",
            result_value=dp_state[target_index],
            locals={"source_string": source_string, "target_index": target_index, "candidate_index": target_index - 1},
            state_formula=f"dp_state[{target_index}] = {' + '.join(build_parts) if build_parts else '0'} = {dp_state[target_index]}",
            column_pointers=[
                _pink("target_index", target_index),
                _blue("candidate_index", target_index - 1),
                _yellow("two_digit_start", target_index - 2),
            ],
        )
    return frames


def build_unique_paths_frames(input_data: tuple[int, int]) -> list[dict]:
    row_count, col_count = input_data
    dp_state = [[1] * col_count for _ in range(row_count)]
    frames = []
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: first row and first column each have one path",
        display_line=3,
        solved_cells=[(row_index, col_index) for row_index in range(row_count) for col_index in range(col_count) if row_index == 0 or col_index == 0],
        row_labels=_range_labels(row_count, "r"),
        col_labels=_range_labels(col_count, "c"),
        result_label="paths",
        result_value=1,
        locals={"row_count": row_count, "col_count": col_count},
        state_formula="dp_state[row][col] = paths from top + paths from left",
    )
    for row_index in range(1, row_count):
        for col_index in range(1, col_count):
            dp_state[row_index][col_index] = dp_state[row_index - 1][col_index] + dp_state[row_index][col_index - 1]
            _emit(
                frames,
                table=dp_state,
                note=f"Paths to ({row_index},{col_index}) come from top plus left",
                display_line=5,
                active_cells=[(row_index, col_index)],
                compare_cells=[(row_index - 1, col_index), (row_index, col_index - 1)],
                solved_cells=[(row_index, col_index)],
                row_labels=_range_labels(row_count, "r"),
                col_labels=_range_labels(col_count, "c"),
                result_label="paths",
                result_value=dp_state[row_index][col_index],
                locals={"row_index": row_index, "col_index": col_index, "row_count": row_count, "col_count": col_count, "candidate_row_index": row_index - 1, "candidate_col_index": col_index - 1},
                state_formula=f"dp_state[{row_index}][{col_index}] = dp_state[{row_index - 1}][{col_index}] + dp_state[{row_index}][{col_index - 1}] = {dp_state[row_index][col_index]}",
            )
    return frames


def build_min_path_sum_frames(grid: list[list[int]]) -> list[dict]:
    row_count, col_count = len(grid), len(grid[0])
    dp_state = [[0] * col_count for _ in range(row_count)]
    frames = []
    for row_index in range(row_count):
        for col_index in range(col_count):
            if row_index == 0 and col_index == 0:
                dp_state[row_index][col_index] = grid[row_index][col_index]
                state_formula = f"dp_state[0][0] = grid[0][0] = {dp_state[row_index][col_index]}"
            elif row_index == 0:
                dp_state[row_index][col_index] = dp_state[row_index][col_index - 1] + grid[row_index][col_index]
                state_formula = f"dp_state[{row_index}][{col_index}] = dp_state[{row_index}][{col_index - 1}] + grid[{row_index}][{col_index}] = {dp_state[row_index][col_index]}"
            elif col_index == 0:
                dp_state[row_index][col_index] = dp_state[row_index - 1][col_index] + grid[row_index][col_index]
                state_formula = f"dp_state[{row_index}][{col_index}] = dp_state[{row_index - 1}][{col_index}] + grid[{row_index}][{col_index}] = {dp_state[row_index][col_index]}"
            else:
                dp_state[row_index][col_index] = min(dp_state[row_index - 1][col_index], dp_state[row_index][col_index - 1]) + grid[row_index][col_index]
                state_formula = f"dp_state[{row_index}][{col_index}] = min(top, left) + grid[{row_index}][{col_index}] = {dp_state[row_index][col_index]}"
            compare = []
            if row_index > 0:
                compare.append((row_index - 1, col_index))
            if col_index > 0:
                compare.append((row_index, col_index - 1))
            _emit(
                frames,
                table=dp_state,
                note=f"Create the cheapest path cost into cell ({row_index},{col_index})",
                display_line=7,
                active_cells=[(row_index, col_index)],
                compare_cells=compare,
                solved_cells=[(row_index, col_index)],
                row_labels=_range_labels(row_count, "r"),
                col_labels=_range_labels(col_count, "c"),
                result_label="min_sum",
                result_value=dp_state[row_index][col_index],
                locals={"row_index": row_index, "col_index": col_index, "row_count": row_count, "col_count": col_count},
                state_formula=state_formula,
            )
    return frames


def build_triangle_frames(triangle: list[list[int]]) -> list[dict]:
    dp = triangle[-1][:]
    working = [row[:] for row in triangle]
    width = len(dp)
    frames = []
    _emit(
        frames,
        table=working,
        note="Start from the bottom row of the triangle",
        display_line=2,
        solved_cells=[(0, idx) for idx in range(len(dp))],
        shape="triangle",
        result_label="min_total",
        result_value=min(dp),
        locals={"row_count": len(triangle), "col_count": width},
    )
    for r in range(len(triangle) - 2, -1, -1):
        for c in range(len(triangle[r])):
            left_child = dp[c]
            right_child = dp[c + 1]
            parent_value = triangle[r][c] + min(left_child, right_child)
            dp[c] = parent_value
            working[r][c] = dp[c]
            solved_cells = [(row, col) for row in range(r + 1, len(triangle)) for col in range(len(triangle[row]))]
            solved_cells.extend((r, col) for col in range(c + 1))
            _emit(
                frames,
                table=working,
                note=f"Add min({left_child}, {right_child}) to parent triangle[{r}][{c}]",
                display_line=5,
                active_cells=[(r, c)],
                compare_cells=[(r + 1, c), (r + 1, c + 1)],
                solved_cells=solved_cells,
                shape="triangle",
                result_label="min_total",
                result_value=dp[c],
                locals={"r": r, "c": c, "row_count": len(triangle), "col_count": width},
                state_formula=f"triangle[{r}][{c}] = {triangle[r][c]} + min({left_child}, {right_child}) = {parent_value}",
            )
    _emit(
        frames,
        table=working,
        note=f"Final answer: minimum total path sum is {dp[0]}",
        display_line=6,
        active_cells=[(0, 0)],
        solved_cells=[(0, 0)],
        shape="triangle",
        result_label="min_total",
        result_value=dp[0],
        locals={"row_count": len(triangle), "col_count": width, "final_total": dp[0]},
        state_formula="Return the value at the top of the triangle after all collapses",
    )
    return frames


def build_edit_distance_frames(input_data: tuple[str, str]) -> list[dict]:
    source_word, target_word = input_data
    row_count, col_count = len(target_word) + 1, len(source_word) + 1
    dp_state = [[0] * col_count for _ in range(row_count)]
    frames = []
    for row_index in range(row_count):
        dp_state[row_index][0] = row_index
    for col_index in range(col_count):
        dp_state[0][col_index] = col_index
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: border cells hold insert and delete costs",
        display_line=4,
        solved_cells=[(row_index, 0) for row_index in range(row_count)] + [(0, col_index) for col_index in range(col_count)],
        row_labels=["Ø"] + list(target_word),
        col_labels=["Ø"] + list(source_word),
        result_label="distance",
        result_value=0,
        locals={"source_word": source_word, "target_word": target_word, "row_count": row_count, "col_count": col_count},
        state_formula="dp_state[row][col] = min(replace, delete, insert) or diagonal carry on match",
    )
    for row_index in range(1, row_count):
        for col_index in range(1, col_count):
            if target_word[row_index - 1] == source_word[col_index - 1]:
                dp_state[row_index][col_index] = dp_state[row_index - 1][col_index - 1]
                compare = [(row_index - 1, col_index - 1)]
                note = f"Characters match at ({row_index},{col_index}); carry diagonal cost"
                state_formula = f"dp_state[{row_index}][{col_index}] = dp_state[{row_index - 1}][{col_index - 1}] = {dp_state[row_index][col_index]}"
            else:
                dp_state[row_index][col_index] = 1 + min(
                    dp_state[row_index - 1][col_index],
                    dp_state[row_index][col_index - 1],
                    dp_state[row_index - 1][col_index - 1],
                )
                compare = [(row_index - 1, col_index), (row_index, col_index - 1), (row_index - 1, col_index - 1)]
                note = f"Take best of replace, delete, or insert at ({row_index},{col_index})"
                state_formula = f"dp_state[{row_index}][{col_index}] = 1 + min(top, left, diagonal) = {dp_state[row_index][col_index]}"
            _emit(
                frames,
                table=dp_state,
                note=note,
                display_line=9,
                active_cells=[(row_index, col_index)],
                compare_cells=compare,
                solved_cells=[(row_index, col_index)],
                row_labels=["Ø"] + list(target_word),
                col_labels=["Ø"] + list(source_word),
                result_label="distance",
                result_value=dp_state[row_index][col_index],
                locals={
                    "row_index": row_index,
                    "col_index": col_index,
                    "source_word": source_word,
                    "target_word": target_word,
                    "row_count": row_count,
                    "col_count": col_count,
                },
                state_formula=state_formula,
            )
    return frames


def build_interleaving_string_frames(input_data: tuple[str, str, str]) -> list[dict]:
    first_string, second_string, third_string = input_data
    row_count, col_count = len(second_string) + 1, len(first_string) + 1
    dp_state = [[False] * col_count for _ in range(row_count)]
    dp_state[0][0] = True
    frames = []
    _emit(frames, table=dp_state, note="Create the DP state: empty prefixes interleave to form an empty string", display_line=4, solved_cells=[(0, 0)], row_labels=["Ø"] + list(second_string), col_labels=["Ø"] + list(first_string), result_label="interleave", result_value=True, locals={"first_string": first_string, "second_string": second_string, "third_string": third_string, "row_count": row_count, "col_count": col_count}, state_formula="dp_state[row][col] is True when the next third_string character can come from left or top")
    for row_index in range(row_count):
        for col_index in range(col_count):
            if row_index == 0 and col_index == 0:
                continue
            third_index = row_index + col_index - 1
            if col_index > 0 and first_string[col_index - 1] == third_string[third_index] and dp_state[row_index][col_index - 1]:
                dp_state[row_index][col_index] = True
            if row_index > 0 and second_string[row_index - 1] == third_string[third_index] and dp_state[row_index - 1][col_index]:
                dp_state[row_index][col_index] = True
            _emit(
                frames,
                table=dp_state,
                note=f"Check whether third_string[{third_index}] can come from first_string or second_string",
                display_line=8,
                active_cells=[(row_index, col_index)],
                compare_cells=[cell for cell in ((row_index, col_index - 1), (row_index - 1, col_index)) if cell[0] >= 0 and cell[1] >= 0],
                solved_cells=[(row_index, col_index)],
                row_labels=["Ø"] + list(second_string),
                col_labels=["Ø"] + list(first_string),
                result_label="interleave",
                result_value=dp_state[row_index][col_index],
                locals={"row_index": row_index, "col_index": col_index, "target_index": third_index, "third_string": third_string},
                state_formula=f"dp_state[{row_index}][{col_index}] = left_match or top_match = {dp_state[row_index][col_index]}",
            )
    return frames


def build_distinct_subsequences_frames(input_data: tuple[str, str]) -> list[dict]:
    s, t = input_data
    rows, cols = len(t) + 1, len(s) + 1
    dp = [[0] * cols for _ in range(rows)]
    frames = []
    for c in range(cols):
        dp[0][c] = 1
    _emit(frames, table=dp, note="Empty target can be formed from any prefix in one way", display_line=4, solved_cells=[(0, c) for c in range(cols)], row_labels=["Ø"] + list(t), col_labels=["Ø"] + list(s), result_label="subseq", result_value=1, locals={"s": s, "t": t})
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r][c - 1]
            compare = [(r, c - 1)]
            if t[r - 1] == s[c - 1]:
                dp[r][c] += dp[r - 1][c - 1]
                compare.append((r - 1, c - 1))
            _emit(frames, table=dp, note=f"Count ways to form t[:{r}] from s[:{c}]", display_line=8, active_cells=[(r, c)], compare_cells=compare, solved_cells=[(r, c)], row_labels=["Ø"] + list(t), col_labels=["Ø"] + list(s), result_label="subseq", result_value=dp[r][c], locals={"r": r, "c": c, "s": s, "t": t})
    return frames


def build_lps_frames(s: str) -> list[dict]:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    frames = []
    for i in range(n):
        dp[i][i] = 1
        _emit(frames, table=dp, note=f"Single character at {i} is a palindrome of length 1", display_line=4, active_cells=[(i, i)], solved_cells=[(i, i)], row_labels=_range_labels(n, "r"), col_labels=_range_labels(n, "c"), result_label="lps", result_value=1, locals={"i": i, "s": s})
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i + 1][j - 1] if length > 2 else 0)
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
            _emit(frames, table=dp, note=f"Best palindrome length inside substring [{i}..{j}]", display_line=9, active_cells=[(i, j)], compare_cells=[cell for cell in ((i + 1, j - 1), (i + 1, j), (i, j - 1)) if 0 <= cell[0] < n and 0 <= cell[1] < n], solved_cells=[(i, j)], row_labels=_range_labels(n, "r"), col_labels=_range_labels(n, "c"), result_label="lps", result_value=dp[i][j], locals={"i": i, "j": j, "s": s})
    return frames


def build_palindromic_substrings_frames(s: str) -> list[dict]:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    count = 0
    frames = []
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length <= 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                count += 1
                _emit(frames, table=[[1 if cell else 0 for cell in row] for row in dp], note=f'Substring "{s[i:j+1]}" is a palindrome', display_line=6, active_cells=[(i, j)], compare_cells=[(i + 1, j - 1)] if length > 2 else [], solved_cells=[(i, j)], row_labels=_range_labels(n, "r"), col_labels=_range_labels(n, "c"), result_label="count", result_value=count, locals={"i": i, "j": j, "s": s})
    return frames


def build_lcs_frames(input_data: tuple[str, str]) -> list[dict]:
    first_string, second_string = input_data
    row_count, col_count = len(second_string) + 1, len(first_string) + 1
    dp_state = [[0] * col_count for _ in range(row_count)]
    frames = []
    _emit(
        frames,
        table=dp_state,
        note="Create the DP state: every LCS border starts at 0",
        display_line=3,
        row_labels=["Ø"] + list(second_string),
        col_labels=["Ø"] + list(first_string),
        result_label="lcs",
        result_value=0,
        locals={"first_string": first_string, "second_string": second_string, "row_count": row_count, "col_count": col_count},
        state_formula="dp_state[row][col] = diagonal + 1 on match, otherwise max(top, left)",
    )
    for row_index in range(1, row_count):
        for col_index in range(1, col_count):
            if second_string[row_index - 1] == first_string[col_index - 1]:
                dp_state[row_index][col_index] = dp_state[row_index - 1][col_index - 1] + 1
                compare = [(row_index - 1, col_index - 1)]
                note = f'Match "{second_string[row_index - 1]}" so take diagonal + 1'
                state_formula = f"dp_state[{row_index}][{col_index}] = dp_state[{row_index - 1}][{col_index - 1}] + 1 = {dp_state[row_index][col_index]}"
            else:
                dp_state[row_index][col_index] = max(dp_state[row_index - 1][col_index], dp_state[row_index][col_index - 1])
                compare = [(row_index - 1, col_index), (row_index, col_index - 1)]
                note = "No match, so take the longer prefix solution"
                state_formula = f"dp_state[{row_index}][{col_index}] = max(top, left) = {dp_state[row_index][col_index]}"
            _emit(
                frames,
                table=dp_state,
                note=note,
                display_line=7,
                active_cells=[(row_index, col_index)],
                compare_cells=compare,
                solved_cells=[(row_index, col_index)],
                row_labels=["Ø"] + list(second_string),
                col_labels=["Ø"] + list(first_string),
                result_label="lcs",
                result_value=dp_state[row_index][col_index],
                locals={"row_index": row_index, "col_index": col_index, "first_string": first_string, "second_string": second_string},
                state_formula=state_formula,
            )
    row_index, col_index = len(second_string), len(first_string)
    path: list[tuple[int, int]] = []
    while row_index > 0 and col_index > 0:
        path.append((row_index, col_index))
        if second_string[row_index - 1] == first_string[col_index - 1]:
            row_index -= 1
            col_index -= 1
        elif dp_state[row_index - 1][col_index] >= dp_state[row_index][col_index - 1]:
            row_index -= 1
        else:
            col_index -= 1
    path.append((row_index, col_index))
    _emit(frames, table=dp_state, note="Trace the path that reconstructs the LCS", display_line=10, trace_cells=path, row_labels=["Ø"] + list(second_string), col_labels=["Ø"] + list(first_string), result_label="lcs", result_value=dp_state[len(second_string)][len(first_string)], locals={"first_string": first_string, "second_string": second_string}, state_formula="Follow matches diagonally, otherwise follow the larger parent state")
    return frames


for _name, _obj in list(globals().items()):
    if _name.startswith("build_") and _name.endswith("_frames") and callable(_obj):
        globals()[_name] = _with_final_answer(_obj)
