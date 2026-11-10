"""
Handler for 'transform' and 'humanize' subcommands.
"""
import sys
import os
import re
import json
import difflib
from catalog.engine.detector import detect_language
from txthumanizer.formatter import bold, red, green, cyan, dim


def parse_transforms_simple(path: str) -> dict:
    replacements = {}
    data = None
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        pass

    if isinstance(data, dict):
        if "replacements" in data and isinstance(data["replacements"], dict):
            replacements.update(data["replacements"])
        for item in data.get("transforms", []):
            if isinstance(item, dict) and "replacements" in item and isinstance(item["replacements"], dict):
                replacements.update(item["replacements"])
        return {"replacements": replacements}

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        in_rep = False
        indent = 0
        for line in text.splitlines():
            if "replacements:" in line:
                in_rep = True
                indent = len(line) - len(line.lstrip())
                continue
            if in_rep:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                curr_indent = len(line) - len(line.lstrip())
                if curr_indent <= indent:
                    in_rep = False
                    continue
                m = re.match(r'^\s*"?([^":]+)"?:\s*"?([^"\n]+)"?', line)
                if m:
                    target = m.group(1).strip().strip('"\'')
                    rep = m.group(2).strip().strip('"\'')
                    replacements[target] = rep
    except Exception:
        pass

    return {"replacements": replacements}


def apply_transforms(text: str, lang: str = None) -> tuple:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    supported_langs = [
        d for d in os.listdir(os.path.join(base_dir, "catalog", "languages"))
        if os.path.isdir(os.path.join(base_dir, "catalog", "languages", d))
    ] if os.path.exists(os.path.join(base_dir, "catalog", "languages")) else ["de", "en"]

    det = detect_language(text)
    detected_lang = lang if lang in supported_langs else det["language"]
    if detected_lang not in supported_langs:
        detected_lang = "de"

    trans_file = os.path.join(base_dir, "catalog", "languages", detected_lang, "transforms.yaml")

    data = parse_transforms_simple(trans_file)
    replacements = data.get("replacements", {})

    modified = text
    applied_count = 0
    changes = []

    for target, replacement in replacements.items():
        pattern = r"\b" + re.escape(target) + r"\b"
        if re.search(pattern, modified, re.I):
            # Pick first option if multiple alternatives given (e.g. "angehen / behandeln")
            rep_clean = replacement.split(" / ")[0]
            new_text, n = re.subn(pattern, rep_clean, modified, flags=re.I)
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
    elif os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            original = f.read()
        target_name = input_path
    else:
        original = input_path
        target_name = "inline_text"

    if not original.strip():
        if is_json:
            print(json.dumps({"error": "Empty input"}))
        else:
            sys.stderr.write("Error: Empty input.\n")
        return 2

    transformed, count, changes, lang = apply_transforms(original, lang=args.lang)

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
