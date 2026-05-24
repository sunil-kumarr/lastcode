from __future__ import annotations

import copy
import inspect
import textwrap


def code_lines_for(func) -> list[str]:
    source = textwrap.dedent(inspect.getsource(func)).splitlines()
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
) -> None:
    frames.append(
        {
            "type": "dp_step",
            "table": copy.deepcopy(table),
            "note": note,
            "display_line": display_line,
            "active_cells": active_cells or [],
            "compare_cells": compare_cells or [],
            "solved_cells": solved_cells or [],
            "trace_cells": trace_cells or [],
            "row_labels": row_labels,
            "col_labels": col_labels,
            "result_label": result_label,
            "result_value": result_value,
            "locals": copy.deepcopy(locals or {}),
        }
    )


def _range_labels(size: int, prefix: str = "") -> list[str]:
    return [f"{prefix}{i}" for i in range(size)]


def build_climbing_stairs_frames(n: int) -> list[dict]:
    frames = []
    if n <= 2:
        _emit(frames, table=[1, 2][:max(n, 1)], note="Base case already gives the answer", display_line=2, solved_cells=[(0, max(n - 1, 0))], col_labels=_range_labels(max(n, 1)), result_label="ways", result_value=n, locals={"n": n})
        return frames
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    _emit(frames, table=dp[1:], note="Seed the first two stair counts", display_line=3, solved_cells=[(0, 0), (0, 1)], col_labels=_range_labels(n), result_label="ways", result_value=2, locals={"n": n})
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        _emit(frames, table=dp[1:], note=f"Ways to reach stair {i} = previous two stairs", display_line=5, active_cells=[(0, i - 1)], compare_cells=[(0, i - 2), (0, i - 3)], solved_cells=[(0, i - 1)], col_labels=_range_labels(n), result_label="ways", result_value=dp[i], locals={"n": n, "i": i})
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
    _emit(frames, table=dp, note="First house defines the starting best loot", display_line=3, solved_cells=[(0, 0)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=dp[0], locals={"i": 0})
    if len(nums) == 1:
        return frames
    dp[1] = max(nums[0], nums[1])
    _emit(frames, table=dp, note="Choose the better of the first two houses", display_line=5, active_cells=[(0, 1)], compare_cells=[(0, 0)], solved_cells=[(0, 1)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=dp[1], locals={"i": 1})
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        _emit(frames, table=dp, note=f"Skip or rob house {i}", display_line=7, active_cells=[(0, i)], compare_cells=[(0, i - 1), (0, i - 2)], solved_cells=[(0, i)], col_labels=_range_labels(len(nums)), result_label="loot", result_value=dp[i], locals={"i": i})
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
    best_excl_last = rob_linear(nums[:-1], 0, frames, 4)
    best_excl_first = rob_linear(nums[1:], 1, frames, 5)
    _emit(frames, table=[best_excl_last, best_excl_first], note="Take the better of the two linear passes", display_line=6, active_cells=[(0, 0), (0, 1)], solved_cells=[(0, 0), (0, 1)], col_labels=["skip last", "skip first"], result_label="loot", result_value=max(best_excl_last, best_excl_first), locals={})
    return frames


def build_coin_change_frames(input_data: tuple[list[int], int]) -> list[dict]:
    coins, amount = input_data
    frames = []
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    _emit(frames, table=dp, note="Initialize all amounts as unreachable except zero", display_line=3, solved_cells=[(0, 0)], col_labels=_range_labels(amount + 1), result_label="min_coins", result_value=0, locals={"amount": amount})
    for coin in coins:
        for total in range(coin, amount + 1):
            candidate = dp[total - coin] + 1
            if candidate < dp[total]:
                dp[total] = candidate
                _emit(frames, table=dp, note=f"Use coin {coin} to improve amount {total}", display_line=6, active_cells=[(0, total)], compare_cells=[(0, total - coin)], solved_cells=[(0, total)], col_labels=_range_labels(amount + 1), result_label="min_coins", result_value=dp[total], locals={"amount": amount, "i": total})
    return frames


def build_coin_change_ii_frames(input_data: tuple[int, list[int]]) -> list[dict]:
    amount, coins = input_data
    frames = []
    dp = [0] * (amount + 1)
    dp[0] = 1
    _emit(frames, table=dp, note="There is one way to make amount zero", display_line=3, solved_cells=[(0, 0)], col_labels=_range_labels(amount + 1), result_label="ways", result_value=1, locals={"amount": amount})
    for coin in coins:
        for total in range(coin, amount + 1):
            dp[total] += dp[total - coin]
            _emit(frames, table=dp, note=f"Add combinations that end with coin {coin}", display_line=6, active_cells=[(0, total)], compare_cells=[(0, total - coin)], solved_cells=[(0, total)], col_labels=_range_labels(amount + 1), result_label="ways", result_value=dp[total], locals={"amount": amount, "i": total})
    return frames


def build_lis_frames(nums: list[int]) -> list[dict]:
    frames = []
    if not nums:
        return frames
    dp = [1] * len(nums)
    _emit(frames, table=dp, note="Every number starts as an increasing subsequence of length 1", display_line=3, solved_cells=[(0, idx) for idx in range(len(nums))], col_labels=_range_labels(len(nums)), result_label="lis", result_value=1, locals={})
    best = 1
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                best = max(best, dp[i])
                _emit(frames, table=dp, note=f"Extend subsequence ending at index {j} into index {i}", display_line=7, active_cells=[(0, i)], compare_cells=[(0, j)], solved_cells=[(0, i)], col_labels=_range_labels(len(nums)), result_label="lis", result_value=best, locals={"i": i, "j": j})
    return frames


def build_partition_equal_subset_sum_frames(nums: list[int]) -> list[dict]:
    total = sum(nums)
    frames = []
    if total % 2:
        _emit(frames, table=[total], note="Odd total means equal partition is impossible", display_line=2, solved_cells=[(0, 0)], col_labels=["sum"], result_label="possible", result_value=False, locals={})
        return frames
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    _emit(frames, table=dp, note="Subset sum 0 is always achievable", display_line=4, solved_cells=[(0, 0)], col_labels=_range_labels(target + 1), result_label="possible", result_value=True, locals={"target": target})
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
                _emit(frames, table=dp, note=f"Use value {num} to reach subset sum {s}", display_line=7, active_cells=[(0, s)], compare_cells=[(0, s - num)], solved_cells=[(0, s)], col_labels=_range_labels(target + 1), result_label="possible", result_value=dp[target], locals={"i": s, "target": target})
    return frames


def build_target_sum_frames(input_data: tuple[list[int], int]) -> list[dict]:
    nums, target = input_data
    offset = sum(nums)
    width = 2 * offset + 1
    dp = [0] * width
    dp[offset] = 1
    frames = []
    _emit(frames, table=dp, note="Offset zero sum into the center of the table", display_line=4, solved_cells=[(0, offset)], col_labels=_range_labels(width), result_label="ways", result_value=1, locals={"target": target})
    for idx, num in enumerate(nums):
        nxt = [0] * width
        for s in range(width):
            if dp[s]:
                nxt[s + num] += dp[s]
                nxt[s - num] += dp[s]
        dp = nxt
        _emit(frames, table=dp, note=f"After number {num}, distribute ways to plus/minus sums", display_line=8, active_cells=[(0, offset + target)] if 0 <= offset + target < width else [], solved_cells=[(0, pos) for pos, value in enumerate(dp) if value], col_labels=_range_labels(width), result_label="ways", result_value=dp[offset + target] if 0 <= offset + target < width else 0, locals={"i": idx, "target": target})
    return frames


def build_word_break_frames(input_data: tuple[str, list[str]]) -> list[dict]:
    s, words = input_data
    word_set = set(words)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    frames = []
    _emit(frames, table=dp, note="Empty prefix is always segmentable", display_line=4, solved_cells=[(0, 0)], col_labels=_range_labels(len(s) + 1), result_label="segmentable", result_value=True, locals={"s": s})
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                _emit(frames, table=dp, note=f'Split "{s[:i]}" at {j} using dictionary word "{s[j:i]}"', display_line=7, active_cells=[(0, i)], compare_cells=[(0, j)], solved_cells=[(0, i)], col_labels=_range_labels(len(s) + 1), result_label="segmentable", result_value=dp[i], locals={"i": i, "j": j, "s": s})
                break
    return frames


def build_decode_ways_frames(s: str) -> list[dict]:
    frames = []
    if not s or s[0] == "0":
        _emit(frames, table=[0], note="A leading zero cannot be decoded", display_line=2, solved_cells=[(0, 0)], col_labels=["0"], result_label="ways", result_value=0, locals={"s": s})
        return frames
    dp = [0] * (len(s) + 1)
    dp[0] = dp[1] = 1
    _emit(frames, table=dp, note="Seed empty and first-character decode counts", display_line=4, solved_cells=[(0, 0), (0, 1)], col_labels=_range_labels(len(s) + 1), result_label="ways", result_value=1, locals={"s": s})
    for i in range(2, len(s) + 1):
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
        if 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]
        _emit(frames, table=dp, note=f"Count one-digit and two-digit decodes ending at position {i}", display_line=8, active_cells=[(0, i)], compare_cells=[(0, i - 1), (0, i - 2)], solved_cells=[(0, i)], col_labels=_range_labels(len(s) + 1), result_label="ways", result_value=dp[i], locals={"i": i, "s": s})
    return frames


def build_unique_paths_frames(input_data: tuple[int, int]) -> list[dict]:
    m, n = input_data
    dp = [[1] * n for _ in range(m)]
    frames = []
    _emit(frames, table=dp, note="First row and first column each have one path", display_line=3, solved_cells=[(r, c) for r in range(m) for c in range(n) if r == 0 or c == 0], row_labels=_range_labels(m, "r"), col_labels=_range_labels(n, "c"), result_label="paths", result_value=1, locals={"m": m, "n": n})
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
            _emit(frames, table=dp, note=f"Paths to ({r},{c}) come from top plus left", display_line=5, active_cells=[(r, c)], compare_cells=[(r - 1, c), (r, c - 1)], solved_cells=[(r, c)], row_labels=_range_labels(m, "r"), col_labels=_range_labels(n, "c"), result_label="paths", result_value=dp[r][c], locals={"r": r, "c": c, "m": m, "n": n})
    return frames


def build_min_path_sum_frames(grid: list[list[int]]) -> list[dict]:
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    frames = []
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                dp[r][c] = grid[r][c]
            elif r == 0:
                dp[r][c] = dp[r][c - 1] + grid[r][c]
            elif c == 0:
                dp[r][c] = dp[r - 1][c] + grid[r][c]
            else:
                dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]
            compare = []
            if r > 0:
                compare.append((r - 1, c))
            if c > 0:
                compare.append((r, c - 1))
            _emit(frames, table=dp, note=f"Cheapest path cost into cell ({r},{c})", display_line=7, active_cells=[(r, c)], compare_cells=compare, solved_cells=[(r, c)], row_labels=_range_labels(rows, "r"), col_labels=_range_labels(cols, "c"), result_label="min_sum", result_value=dp[r][c], locals={"r": r, "c": c})
    return frames


