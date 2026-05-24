"""sys.settrace-based frame recorder for algorithm visualization."""

from __future__ import annotations

import copy
import sys
from typing import Callable

_DEFAULT_MARKER_FNS: frozenset[str] = frozenset({"_viz_visit", "_viz_mark", "_viz_count"})


class Recorder:
    """Collects execution frames from an instrumented function."""

    def __init__(self) -> None:
        self.frames: list[dict] = []
        self._dfs_depth: int = 0
        self._marker_fns: frozenset[str] = _DEFAULT_MARKER_FNS
        self._nested_fns: frozenset[str] = frozenset()
        self._target_fn_names: frozenset[str] = frozenset()
        self._marker_handlers: dict[str, Callable] = {}

    def record(
        self,
        fn_name: str,
        func,
        *args,
        marker_fns: set[str] | None = None,
        nested_fns: set[str] | None = None,
        marker_handlers: dict[str, Callable] | None = None,
        **kwargs,
    ) -> list[dict]:
        """Run func(*args) under sys.settrace and return collected frames.

        Args:
            fn_name: Name of the top-level function to trace.
            func: The function to execute.
            marker_fns: Set of marker function names to intercept.
                        Defaults to {"_viz_visit", "_viz_mark", "_viz_count"}.
            nested_fns: Set of nested function names to trace for depth tracking.
                        Defaults to empty (no depth tracking).
            marker_handlers: Dict mapping marker fn name → callable(frame) → dict | None.
                             If None, uses built-in count_islands handlers.
        """
        self.frames = []
        self._dfs_depth = 0
        self._marker_fns = frozenset(marker_fns) if marker_fns is not None else _DEFAULT_MARKER_FNS
        self._nested_fns = frozenset(nested_fns) if nested_fns is not None else frozenset()
        self._target_fn_names = frozenset({fn_name}) | self._nested_fns
        self._marker_handlers = marker_handlers or self._default_handlers()

        # Prepend initial signature frame representing the function call (line 1)
        import inspect
        try:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            initial_locals = dict(bound.arguments)
            _, start_line = inspect.getsourcelines(func)
            if start_line is not None:
                self.frames.append({
                    "type": "line",
                    "lineno": start_line,
                    "filename": func.__code__.co_filename,
                    "fn": func.__name__,
                    "locals": self._safe_deepcopy(initial_locals),
                    "dfs_depth": 0,
                })
        except Exception:
            pass

        old_trace = sys.gettrace()
        sys.settrace(self._global_trace)
        try:
            func(*args, **kwargs)
        finally:
            sys.settrace(old_trace)

        return self.frames

    # ------------------------------------------------------------------
    # Default handlers (count_islands compatible)
    # ------------------------------------------------------------------

    @staticmethod
    def _default_handlers() -> dict[str, Callable]:
        def handle_viz_visit(locs: dict, depth: int) -> dict | None:
            r, c = locs.get("r"), locs.get("c")
            if r is not None and c is not None:
                return {"type": "cell_visit", "r": r, "c": c, "color": "current", "dfs_depth": depth}
            return None

        def handle_viz_mark(locs: dict, depth: int) -> dict | None:
            r, c = locs.get("r"), locs.get("c")
            if r is not None and c is not None:
                return {"type": "cell_mark", "r": r, "c": c, "color": "visited", "dfs_depth": depth}
            return None

        def handle_viz_count(locs: dict, depth: int) -> dict | None:
            count = locs.get("count")
            if count is not None:
                return {"type": "count_update", "count": count, "dfs_depth": depth}
            return None

        return {
            "_viz_visit": handle_viz_visit,
            "_viz_mark":  handle_viz_mark,
            "_viz_count": handle_viz_count,
        }

    # ------------------------------------------------------------------
    # Trace callbacks
    # ------------------------------------------------------------------

    def _global_trace(self, frame, event: str, arg):
        fn_name = frame.f_code.co_name

        if event == "call":
            if fn_name in self._marker_fns:
                handler = self._marker_handlers.get(fn_name)
                if handler:
                    locs = dict(frame.f_locals)
                    result = handler(locs, self._dfs_depth)
                    if result:
                        if frame.f_back:
                            result["lineno"] = frame.f_back.f_lineno
                            result["filename"] = frame.f_back.f_code.co_filename
                            result["locals"] = self._safe_deepcopy(dict(frame.f_back.f_locals))
                        self.frames.append(result)
                return None

            if fn_name in self._nested_fns:
                self._dfs_depth += 1

            if fn_name in self._target_fn_names:
                return self._local_trace

        return None

    def _local_trace(self, frame, event: str, arg):
        fn_name = frame.f_code.co_name

        if event == "call":
            return self._local_trace

        if event == "return":
            if fn_name in self._nested_fns:
                self._dfs_depth = max(0, self._dfs_depth - 1)
                self.frames.append({
                    "type": "dfs_return",
                    "dfs_depth": self._dfs_depth,
                    "locals": self._safe_deepcopy(dict(frame.f_locals)),
                })
            return self._local_trace

        if event == "line":
            if fn_name in self._target_fn_names:
                self._emit_line_frame(frame)
            return self._local_trace

        return self._local_trace

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _emit_line_frame(self, frame) -> None:
        try:
            locals_snap = self._safe_deepcopy(dict(frame.f_locals))
        except Exception:
            locals_snap = {}
        self.frames.append({
            "type": "line",
            "lineno": frame.f_lineno,
            "filename": frame.f_code.co_filename,
            "fn": frame.f_code.co_name,
            "locals": locals_snap,
            "dfs_depth": self._dfs_depth,
        })

    @staticmethod
    def _safe_deepcopy(obj: dict) -> dict:
        result = {}
        for k, v in obj.items():
            if k.startswith("_"):
                continue
            try:
                result[k] = copy.deepcopy(v)
            except Exception:
                result[k] = repr(v)
        return result
