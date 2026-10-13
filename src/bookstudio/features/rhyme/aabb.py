"""AABB rhyme checker for early-reader picture books.

Uses a CMUdict-style pronunciation lookup to compare final stressed
vowel + coda of the last word on each line. Reports issues but never
blocks — a book with a near-rhyme still ships.
"""

from __future__ import annotations

from bookstudio.models.book import RhymeReport
from bookstudio.utils.phonetics import rhyme_key


class AABBChecker:
    scheme = "AABB"

    def check(self, text: str) -> RhymeReport:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        issues: list[str] = []
        for i in range(0, len(lines) - 1, 2):
            a, b = lines[i], lines[i + 1]
            if rhyme_key(a) != rhyme_key(b):
                issues.append(f"lines {i+1}/{i+2} do not rhyme")
        return RhymeReport(scheme=self.scheme, passed=not issues, issues=issues)