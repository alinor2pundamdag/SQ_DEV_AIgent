# Project Status

Last updated: 2026-10-15

## Confirmed baseline
- Repository: `alinor2pundamdag/SQ_DEV_AIgent`
- Default branch: `main`
- Target: local-first coding assistant for AndroidIDE Terminal.
- Runtime target: Python/Bash, local llama.cpp and Qwen2.5-Coder GGUF.
- User command: global `ai`.

## Existing device runtime (reported earlier; not re-probed here)
- Model: `/home/test/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf`
- llama.cpp binary: `/home/test/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion`

## Added to GitHub
- CLI commands: doctor, inspect, plan, ask, research, diff, apply, test.
- Local model invocation with environment-variable configuration.
- Read-only project inventory with common secret and generated-directory exclusions.
- Patch path validation, existing-file backups, and typed apply confirmation.
- User-entered test/build command with typed run confirmation.
- Unit tests for path validation and project inventory.
- AndroidIDE setup, architecture, roadmap, and MIT license documentation.

## Not yet verified
- Unit tests on AndroidIDE's Python 3.6.9 runtime.
- Compatibility of local llama.cpp flags with the installed binary.
- End-to-end patch application and backup workflow on device.
- Fully autonomous bounded repair loop; this is not implemented yet.
- The GitHub files have been committed, but their runtime behavior must still be tested before installation is recommended.
