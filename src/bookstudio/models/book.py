"""Book + page domain models.

These are plain dataclasses with explicit (de)serialisation so a
``.bkproj`` file is human-readable JSON and diffable in git.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class RhymeReport:
    scheme: str
    passed: bool
    issues: list[str] = field(default_factory=list)


@dataclass
class PageDraft:
    index: int
    beat: str
    text: str = ""
    illustration_prompt: str = ""
    illustration_path: str | None = None
    rhyme_report: RhymeReport | None = None

    @property
    def word_count(self) -> int:
        return len(self.text.split())


@dataclass
class BookProject:
    project_id: str
    premise: str
    title: str = "Untitled Picture Book"
    overrides: dict[str, Any] = field(default_factory=dict)
    pages: list[PageDraft] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    def save(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "BookProject":
        raw = json.loads(path.read_text("utf-8"))
        raw["pages"] = [PageDraft(**p) for p in raw.get("pages", [])]
        return cls(**raw)