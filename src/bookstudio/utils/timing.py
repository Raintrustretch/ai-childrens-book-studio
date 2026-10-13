"""Decorator for timing pipeline stages — used by the profiler panel."""

from __future__ import annotations

import functools
import logging
import time
from typing import Callable, TypeVar

log = logging.getLogger("bookstudio.timing")
F = TypeVar("F", bound=Callable)


def timed(fn: F) -> F:
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            log.info("%s took %.1fms", fn.__qualname__, elapsed_ms)
    return wrapper  # type: ignore[return-value]