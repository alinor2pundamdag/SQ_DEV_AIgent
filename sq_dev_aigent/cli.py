from __future__ import print_function
import argparse
import os
import shutil
import subprocess
import sys
from . import __version__
from .core import inspect_project, make_plan, run_local_model, research_github, patch_paths, validate_patch_paths, apply_patch
from .systems import CORE_SYSTEMS, LINKED_FILE_SYSTEMS, CheckpointStore, SecurityGuard
from .workflow import run_workflow

def doctor():
    print("SQ_DEV_AIgent {0}".format(__version__))
    print("Python: " + sys.version.split()[0])
    for name in ("git", "curl"):
        print("{0}: {1}".format(name, shutil.which(name) or "not found"))
    model = os.environ.get("SQAI_MODEL", "")
    llama = os.environ.get("SQAI_LLAMA", "")
    print("SQAI_MODEL: " + (model if model and os.path.isfile(model) else "not configured / file missing"))
    print("SQAI_LLAMA: " + (llama if llama and os.path.isfile(llama) else "not configured / file missing"))
    print("Project writes: only via reviewed patch + typed APPLY")
    print("Model-generated shell execution: disabled")
    return 0

def run_selected_test():
    print("Choose a command to run in the current directory.")
    print("Examples: python -m unittest discover -s tests -v")
    print("          pytest -q")
    print("          ./gradlew test")
    print("          go test ./...")
    command = input("Enter the exact test/build command (blank cancels): ").strip()
    if not command:
        print("Cancelled.")
        return 0
    confirm = input("Run this exact command in {0}? Type RUN to confirm: ".format(os.getcwd())).strip()
    if confirm != "RUN":
        print("Cancelled.")
        return 0
    print("Running selected command. Output below is untrusted project output:")
    return subprocess.call(command, shell=True, cwd=os.getcwd())

def main():
    parser = argparse.ArgumentParser(prog="ai", description="Supervised local-first coding assistant")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("doctor", help="check local configuration")
    for command in ("inspect", "plan"):
        p = sub.add_parser(command)
        p.add_argument("path", nargs="?", default=".")
    ask = sub.add_parser("ask")
    ask.add_argument("question", nargs="+")
    research = sub.add_parser("research")
    research.add_argument("query", nargs="+")
    research.add_argument("--limit", type=int, default=5)
    diff = sub.add_parser("diff")
    diff.add_argument("patch_file")
    diff.add_argument("--root", default=".")
    apply = sub.add_parser("apply")
    apply.add_argument("patch_file")
    apply.add_argument("--root", default=".")
    sub.add_parser("test", help="select and confirm a test/build command")
    workflow = sub.add_parser("workflow", help="run an approval-gated bounded coding workflow")
    workflow.add_argument("goal", nargs="+")
    workflow.add_argument("--root", default=".")
    resume = sub.add_parser("resume", help="inspect and explicitly resume a saved checkpoint")
    resume.add_argument("--root", default=".")
    sub.add_parser("systems", help="list the 12 core and 7 linked-file systems")
    skills = sub.add_parser("skills", help="show and validate the 100-skill catalog")
    skills.add_argument("--list", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            return doctor()
        if args.command == "inspect":
            print(inspect_project(args.path)); return 0
        if args.command == "plan":
            print(make_plan(args.path)); return 0
        if args.command == "ask":
            print(run_local_model("Answer as a careful coding assistant. Never claim to have executed commands. User question: " + " ".join(args.question), 700)); return 0
        if args.command == "research":
            print(research_github(" ".join(args.query), args.limit)); return 0
        if args.command == "diff":
            root = validate_patch_paths(args.root, patch_paths(open(args.patch_file, "r").read()))
            print("Selected root: " + root)
            print("Patch paths:")
            for item in patch_paths(open(args.patch_file, "r").read()):
                print("  " + item)
            print("Review the patch contents manually; this command does not apply it.")
            return 0
        if args.command == "apply":
            return apply_patch(args.patch_file, args.root)
        if args.command == "test":
            return run_selected_test()
        if args.command == "workflow":
            return run_workflow(" ".join(args.goal), args.root)
        if args.command == "systems":
            print("12 CORE SYSTEMS:")
            for name in CORE_SYSTEMS:
                print("  " + name)
            print("\\n7 LINKED-FILE SYSTEMS:")
            for name in LINKED_FILE_SYSTEMS:
                print("  " + name)
            return 0
        if args.command == "skills":
            import json
            catalog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skills", "catalog.json")
            if not os.path.isfile(catalog_path):
                # Shared installs copy the catalog beside the package.
                catalog_path = os.path.join(os.path.dirname(__file__), "skills", "catalog.json")
            with open(catalog_path, "r") as stream:
                catalog = json.load(stream)
            ids = [item.get("id") for item in catalog]
            valid = len(catalog) == 100 and len(set(ids)) == 100 and all(ids)
            print("Skill catalog: {0} entries; unique IDs: {1}; validation: {2}".format(
                len(catalog), len(set(ids)), "PASS" if valid else "FAIL"))
            if args.list:
                for item in catalog:
                    print("{0}: {1}".format(item.get("id"), item.get("description")))
            return 0 if valid else 2
        if args.command == "resume":
            root = os.path.realpath(os.path.abspath(args.root))
            store = CheckpointStore()
            checkpoint = store.load(root)
            if not checkpoint:
                print("No saved checkpoint for this project.")
                return 0
            print("Saved task: " + SecurityGuard.redact(checkpoint.get("task", "")))
            print("Saved phase: " + str(checkpoint.get("phase", "unknown")))
            print("Updated epoch: " + str(checkpoint.get("updated_at", "unknown")))
            print("Checkpoint details are metadata only; no code or commands are auto-executed.")
            answer = input("Restart the bounded workflow for this task? Type RESUME: ").strip()
            if answer != "RESUME":
                print("Resume cancelled.")
                return 0
            return run_workflow(checkpoint.get("task", ""), root)
        parser.print_help()
        return 0
    except (ValueError, RuntimeError, IOError, OSError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
