import unittest
import os
import sys
import tempfile
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from txthumanizer.commands.review_cmd import run_review

class DummyArgs:
    def __init__(self, path, backup=False, lang="de"):
        self.path = path
        self.backup = backup
        self.lang = lang

class TestCliReview(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def test_review_accept_change(self):
        test_file = os.path.join(self.tmp_dir, "sample.md")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Wir müssen das Problem adressieren.")

        old_stdin = sys.stdin
        sys.stdin = io.StringIO("y\n")
        try:
            args = DummyArgs(test_file, backup=True)
            ret = run_review(args)
            self.assertEqual(ret, 0)
        finally:
            sys.stdin = old_stdin

        with open(test_file, "r", encoding="utf-8") as f:
            updated = f.read()

        self.assertIn("angehen", updated)
        self.assertTrue(os.path.exists(test_file + ".bak"))

    def test_review_skip_change(self):
        test_file = os.path.join(self.tmp_dir, "sample_skip.md")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Wir müssen das Problem adressieren.")

        old_stdin = sys.stdin
        sys.stdin = io.StringIO("n\n")
        try:
            args = DummyArgs(test_file, backup=False)
            ret = run_review(args)
            self.assertEqual(ret, 0)
        finally:
            sys.stdin = old_stdin

        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("adressieren", content)

if __name__ == "__main__":
    unittest.main()
