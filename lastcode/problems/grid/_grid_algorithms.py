from __future__ import annotations

import copy
import inspect
import re
import textwrap
from collections import deque

from lastcode.recorder import Recorder


def _viz_probe(r: int, c: int) -> None:
    pass


def _viz_visit(r: int, c: int) -> None:
    pass


def _viz_mark(r: int, c: int) -> None:
    pass


def _viz_water(r: int, c: int) -> None:
    pass


def _viz_count(count: int) -> None:
    pass


def _viz_complete() -> None:
    pass


DIR4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIR8 = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def code_lines_for(func) -> list[str]:
    source = textwrap.dedent(inspect.getsource(func)).splitlines()
    signature = inspect.signature(func)
    clean_name = func.__name__.removeprefix("_").removesuffix("_instrumented")
    params = ", ".join(signature.parameters.keys())
    lines: list[str] = []
    for line in source:
        stripped = line.strip()
        if not stripped or stripped.startswith("_viz_") or "_viz_" in stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("def "):
            line = f"def {clean_name}({params}):"
        lines.append(line.rstrip())
    return lines


def run_grid_algorithm(fn_name: str, func, input_data, nested_fns: set[str] | None = None) -> list[dict]:
    recorder = Recorder()
    return recorder.record(
        fn_name,
        func,
        copy.deepcopy(input_data),
        nested_fns=nested_fns or set(),
    )


def _max_area_island_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    max_area = 0
    count = 0

    def dfs(r: int, c: int) -> int:
        if not (0 <= r < rows and 0 <= c < cols):
            return 0
        _viz_probe(r, c)
        if visited[r][c]:
            _viz_mark(r, c)
            return 0
        if grid[r][c] == 0:
            _viz_water(r, c)
            return 0
        _viz_visit(r, c)
        visited[r][c] = True
        _viz_mark(r, c)
        area = 1
        for dr, dc in DIR4:
            area += dfs(r + dr, c + dc)
        return area

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                area = dfs(r, c)
                max_area = max(max_area, area)
                count = max_area
                _viz_count(count)
                _viz_complete()
    return max_area


def _island_perimeter_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    perimeter = 0
    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 0:
                _viz_water(r, c)
                continue
            _viz_visit(r, c)
            _viz_mark(r, c)
            edges = 4
            for dr, dc in DIR4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    edges -= 1
            perimeter += edges
            count = perimeter
            _viz_count(count)
    _viz_complete()
    return perimeter


def _closed_island_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    count = 0

    def dfs(r: int, c: int) -> bool:
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        _viz_probe(r, c)
        if visited[r][c]:
            _viz_mark(r, c)
            return True
        if grid[r][c] == 1:
            _viz_water(r, c)
            return True
        _viz_visit(r, c)
        visited[r][c] = True
        _viz_mark(r, c)
        closed = not (r == 0 or c == 0 or r == rows - 1 or c == cols - 1)
        for dr, dc in DIR4:
            closed = dfs(r + dr, c + dc) and closed
        return closed

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and not visited[r][c] and dfs(r, c):
                count += 1
                _viz_count(count)
                _viz_complete()
    return count


def _num_enclaves_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols):
            return
        _viz_probe(r, c)
        if grid[r][c] == 0:
            _viz_water(r, c)
            return
        _viz_visit(r, c)
        grid[r][c] = 0
        _viz_mark(r, c)
        for dr, dc in DIR4:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in (0, cols - 1):
            if grid[r][c] == 1:
                dfs(r, c)
    for c in range(cols):
        for r in (0, rows - 1):
            if grid[r][c] == 1:
                dfs(r, c)

    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 1:
                _viz_mark(r, c)
                count += 1
                _viz_count(count)
            else:
                _viz_water(r, c)
    _viz_complete()
    return count


def _shortest_path_binary_matrix_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] != 0 or grid[rows - 1][cols - 1] != 0:
        _viz_complete()
        return -1
    q = deque([(0, 0, 1)])
    seen = {(0, 0)}
    count = -1
    while q:
        r, c, steps = q.popleft()
        _viz_probe(r, c)
        _viz_visit(r, c)
        _viz_mark(r, c)
        if (r, c) == (rows - 1, cols - 1):
            count = steps
            _viz_count(count)
            _viz_complete()
            return steps
        for dr, dc in DIR8:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                _viz_probe(nr, nc)
                if grid[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, steps + 1))
                    _viz_mark(nr, nc)
                else:
                    _viz_water(nr, nc)
    _viz_complete()
    return -1


def _update_matrix_instrumented(grid: list[list[int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))
                _viz_mark(r, c)
            else:
                _viz_water(r, c)
    count = 0
    while q:
        r, c = q.popleft()
        _viz_visit(r, c)
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                _viz_probe(nr, nc)
                if dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    count = dist[nr][nc]
                    q.append((nr, nc))
                    _viz_mark(nr, nc)
                    _viz_count(count)
                else:
                    _viz_water(nr, nc)
    _viz_complete()
    return dist


def _shortest_bridge_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    q = deque()
    seen = [[False] * cols for _ in range(rows)]
    found = False

    def dfs(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols):
            return
        _viz_probe(r, c)
        if seen[r][c]:
            _viz_mark(r, c)
            return
        if grid[r][c] == 0:
            _viz_water(r, c)
            return
        seen[r][c] = True
        q.append((r, c, 0))
        _viz_visit(r, c)
        _viz_mark(r, c)
        for dr, dc in DIR4:
            dfs(r + dr, c + dc)

    for r in range(rows):
        if found:
            break
        for c in range(cols):
            if grid[r][c] == 1:
                dfs(r, c)
                found = True
                break

    count = 0
    while q:
        r, c, steps = q.popleft()
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]:
                _viz_probe(nr, nc)
                if grid[nr][nc] == 1:
                    count = steps
                    _viz_count(count)
                    _viz_complete()
                    return steps
                seen[nr][nc] = True
                q.append((nr, nc, steps + 1))
                _viz_water(nr, nc)
    _viz_complete()
    return 0


