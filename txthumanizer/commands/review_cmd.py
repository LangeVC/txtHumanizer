"""
Handler for 'review' subcommand (Interactive human-in-the-loop review).
"""
import sys
import os
from catalog.engine.detector import compile_phrase_pattern, detect_language, normalize_text
from txthumanizer.commands.check_cmd import get_supported_languages, resolve_effective_language
from txthumanizer.commands.transform_cmd import filter_replacements, parse_transforms_simple
from txthumanizer.config import load_config
from txthumanizer.formatter import bold, red, green, yellow, cyan, dim


def run_review(args, is_json: bool = False) -> int:
    path = args.path
    if not os.path.exists(path):
        sys.stderr.write(f"File not found: {path}\n")
        return 2

    with open(path, "r", encoding="utf-8") as f:
        content = normalize_text(f.read())

    config = load_config(start_path=path)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    supported_langs = get_supported_languages("transforms.yaml")

    det = detect_language(content)
    lang = resolve_effective_language(
        getattr(args, "lang", None),
        config,
        det.get("language"),
        supported_langs,
    )

    trans_file = os.path.join(base_dir, "catalog", "languages", lang, "transforms.yaml")
    data = parse_transforms_simple(trans_file)
    replacements = filter_replacements(data, config.get("disabled_rules"))

    # Collect all match candidates using NFC/boundary-aware patterns
    raw_candidates = []
    for target, rep in replacements.items():
        pattern = compile_phrase_pattern(target)
        rep_clean = rep.split(" / ")[0]
        for m in pattern.finditer(content):
            raw_candidates.append({
                "target": m.group(0),
                "replacement": rep_clean,
                "start": m.start(),
                "end": m.end()
            })

    # Sort candidates by appearance in file and keep non-overlapping matches
    raw_candidates.sort(key=lambda c: (c["start"], -(c["end"] - c["start"])))
    candidates = []
    prev_end = 0
    for c in raw_candidates:
        if c["start"] >= prev_end:
            candidates.append(c)
            prev_end = c["end"]

    if not candidates:
        print(f"\n{green('✔ No AI-typical phrases found in')} {bold(path)}")
        return 0

    print(f"\n{bold('Interactive Review:')} {path} ({lang.upper()})")
    print(f"Found {len(candidates)} suggestion(s). Options: [y]es, [n]o, [a]ll, [e]dit, [q]uit\n")

    accepted = 0
    skipped = 0
    edited = 0
    auto_accept_all = False
    new_content = ""
    last_idx = 0

    for i, c in enumerate(candidates, 1):
        target = c["target"]
        suggested = c["replacement"]
        start = c["start"]
        end = c["end"]

        # Append preceding unmodified text
        new_content += content[last_idx:start]

        if auto_accept_all:
            new_content += suggested
            last_idx = end
            accepted += 1
            continue

        # Extract context around the match
        ctx_start = max(0, start - 40)
        ctx_end = min(len(content), end + 40)
        before = content[ctx_start:start]
        matched = content[start:end]
        after = content[end:ctx_end]

        print("-" * 60)
        print(f"[{i}/{len(candidates)}] {dim('Context:')} ...{before}{red(bold(matched))}{after}...")
        print(f"  Replace: {red(target)}  →  {green(suggested)}")

        choice = ""
        while choice not in ("y", "n", "a", "e", "q"):
            try:
                sys.stdout.write(f"  Apply change? [{bold('y')}/n/a/e/q]: ")
                sys.stdout.flush()
                choice = sys.stdin.readline().strip().lower()
                if not choice: # Default to yes
                    choice = "y"
            except (EOFError, KeyboardInterrupt):
                print(f"\n{yellow('Review interrupted.')}")
                return 1

        if choice == "y":
            new_content += suggested
            last_idx = end
            accepted += 1
        elif choice == "a":
            new_content += suggested
            last_idx = end
            accepted += 1
            auto_accept_all = True
        elif choice == "n":
            new_content += matched
            last_idx = end
            skipped += 1
        elif choice == "e":
            sys.stdout.write(f"  Enter custom replacement: ")
            sys.stdout.flush()
            custom_rep = sys.stdin.readline().strip()
            new_content += custom_rep
            last_idx = end
            edited += 1
        elif choice == "q":
            print(f"\n{yellow('Quitting review without further changes.')}")
            new_content += content[start:]
            last_idx = len(content)
            break

    # Append any remaining content
    new_content += content[last_idx:]

    total_changes = accepted + edited
    if total_changes > 0:
        if getattr(args, "backup", False):
            bak_path = path + ".bak"
            with open(bak_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"{dim('Backup created:')} {bak_path}")

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"\n{green('✔ Saved')} {bold(path)}: {accepted} accepted, {edited} custom, {skipped} skipped.\n")
    else:
        print(f"\n{yellow('No changes made to')} {bold(path)}.\n")

    return 0
