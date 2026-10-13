from bookstudio.core.registry import ModuleSpec


def register(registry) -> None:
    from bookstudio.features.illustration.diffusion_local import LocalDiffusionIllustrator
    registry.register(ModuleSpec(
        name="diffusion-local", capability="illustration",
        factory=LocalDiffusionIllustrator, priority=10,
    ))