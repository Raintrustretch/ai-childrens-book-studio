# Security Policy

## Scope

ai-childrens-book-studio runs **fully offline** by default. It loads
local GGUF and diffusers models from `%LOCALAPPDATA%\AIBChildrensBookStudio\models`.
No telemetry, no network calls, no cloud upload of a child's premise or
generated art.

## Reporting a vulnerability

Open a private security advisory on the GitHub repo, or email the
maintainer listed in `pyproject.toml`. Please include:

- the affected version (`bookstudio.version.__version__`)
- a minimal `.bkproj` that reproduces the issue
- the OS build and Python version

We aim to acknowledge within 72 hours.

## Model supply chain

Only load model files from the app's model cache directory. A malicious
GGUF or safetensors file can execute arbitrary code through the loader;
verify hashes before first load.

## Known non-issues

- The safety scrubber is a denylist, not a classifier. It is a
  first-pass filter, not a guarantee. Human review of generated pages
  is expected before publishing.