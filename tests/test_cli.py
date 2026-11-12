#!/usr/bin/env python3
"""
Integration tests for txt-humanizer CLI.
"""
import sys
import os
import subprocess
import json
import tempfile
import unicodedata

BIN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "txt-humanizer"))


def run_cli(args, stdin=None, cwd=None):
    cmd = [sys.executable, BIN_PATH] + args
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, cwd=cwd)
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


def test_cli_check_all_seven_languages():
    samples = {
        "de": ("Es ist wichtig zu betonen, dass dieses bedeutendes Themenfeld maßgeblich ist.", "K2"),
        "en": ("This watershed moment serves as a testament to her enduring legacy.", "EN-PUFFERY"),
        "fr": ("Il est important de souligner que les données jouent un rôle crucial dans ce projet.", "FR-CLICHE-DISCOURS"),
        "es": ("Es fundamental destacar que este informe cabe mencionar que es clave en términos de diseño.", "ES-CLICHE-DISCOURS"),
        "it": ("È fondamentale sottolineare che questo progetto vale la pena ricordare che è utile.", "IT-CLICHE-DISCOURS"),
        "pt": ("É fundamental ressaltar que este projeto vale ressaltar que ajuda a equipe.", "PT-CLICHE-DISCOURS"),
        "vi": ("Đáng chú ý là báo cáo này phân tích các dữ liệu một cách cẩn thận.", "VI-CLICHE-DISCOURS"),
    }
    for lang, (text, expected_rule) in samples.items():
        code, out, err = run_cli(["check", "-", "-j"], stdin=text)
        assert code == 0, f"{lang} failed: {err}"
        data = json.loads(out)
        assert data["language"] == lang, f"Expected {lang}, got {data['language']}"
        rule_ids = {m["id"] for m in data["matches"]}
        assert expected_rule in rule_ids, f"Expected {expected_rule} in {rule_ids} for {lang}"

    # Vietnamese NFD input matches, while partial subword ('Đáng chú ý làm') does not
    nfd_vi = unicodedata.normalize("NFD", "Đáng chú ý là báo cáo này phân tích các dữ liệu.")
    code, out, _ = run_cli(["check", "-", "--lang", "vi", "-j"], stdin=nfd_vi)
    assert code == 0
    assert json.loads(out)["matches_count"] >= 1

    subword_vi = "Đáng chú ý làm sao khi chúng ta phân tích dữ liệu của dự án."
    code, out, _ = run_cli(["check", "-", "--lang", "vi", "-j"], stdin=subword_vi)
    assert code == 0
    assert json.loads(out)["matches_count"] == 0


def test_cli_check_config_overrides():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, ".git"))
        rc_path = os.path.join(tmpdir, ".txthumanizerrc.yaml")
        with open(rc_path, "w", encoding="utf-8") as f:
            f.write(
                """
default_lang: en
fail_on: review
thresholds:
  review: 0.4
  suspect: 3.0
disabled_rules:
  - EN-SUPERFICIAL
weight_overrides:
  EN-PUFFERY: 0.5
"""
            )
        doc_path = os.path.join(tmpdir, "note.md")
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(
                "This watershed moment is highlighting the importance of leadership."
            )

        # Config applies: EN-SUPERFICIAL disabled, EN-PUFFERY weight=0.5 >= review(0.4), fail_on=review -> exit 1
        code, out, _ = run_cli(["check", doc_path, "-j"])
        assert code == 1
        data = json.loads(out)
        assert data["language"] == "en"
        assert data["score"] == 0.5
        assert data["verdict"] == "review"
        assert [m["id"] for m in data["matches"]] == ["EN-PUFFERY"]

        # Explicit CLI --fail-on suspect overrides config fail_on: review -> exit 0
        code, _, _ = run_cli(["check", doc_path, "--fail-on", "suspect", "-j"])
        assert code == 0

        # Explicit CLI --threshold 1.0 overrides config fail_on: review -> exit 0
        code, _, _ = run_cli(["check", doc_path, "--threshold", "1.0", "-j"])
        assert code == 0

        # Explicit CLI --lang de overrides config default_lang: en
        code, out, _ = run_cli(["check", doc_path, "--lang", "de", "-j"])
        assert code == 0
        assert json.loads(out)["language"] == "de"


def test_cli_scan_config_ignore_and_fail_on():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, ".git"))
        os.makedirs(os.path.join(tmpdir, "ignored_dir"))
        os.makedirs(os.path.join(tmpdir, "docs"))

        with open(os.path.join(tmpdir, ".txthumanizerrc.yaml"), "w", encoding="utf-8") as f:
            f.write(
                """
fail_on: suspect
ignore_paths:
  - ignored_dir
  - "*.draft.md"
"""
            )

        with open(os.path.join(tmpdir, "ignored_dir", "secret.md"), "w", encoding="utf-8") as f:
            f.write("Certainly! This watershed moment serves as a testament to enduring legacy.")
        with open(os.path.join(tmpdir, "docs", "notes.draft.md"), "w", encoding="utf-8") as f:
            f.write("Certainly! This watershed moment serves as a testament to enduring legacy.")
        with open(os.path.join(tmpdir, "docs", "clean.md"), "w", encoding="utf-8") as f:
            f.write("I walked the dog in the sunny park yesterday morning.")

        code, out, _ = run_cli(["scan", tmpdir, "-j"])
        assert code == 0
        payload = json.loads(out)
        assert payload["summary"]["total"] == 1
        assert payload["files"][0]["file"] == os.path.join("docs", "clean.md")

        # Add a suspect file in a non-ignored directory -> config fail_on: suspect causes exit 1
        with open(os.path.join(tmpdir, "docs", "bad.md"), "w", encoding="utf-8") as f:
            f.write("Certainly! This watershed moment serves as a testament to her enduring legacy, highlighting the importance of leadership.")

        code, out, _ = run_cli(["scan", tmpdir, "-j"])
        assert code == 1
        payload = json.loads(out)
        assert payload["summary"]["total"] == 2
        assert payload["summary"]["suspect"] == 1


def test_cli_transform_config_disabled_rules():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, ".git"))
        with open(os.path.join(tmpdir, ".txthumanizerrc.yaml"), "w", encoding="utf-8") as f:
            f.write(
                """
default_lang: de
disabled_rules:
  - R7
"""
            )
        doc_path = os.path.join(tmpdir, "draft.md")
        text = "Wir möchten diese Maßnahmen zeitnah implementieren."
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(text)

        code, out, _ = run_cli(["transform", doc_path, "-j"])
        assert code == 0
        data = json.loads(out)
        assert data["language"] == "de"
        assert data["changes_applied"] == 0
        assert data["result"] == text


if __name__ == "__main__":
    tests = [
        test_cli_help,
        test_cli_detect_text,
        test_cli_detect_json,
        test_cli_check_clean,
        test_cli_check_suspect_exit_code,
        test_cli_check_stdin_pipe,
        test_cli_transform_diff,
        test_cli_rules,
        test_cli_check_all_seven_languages,
        test_cli_check_config_overrides,
        test_cli_scan_config_ignore_and_fail_on,
        test_cli_transform_config_disabled_rules,
    ]
    for t in tests:
        t()
        print(f"[PASS] {t.__name__}")
    print("\nALL CLI INTEGRATION TESTS PASSED SUCCESSFULLY!")
