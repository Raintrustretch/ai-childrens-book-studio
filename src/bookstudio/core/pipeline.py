"""End-to-end book pipeline: premise -> outline -> pages -> art -> PDF.

The pipeline is a straight line of capability calls. Each stage pulls
its implementation from the registry, so a project can swap the story
engine, rhyme checker, or illustration backend without pipeline edits.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from bookstudio.config.settings import Settings
from bookstudio.core.registry import PluginRegistry
from bookstudio.models.book import BookProject, PageDraft
from bookstudio.utils.timing import timed

log = logging.getLogger("bookstudio.pipeline")


@dataclass
class PipelineResult:
    project: BookProject
    output_pdf: Path | None = None
    warnings: list[str] = field(default_factory=list)


class BookPipeline:
    def __init__(self, registry: PluginRegistry, settings: Settings) -> None:
        self.registry = registry
        self.settings = settings

    @timed
    def render_project(self, project_path: str | Path) -> PipelineResult:
        project = BookProject.load(Path(project_path))
        return self.build(project)

    def build(self, project: BookProject) -> PipelineResult:
        settings = self.settings.with_overrides(project.overrides)
        story = self.registry.resolve("story", settings.text_backend).factory()
        rhyme = self.registry.resolve("rhyme", settings.rhyme_scheme).factory()
        art = self.registry.resolve("illustration", settings.art_backend).factory()
        layout = self.registry.resolve("layout").factory()
        export = self.registry.resolve("export").factory()

        outline = story.outline(project.premise, settings)  # type: ignore[attr-defined]
        pages: list[PageDraft] = []
        for idx, beat in enumerate(outline.beats[: settings.page_count]):
            draft = story.write_page(beat, settings)  # type: ignore[attr-defined]
            draft.rhyme_report = rhyme.check(draft.text)  # type: ignore[attr-defined]
            pages.append(draft)
            log.info("page %02d drafted (%d words)", idx + 1, draft.word_count)

        for page in pages:
            page.illustration_path = art.illustrate(page, settings)  # type: ignore[attr-defined]

        book = layout.assemble(project, pages, settings)  # type: ignore[attr-defined]
        out = export.to_pdf(book, settings)  # type: ignore[attr-defined]
        return PipelineResult(project=project, output_pdf=out)