def build_triangle_frames(triangle: list[list[int]]) -> list[dict]:
    dp = triangle[-1][:]
    frames = []
    _emit(frames, table=dp, note="Start from the bottom row of the triangle", display_line=3, solved_cells=[(0, idx) for idx in range(len(dp))], col_labels=_range_labels(len(dp)), result_label="min_total", result_value=min(dp), locals={})
    for r in range(len(triangle) - 2, -1, -1):
        for c in range(len(triangle[r])):
            dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])
            _emit(frames, table=dp[: len(triangle[r])], note=f"Collapse row {r} using the two children below", display_line=5, active_cells=[(0, c)], compare_cells=[(0, c), (0, c + 1)], solved_cells=[(0, c)], col_labels=_range_labels(len(triangle[r])), result_label="min_total", result_value=dp[c], locals={"r": r, "c": c})
    return frames


def build_edit_distance_frames(input_data: tuple[str, str]) -> list[dict]:
    word1, word2 = input_data
    rows, cols = len(word2) + 1, len(word1) + 1
    dp = [[0] * cols for _ in range(rows)]
    frames = []
    for r in range(rows):
        dp[r][0] = r
    for c in range(cols):
        dp[0][c] = c
    _emit(frames, table=dp, note="Initialize insert/delete costs on the borders", display_line=4, solved_cells=[(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)], row_labels=["Ø"] + list(word2), col_labels=["Ø"] + list(word1), result_label="distance", result_value=0, locals={"word1": word1, "word2": word2})
    for r in range(1, rows):
        for c in range(1, cols):
            if word2[r - 1] == word1[c - 1]:
                dp[r][c] = dp[r - 1][c - 1]
                compare = [(r - 1, c - 1)]
                note = f"Characters match at ({r},{c}); carry diagonal cost"
            else:
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                compare = [(r - 1, c), (r, c - 1), (r - 1, c - 1)]
                note = f"Take best of replace, delete, or insert at ({r},{c})"
            _emit(frames, table=dp, note=note, display_line=9, active_cells=[(r, c)], compare_cells=compare, solved_cells=[(r, c)], row_labels=["Ø"] + list(word2), col_labels=["Ø"] + list(word1), result_label="distance", result_value=dp[r][c], locals={"r": r, "c": c, "word1": word1, "word2": word2})
    return frames


