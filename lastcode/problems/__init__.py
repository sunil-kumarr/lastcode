"""Algorithm problem definitions for lastcode."""

from __future__ import annotations

import importlib

from lastcode.problems.registry import PROBLEM_MAP


def __getattr__(name: str):
    module_path = PROBLEM_MAP.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return importlib.import_module(module_path)


__all__ = sorted(PROBLEM_MAP)
