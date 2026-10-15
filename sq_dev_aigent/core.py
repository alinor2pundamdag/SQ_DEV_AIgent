from __future__ import print_function
import os
import re
import subprocess
import time
import shutil

SKIP_DIRS = set([".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__", "build", "dist"])
MAX_FILES = 120
MAX_FILE_BYTES = 160000
TEXT_EXTS = set([".py", ".sh", ".bash", ".js", ".ts", ".tsx", ".jsx", ".json", ".toml", ".yaml", ".yml", ".md", ".txt", ".go", ".rs", ".java", ".kt", ".gradle", ".xml", ".properties", ".html", ".css", ".sql", ".c", ".h", ".cpp", ".hpp"])

def safe_root(path):
    root = os.path.realpath(os.path.abspath(path or "."))
    if not os.path.isdir(root):
        raise ValueError("Project root is not a directory: " + root)
    return root

def project_files(root, limit=MAX_FILES):
    root = safe_root(root)
    found = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in sorted(names):
            full = os.path.join(current, name)
            rel = os.path.relpath(full, root)
            if name in (".env", "id_rsa", "id_ed25519", "credentials.json"):
                continue
            if name.startswith(".env."):
                continue
            if os.path.islink(full):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_EXTS and name not in ("Makefile", "Dockerfile", "requirements.txt", "Cargo.lock", "go.mod", "go.sum", "package-lock.json", "gradlew", "gradlew.bat"):
                continue
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            found.append(rel)
            if len(found) >= limit:
                return sorted(found)
    return sorted(found)

