# Architecture

## Components
- `cli.py`: command parsing and user-visible operations.
- `core.py`: project inventory, local model invocation, public GitHub search, patch path checks, backups, and supervised patch application.
- `install.sh`: installs a launcher in `~/.local/bin`; no model downloads.

## Execution boundaries
The model can provide text, plans, and proposed edits, but model output is never passed to a shell. Applying code requires a separate patch file and the exact confirmation word `APPLY`. Test/build commands are typed by the user and require `RUN`.

## File boundaries
Project inventory excludes hidden directories, common dependency/build directories, common environment-secret filenames, symlinks, unsupported extensions, and oversized files. This is a best-effort filter, not a security sandbox.

Patch paths reject absolute paths, parent traversal, and symlink targets. Existing files are copied under `.sqai-backups/<timestamp>/` before `git apply`. Keep backups out of public commits.

## Model runtime
The CLI expects an executable compatible with llama.cpp's `llama-completion` options: `-m MODEL -p PROMPT -n TOKENS --temp 0.2`. Verify the installed binary's help if flags differ.

## Deliberate non-goals
No unattended code changes, auto-installing dependencies, automatic deployment, secret retrieval, APK installation, or unbounded repair loops. A later version may add bounded orchestration only after separate tests and approval gates.
