"""Qt application bootstrap for the desktop studio.

Responsibilities:
  * parse CLI args (``--project``, ``--headless``, ``--render-only``)
  * build the plugin registry and load feature modules
  * construct the main window and enter the Qt event loop

Headless mode is used by the test suite and by CI render checks.
"""

from __future__ import annotations

import argparse
import logging
import sys

from bookstudio.bootstrap.paths import user_data_dir
from bookstudio.config.settings import Settings
from bookstudio.core.registry import PluginRegistry
from bookstudio.utils.logging import configure_logging

log = logging.getLogger("bookstudio.bootstrap")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="bookstudio", add_help=True)
    parser.add_argument("--project", help="path to a .bkproj project file")
    parser.add_argument("--headless", action="store_true",
                        help="run without a display (CI / render checks)")
    parser.add_argument("--render-only", metavar="PROJECT",
                        help="render an existing project then exit")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    return parser.parse_args(argv)


def run_desktop(argv: list[str]) -> int:
    args = _parse_args(argv)
    configure_logging(verbosity=args.verbose)

    settings = Settings.load(user_data_dir())
    registry = PluginRegistry.discover()
    log.info("loaded %d feature modules", len(registry.modules()))

    if args.headless or args.render_only:
        from bookstudio.core.pipeline import BookPipeline
        pipeline = BookPipeline(registry=registry, settings=settings)
        target = args.render_only or args.project
        if not target:
            log.error("headless mode requires --project or --render-only")
            return 2
        pipeline.render_project(target)
        return 0

    from bookstudio.ui.main_window import MainWindow
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv[:1])
    window = MainWindow(registry=registry, settings=settings,
                        initial_project=args.project)
    window.show()
    return app.exec()