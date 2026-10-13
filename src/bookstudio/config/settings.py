"""User + project settings.

Settings are layered: packaged defaults -> user settings.json ->
per-project ``.bkproj`` overrides. Each layer is a plain mapping; the
final merged view is validated once into a frozen dataclass.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bookstudio.config.defaults import DEFAULT_SETTINGS


@dataclass(frozen=True)
class Settings:
    text_backend: str = "local-llm"
    art_backend: str = "diffusion-local"
    target_age_band: str = "3-5"
    page_count: int = 24
    rhyme_scheme: str = "AABB"
    illustration_style: str = "watercolor"
    safety_filter: str = "child-safe-strict"
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, data_dir: Path) -> "Settings":
        merged = dict(DEFAULT_SETTINGS)
        user_file = data_dir / "settings.json"
        if user_file.exists():
            merged.update(json.loads(user_file.read_text("utf-8")))
        return cls(**{k: v for k, v in merged.items()
                      if k in cls.__dataclass_fields__})

    def with_overrides(self, overrides: dict[str, Any]) -> "Settings":
        merged = {**self.__dict__, **overrides}
        return Settings(**{k: v for k, v in merged.items()
                           if k in self.__dataclass_fields__})