def build_interleaving_string_frames(input_data: tuple[str, str, str]) -> list[dict]:
    s1, s2, s3 = input_data
    rows, cols = len(s2) + 1, len(s1) + 1
    dp = [[False] * cols for _ in range(rows)]
    dp[0][0] = True
    frames = []
    _emit(frames, table=dp, note="Empty prefixes interleave to form an empty string", display_line=4, solved_cells=[(0, 0)], row_labels=["Ø"] + list(s2), col_labels=["Ø"] + list(s1), result_label="interleave", result_value=True, locals={"s1": s1, "s2": s2, "s3": s3})
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                continue
            idx = r + c - 1
            if c > 0 and s1[c - 1] == s3[idx] and dp[r][c - 1]:
                dp[r][c] = True
            if r > 0 and s2[r - 1] == s3[idx] and dp[r - 1][c]:
                dp[r][c] = True
            _emit(frames, table=dp, note=f"Check whether s3[{idx}] can come from s1 or s2", display_line=8, active_cells=[(r, c)], compare_cells=[cell for cell in ((r, c - 1), (r - 1, c)) if cell[0] >= 0 and cell[1] >= 0], solved_cells=[(r, c)], row_labels=["Ø"] + list(s2), col_labels=["Ø"] + list(s1), result_label="interleave", result_value=dp[r][c], locals={"r": r, "c": c, "s3": s3})
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
    s1, s2 = input_data
    rows, cols = len(s2) + 1, len(s1) + 1
    dp = [[0] * cols for _ in range(rows)]
    frames = []
    _emit(frames, table=dp, note="Initialize the LCS table with zeros", display_line=3, row_labels=["Ø"] + list(s2), col_labels=["Ø"] + list(s1), result_label="lcs", result_value=0, locals={"s1": s1, "s2": s2})
    for r in range(1, rows):
        for c in range(1, cols):
            if s2[r - 1] == s1[c - 1]:
                dp[r][c] = dp[r - 1][c - 1] + 1
                compare = [(r - 1, c - 1)]
                note = f'Match "{s2[r - 1]}" so take diagonal + 1'
            else:
                dp[r][c] = max(dp[r - 1][c], dp[r][c - 1])
                compare = [(r - 1, c), (r, c - 1)]
                note = "No match, so take the longer prefix solution"
            _emit(frames, table=dp, note=note, display_line=7, active_cells=[(r, c)], compare_cells=compare, solved_cells=[(r, c)], row_labels=["Ø"] + list(s2), col_labels=["Ø"] + list(s1), result_label="lcs", result_value=dp[r][c], locals={"r": r, "c": c, "s1": s1, "s2": s2})
    r, c = len(s2), len(s1)
    path: list[tuple[int, int]] = []
    while r > 0 and c > 0:
        path.append((r, c))
        if s2[r - 1] == s1[c - 1]:
            r -= 1
            c -= 1
        elif dp[r - 1][c] >= dp[r][c - 1]:
            r -= 1
        else:
            c -= 1
    path.append((r, c))
    _emit(frames, table=dp, note="Trace the path that reconstructs the LCS", display_line=15, trace_cells=path, row_labels=["Ø"] + list(s2), col_labels=["Ø"] + list(s1), result_label="lcs", result_value=dp[len(s2)][len(s1)], locals={"s1": s1, "s2": s2})
    return frames
