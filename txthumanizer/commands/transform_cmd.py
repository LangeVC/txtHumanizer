"""
Handler for 'transform' and 'humanize' subcommands.
"""
import sys
import os
import re
import json
import difflib
from catalog.engine.detector import compile_phrase_pattern, detect_language, normalize_text
from txthumanizer.commands.check_cmd import get_supported_languages, resolve_effective_language
from txthumanizer.config import load_config
from txthumanizer.formatter import bold, red, green, cyan, dim


def parse_transforms_simple(path: str) -> dict:
    replacements = {}
    rules = []
    data = None
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        pass

    if isinstance(data, dict):
        if "replacements" in data and isinstance(data["replacements"], dict):
            top_reps = dict(data["replacements"])
            replacements.update(top_reps)
            rules.append({"id": None, "replacements": top_reps})
        for item in data.get("transforms", []):
            if not isinstance(item, dict):
                continue
            rule_id = item.get("id")
            raw_reps = item.get("replacements")
            item_reps = {}
            if isinstance(raw_reps, dict):
                item_reps = dict(raw_reps)
            elif isinstance(raw_reps, list) and item.get("trigger"):
                non_empty = [str(r) for r in raw_reps if isinstance(r, str) and r]
                if non_empty:
                    item_reps = {str(item["trigger"]): " / ".join(non_empty)}
                elif raw_reps:
                    item_reps = {str(item["trigger"]): str(raw_reps[0])}
            if item_reps:
                replacements.update(item_reps)
                rules.append({"id": rule_id, "replacements": item_reps})
        return {"replacements": replacements, "rules": rules}

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        current_id = None
        current_reps = {}
        in_rep = False
        indent = 0
        for line in text.splitlines():
            id_m = re.match(r'^\s*-\s+id:\s*"?([^"\n]+)"?', line)
            if id_m:
                if current_reps:
                    rules.append({"id": current_id, "replacements": current_reps})
                    current_reps = {}
                current_id = id_m.group(1).strip().strip('"\'')
                in_rep = False
                continue
            if "replacements:" in line:
                if current_reps:
                    rules.append({"id": current_id, "replacements": current_reps})
                    current_reps = {}
                in_rep = True
                indent = len(line) - len(line.lstrip())
                continue
            if in_rep:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                curr_indent = len(line) - len(line.lstrip())
                if curr_indent <= indent:
                    if current_reps:
                        rules.append({"id": current_id, "replacements": current_reps})
                        current_reps = {}
                    in_rep = False
                    continue
                m = re.match(r'^\s*"?([^":]+)"?:\s*"?([^"\n]+)"?', line)
                if m:
                    target = m.group(1).strip().strip('"\'')
                    rep = m.group(2).strip().strip('"\'')
                    replacements[target] = rep
                    current_reps[target] = rep
        if current_reps:
            rules.append({"id": current_id, "replacements": current_reps})
    except Exception:
        pass

    return {"replacements": replacements, "rules": rules}


def filter_replacements(data: dict, disabled_rules) -> dict:
    """Return active trigger->replacement pairs excluding any disabled transform rule IDs."""
    disabled = set(disabled_rules or [])
    rules = data.get("rules")
    if isinstance(rules, list):
        active = {}
        for rule in rules:
            rule_id = rule.get("id")
            if rule_id and rule_id in disabled:
                continue
            active.update(rule.get("replacements", {}))
        return active
    return dict(data.get("replacements", {}))


def apply_transforms(text: str, lang: str = None, config: dict = None) -> tuple:
    cfg = load_config() if config is None else config
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    supported_langs = get_supported_languages("transforms.yaml")

    normalized = normalize_text(text)
    det = detect_language(normalized)
    detected_lang = resolve_effective_language(
        lang,
        cfg,
        det.get("language"),
        supported_langs,
    )

    trans_file = os.path.join(base_dir, "catalog", "languages", detected_lang, "transforms.yaml")

    data = parse_transforms_simple(trans_file)
    replacements = filter_replacements(data, cfg.get("disabled_rules"))

    modified = normalized
    applied_count = 0
    changes = []

    for target, replacement in replacements.items():
        pattern = compile_phrase_pattern(target)
        # Pick first option if multiple alternatives given (e.g. "angehen / behandeln")
        rep_clean = replacement.split(" / ")[0]
        new_text, n = pattern.subn(lambda _m, rep=rep_clean: rep, modified)
        if n > 0:
            applied_count += n
            modified = new_text
            changes.append({"target": target, "replacement": rep_clean, "count": n})

    return modified, applied_count, changes, detected_lang


def run_transform(args, is_json: bool = False) -> int:
    input_path = args.input
    is_stdin = input_path == "-"

    if is_stdin:
        original = sys.stdin.read()
        target_name = "stdin"
        config = load_config()
    elif os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            original = f.read()
        target_name = input_path
        config = load_config(start_path=input_path)
    else:
        original = input_path
        target_name = "inline_text"
        config = load_config()

    if not original.strip():
        if is_json:
            print(json.dumps({"error": "Empty input"}))
        else:
            sys.stderr.write("Error: Empty input.\n")
        return 2

    transformed, count, changes, lang = apply_transforms(
        original,
        lang=getattr(args, "lang", None),
        config=config,
    )

    if is_json or getattr(args, "json", False):
        print(json.dumps({
            "target": target_name,
            "language": lang,
            "changes_applied": count,
            "replacements": changes,
            "result": transformed
        }, ensure_ascii=False, indent=2))
        return 0

    if args.diff:
        diff_lines = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            transformed.splitlines(keepends=True),
            fromfile=f"a/{target_name}",
            tofile=f"b/{target_name}"
        ))
        if not diff_lines:
            print(dim("No rule-based changes applied."))
        else:
            for line in diff_lines:
                if line.startswith("+"):
                    sys.stdout.write(green(line))
                elif line.startswith("-"):
                    sys.stdout.write(red(line))
                elif line.startswith("@"):
                    sys.stdout.write(cyan(line))
                else:
                    sys.stdout.write(line)
        return 0

    if args.in_place:
        if is_stdin:
            sys.stderr.write("Error: Cannot use --in-place with stdin.\n")
            return 2
        with open(input_path, "w", encoding="utf-8") as fp:
            fp.write(transformed)
        print(green(f"Updated {input_path} ({count} replacements applied)."))
        return 0

    # Default output: print transformed text
    sys.stdout.write(transformed)
    return 0
