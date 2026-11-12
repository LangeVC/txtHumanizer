"""
Handler for 'scan' subcommand (High-Volume & Multi-Core Directory Scanning).
"""
import sys
import os
import json
import fnmatch
import concurrent.futures
from txthumanizer.commands.check_cmd import evaluate_text
from txthumanizer.config import load_config
from txthumanizer.formatter import bold, red, yellow, green, cyan, dim, score_badge

IGNORED_DIRS = {".git", ".skillweave", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".idea", ".vscode"}
FAST_PATH_FILE_THRESHOLD = 500


def _is_ignored_path(rel_posix: str, name: str, ignore_patterns: list) -> bool:
    """Return True if basename or relative POSIX path matches any ignore pattern."""
    for raw_pattern in ignore_patterns:
        pat = str(raw_pattern).strip().replace("\\", "/")
        if pat.startswith("./"):
            pat = pat[2:]
        pat = pat.rstrip("/")
        if not pat:
            continue
        if (
            name == pat
            or rel_posix == pat
            or rel_posix.startswith(pat + "/")
            or fnmatch.fnmatch(name, pat)
            or fnmatch.fnmatch(rel_posix, pat)
        ):
            return True
    return False


def _scan_single_file(args_tuple):
    if len(args_tuple) == 3:
        path, base_dir, config = args_tuple
    else:
        path, base_dir = args_tuple
        config = None

    try:
        # Quick null-byte check for binary files
        with open(path, "rb") as fp:
            chunk = fp.read(1024)
            if b"\x00" in chunk:
                return {"file": os.path.relpath(path, base_dir), "skipped": "binary"}

        with open(path, "r", encoding="utf-8", errors="ignore") as fp:
            content = fp.read()

        res = evaluate_text(content, config=config)
        res["file"] = os.path.relpath(path, base_dir)
        return res
    except Exception as e:
        return {"file": os.path.relpath(path, base_dir), "error": str(e), "verdict": "error"}


def run_scan(args, is_json: bool = False) -> int:
    directory = args.directory
    if not os.path.isdir(directory):
        if is_json:
            print(json.dumps({"error": f"Directory not found: {directory}"}))
        else:
            sys.stderr.write(f"Error: Directory not found: {directory}\n")
        return 2

    config = load_config(start_path=directory)
    ignore_patterns = config.get("ignore_paths") or []

    exts = tuple("." + e.strip().lstrip(".") for e in args.ext.split(","))

    # Fast directory walk with directory pruning
    matched_files = []
    for root, dirs, files in os.walk(directory):
        rel_root = os.path.relpath(root, directory)
        rel_root_posix = "" if rel_root == "." else rel_root.replace(os.sep, "/")

        # In-place prune ignored directories
        kept_dirs = []
        for d in dirs:
            if d in IGNORED_DIRS or d.startswith("."):
                continue
            rel_d = f"{rel_root_posix}/{d}" if rel_root_posix else d
            if ignore_patterns and _is_ignored_path(rel_d, d, ignore_patterns):
                continue
            kept_dirs.append(d)
        dirs[:] = kept_dirs

        for f in files:
            if not f.endswith(exts):
                continue
            rel_f = f"{rel_root_posix}/{f}" if rel_root_posix else f
            if ignore_patterns and _is_ignored_path(rel_f, f, ignore_patterns):
                continue
            matched_files.append(os.path.join(root, f))

    matched_files.sort()
    if not matched_files:
        if is_json:
            print(json.dumps({"scanned": 0, "results": []}))
        else:
            print(f"No files matching {args.ext} found in {directory}.")
        return 0

    # Determine worker count with adaptive fast path for small/medium trees
    workers_arg = getattr(args, "workers", "auto")
    is_auto = workers_arg == "auto" or not workers_arg
    explicit_workers = None

    if not is_auto:
        try:
            explicit_workers = max(1, int(workers_arg))
        except ValueError:
            is_auto = True

    use_fast_path = is_auto and len(matched_files) < FAST_PATH_FILE_THRESHOLD
    if use_fast_path:
        max_workers = 1
    elif explicit_workers is not None:
        max_workers = explicit_workers
    else:
        max_workers = os.cpu_count() or 4

    results = []
    stats = {"clean": 0, "review": 0, "suspect": 0, "total": len(matched_files)}
    any_failed = False

    fail_on = getattr(args, "fail_on", None)
    if fail_on is None:
        fail_on = config.get("fail_on")

    tasks_payload = [(p, directory, config) for p in matched_files]

    use_pool = max_workers > 1 and (
        (not is_auto and len(matched_files) > 1)
        or (is_auto and len(matched_files) >= FAST_PATH_FILE_THRESHOLD)
    )

    if use_pool:
        workers_used = max_workers
        worker_label = f"{workers_used} worker(s)"
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            raw_results = list(executor.map(_scan_single_file, tasks_payload, chunksize=25))
    else:
        workers_used = 1
        worker_label = "1 worker (fast path)" if use_fast_path else "1 worker(s)"
        raw_results = [_scan_single_file(p) for p in tasks_payload]

    for res in raw_results:
        results.append(res)
        verdict = res.get("verdict")
        if verdict in stats:
            stats[verdict] += 1

        if fail_on == "suspect" and verdict == "suspect":
            any_failed = True
        elif fail_on == "review" and verdict in ("review", "suspect"):
            any_failed = True

    # Output formatting
    if is_json or getattr(args, "json", False):
        output_payload = {"summary": stats, "files": results}
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
    elif not getattr(args, "silent", False):
        print(f"\n{bold('txt-humanizer Directory Scan:')} {directory}")
        print(f"{dim('Scanned ' + str(len(matched_files)) + ' files with ' + worker_label)}\n")
        print(f"{'FILE':<38} {'LANG':<6} {'VARIETY':<10} {'SCORE':<24}")
        print("-" * 78)

        # Show first 50 results to avoid terminal flood on huge trees
        display_results = results[:50]
        for r in display_results:
            if "error" in r:
                print(f"{r['file']:<38} {red('ERROR: ' + r['error'])}")
                continue
            if r.get("skipped"):
                print(f"{r['file']:<38} {dim('SKIPPED (' + r['skipped'] + ')')}")
                continue

            badge = score_badge(r.get('score', 0.0))
            rel_file = r['file'] if len(r['file']) <= 36 else "..." + r['file'][-33:]
            lang_str = r.get('language', '??').upper()
            var_str = r.get('variety', '??')
            print(f"{rel_file:<38} {lang_str:<6} {var_str:<10} {badge}")

        if len(results) > 50:
            print(dim(f"... and {len(results) - 50} more files"))

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
