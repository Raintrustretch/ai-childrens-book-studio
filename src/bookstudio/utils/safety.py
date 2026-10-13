"""Child-safe prompt scrubbing.

Strips tokens known to push illustration or story models toward scary,
violent, or age-inappropriate output. Applied before any prompt reaches
a generative backend — the filter is a denylist, not a classifier, so
it stays fast and auditable.
"""

from __future__ import annotations

import re

_DENYLIST = {
    "blood", "bloody", "gore", "gun", "knife", "dead", "death", "kill",
    "corpse", "scream", "horror", "nightmare", "demon", "hell", "war",
}
_TOKEN = re.compile(r"[a-z']+", re.IGNORECASE)


def scrub_prompt(prompt: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        word = match.group(0)
        return "gentle" if word.lower() in _DENYLIST else word
    return _TOKEN.sub(_replace, prompt)