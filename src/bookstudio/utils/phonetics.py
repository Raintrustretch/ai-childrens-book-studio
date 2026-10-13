"""Lightweight rhyme-key extraction.

Reduces a word to its final stressed vowel + trailing consonants using
a small built-in pronunciation table. Falls back to a suffix heuristic
for words outside the table — good enough for AABB checks on simple
picture-book vocabulary.
"""

from __future__ import annotations

import re

_VOWELS = "aeiouy"
_PRONUNCIATION: dict[str, str] = {
    "cat": "AE1 T", "hat": "HH AE1 T", "mat": "M AE1 T",
    "moon": "M UW1 N", "spoon": "S P UW1 N", "soon": "S UW1 N",
    "star": "S T AA1 R", "far": "F AA1 R", "car": "K AA1 R",
}

_SUFFIX_STRIP = re.compile(r"(ing|ed|es|s)$", re.IGNORECASE)


def rhyme_key(line: str) -> str:
    words = re.findall(r"[a-z']+", line.lower())
    if not words:
        return ""
    last = words[-1]
    if last in _PRONUNCIATION:
        phon = _PRONUNCIATION[last]
        stressed = [p for p in phon.split() if p[-1].isdigit()]
        return " ".join(stressed[-1:]) + " " + phon.split()[-1]
    stripped = _SUFFIX_STRIP.sub("", last)
    for i in range(len(stripped) - 1, -1, -1):
        if stripped[i] in _VOWELS:
            return stripped[i:]
    return stripped