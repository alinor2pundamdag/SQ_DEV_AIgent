# Project Status

Last verified: 2026-10-15

## Confirmed baseline
- Repository: `alinor2pundamdag/SQ_DEV_AIgent`
- Default branch: `main`
- Intended target: a local-first coding assistant for AndroidIDE Terminal.
- Intended runtime: Python and Bash, with local llama.cpp / Qwen2.5-Coder integration.
- Intended user command: `ai`, available from project directories.

## Existing device runtime (reported earlier; not re-probed in this commit)
- Model: `/home/test/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf`
- llama.cpp binary: `/home/test/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion`

## Implementation status
This repository is at the initial documentation/bootstrap stage. Do not treat the planned autonomous edit/test/repair loop as implemented until source files, tests, and runtime behavior have been verified.

## Safety and reliability requirements
- Keep changes scoped to the selected project and prefer small diffs.
- Back up files before modifying them.
- Require approval for destructive operations.
- Protect credentials, tokens, and private data.
- Never claim a test or build passed without captured evidence.
- Bound automated repair attempts and report failures honestly.
