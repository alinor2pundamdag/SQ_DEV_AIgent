# Project Status

Last updated: 2026-10-15

## Confirmed repository baseline
- Repository: `alinor2pundamdag/SQ_DEV_AIgent`
- Default branch: `main`
- Target: local-first coding assistant for AndroidIDE Terminal, designed to be portable to other terminals.
- Runtime: Python/Bash, local llama.cpp and Qwen2.5-Coder GGUF.
- Global command: `ai`.
- Shared install: `~/.local/share/sq-dev-aigent/app`.
- Shared state: `~/.local/share/sq-dev-aigent/checkpoints` and `proposals`.

## Added to GitHub
- CLI: doctor, inspect, plan, ask, research, diff, apply, test, workflow, resume, systems, skills.
- Named 12 core systems and 7 linked-file systems.
- Canonical catalog of 100 uniquely identified skills.
- Bounded workflow: proposal → explicit patch approval → exact user-approved test/build command → evidence-based result; at most three proposals.
- Shared project-scoped checkpoints and explicit resume confirmation.
- Patch preflight, symlink/traversal checks, existing-file backups, local-model timeout, redacted test output.
- Unit/integration tests for paths, symlink rejection, checkpoint isolation, redaction, repair limit, catalog size, public search parsing, and approved patch application.
- CI catalog validation and installer smoke test.
- Durable shared installer that should remain usable after the checkout is moved or removed.
- Master blueprint, architecture, AndroidIDE setup, roadmap, and updated README.

## Current verification state
- GitHub writes succeeded for the implementation and test commits listed in repository history.
- GitHub Actions acceptance run #53 completed successfully on the PR merge ref: Python 3.8 and 3.11 both passed module compilation, all 17 unit tests, 100-skill catalog validation, installer syntax, and the shared-install smoke test.
- Python 3.6.15 was unavailable on the Ubuntu 24.04 hosted runner; the CI matrix now uses 3.8 and 3.11. Python 3.6.9 compatibility remains a device-side acceptance gate.
- AndroidIDE device tests have not been run from this session.
- The earlier reported device runtime paths remain un-reprobed:
  - Model: `/home/test/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf`
  - llama.cpp: `/home/test/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion`
- Local model CLI flags and Python 3.6.9 behavior still require on-device confirmation.
- Android Link Map is heuristic, not a full dependency/semantic index.
- Research supports GitHub repository search, public web snippets, and filtering to an allowlist of official documentation hosts. Full-page source, version, compatibility, and license verification is not automated.

## Next acceptance gates
1. Re-run CI against the current main-branch implementation after the latest code changes.
2. Test in AndroidIDE with the existing Python 3.6.9 runtime and installed llama.cpp binary.
3. Run the workflow on a disposable Git repository and verify apply, backup, test failure, bounded repair, resume, and cancellation behavior.
4. Update this file only with actual observed results.
