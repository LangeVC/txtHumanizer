import unittest
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from txthumanizer.commands.scan_cmd import run_scan

class DummyScanArgs:
    def __init__(self, directory, workers="auto", fail_on=None):
        self.directory = directory
        self.workers = workers
        self.ext = "md,txt"
        self.report_file = None
        self.fail_on = fail_on
        self.json = False
        self.silent = True

class TestBenchmarkScan(unittest.TestCase):
    def test_multi_worker_scan_throughput(self):
        tmp_dir = tempfile.mkdtemp()
        num_files = 200
        # Generate synthetic files
        sample_texts = [
            "Das ist ein einfacher und natürlicher deutscher Text ohne KI-Muster.",
            "Wir parkieren das Velo beim Spital in Zürich.",
            "Es ist wichtig zu betonen, dass wir die Effizienz nachhaltig steigern.",
            "Certainly! Here is an AI generated response with some conversational fluff."
        ]
        for i in range(num_files):
            file_path = os.path.join(tmp_dir, f"doc_{i:04d}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(sample_texts[i % len(sample_texts)] + f" (id: {i})")

        t0 = time.perf_counter()
        args = DummyScanArgs(tmp_dir, workers="auto")
        ret = run_scan(args, is_json=True)
        elapsed = time.perf_counter() - t0

        self.assertEqual(ret, 0)
        throughput = num_files / max(elapsed, 0.0001)
        # Verify throughput is high
        self.assertGreater(throughput, 100.0, f"Throughput should exceed 100 files/sec, got {throughput:.1f}")

if __name__ == "__main__":
    unittest.main()
