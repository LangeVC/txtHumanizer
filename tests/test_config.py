"""Unit tests for txthumanizer.config."""
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from txthumanizer.config import (
    DEFAULT_CONFIG,
    _parse_rc_stdlib,
    discover_config_file,
    load_config,
    parse_rc_yaml,
)


def test_defaults_when_no_config_exists(tmp_path):
    # Create a .git boundary so upward discovery stops inside tmp_path
    (tmp_path / ".git").mkdir()
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)

    cfg = load_config(start_path=str(nested))

    assert cfg == DEFAULT_CONFIG
    assert cfg["default_lang"] is None
    assert cfg["fail_on"] is None
    assert cfg["thresholds"] == {"review": 1.0, "suspect": 2.5}
    assert cfg["disabled_rules"] == []
    assert cfg["weight_overrides"] == {}
    assert cfg["ignore_paths"] == []
    assert cfg["config_path"] is None

    # Mutating the returned dict must not mutate DEFAULT_CONFIG
    cfg["thresholds"]["review"] = 9.9
    cfg["disabled_rules"].append("K14")
    cfg["weight_overrides"]["K2"] = 0.1
    cfg["ignore_paths"].append("drafts")
    assert DEFAULT_CONFIG["thresholds"]["review"] == 1.0
    assert DEFAULT_CONFIG["disabled_rules"] == []
    assert DEFAULT_CONFIG["weight_overrides"] == {}
    assert DEFAULT_CONFIG["ignore_paths"] == []


def test_discover_upward_from_file_and_dir(tmp_path):
    (tmp_path / ".git").mkdir()
    rc_file = tmp_path / ".txthumanizerrc.yaml"
    rc_file.write_text("default_lang: de\n", encoding="utf-8")

    nested_dir = tmp_path / "docs" / "chapters"
    nested_dir.mkdir(parents=True)
    target_file = nested_dir / "intro.md"
    target_file.write_text("Hallo Welt", encoding="utf-8")

    assert discover_config_file(str(nested_dir)) == str(rc_file)
    assert discover_config_file(str(target_file)) == str(rc_file)


def test_discover_prefers_yaml_over_yml(tmp_path):
    (tmp_path / ".git").mkdir()
    yml_file = tmp_path / ".txthumanizerrc.yml"
    yml_file.write_text("default_lang: en\n", encoding="utf-8")
    assert discover_config_file(str(tmp_path)) == str(yml_file)

    yaml_file = tmp_path / ".txthumanizerrc.yaml"
    yaml_file.write_text("default_lang: fr\n", encoding="utf-8")
    assert discover_config_file(str(tmp_path)) == str(yaml_file)


def test_discover_stops_at_git_boundary(tmp_path):
    # Config outside the repo should NOT be picked up past .git
    outer_rc = tmp_path / ".txthumanizerrc.yaml"
    outer_rc.write_text("default_lang: en\n", encoding="utf-8")

    repo = tmp_path / "myrepo"
    (repo / ".git").mkdir(parents=True)
    sub = repo / "src" / "notes"
    sub.mkdir(parents=True)

    assert discover_config_file(str(sub)) is None

    # Config in the .git root directory itself IS discovered before stopping
    repo_rc = repo / ".txthumanizerrc.yml"
    repo_rc.write_text("default_lang: de\n", encoding="utf-8")
    assert discover_config_file(str(sub)) == str(repo_rc)


