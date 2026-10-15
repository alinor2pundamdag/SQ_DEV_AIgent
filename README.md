# SQ_DEV_AIgent

Local-first coding assistant for AndroidIDE Terminal, designed around a local Qwen2.5-Coder GGUF model through llama.cpp and a global `ai` command. The shared install and checkpoint memory live in the user's home directory, so the launcher can be used across project folders and does not depend on the original checkout remaining in place.

## Current capabilities
- `ai doctor`: inspect Python, Git, and local model configuration.
- `ai inspect [path]`: read-only project inventory and Git summary.
- `ai plan [path]`: request a plan from the local model, with a safe fallback checklist.
- `ai ask <question>`: ask the configured local model.
- `ai research <query>`: search public GitHub repositories over HTTPS.
- `ai research <query> --web`: search public web result snippets.
- `ai research <query> --official`: search and filter results to a built-in allowlist of official documentation hosts. Search snippets are untrusted; verify source pages, versions, compatibility, and licenses before reusing code.
- `ai diff <patch-file> --root <project>`: validate patch paths and show a preview.
- `ai apply <patch-file> --root <project>`: preflight a patch, show targets, back up existing files, and apply only after typing `APPLY`.
- `ai test`: run a user-entered test/build command only after typing `RUN`.
- `ai workflow <goal> --root <project>`: bounded proposal → approval → test → diagnosis workflow; maximum three proposals, each patch is individually approved.
- `ai resume --root <project>`: inspect a saved checkpoint and restart the task only after typing `RESUME`.
- `ai systems`: list the 12 core systems and 7 linked-file systems.
- `ai skills`: validate the canonical catalog of 100 unique skills; `ai skills --list` lists them.

This is an approval-gated coding assistant, not an unattended self-modifying agent. Model-generated shell commands are never executed. Test/build commands must be typed and approved by the user. Model output, repository text, and test output are treated as untrusted data.

## Requirements
- Python 3.6+ standard library
- Git (required for patch preflight/application; optional for inspection)
- llama.cpp executable compatible with `llama-completion` flags (optional)
- Local GGUF model file (optional)

## Install a shared, persistent copy
From the repository checkout:
```sh
sh install.sh
ai doctor
ai systems
ai skills
ai inspect .
```
The installer copies the package and skill catalog to `~/.local/share/sq-dev-aigent/app` and installs `~/.local/bin/ai`. The command therefore remains available if the original checkout is moved or removed. If `~/.local/bin` is not on PATH, add it to the shell profile used by AndroidIDE Terminal.

## Configure the local model
```sh
export SQAI_MODEL="$HOME/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf"
export SQAI_LLAMA="$HOME/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion"
```
Persist these exports in the AndroidIDE Terminal shell profile if desired. Verify paths and CLI flags on the device before relying on model features. Never commit model weights, credentials, or private project data.

## Safe workflow example
```sh
ai inspect .
ai plan .
ai workflow "Fix the failing tests without changing unrelated behavior" --root .
```
The workflow asks for the exact test/build command first. It proposes a unified diff, shows target paths and likely related files, and requires `APPLY` before each patch. The exact test/build command requires `RUN`. A failed test may lead to another proposal only after typing `REPAIR`, with at most three attempts. Stop any time by declining a confirmation.

## Development checks
```sh
python -m py_compile sq_dev_aigent/*.py
python -m unittest discover -s tests -v
sh -n install.sh
sh tests/test_installer.sh
```
GitHub Actions runs compilation, unit tests, catalog validation, installer syntax, and a shared-install smoke test. The workflow can also be started from GitHub Actions → Validate foundation → Run workflow. Check the run result; repository commits alone do not prove CI passed.

See [master blueprint](docs/MASTER_BLUEPRINT.md), [AndroidIDE setup](docs/ANDROIDIDE_SETUP.md), [architecture](docs/ARCHITECTURE.md), [roadmap](docs/ROADMAP.md), and [project status](docs/PROJECT_STATUS.md).
