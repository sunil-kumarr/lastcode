"""
main.py — entry point for lastcode.

Usage:
    lastcode
    python -m lastcode
"""

from __future__ import annotations


def main() -> None:
    """Launch the lastcode TUI application."""
    from lastcode.app import lastcodeApp

    app = lastcodeApp()
    app.run()


if __name__ == "__main__":
    main()
