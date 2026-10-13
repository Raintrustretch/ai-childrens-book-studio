"""Local diffusion illustrator (SDXL-lite, distilled for picture books).

Illustration prompts are constructed from the page text plus a style
preset, then passed through a child-safe prompt rewriter that strips
scary, violent, or age-inappropriate tokens before sampling.
"""

from __future__ import annotations

import logging
from pathlib import Path

from bookstudio.bootstrap.paths import project_scratch_dir
from bookstudio.config.settings import Settings
from bookstudio.models.book import PageDraft
from bookstudio.services.diffusion_client import DiffusionClient
from bookstudio.utils.safety import scrub_prompt

log = logging.getLogger("bookstudio.illustration")

STYLE_PRESETS = {
    "watercolor": "soft watercolor, warm palette, gentle outlines",
    "crayon": "waxy crayon texture, bold shapes, primary palette",
    "papercraft": "layered paper cutout, flat lighting, tactile edges",
}


class LocalDiffusionIllustrator:
    def __init__(self) -> None:
        self.client = DiffusionClient(model_name="picturebook-sdxl-lite")

    def illustrate(self, page: PageDraft, settings: Settings) -> str:
        style = STYLE_PRESETS.get(settings.illustration_style, STYLE_PRESETS["watercolor"])
        prompt = scrub_prompt(f"{page.text} — {style}")
        out_dir = project_scratch_dir(f"page-{page.index:02d}")
        out_path = out_dir / "illustration.png"
        self.client.sample(prompt=prompt, seed=settings.extras.get("seed", 6767),
                           out_path=out_path)
        log.info("illustrated page %02d -> %s", page.index, out_path.name)
        return str(out_path)