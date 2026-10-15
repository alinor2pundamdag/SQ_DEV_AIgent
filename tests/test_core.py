import json
import os
import tempfile
import unittest
import subprocess
from unittest.mock import patch as mock_patch
from sq_dev_aigent.core import patch_paths, validate_patch_paths, project_files, safe_root, _SearchResultParser
from sq_dev_aigent.systems import (CheckpointStore, SecurityGuard, RippleLoop,
                                   RequirementChecklist, CORE_SYSTEMS, LINKED_FILE_SYSTEMS,
                                   AutoContinue)

class CoreTests(unittest.TestCase):
    def test_patch_paths(self):
        patch = "--- a/src/main.py\n+++ b/src/main.py\n@@ -1 +1 @@\n-a\n+b\n"
        self.assertEqual(patch_paths(patch), ["src/main.py"])

    def test_new_and_deleted_file_paths(self):
        new_patch = "--- /dev/null\n+++ b/src/new.py\n@@ -0,0 +1 @@\n+new\n"
        delete_patch = "--- a/src/old.py\n+++ /dev/null\n@@ -1 +0,0 @@\n-old\n"
        self.assertEqual(patch_paths(new_patch), ["src/new.py"])
        self.assertEqual(patch_paths(delete_patch), ["src/old.py"])

    def test_reject_quoted_patch_paths(self):
        patch = '--- "a/file name.txt"\\n+++ "b/file name.txt"\\n'
        with self.assertRaises(ValueError):
            patch_paths(patch)

    def test_reject_parent_path(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                validate_patch_paths(root, ["../outside.txt"])

    def test_reject_absolute_path(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                validate_patch_paths(root, [os.path.abspath(os.path.join(root, "x"))])

    def test_reject_symlink_path_component(self):
        with tempfile.TemporaryDirectory() as root:
            target = os.path.join(root, "real")
            os.mkdir(target)
            link = os.path.join(root, "link")
            os.symlink(target, link)
            with self.assertRaises(ValueError):
                validate_patch_paths(root, ["link/new.py"])

    def test_project_inventory(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "README.md"), "w") as stream:
                stream.write("hello")
            with open(os.path.join(root, ".env"), "w") as stream:
                stream.write("TOKEN=never-list")
            self.assertIn("README.md", project_files(root))
            self.assertNotIn(".env", project_files(root))

    def test_root_must_exist(self):
        with self.assertRaises(ValueError):
            safe_root("/this/path/should/not/exist/sqai-test")

    def test_shared_checkpoint_is_project_scoped(self):
        with tempfile.TemporaryDirectory() as base:
            with tempfile.TemporaryDirectory() as project:
                store = CheckpointStore(base)
                store.save(project, "finish tests", "verification", {"attempt": 1})
                checkpoint = store.load(project)
                self.assertEqual(checkpoint["task"], "finish tests")
                self.assertEqual(checkpoint["phase"], "verification")
                self.assertIsNone(store.load(base))

    def test_patch_apply_preflight_and_backup(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as temp:
            subprocess.check_call(["git", "init", root], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            target = os.path.join(root, "file.txt")
            with open(target, "w") as stream:
                stream.write("before\\n")
            patch_file = os.path.join(temp, "change.patch")
            with open(patch_file, "w") as stream:
                stream.write("--- a/file.txt\\n+++ b/file.txt\\n@@ -1 +1 @@\\n-before\\n+after\\n")
            with mock_patch("builtins.input", return_value="APPLY"):
                from sq_dev_aigent.core import apply_patch
                self.assertEqual(apply_patch(patch_file, root), 0)
            with open(target, "r") as stream:
                self.assertEqual(stream.read(), "after\\n")
            backup_root = os.path.join(root, ".sqai-backups")
            self.assertTrue(os.path.isdir(backup_root))
            backup_files = []
            for current, dirs, names in os.walk(backup_root):
                backup_files.extend(names)
            self.assertIn("file.txt", backup_files)

    def test_secret_redaction(self):
        text = "api_key=abc123 AWS_SECRET_ACCESS_KEY=secret456 Authorization: Bearer abc.def"
        redacted = SecurityGuard.redact(text)
        self.assertNotIn("abc123", redacted)
        self.assertNotIn("secret456", redacted)
        self.assertNotIn("abc.def", redacted)

    def test_auto_continue_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as base, tempfile.TemporaryDirectory() as project:
            store = CheckpointStore(base)
            store.save(project, "continue work", "verification", {"attempt": 1})
            auto = AutoContinue(store)
            self.assertIsNotNone(auto.pending(project))
            self.assertIsNone(auto.confirm_resume(project, "yes"))
            resumed = auto.confirm_resume(project, "RESUME")
            self.assertEqual(resumed["task"], "continue work")

    def test_repair_loop_caps_attempts(self):
        loop = RippleLoop(99)
        self.assertEqual(loop.max_attempts, 3)
        with self.assertRaises(ValueError):
            loop.record(4, "repair", "should not run")

    def test_requirement_checklist(self):
        checklist = RequirementChecklist(["test", "review"])
        checklist.mark(0, "pass", "exit code 0")
        self.assertFalse(checklist.complete())
        checklist.mark(1, "pass", "human reviewed")
        self.assertTrue(checklist.complete())

    def test_expected_system_counts(self):
        self.assertEqual(len(CORE_SYSTEMS), 12)
        self.assertEqual(len(LINKED_FILE_SYSTEMS), 7)

    def test_public_search_result_parser(self):
        parser = _SearchResultParser()
        parser.feed('<a class="result__a" href="https://docs.python.org/">Python Docs</a>')
        parser.feed('<a class="result__snippet" href="https://docs.python.org/">Official Python reference</a>')
        self.assertEqual(parser.results[0]["title"], "Python Docs")
        self.assertIn("docs.python.org", parser.results[0]["url"])
        self.assertIn("Official Python reference", parser.results[0]["snippet"])

    def test_catalog_has_100_unique_skills(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skills", "catalog.json")
        with open(path, "r") as stream:
            catalog = json.load(stream)
        self.assertEqual(len(catalog), 100)
        ids = [item["id"] for item in catalog]
        self.assertEqual(len(set(ids)), 100)

if __name__ == "__main__":
    unittest.main()
