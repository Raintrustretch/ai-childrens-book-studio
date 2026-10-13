"""Thin wrapper over a local llama.cpp runtime.

Kept deliberately dumb: one method, one model handle, no retries beyond
a single cold-start reload. If the runtime is missing, we raise a typed
error the UI can surface as a setup prompt rather than a crash.
"""

from __future__ import annotations

import logging

log = logging.getLogger("bookstudio.llm")


class LLMUnavailable(RuntimeError):
    pass


class LocalLLMClient:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._handle = None

    def _ensure_loaded(self) -> None:
        if self._handle is not None:
            return
        try:
            import llama_cpp  # type: ignore
        except ImportError as exc:
            raise LLMUnavailable(
                "llama-cpp-python not installed; run `pip install llama-cpp-python`"
            ) from exc
        self._handle = llama_cpp.Llama(model_path=self.model_name, n_ctx=4096)

    def complete(self, prompt: str, max_tokens: int = 256) -> str:
        self._ensure_loaded()
        out = self._handle(prompt, max_tokens=max_tokens, temperature=0.8)
        return out["choices"][0]["text"]