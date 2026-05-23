"""
main.py — entry point for neonodes.

Usage:
    neonodes
    python -m neonodes
"""

from __future__ import annotations


def main() -> None:
    """Launch the neonodes TUI application."""
    from neonodes.app import NeonodesApp

    app = NeonodesApp()
    app.run()


if __name__ == "__main__":
    main()
