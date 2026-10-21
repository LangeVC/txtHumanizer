import unittest
import os

class TestPreCommitHook(unittest.TestCase):
    def test_precommit_manifest_valid(self):
        hook_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".pre-commit-hooks.yaml")
        self.assertTrue(os.path.isfile(hook_path), ".pre-commit-hooks.yaml must exist")
        with open(hook_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check required fields
        self.assertIn("id: txt-humanizer", content)
        self.assertIn("name: txt-humanizer", content)
        self.assertIn("entry: bin/txt-humanizer check --fail-on suspect", content)
        self.assertIn("types: [text]", content)
        self.assertIn("files:", content)

if __name__ == "__main__":
    unittest.main()
