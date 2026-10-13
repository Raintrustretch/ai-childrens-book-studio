"""Tests for the child-safe prompt scrubber."""

from __future__ import annotations

from bookstudio.utils.safety import scrub_prompt


def test_denylisted_words_are_replaced():
    assert "gentle" in scrub_prompt("a bloody knife in the dark")


def test_clean_prompt_untouched():
    assert scrub_prompt("a bear and a moon") == "a bear and a moon"