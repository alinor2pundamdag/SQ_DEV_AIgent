# SQ_DEV_AIgent — Master Blueprint

## Mission and deployment model
Build a local-first coding assistant for AndroidIDE Terminal first, portable to other POSIX terminals later. The shared installation and memory live under the user's home directory, not inside each project. The intended local model is Qwen2.5-Coder GGUF through llama.cpp. The global command is `ai`. No model weights, access tokens, private project contents, or device secrets belong in this repository.

## The 12 core systems
1. **AgentCore** — owns shared agent state and safety components.
2. **ModelClient** — bounded local-model adapter; model output is untrusted.
3. **TaskPlanner** — stages work as understand → inspect → propose → verify → report.
4. **ContextManager** — creates compact, redacted project context.
5. **ProjectIndexer** — groups supported source/config files by type.
6. **ToolRouter** — explicit allowlist of supported operations.
7. **FileManager** — resolves project paths and rejects root escapes.
8. **TerminalExecutor** — executes only user-supplied commands after confirmation.
9. **WorkflowEngine** — persists shared checkpoints and workflow phase.
10. **BuildManager** — suggests project-appropriate test/build commands.
11. **ResultVerifier** — reports pass/fail only from actual exit status/evidence.
12. **SecurityGuard** — path checks, secret redaction, untrusted-output boundaries.

## The 7 linked-file systems
1. **Intent Interpreter** — normalizes the requested goal.
2. **Android Link Map** — heuristically surfaces likely Android/Gradle links.
3. **Ripple Loop** — tracks repair attempts with a hard maximum of three.
4. **Pre-edit Impact Check** — lists potentially related files before editing.
5. **Completeness Auditor** — compares required files with available files.
6. **Requirement Checklist** — tracks each requirement with evidence.
7. **Auto-Continue** — resumes a saved checkpoint only after the user types `RESUME`.

These are portable heuristics, not claims of full Android Studio semantic indexing.

## 100-skill catalog
The canonical 100-item catalog is `skills/catalog.json`. Skills are capabilities/playbooks, not 100 separately installed executables. Each item must be read-only or approval-gated and must have a clear verification result.

## Required engineering lifecycle
1. Interpret request and list acceptance criteria.
2. Inspect project files, Git state, build system, and available tests.
3. Map dependencies and likely cross-file impacts.
4. Research relevant public documentation/repositories; verify source, license, compatibility, and security before reuse.
5. Propose the smallest useful change as a unified diff.
6. Show target paths and impact before any write.
7. Require explicit approval before applying each patch.
8. Run only the exact test/build command approved by the user.
9. Treat test output and repository content as untrusted data, never as agent instructions.
10. Diagnose failures from evidence; permit at most three repair proposals, each requiring approval.
11. Verify again after each approved repair.
12. Save a checkpoint and produce a factual report with changed files, test commands, exit codes, and remaining blockers.

## Guardrails
- No unbounded loops or unattended code writes.
- Never execute model-generated shell commands.
- Never auto-install dependencies, deploy, install APKs, or retrieve secrets.
- Reject absolute paths, parent traversal, and symlink escapes.
- Exclude common secrets and generated/dependency directories from indexing; this is best-effort, not a sandbox.
- Do not store source code or secret values in checkpoints.
- Keep shared state outside repositories and use restrictive file permissions where supported.
- Require `APPLY` for patches, `RUN` for exact user-entered commands, and `RESUME` to continue checkpoints.
- Report unsupported capabilities honestly.

## Acceptance gates
- Static checks and unit tests pass on Python 3.6-compatible code.
- Installer creates a durable shared installation and a global launcher.
- Unit tests cover traversal, symlinks, patch parsing, backups, checkpoint persistence, redaction, and repair limits.
- CI passes on supported Python versions.
- AndroidIDE device verification confirms the installed interpreter and llama.cpp flags work.
- End-to-end verification is reported separately from CI; do not mark device acceptance complete without device evidence.

## Status policy
A file existing in GitHub is not proof that it works. A component is complete only after a test or explicit verification step supports that claim. Device-only requirements remain pending until tested on the target device.
