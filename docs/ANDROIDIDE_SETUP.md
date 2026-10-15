# AndroidIDE Terminal Setup

This guide is intentionally conservative. It does not download a model or compile llama.cpp.

## 1. Confirm existing runtime
```sh
ls -lh "$HOME/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf"
ls -lh "$HOME/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion"
```
If these files are not present at those paths, stop and locate the existing files rather than reinstalling them.

## 2. Configure paths for this shell
```sh
export SQAI_MODEL="$HOME/sq-dev-ai/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf"
export SQAI_LLAMA="$HOME/sq-dev-ai/runtime/llama.cpp-source/build/bin/llama-completion"
```
To persist, add those exports to the shell profile used by AndroidIDE Terminal. Do not put model files or credentials in Git.

## 3. Install the launcher
From a clean clone of this repository:
```sh
sh install.sh
```
If `~/.local/bin` is not on PATH, add the line printed by the installer to the relevant shell profile and reopen the terminal.

## 4. Verify
```sh
ai doctor
ai inspect .
python -m unittest discover -s tests -v
```

## 5. Use safely
Run `ai plan .` first. Review changes as unified diff files. Use `ai diff patch.diff --root /path/to/project` before `ai apply patch.diff --root /path/to/project`. Applying requires typing `APPLY`. Choose test/build commands yourself; `ai test` asks for confirmation before running the exact command.

## Notes
- Python 3.6+ standard library is enough for runtime commands.
- `setup.py` is optional; the installer avoids package installation.
- Do not run scripts from repositories you have not reviewed.
