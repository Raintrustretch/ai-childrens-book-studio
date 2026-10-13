"""Filesystem locations for user data, caches, and bundled fonts."""

from __future__ import annotations

import os
from pathlib import Path

_APP_DIRNAME = "AIBChildrensBookStudio"


def user_data_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local"
    path = Path(base) / _APP_DIRNAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def model_cache_dir() -> Path:
    path = user_data_dir() / "models"
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_scratch_dir(project_id: str) -> Path:
    path = user_data_dir() / "scratch" / project_id
    path.mkdir(parents=True, exist_ok=True)
    return path