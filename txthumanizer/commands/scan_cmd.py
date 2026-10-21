"""
Handler for 'scan' subcommand (Batch directory scanning).
"""
import sys
import os
import json
from txthumanizer.commands.check_cmd import evaluate_text
from txthumanizer.formatter import bold, red, yellow, green, cyan, dim, score_badge


def run_scan(args, is_json: bool = False) -> int:
    directory = args.directory
    if not os.path.isdir(directory):
        if is_json:
            print(json.dumps({"error": f"Directory not found: {directory}"}))
        else:
            sys.stderr.write(f"Error: Directory not found: {directory}\n")
        return 2

    exts = tuple("." + e.strip().lstrip(".") for e in args.ext.split(","))
    matched_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(exts):
                matched_files.append(os.path.join(root, f))

    matched_files.sort()
    if not matched_files:
        if is_json:
            print(json.dumps({"scanned": 0, "results": []}))
        else:
            print(f"No files matching {args.ext} found in {directory}.")
        return 0

    results = []
    stats = {"clean": 0, "review": 0, "suspect": 0, "total": len(matched_files)}
    any_failed = False

    for path in matched_files:
        try:
            with open(path, "r", encoding="utf-8") as fp:
                content = fp.read()
            res = evaluate_text(content)
            res["file"] = os.path.relpath(path, directory)
            results.append(res)
            stats[res["verdict"]] += 1

            if args.fail_on == "suspect" and res["verdict"] == "suspect":
                any_failed = True
            elif args.fail_on == "review" and res["verdict"] in ("review", "suspect"):
                any_failed = True
        except Exception as e:
            results.append({"file": path, "error": str(e)})

    # Output formatting
    if is_json or getattr(args, "json", False):
        output_payload = {"summary": stats, "files": results}
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
    elif not getattr(args, "silent", False):
        print(f"\n{bold('txt-humanizer Directory Scan:')} {directory}")
        print(f"{dim('Found ' + str(len(matched_files)) + ' files matching ' + args.ext)}\n")
        print(f"{'FILE':<38} {'LANG':<6} {'VARIETY':<10} {'SCORE':<24}")
        print("-" * 78)

        for r in results:
            if "error" in r:
                print(f"{r['file']:<38} {red('ERROR: ' + r['error'])}")
                continue

            badge = score_badge(r['score'])
            rel_file = r['file'] if len(r['file']) <= 36 else "..." + r['file'][-33:]
            print(f"{rel_file:<38} {r['language'].upper():<6} {r['variety']:<10} {badge}")

        print("-" * 78)
        print(f"Summary: {green(str(stats['clean']) + ' clean')}, "
              f"{yellow(str(stats['review']) + ' review')}, "
              f"{red(str(stats['suspect']) + ' suspect')}\n")

    # Save report if requested
    if args.report_file:
        try:
            with open(args.report_file, "w", encoding="utf-8") as rf:
                json.dump({"summary": stats, "files": results}, rf, ensure_ascii=False, indent=2)
            if not getattr(args, "silent", False):
                print(dim(f"Report saved to {args.report_file}"))
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to save report: {e}\n")

    return 1 if any_failed else 0
