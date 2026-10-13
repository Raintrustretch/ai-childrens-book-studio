"""Entry point: ``python -m bookstudio``.

Boots the Qt application, wires the plugin registry, and hands control
to the main window. Kept deliberately tiny so the desktop shell can be
swapped without touching pipeline code.
"""

from __future__ import annotations

import sys

from bookstudio.bootstrap.app import run_desktop


def main(argv: list[str] | None = None) -> int:
    return run_desktop(argv if argv is not None else sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())