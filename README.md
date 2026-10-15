# SQ_DEV_AIgent

Local-first AI coding assistant for AndroidIDE Terminal, designed to use a local Qwen2.5-Coder GGUF model through llama.cpp and expose a global `ai` command.

## Implemented in this foundation
- `ai doctor`: inspect runtime configuration.
- `ai inspect [path]`: read-only project inventory and Git summary.
- `ai plan [path]`: request a plan from the local model, with a safe fallback checklist.
- `ai ask <question>`: ask the configured local model.
- `ai research <query>`: search public GitHub repositories using HTTPS.
- `ai diff <patch-file>`: validate paths and list patch targets without applying changes.
- `ai apply <patch-file>`: validate paths, back up existing target files, and apply only after typing `APPLY`.
- `ai test`: run a user-entered test/build command only after typing `RUN`.

This is a supervised foundation, not yet a fully autonomous self-healing agent. Device-side compatibility and end-to-end tests are still pending.

## Requirements
- Python 3.6+ (standard library only)
- Git (required for applying patches; optional for inspection)
- llama.cpp `llama-completion` (optional, for local model use)
- A local GGUF model file (optional)

## Quick start
From the repository directory:
```sh
sh install.sh
ai doctor
ai inspect .
ai plan .
ai ask "Explain the current project structure"
```
The installer adds a launcher to `~/.local/bin/ai`. If that directory is not on PATH, add it to your shell PATH. Installation does not download models or change project files.

## Configure the model
```sh
export SQAI_MODEL="$HOME/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf"
export SQAI_LLAMA="$HOME/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion"
```
Persist these exports in the shell profile used by AndroidIDE Terminal if desired. Never put secrets, access tokens, or model weights in this repository.

## Safety
- Model-generated text is never executed as a shell command.
- Code changes must be provided as a unified diff and require explicit confirmation.
- Patch paths reject absolute paths and parent traversal; symlink targets are rejected.
- Existing files touched by a patch are backed up under `.sqai-backups/<timestamp>/`.
- Test/build commands are selected by the user and require confirmation.
- No automatic package installation, deployment, APK installation, or unbounded repair attempts.

## Development
```sh
python -m unittest discover -s tests -v
python -m py_compile sq_dev_aigent/*.py
```

See [AndroidIDE setup](docs/ANDROIDIDE_SETUP.md), [architecture](docs/ARCHITECTURE.md), and [roadmap](docs/ROADMAP.md).
