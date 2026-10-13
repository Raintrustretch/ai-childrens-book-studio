"""Packaged defaults. Anything not overridden by the user lands here."""

DEFAULT_SETTINGS: dict = {
    "text_backend": "local-llm",
    "art_backend": "diffusion-local",
    "target_age_band": "3-5",
    "page_count": 24,
    "rhyme_scheme": "AABB",
    "illustration_style": "watercolor",
    "safety_filter": "child-safe-strict",
    "extras": {
        "llm_model": "storyteller-3b-q4_k_m",
        "diffusion_model": "picturebook-sdxl-lite",
        "max_tokens_per_page": 90,
        "seed": 6767,
    },
}