def _as_far_from_land_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    q = deque()
    seen = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 1:
                q.append((r, c, 0))
                seen[r][c] = True
                _viz_mark(r, c)
            else:
                _viz_water(r, c)
    if not q or len(q) == rows * cols:
        _viz_complete()
        return -1
    count = 0
    while q:
        r, c, dist = q.popleft()
        _viz_visit(r, c)
        count = max(count, dist)
        _viz_count(count)
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]:
                seen[nr][nc] = True
                q.append((nr, nc, dist + 1))
                _viz_probe(nr, nc)
                _viz_mark(nr, nc)
    _viz_complete()
    return count


def _unique_paths_ii_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    count = 0
    if grid[0][0] == 1:
        _viz_complete()
        return 0
    dp[0][0] = 1
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 1:
                _viz_water(r, c)
                dp[r][c] = 0
                continue
            _viz_mark(r, c)
            if r == 0 and c == 0:
                continue
            top = dp[r - 1][c] if r > 0 else 0
            left = dp[r][c - 1] if c > 0 else 0
            dp[r][c] = top + left
            count = dp[r][c]
            _viz_count(count)
    _viz_complete()
    return dp[rows - 1][cols - 1]


def _maximal_square_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    best = 0
    count = 0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            _viz_probe(r - 1, c - 1)
            if grid[r - 1][c - 1] == 1:
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                best = max(best, dp[r][c])
                count = best * best
                _viz_mark(r - 1, c - 1)
                _viz_count(count)
            else:
                _viz_water(r - 1, c - 1)
    _viz_complete()
    return best * best


def _largest_1_bordered_square_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    left = [[0] * cols for _ in range(rows)]
    up = [[0] * cols for _ in range(rows)]
    best = 0
    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 1:
                left[r][c] = 1 + (left[r][c - 1] if c else 0)
                up[r][c] = 1 + (up[r - 1][c] if r else 0)
                side = min(left[r][c], up[r][c])
                while side > best:
                    if up[r][c - side + 1] >= side and left[r - side + 1][c] >= side:
                        best = side
                        count = best * best
                        _viz_count(count)
                        break
                    side -= 1
                _viz_mark(r, c)
            else:
                _viz_water(r, c)
    _viz_complete()
    return best * best


def _count_square_submatrices_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 1:
                if r == 0 or c == 0:
                    dp[r][c] = 1
                else:
                    dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                count += dp[r][c]
                _viz_mark(r, c)
                _viz_count(count)
            else:
                _viz_water(r, c)
    _viz_complete()
    return count


def _game_of_life_instrumented(grid: list[list[int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    next_grid = [[0] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            live = 0
            for dr, dc in DIR8:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    live += 1
            if grid[r][c] == 1 and live in (2, 3):
                next_grid[r][c] = 1
            elif grid[r][c] == 0 and live == 3:
                next_grid[r][c] = 1
            if next_grid[r][c] == 1:
                count += 1
                _viz_mark(r, c)
                _viz_count(count)
            else:
                _viz_water(r, c)
    _viz_complete()
    return next_grid


def _making_large_island_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    sizes: dict[int, int] = {}
    island_id = 2

    def dfs(r: int, c: int, marker: int) -> int:
        if not (0 <= r < rows and 0 <= c < cols):
            return 0
        _viz_probe(r, c)
        if grid[r][c] != 1:
            if grid[r][c] == 0:
                _viz_water(r, c)
            else:
                _viz_mark(r, c)
            return 0
        grid[r][c] = marker
        _viz_visit(r, c)
        _viz_mark(r, c)
        area = 1
        for dr, dc in DIR4:
            area += dfs(r + dr, c + dc, marker)
        return area

    best = 0
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                sizes[island_id] = dfs(r, c, island_id)
                best = max(best, sizes[island_id])
                count = best
                _viz_count(count)
                island_id += 1

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                continue
            _viz_probe(r, c)
            seen_ids = set()
            area = 1
            for dr, dc in DIR4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] > 1:
                    seen_ids.add(grid[nr][nc])
            for marker in seen_ids:
                area += sizes[marker]
            best = max(best, area)
            count = best
            _viz_water(r, c)
            _viz_count(count)
    _viz_complete()
    return best if best else rows * cols


def _count_servers_instrumented(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    row_count = [sum(row) for row in grid]
    col_count = [sum(grid[r][c] for r in range(rows)) for c in range(cols)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] == 1 and (row_count[r] > 1 or col_count[c] > 1):
                count += 1
                _viz_mark(r, c)
                _viz_count(count)
            else:
                _viz_water(r, c)
    _viz_complete()
    return count


def _find_farmland_instrumented(grid: list[list[int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    answer = []
    count = 0
    for r in range(rows):
        for c in range(cols):
            _viz_probe(r, c)
            if grid[r][c] != 1:
                _viz_water(r, c)
                continue
            if r > 0 and grid[r - 1][c] == 1:
                _viz_mark(r, c)
                continue
            if c > 0 and grid[r][c - 1] == 1:
                _viz_mark(r, c)
                continue
            rr, cc = r, c
            while rr + 1 < rows and grid[rr + 1][c] == 1:
                rr += 1
            while cc + 1 < cols and grid[r][cc + 1] == 1:
                cc += 1
            for i in range(r, rr + 1):
                for j in range(c, cc + 1):
                    _viz_mark(i, j)
            answer.append([r, c, rr, cc])
            count = len(answer)
            _viz_count(count)
    _viz_complete()
    return answer
