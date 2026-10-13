"""Local diffusion sampler adapter (diffusers backend, CPU or CUDA)."""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("bookstudio.diffusion")


class DiffusionClient:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._pipe = None

    def _ensure_loaded(self) -> None:
        if self._pipe is not None:
            return
        from diffusers import StableDiffusionXLPipeline  # type: ignore
        import torch  # type: ignore
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._pipe = StableDiffusionXLPipeline.from_pretrained(
            self.model_name, torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)

    def sample(self, prompt: str, seed: int, out_path: Path) -> Path:
        self._ensure_loaded()
        import torch  # type: ignore
        generator = torch.Generator(device="cpu").manual_seed(seed)
        image = self._pipe(prompt, generator=generator, num_inference_steps=24).images[0]
        image.save(out_path)
        return out_path