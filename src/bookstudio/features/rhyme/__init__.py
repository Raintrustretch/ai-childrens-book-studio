from bookstudio.core.registry import ModuleSpec


def register(registry) -> None:
    from bookstudio.features.rhyme.aabb import AABBChecker
    registry.register(ModuleSpec(
        name="AABB", capability="rhyme", factory=AABBChecker, priority=10,
    ))