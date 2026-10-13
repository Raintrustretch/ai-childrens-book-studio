"""Smoke tests for the book pipeline using a stub registry."""

from __future__ import annotations

from pathlib import Path

import pytest

from bookstudio.config.settings import Settings
from bookstudio.core.pipeline import BookPipeline
from bookstudio.core.registry import ModuleSpec, PluginRegistry
from bookstudio.models.book import BookProject, PageDraft, RhymeReport


class _StubStory:
    def outline(self, premise, settings):
        from bookstudio.features.story.local_llm import Outline, OutlineBeat
        return Outline(title=premise, beats=[OutlineBeat(0, "a small bear wakes up")])

    def write_page(self, beat, settings):
        return PageDraft(index=beat.index, beat=beat.summary,
                         text="the bear saw the moon\nand hummed a soft tune")


class _StubRhyme:
    def check(self, text):
        return RhymeReport(scheme="AABB", passed=True)


class _StubArt:
    def illustrate(self, page, settings):
        return "stub.png"


class _StubLayout:
    def assemble(self, project, pages, settings):
        return {"pages": [p.text for p in pages]}


class _StubExport:
    def to_pdf(self, book, settings):
        return Path("out.pdf")


def _stub_registry() -> PluginRegistry:
    reg = PluginRegistry()
    reg.register(ModuleSpec("stub-story", "story", _StubStory))
    reg.register(ModuleSpec("stub-rhyme", "rhyme", _StubRhyme))
    reg.register(ModuleSpec("stub-art", "illustration", _StubArt))
    reg.register(ModuleSpec("stub-layout", "layout", _StubLayout))
    reg.register(ModuleSpec("stub-export", "export", _StubExport))
    return reg


def test_pipeline_builds_one_page_book():
    project = BookProject(project_id="t1", premise="a bear who loves the moon")
    result = BookPipeline(_stub_registry(), Settings()).build(project)
    assert result.output_pdf == Path("out.pdf")
    assert result.project.premise == "a bear who loves the moon"


def test_rhyme_key_matches_family():
    from bookstudio.utils.phonetics import rhyme_key
    assert rhyme_key("the cat") == rhyme_key("a hat")