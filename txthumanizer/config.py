"""
Configuration discovery, YAML parsing, and normalization for txt-humanizer.

Supports `.txthumanizerrc.yaml` and `.txthumanizerrc.yml` with zero required
external dependencies: uses PyYAML (`yaml.safe_load`) when installed and falls
back to a pure-Python stdlib parser otherwise.
"""
from __future__ import annotations

import copy
import math
import os
import re
from typing import Any, Dict, List, Optional, Tuple

CONFIG_FILENAMES: Tuple[str, str] = (".txthumanizerrc.yaml", ".txthumanizerrc.yml")
SUPPORTED_LANGS = frozenset({"de", "en", "fr", "es", "it", "pt", "vi"})
VALID_FAIL_ON = frozenset({"review", "suspect"})

DEFAULT_CONFIG: Dict[str, Any] = {
    "default_lang": None,
    "fail_on": None,
    "thresholds": {
        "review": 1.0,
        "suspect": 2.5,
    },
    "disabled_rules": [],
    "weight_overrides": {},
    "ignore_paths": [],
    "config_path": None,
}

_INT_RE = re.compile(r"^[+-]?[0-9]+$")
_FLOAT_RE = re.compile(
    r"^[+-]?(?:[0-9]+\.[0-9]*|\.[0-9]+|[0-9]+)(?:[eE][+-]?[0-9]+)?$"
)


def _clone_default_config() -> Dict[str, Any]:
    """Return an isolated deep copy of DEFAULT_CONFIG."""
    return copy.deepcopy(DEFAULT_CONFIG)