def git_output(root, args):
    if not shutil.which("git"):
        return ""
    try:
        p = subprocess.Popen(["git"] + args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        if p.returncode == 0:
            return out.decode("utf-8", "replace").strip()
    except Exception:
        pass
    return ""

def inspect_project(path="."):
    root = safe_root(path)
    files = project_files(root)
    branch = git_output(root, ["branch", "--show-current"])
    commit = git_output(root, ["log", "-1", "--oneline"])
    status = git_output(root, ["status", "--short"])
    lines = ["Project root: " + root, "Tracked context:"]
    lines.append("Git branch: " + (branch or "(not a Git branch)"))
    lines.append("Latest commit: " + (commit or "(unavailable)"))
    lines.append("Working tree: " + ("clean" if not status else "has changes"))
    lines.append("Readable files ({0} shown):".format(len(files)))
    lines.extend(["  " + f for f in files] if files else ["  (no supported text files found)"])
    if len(files) >= MAX_FILES:
        lines.append("Note: file listing is capped at {0}.".format(MAX_FILES))
    return "\n".join(lines)

def run_local_model(prompt, max_tokens=700):
    model = os.environ.get("SQAI_MODEL", "").strip()
    llama = os.environ.get("SQAI_LLAMA", "").strip()
    if not model or not os.path.isfile(model):
        raise RuntimeError("SQAI_MODEL is unset or the model file does not exist.")
    if not llama or not os.path.isfile(llama):
        raise RuntimeError("SQAI_LLAMA is unset or the llama.cpp executable does not exist.")
    command = [llama, "-m", model, "-p", prompt, "-n", str(max_tokens), "--temp", "0.2"]
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = p.communicate(timeout=180)
        except subprocess.TimeoutExpired:
            p.kill()
            out, err = p.communicate()
            raise RuntimeError("Local model timed out after 180 seconds.")
    except OSError as exc:
        raise RuntimeError("Could not start local model: " + str(exc))
    text = out.decode("utf-8", "replace").strip()
    if p.returncode != 0:
        detail = err.decode("utf-8", "replace")[-1500:]
        raise RuntimeError("llama.cpp exited with status {0}: {1}".format(p.returncode, detail))
    return text or "(Model returned no text.)"

def make_plan(path="."):
    context = inspect_project(path)
    prompt = ("You are SQ_DEV_AIgent, a cautious software engineering assistant. "
              "Use only the project inventory below; do not invent files or claim tests ran. "
              "Provide: inferred stack, likely entry points, risks, a prioritized 5-step plan, "
              "and verification commands. Do not propose destructive actions.\n\n" + context)
    try:
        return run_local_model(prompt, 700)
    except RuntimeError as exc:
        return ("Local model unavailable: {0}\n\nSafe starter plan:\n"
                "1. Inspect README and project configuration.\n"
                "2. Identify the entry point and current test/build commands.\n"
                "3. Reproduce the requested issue before editing.\n"
                "4. Propose a small unified diff and review every path.\n"
                "5. Run the selected test/build command and report the actual result.").format(exc)

def research_github(query, limit=5):
    import json
    import urllib.parse
    import urllib.request
    url = "https://api.github.com/search/repositories?q={0}&sort=stars&order=desc&per_page={1}".format(
        urllib.parse.quote(query), max(1, min(int(limit), 10)))
    request = urllib.request.Request(url, headers={"User-Agent": "SQ-DEV-AIgent/0.1", "Accept": "application/vnd.github+json"})
    try:
        response = urllib.request.urlopen(request, timeout=12)
        payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError("GitHub public search failed: " + str(exc))
    results = []
    for item in payload.get("items", []):
        results.append("{0} (★ {1})\n  {2}\n  {3}".format(
            item.get("full_name", "(unknown)"), item.get("stargazers_count", 0),
            item.get("html_url", ""), (item.get("description") or "").replace("\n", " ")[:240]))
    return "\n\n".join(results) if results else "No public repositories found."

def patch_paths(patch_text):
    paths = []
    for line in patch_text.splitlines():
        if line.startswith("--- ") or line.startswith("+++ "):
            value = line[4:].split("\t", 1)[0].strip()
            if value == "/dev/null":
                continue
            if value.startswith('"') or value.endswith('"'):
                raise ValueError("Quoted patch paths are unsupported; use simple relative paths.")
            if value.startswith("a/") or value.startswith("b/"):
                value = value[2:]
            paths.append(value)
    return sorted(set(paths))

def validate_patch_paths(root, paths):
    root = safe_root(root)
    if not paths:
        raise ValueError("Patch contains no recognizable file paths.")
    for rel in paths:
        if not rel or os.path.isabs(rel) or rel == ".." or rel.startswith("../") or "/../" in rel or rel.startswith("~"):
            raise ValueError("Unsafe patch path rejected: " + rel)
        joined = os.path.abspath(os.path.join(root, rel))
        target = os.path.realpath(joined)
        if target != root and not target.startswith(root + os.sep):
            raise ValueError("Patch escapes selected project root: " + rel)
        # Reject symlinks in every existing component, not only the final target.
        cursor = root
        for part in rel.split(os.sep):
            if part in ("", "."):
                continue
            cursor = os.path.join(cursor, part)
            if os.path.islink(cursor):
                raise ValueError("Symlink patch path rejected: " + rel)
    return root

def backup_existing(root, paths):
    stamp = time.strftime("%Y%m%d-%H%M%S") + "-{0}".format(int(time.time() * 1000) % 1000000)
    backup_root = os.path.join(root, ".sqai-backups", stamp)
    copied = []
    for rel in paths:
        source = os.path.join(root, rel)
        if os.path.isfile(source):
            dest = os.path.join(backup_root, rel)
            parent = os.path.dirname(dest)
            if not os.path.isdir(parent):
                os.makedirs(parent)
            shutil.copy2(source, dest)
            copied.append(os.path.relpath(dest, root))
    return copied

def apply_patch(path, root="."):
    root = safe_root(root)
    patch_file = os.path.realpath(os.path.abspath(path))
    if not os.path.isfile(patch_file):
        raise ValueError("Patch file does not exist: " + patch_file)
    with open(patch_file, "r") as stream:
        patch_text = stream.read()
    paths = patch_paths(patch_text)
    validate_patch_paths(root, paths)
    if not shutil.which("git"):
        raise RuntimeError("Git is required for applying unified diffs.")
    if not git_output(root, ["rev-parse", "--show-toplevel"]):
        raise RuntimeError("Selected project root is not inside a Git repository. Refusing to apply.")
    check = subprocess.Popen(["git", "apply", "--check", patch_file], cwd=root,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check_out, check_err = check.communicate()
    if check.returncode != 0:
        detail = check_err.decode("utf-8", "replace")[-2000:]
        raise RuntimeError("Patch does not apply cleanly; no files changed: " + detail)
    print("Patch targets:")
    for rel in paths:
        print("  " + rel)
    answer = input("Apply this patch to the selected project? Type APPLY to confirm: ").strip()
    if answer != "APPLY":
        print("Cancelled; no files changed.")
        return 1
    backups = backup_existing(root, paths)
    command = ["git", "apply", "--whitespace=nowarn", patch_file]
    p = subprocess.Popen(command, cwd=root)
    code = p.wait()
    if code != 0:
        print("git apply failed (exit {0}). Backups, if any, are in .sqai-backups.".format(code))
        return code
    print("Patch applied. Backup copies: {0}".format(", ".join(backups) if backups else "(new files only)"))
    print("Review with: git diff --check && git diff")
    print("No tests were run automatically.")
    return 0
