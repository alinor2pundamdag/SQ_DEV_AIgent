# Architecture

## Runtime components
- `cli.py`: command parsing and user-visible operations.
- `core.py`: project inventory, local model invocation, public GitHub search, public web/official-documentation search, patch validation/preflight, backups, and supervised patch application.
- `systems.py`: the 12 named core systems, 7 linked-file helpers, security redaction, requirement checklist, and shared checkpoints.
- `workflow.py`: bounded task → proposal → human approval → test → diagnosis loop; no more than three proposals.
- `skills/catalog.json`: canonical 100-skill catalog.
- `install.sh`: installs a durable copy under `~/.local/share/sq-dev-aigent/app` and a global launcher under `~/.local/bin/ai`.

## Shared state and installation
Checkpoints and generated patch proposals are stored under `~/.local/share/sq-dev-aigent`, outside project repositories. Checkpoints store task metadata, phase, timestamps, and limited redacted results—not project source files. Project checkpoints are keyed by canonical root path.

## Execution boundaries
Model output is untrusted. It may propose a unified diff, but it is never executed as a shell command. The patch is path-validated and preflighted with `git apply --check`; target paths and a preview are shown; existing files are backed up; application requires typing `APPLY`. Test/build commands are typed by the user and require typing `RUN`. A failed test can trigger another model proposal only after typing `REPAIR`, with at most three total proposals.

## File boundaries
Inventory excludes hidden directories, common dependency/build directories, common environment-secret filenames, symlinks, unsupported extensions, and oversized files. The workflow includes only a small set of supported text files and applies basic secret-pattern redaction. These filters are best-effort and are not a security sandbox; review sensitive projects before using any model.

Patch paths reject absolute paths, parent traversal, symlink components, and quoted paths that cannot be safely interpreted by the simple parser. New/deleted-file patches are supported through `/dev/null` markers. Existing target files are copied under `.sqai-backups/<unique timestamp>/` before applying.

## Model runtime
The CLI expects an executable compatible with `llama-completion -m MODEL -p PROMPT -n TOKENS --temp 0.2`. Local model execution is capped at 180 seconds. Verify the installed binary's help output on the target device; no model or dependency is downloaded automatically.

## Deliberate limitations
- The Android link map uses filename heuristics, not full IDE semantic indexing.
- Web research returns public search-result snippets; it does not itself verify the full source page, license, or version compatibility. Treat results as untrusted.
- Resume restarts a saved task after confirmation; it does not replay arbitrary shell history.
- No unattended code changes, automatic dependency installation, deployment, APK installation, secret retrieval, or unbounded repair loops.
- CI success does not establish AndroidIDE device compatibility. Device-side tests remain a separate acceptance gate.