def discover_config_file(start_path: Optional[str] = None) -> Optional[str]:
    """
    Walk upward from `start_path` (or `os.getcwd()` if None) looking for
    `.txthumanizerrc.yaml` then `.txthumanizerrc.yml`.

    Stops after checking the directory containing a `.git` entry or at the
    filesystem root.
    """
    if start_path is None:
        current = os.path.abspath(os.getcwd())
    else:
        abs_path = os.path.abspath(start_path)
        current = abs_path if os.path.isdir(abs_path) else os.path.dirname(abs_path)

    while True:
        for filename in CONFIG_FILENAMES:
            candidate = os.path.join(current, filename)
            if os.path.isfile(candidate):
                return candidate

        if os.path.exists(os.path.join(current, ".git")):
            return None

        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _strip_comment(line: str) -> str:
    """Strip an unquoted `# ...` YAML comment from a single line."""
    in_single = False
    in_double = False
    i = 0
    length = len(line)
    while i < length:
        ch = line[i]
        if in_single:
            if ch == "'":
                if i + 1 < length and line[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
        elif in_double:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_double = False
        else:
            if ch == "'":
                in_single = True
            elif ch == '"':
                in_double = True
            elif ch == "#" and (i == 0 or line[i - 1].isspace()):
                return line[:i]
        i += 1
    return line


def _find_mapping_colon(text: str, require_space_after: bool = True) -> int:
    """Return index of the first unquoted `:` separator, or -1."""
    in_single = False
    in_double = False
    bracket_depth = 0
    brace_depth = 0
    i = 0
    length = len(text)
    while i < length:
        ch = text[i]
        if in_single:
            if ch == "'":
                if i + 1 < length and text[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
        elif in_double:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_double = False
        else:
            if ch == "'":
                in_single = True
            elif ch == '"':
                in_double = True
            elif ch == "[":
                bracket_depth += 1
            elif ch == "]":
                bracket_depth = max(0, bracket_depth - 1)
            elif ch == "{":
                brace_depth += 1
            elif ch == "}":
                brace_depth = max(0, brace_depth - 1)
            elif ch == ":" and bracket_depth == 0 and brace_depth == 0:
                if not require_space_after or i + 1 == length or text[i + 1].isspace():
                    return i
        i += 1
    return -1


def _split_inline_items(inner: str, line_no: int) -> List[str]:
    """Split top-level comma-separated items inside `[...]` or `{...}`."""
    if not inner.strip():
        return []

    items: List[str] = []
    start = 0
    in_single = False
    in_double = False
    bracket_depth = 0
    brace_depth = 0
    i = 0
    length = len(inner)

    while i < length:
        ch = inner[i]
        if in_single:
            if ch == "'":
                if i + 1 < length and inner[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
        elif in_double:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_double = False
        else:
            if ch == "'":
                in_single = True
            elif ch == '"':
                in_double = True
            elif ch == "[":
                bracket_depth += 1
            elif ch == "]":
                bracket_depth -= 1
                if bracket_depth < 0:
                    raise ValueError(f"Line {line_no}: unexpected ']'")
            elif ch == "{":
                brace_depth += 1
            elif ch == "}":
                brace_depth -= 1
                if brace_depth < 0:
                    raise ValueError(f"Line {line_no}: unexpected '}}'")
            elif ch == "," and bracket_depth == 0 and brace_depth == 0:
                part = inner[start:i].strip()
                if not part:
                    raise ValueError(f"Line {line_no}: empty item in inline collection")
                items.append(part)
                start = i + 1
        i += 1

    if in_single or in_double or bracket_depth != 0 or brace_depth != 0:
        raise ValueError(f"Line {line_no}: unclosed quote or delimiter in inline collection")

    tail = inner[start:].strip()
    if tail:
        items.append(tail)
    return items


def _parse_quoted_string(raw: str, quote: str, line_no: int) -> str:
    """Parse a single- or double-quoted YAML scalar string."""
    chars: List[str] = []
    i = 1
    length = len(raw)
    closed = False

    while i < length:
        ch = raw[i]
        if quote == "'":
            if ch == "'":
                if i + 1 < length and raw[i + 1] == "'":
                    chars.append("'")
                    i += 2
                    continue
                closed = True
                i += 1
                break
            chars.append(ch)
        else:
            if ch == "\\":
                if i + 1 >= length:
                    raise ValueError(f"Line {line_no}: trailing backslash in double-quoted string")
                esc = raw[i + 1]
                escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"'}
                chars.append(escapes.get(esc, esc))
                i += 2
                continue
            if ch == '"':
                closed = True
                i += 1
                break
            chars.append(ch)
        i += 1

    if not closed or raw[i:].strip():
        raise ValueError(f"Line {line_no}: malformed quoted string {raw!r}")
    return "".join(chars)


def _parse_scalar(raw: str, line_no: int) -> Any:
    """Parse a YAML scalar (quoted string, null/none/~, bool, int, float, or string)."""
    if raw.startswith('"'):
        return _parse_quoted_string(raw, '"', line_no)
    if raw.startswith("'"):
        return _parse_quoted_string(raw, "'", line_no)

    lower = raw.lower()
    if lower in ("null", "none", "~"):
        return None
    if lower == "true":
        return True
    if lower == "false":
        return False
    if _INT_RE.match(raw):
        return int(raw)
    if _FLOAT_RE.match(raw):
        return float(raw)
    return raw


def _parse_value(raw: str, line_no: int) -> Any:
    """Parse an inline YAML value (inline list, inline dict, or scalar)."""
    if raw.startswith("["):
        if not raw.endswith("]"):
            raise ValueError(f"Line {line_no}: unclosed inline list")
        parts = _split_inline_items(raw[1:-1], line_no)
        return [_parse_value(part, line_no) for part in parts]

    if raw.startswith("{"):
        if not raw.endswith("}"):
            raise ValueError(f"Line {line_no}: unclosed inline mapping")
        parts = _split_inline_items(raw[1:-1], line_no)
        mapping: Dict[str, Any] = {}
        for part in parts:
            colon_idx = _find_mapping_colon(part, require_space_after=False)
            if colon_idx <= 0:
                raise ValueError(f"Line {line_no}: invalid inline mapping entry {part!r}")
            raw_key = part[:colon_idx].strip()
            raw_val = part[colon_idx + 1:].strip()
            key = str(_parse_scalar(raw_key, line_no))
            mapping[key] = _parse_value(raw_val, line_no) if raw_val else None
        return mapping

    return _parse_scalar(raw, line_no)


def _preprocess_lines(text: str) -> List[Tuple[int, int, str]]:
    """Strip comments and blank lines, returning `(line_no, indent, trimmed)` tuples."""
    cleaned = text.lstrip("\ufeff")
    tokens: List[Tuple[int, int, str]] = []

    for line_no, raw_line in enumerate(cleaned.splitlines(), 1):
        no_comment = _strip_comment(raw_line)
        trimmed = no_comment.strip()
        if not trimmed or trimmed in ("---", "..."):
            continue
        leading = no_comment[: len(no_comment) - len(no_comment.lstrip(" \t"))]
        if "\t" in leading:
            raise ValueError(f"Line {line_no}: tabs are not allowed in YAML indentation")
        tokens.append((line_no, len(leading), trimmed))

    return tokens


def _parse_sequence(
    tokens: List[Tuple[int, int, str]], idx: int, base_indent: int
) -> Tuple[List[Any], int]:
    """Parse a YAML block sequence starting at `idx`."""
    items: List[Any] = []
    while idx < len(tokens):
        line_no, indent, trimmed = tokens[idx]
        if indent < base_indent:
            break
        if indent > base_indent:
            raise ValueError(f"Line {line_no}: unexpected indentation in list")
        if not (trimmed == "-" or trimmed.startswith("- ")):
            break

        item_str = trimmed[1:].strip()
        idx += 1
        if item_str:
            items.append(_parse_value(item_str, line_no))
        elif idx < len(tokens) and tokens[idx][1] > indent:
            next_trimmed = tokens[idx][2]
            if next_trimmed == "-" or next_trimmed.startswith("- "):
                val, idx = _parse_sequence(tokens, idx, tokens[idx][1])
            else:
                val, idx = _parse_mapping(tokens, idx, tokens[idx][1])
            items.append(val)
        else:
            items.append(None)

    return items, idx


def _parse_mapping(
    tokens: List[Tuple[int, int, str]], idx: int, base_indent: int
) -> Tuple[Dict[str, Any], int]:
    """Parse a YAML block mapping starting at `idx`."""
    mapping: Dict[str, Any] = {}
    while idx < len(tokens):
        line_no, indent, trimmed = tokens[idx]
        if indent < base_indent:
            break
        if indent > base_indent:
            raise ValueError(f"Line {line_no}: unexpected indentation in mapping")
        if trimmed == "-" or trimmed.startswith("- "):
            break

        colon_idx = _find_mapping_colon(trimmed)
        if colon_idx <= 0:
            raise ValueError(f"Line {line_no}: expected 'key: value' entry, got {trimmed!r}")

        raw_key = trimmed[:colon_idx].strip()
        raw_val = trimmed[colon_idx + 1:].strip()
        key = _parse_scalar(raw_key, line_no)
        if key is None or key == "":
            raise ValueError(f"Line {line_no}: empty mapping key")
        key_str = str(key)

        idx += 1
        if raw_val:
            mapping[key_str] = _parse_value(raw_val, line_no)
        elif idx < len(tokens):
            _, next_indent, next_trimmed = tokens[idx]
            if (next_trimmed == "-" or next_trimmed.startswith("- ")) and next_indent >= indent:
                val, idx = _parse_sequence(tokens, idx, next_indent)
                mapping[key_str] = val
            elif next_indent > indent:
                val, idx = _parse_mapping(tokens, idx, next_indent)
                mapping[key_str] = val
            else:
                mapping[key_str] = None
        else:
            mapping[key_str] = None

    return mapping, idx


def _parse_rc_stdlib(text: str) -> Dict[str, Any]:
    """Pure-Python stdlib YAML subset parser for `.txthumanizerrc.yaml`."""
    tokens = _preprocess_lines(text)
    if not tokens:
        return {}

    first_line, first_indent, first_trimmed = tokens[0]
    if first_trimmed == "-" or first_trimmed.startswith("- "):
        raise ValueError(f"Line {first_line}: top-level YAML configuration must be a mapping")

    parsed, next_idx = _parse_mapping(tokens, 0, first_indent)
    if next_idx < len(tokens):
        bad_line = tokens[next_idx][0]
        raise ValueError(f"Line {bad_line}: unexpected trailing YAML content")
    return parsed


def parse_rc_yaml(text: str) -> Dict[str, Any]:
    """
    Parse YAML rc text using `yaml.safe_load` when PyYAML is available,
    otherwise falling back to `_parse_rc_stdlib`.
    """
    if not isinstance(text, str):
        raise ValueError("YAML configuration text must be a string")
    if not text.strip():
        return {}

    try:
        import yaml  # type: ignore
    except ImportError:
        return _parse_rc_stdlib(text)

    try:
        loaded = yaml.safe_load(text)
    except Exception as exc:
        raise ValueError(f"Invalid YAML configuration: {exc}") from exc

    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError("Top-level YAML configuration must be a mapping")
    return loaded


def _coerce_float(value: Any) -> Optional[float]:
    """Convert non-bool numeric value to finite float, or return None."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(num) or math.isinf(num):
        return None
    return num


def _normalize_str_list(value: Any) -> List[str]:
    """Normalize a YAML list (or single string) into deduplicated non-empty strings."""
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped or stripped.lower() in ("null", "none", "~"):
            return []
        return [stripped]
    if not isinstance(value, list):
        return []

    seen = set()
    result: List[str] = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def _normalize_config(raw: Dict[str, Any], config_path: Optional[str]) -> Dict[str, Any]:
    """Merge parsed rc dictionary into a normalized DEFAULT_CONFIG copy."""
    cfg = _clone_default_config()
    cfg["config_path"] = config_path

    raw_lang = raw.get("default_lang")
    if isinstance(raw_lang, str):
        lang = raw_lang.strip().lower()
        if lang in SUPPORTED_LANGS:
            cfg["default_lang"] = lang

    raw_fail_on = raw.get("fail_on")
    if isinstance(raw_fail_on, str):
        fail_on = raw_fail_on.strip().lower()
        if fail_on in VALID_FAIL_ON:
            cfg["fail_on"] = fail_on

    raw_thresholds = raw.get("thresholds")
    if isinstance(raw_thresholds, dict):
        review_val = _coerce_float(raw_thresholds.get("review"))
        if review_val is not None and review_val >= 0.0:
            cfg["thresholds"]["review"] = review_val

        suspect_val = _coerce_float(raw_thresholds.get("suspect"))
        if suspect_val is not None and suspect_val >= 0.0:
            cfg["thresholds"]["suspect"] = suspect_val

        if cfg["thresholds"]["suspect"] < cfg["thresholds"]["review"]:
            cfg["thresholds"]["suspect"] = cfg["thresholds"]["review"]

    cfg["disabled_rules"] = _normalize_str_list(raw.get("disabled_rules"))
    cfg["ignore_paths"] = _normalize_str_list(raw.get("ignore_paths"))

    raw_weights = raw.get("weight_overrides")
    if isinstance(raw_weights, dict):
        weights: Dict[str, float] = {}
        for k, v in raw_weights.items():
            key = str(k).strip()
            num = _coerce_float(v)
            if key and num is not None and num >= 0.0:
                weights[key] = num
        cfg["weight_overrides"] = weights

    return cfg


def load_config(
    start_path: Optional[str] = None,
    explicit_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Load and normalize txt-humanizer configuration.

    If `explicit_path` is provided, it must point to a readable, valid YAML
    mapping file or a `ValueError` is raised. Otherwise, searches upward from
    `start_path` via `discover_config_file` and falls back cleanly to defaults
    when no file exists or an auto-discovered file is unreadable/invalid.
    """
    if explicit_path is not None:
        if not explicit_path or not isinstance(explicit_path, str):
            raise ValueError("Explicit config path must be a non-empty string")
        abs_explicit = os.path.abspath(explicit_path)
        if not os.path.isfile(abs_explicit):
            raise ValueError(f"Config file not found: {explicit_path}")
        try:
            with open(abs_explicit, "r", encoding="utf-8") as fh:
                content = fh.read()
            parsed = parse_rc_yaml(content)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"Invalid config file '{explicit_path}': {exc}") from exc
        return _normalize_config(parsed, abs_explicit)

    discovered = discover_config_file(start_path)
    if discovered is None:
        return _clone_default_config()

    try:
        with open(discovered, "r", encoding="utf-8") as fh:
            content = fh.read()
        parsed = parse_rc_yaml(content)
    except (OSError, UnicodeDecodeError, ValueError):
        return _clone_default_config()

    return _normalize_config(parsed, discovered)