def test_discover_defaults_to_cwd(tmp_path, monkeypatch):
    (tmp_path / ".git").mkdir()
    rc_file = tmp_path / ".txthumanizerrc.yaml"
    rc_file.write_text("default_lang: it\n", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()

    monkeypatch.chdir(sub)
    assert discover_config_file() == str(rc_file)


def test_stdlib_parser_nested_dicts_lists_comments_and_nulls():
    yaml_text = """
# Top-level comment
default_lang: "de"    # inline comment
fail_on: none         # treated as null

thresholds:
  review: 1.25        # float
  suspect: 3          # int coerced in load_config

disabled_rules:
  - K14               # inline comment on list item
  - "EN-EM-DASH"
  - 'FR#RULE'         # hash inside single quotes preserved

weight_overrides:
  K2: 0.25
  "K8": 0.0

ignore_paths: [node_modules, "*.draft.md", 'build/out']
"""
    parsed = _parse_rc_stdlib(yaml_text)
    assert parsed == {
        "default_lang": "de",
        "fail_on": None,
        "thresholds": {"review": 1.25, "suspect": 3},
        "disabled_rules": ["K14", "EN-EM-DASH", "FR#RULE"],
        "weight_overrides": {"K2": 0.25, "K8": 0.0},
        "ignore_paths": ["node_modules", "*.draft.md", "build/out"],
    }


def test_stdlib_parser_scalars_null_variants_and_inline_dicts():
    yaml_text = """
a: null
b: ~
c: None
d: ""
e: "hello # world"
f: 'it''s ok'
g: true
h: false
i: -2
j: 0.5
weight_overrides: {"K2":0.25, K5: 1.5}
disabled_rules:
- K1
- K2
empty_list: []
empty_dict: {}
bare_key:
next_key: after_bare
"""
    parsed = _parse_rc_stdlib(yaml_text)
    assert parsed["a"] is None
    assert parsed["b"] is None
    assert parsed["c"] is None
    assert parsed["d"] == ""
    assert parsed["e"] == "hello # world"
    assert parsed["f"] == "it's ok"
    assert parsed["g"] is True
    assert parsed["h"] is False
    assert parsed["i"] == -2
    assert parsed["j"] == 0.5
    assert parsed["weight_overrides"] == {"K2": 0.25, "K5": 1.5}
    assert parsed["disabled_rules"] == ["K1", "K2"]
    assert parsed["empty_list"] == []
    assert parsed["empty_dict"] == {}
    assert parsed["bare_key"] is None
    assert parsed["next_key"] == "after_bare"


def test_parse_rc_yaml_fallback_when_pyyaml_unavailable(monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)

    sample = """
default_lang: es
fail_on: review
thresholds:
  review: 0.8
  suspect: 2.2
disabled_rules: [ES-1, ES-2]
weight_overrides:
  K2: 0.4
ignore_paths:
  - vendor
"""
    assert parse_rc_yaml(sample) == _parse_rc_stdlib(sample)


def test_parse_rc_yaml_uses_pyyaml_when_available(monkeypatch):
    calls = []
    fake_yaml = types.ModuleType("yaml")

    def fake_safe_load(text):
        calls.append(text)
        return {"default_lang": "pt", "thresholds": {"review": 1.5, "suspect": 3.0}}

    fake_yaml.safe_load = fake_safe_load
    monkeypatch.setitem(sys.modules, "yaml", fake_yaml)

    result = parse_rc_yaml("default_lang: pt\n")
    assert len(calls) == 1
    assert result == {"default_lang": "pt", "thresholds": {"review": 1.5, "suspect": 3.0}}


def test_load_config_merges_and_normalizes(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)
    (tmp_path / ".git").mkdir()
    rc = tmp_path / ".txthumanizerrc.yaml"
    rc.write_text(
        """
default_lang: EN
fail_on: suspect
thresholds:
  review: 3.0
  suspect: 2.0   # < review; normalized up to review
disabled_rules:
  - K14
  - K14
  - ""
weight_overrides:
  K2: 0.25
  BAD: "not-a-float"
  NEG: -1.0
ignore_paths: ["dist", "*.bak"]
""",
        encoding="utf-8",
    )

    cfg = load_config(start_path=str(tmp_path))
    assert cfg["default_lang"] == "en"
    assert cfg["fail_on"] == "suspect"
    assert cfg["thresholds"] == {"review": 3.0, "suspect": 3.0}
    assert cfg["disabled_rules"] == ["K14"]
    assert cfg["weight_overrides"] == {"K2": 0.25}
    assert cfg["ignore_paths"] == ["dist", "*.bak"]
    assert cfg["config_path"] == str(rc)


def test_load_config_empty_and_invalid_discovered_fallback(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)
    (tmp_path / ".git").mkdir()
    rc = tmp_path / ".txthumanizerrc.yaml"

    # Empty / comment-only file returns defaults with config_path set
    rc.write_text("# only comments\n\n", encoding="utf-8")
    cfg_empty = load_config(start_path=str(tmp_path))
    assert cfg_empty["thresholds"] == {"review": 1.0, "suspect": 2.5}
    assert cfg_empty["config_path"] == str(rc)

    # Malformed discovered YAML falls back cleanly to defaults without raising
    rc.write_text("disabled_rules: [unclosed\n", encoding="utf-8")
    cfg_bad = load_config(start_path=str(tmp_path))
    assert cfg_bad == DEFAULT_CONFIG

    # Unreadable bytes in discovered file fall back cleanly
    rc.write_bytes(b"\xff\xfe\x00\x00")
    cfg_binary = load_config(start_path=str(tmp_path))
    assert cfg_binary == DEFAULT_CONFIG


def test_load_config_explicit_path_valid_and_invalid(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)
    explicit = tmp_path / "custom.yaml"
    explicit.write_text("default_lang: vi\nfail_on: review\n", encoding="utf-8")

    cfg = load_config(explicit_path=str(explicit))
    assert cfg["default_lang"] == "vi"
    assert cfg["fail_on"] == "review"
    assert cfg["config_path"] == str(explicit)

    # Missing explicit file raises ValueError
    with pytest.raises(ValueError, match="Config file not found"):
        load_config(explicit_path=str(tmp_path / "missing.yaml"))

    # Directory as explicit path raises ValueError
    with pytest.raises(ValueError, match="Config file not found"):
        load_config(explicit_path=str(tmp_path))

    # Empty string explicit path raises ValueError
    with pytest.raises(ValueError, match="non-empty"):
        load_config(explicit_path="")

    # Invalid YAML at explicit path raises ValueError
    bad_explicit = tmp_path / "broken.yaml"
    bad_explicit.write_text("not_a_key_value_line\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid config file"):
        load_config(explicit_path=str(bad_explicit))
