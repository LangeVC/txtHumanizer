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
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        pass

    replacements = {}
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Extract replacements: block
    if "replacements:" in text:
        block = text[text.find("replacements:"):].split("\n\n")[0]
        for line in block.splitlines():
            m = re.match(r'^\s*"?([^":]+)"?:\s*"?([^"\n]+)"?', line)
            if m:
                replacements[m.group(1).strip()] = m.group(2).strip()

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
    is_stdin = input_path == "-" or not sys.stdin.isatty() and not os.path.exists(input_path)

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
