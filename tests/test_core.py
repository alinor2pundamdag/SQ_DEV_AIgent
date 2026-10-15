import os
import tempfile
import unittest
from sq_dev_aigent.core import patch_paths, validate_patch_paths, project_files, safe_root

class CoreTests(unittest.TestCase):
    def test_patch_paths(self):
        patch = "--- a/src/main.py\n+++ b/src/main.py\n@@ -1 +1 @@\n-a\n+b\n"
        self.assertEqual(patch_paths(patch), ["src/main.py"])

    def test_reject_parent_path(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                validate_patch_paths(root, ["../outside.txt"])

    def test_reject_absolute_path(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                validate_patch_paths(root, [os.path.abspath(os.path.join(root, "x"))])

    def test_project_inventory(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "README.md"), "w") as stream:
                stream.write("hello")
            self.assertIn("README.md", project_files(root))

    def test_root_must_exist(self):
        with self.assertRaises(ValueError):
            safe_root("/this/path/should/not/exist/sqai-test")

if __name__ == "__main__":
    unittest.main()
