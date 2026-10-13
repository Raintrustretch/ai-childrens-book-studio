from bookstudio.core.registry import ModuleSpec


def register(registry) -> None:
    from bookstudio.features.story.local_llm import LocalLLMStoryEngine
    registry.register(ModuleSpec(
        name="local-llm", capability="story",
        factory=LocalLLMStoryEngine, priority=10,
    ))