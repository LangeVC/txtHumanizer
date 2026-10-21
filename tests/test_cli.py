#!/usr/bin/env python3
"""
Integration tests for txt-humanizer CLI.
"""
import sys
import os
import subprocess
import json

BIN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "txt-humanizer"))


def run_cli(args, stdin=None):
    cmd = [sys.executable, BIN_PATH] + args
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def test_cli_help():
    code, out, _ = run_cli(["--help"])
    assert code == 0
    assert "txt-humanizer" in out
    assert "detect" in out
    assert "check" in out


def test_cli_detect_text():
    code, out, _ = run_cli(["detect", "Wir parkieren das Velo beim Spital."])
    assert code == 0
    assert "DE" in out
    assert "de-CH" in out


def test_cli_detect_json():
    code, out, _ = run_cli(["detect", "This is an important test.", "--json"])
    assert code == 0
    data = json.loads(out)
    assert data["language"] == "en"
    assert "variety" in data


def test_cli_check_clean():
    code, out, _ = run_cli(["check", "I walked the dog in the sunny park yesterday morning.", "--fail-on", "suspect"])
    assert code == 0, f"Expected clean exit 0, got {code}"
    assert "Clean" in out or "0." in out


def test_cli_check_suspect_exit_code():
    suspect_text = "This watershed moment serves as a testament to her enduring legacy, highlighting the importance of leadership."
    code, out, _ = run_cli(["check", suspect_text, "--fail-on", "suspect"])
    assert code == 1, f"Expected suspect exit code 1, got {code}"


def test_cli_check_stdin_pipe():
    suspect_text = "Künstliche Intelligenz ist ein bedeutendes Themenfeld. Es ist wichtig zu betonen, dass dies maßgeblich ist."
    code, out, _ = run_cli(["check", "-", "-j"], stdin=suspect_text)
    assert code == 0
    data = json.loads(out)
    assert data["language"] == "de"
    assert len(data["matches"]) > 0


def test_cli_transform_diff():
    text = "Wir möchten diese Maßnahmen zeitnah implementieren."
    code, out, _ = run_cli(["transform", text, "--diff"])
    assert code == 0
    assert "-Wir möchten" in out or "+Wir möchten" in out
    assert "umsetzen" in out


def test_cli_rules():
    code, out, _ = run_cli(["rules", "--lang", "de", "--tier", "1"])
    assert code == 0
    assert "A1" in out
    assert "A8" in out


if __name__ == "__main__":
    tests = [
        test_cli_help,
        test_cli_detect_text,
        test_cli_detect_json,
        test_cli_check_clean,
        test_cli_check_suspect_exit_code,
        test_cli_check_stdin_pipe,
        test_cli_transform_diff,
        test_cli_rules
    ]
    for t in tests:
        t()
        print(f"[PASS] {t.__name__}")
    print("\nALL CLI INTEGRATION TESTS PASSED SUCCESSFULLY!")
