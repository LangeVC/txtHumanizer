"""
Handler for 'review' subcommand (Interactive human-in-the-loop review).
"""
import sys
import os
import re
from catalog.engine.detector import detect_language
from txthumanizer.commands.transform_cmd import parse_transforms_simple
from txthumanizer.formatter import bold, red, green, yellow, cyan, dim


def run_review(args, is_json: bool = False) -> int:
    path = args.path
    if not os.path.exists(path):
        sys.stderr.write(f"File not found: {path}\n")
        return 2

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    supported_langs = [
        d for d in os.listdir(os.path.join(base_dir, "catalog", "languages"))
        if os.path.isdir(os.path.join(base_dir, "catalog", "languages", d))
    ] if os.path.exists(os.path.join(base_dir, "catalog", "languages")) else ["de", "en"]

    det = detect_language(content)
    lang = getattr(args, "lang", None)
    if not lang or lang not in supported_langs:
        lang = det["language"] if det["language"] in supported_langs else "de"

    trans_file = os.path.join(base_dir, "catalog", "languages", lang, "transforms.yaml")
    data = parse_transforms_simple(trans_file)
    replacements = data.get("replacements", {})

    # Collect all match candidates
    candidates = []
    for target, rep in replacements.items():
        pattern = r"\b" + re.escape(target) + r"\b"
        for m in re.finditer(pattern, content, re.I):
            candidates.append({
                "target": m.group(0),
                "replacement": rep.split(" / ")[0],
                "start": m.start(),
                "end": m.end()
            })

    # Sort candidates by appearance in file
    candidates.sort(key=lambda c: c["start"])

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
