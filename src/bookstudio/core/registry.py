"""Feature-module registry.

Every stage of the book pipeline registers itself by name and capability
tag. The registry is what lets ``text``, ``rhyme``, ``art``, and
``layout`` be swapped independently without the pipeline knowing their
concrete classes.
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from dataclasses import dataclass
from typing import Callable, Iterable

log = logging.getLogger("bookstudio.registry")

CAPABILITIES = ("story", "rhyme", "illustration", "layout", "export")


@dataclass(frozen=True)
class ModuleSpec:
    name: str
    capability: str
    factory: Callable[[], object]
    priority: int = 100


class PluginRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, ModuleSpec] = {}

    def register(self, spec: ModuleSpec) -> None:
        if spec.capability not in CAPABILITIES:
            raise ValueError(f"unknown capability: {spec.capability}")
        self._modules[spec.name] = spec

    def modules(self, capability: str | None = None) -> Iterable[ModuleSpec]:
        specs = sorted(self._modules.values(), key=lambda s: s.priority)
        if capability is None:
            return specs
        return [s for s in specs if s.capability == capability]

    def resolve(self, capability: str, name: str | None = None) -> ModuleSpec:
        candidates = list(self.modules(capability))
        if not candidates:
            raise LookupError(f"no module registered for {capability!r}")
        if name is None:
            return candidates[0]
        for spec in candidates:
            if spec.name == name:
                return spec
        raise LookupError(f"{capability!r} module {name!r} not found")

    @classmethod
    def discover(cls) -> "PluginRegistry":
        registry = cls()
        package = importlib.import_module("bookstudio.features")
        for info in pkgutil.iter_modules(package.__path__):
            mod = importlib.import_module(f"bookstudio.features.{info.name}")
            register = getattr(mod, "register", None)
            if callable(register):
                register(registry)
                log.debug("registered feature module %s", info.name)
        return registry