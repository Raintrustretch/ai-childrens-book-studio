# Contributing to ai-childrens-book-studio

Thanks for wanting to help build the picture-book engine.

## Ground rules

- Every pipeline stage is a **feature module** under
  `src/bookstudio/features/<stage>/`. Register it in that package's
  `__init__.py` via `register(registry)`.
- Do not call another stage directly. Resolve it through
  `PluginRegistry.resolve(capability, name)`.
- Child-safe output is non-negotiable. Any new text or art backend must
  pass `bookstudio.utils.safety.scrub_prompt` before sampling.
- Keep the desktop shell (`bookstudio.ui`) free of pipeline logic.

## Adding a backend

1. Create `features/<stage>/<backend_name>.py`.
2. Implement the stage interface (`outline`/`write_page`, `illustrate`,
   `assemble`, `to_pdf`).
3. Register it with a `ModuleSpec` and a priority.
4. Add a stub-based test in `tests/` so CI runs without GPU or model
   downloads.

## Running locally

```
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
python -m bookstudio --headless --project examples/sample.bkproj
```

## Code style

- `ruff check src tests` must pass.
- 92-column lines, type hints on all public functions.
- No new global mutable state.