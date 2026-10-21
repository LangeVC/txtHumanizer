"""
Core CLI Dispatcher for txt-humanizer.
"""
import sys
import os
import argparse
import json
from txthumanizer import __version__
from txthumanizer.formatter import red, bold, cyan, green


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # Parent parser for common flags so they can be placed before or after subcommand
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-j", "--json", action="store_true", help="Output machine-readable JSON")
    common.add_argument("-q", "--silent", action="store_true", help="Suppress non-error human output")

    parser = argparse.ArgumentParser(
        prog="txt-humanizer",
        description="txt-humanizer: Multilingual, dialect-aware AI detection & humanization CLI.",
        parents=[common],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  txt-humanizer detect "Wir parkieren das Velo beim Spital."
  cat draft.md | txt-humanizer check - --fail-on suspect
  txt-humanizer check article.md --format json
  txt-humanizer scan ./docs/ --report-file scan.json
  txt-humanizer transform post.md --diff
  txt-humanizer rules --lang de
  txt-humanizer init-hook
        """
    )

    parser.add_argument("-v", "--version", action="version", version=f"txt-humanizer {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # 1. detect
    detect_parser = subparsers.add_parser("detect", parents=[common], help="Detect primary language, variety and human signals")
    detect_parser.add_argument("input", nargs="?", default="-", help="Text string, file path, or '-' for stdin")

    # 2. check / analyze
    check_parser = subparsers.add_parser("check", aliases=["analyze"], parents=[common], help="Check text for AI patterns and calculate suspicion score")
    check_parser.add_argument("input", nargs="?", default="-", help="Text file path or '-' for stdin")
    check_parser.add_argument("--fail-on", choices=["suspect", "review"], help="Exit with code 1 if verdict reaches this level (CI gate)")
    check_parser.add_argument("--threshold", type=float, default=None, help="Custom score threshold to trigger exit code 1")
    check_parser.add_argument("--lang", default=None, help="Force language (de or en). Default: auto-detect")

    # 3. scan
    scan_parser = subparsers.add_parser("scan", parents=[common], help="Recursively scan a directory of files for AI density")
    scan_parser.add_argument("directory", help="Path to directory")
    scan_parser.add_argument("--ext", default="md,txt", help="Comma-separated file extensions to scan (default: md,txt)")
    scan_parser.add_argument("--report-file", default=None, help="Path to write JSON/Markdown summary report")
    scan_parser.add_argument("--fail-on", choices=["suspect", "review"], help="Exit with code 1 if any file triggers this level")

    # 4. transform
    trans_parser = subparsers.add_parser("transform", aliases=["humanize"], parents=[common], help="Apply rule-based vocabulary and syntax humanization")
    trans_parser.add_argument("input", nargs="?", default="-", help="File to transform or '-' for stdin")
    trans_parser.add_argument("-i", "--in-place", action="store_true", help="Write changes directly back to file")
    trans_parser.add_argument("--diff", action="store_true", help="Show colored unified diff of changes")
    trans_parser.add_argument("--lang", default=None, help="Force language (de or en). Default: auto-detect")

    # 5. rules
    rules_parser = subparsers.add_parser("rules", parents=[common], help="Explore catalog criteria and scoring weights")
    rules_parser.add_argument("--lang", default="de", choices=["de", "en"], help="Language catalog to inspect (default: de)")
    rules_parser.add_argument("--tier", type=int, choices=[1, 2, 3], help="Filter by tier level (1, 2, or 3)")

    # 6. init-hook
    hook_parser = subparsers.add_parser("init-hook", parents=[common], help="Install Git pre-commit hook in the current repository")
    hook_parser.add_argument("--fail-on", default="suspect", choices=["suspect", "review"], help="Level at which hook blocks commit")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    is_json = getattr(args, "json", False) or args.json

    try:
        # Dynamic import of subcommand handlers
        if args.command == "detect":
            from txthumanizer.commands.detect_cmd import run_detect
            return run_detect(args, is_json=is_json)
        elif args.command in ("check", "analyze"):
            from txthumanizer.commands.check_cmd import run_check
            return run_check(args, is_json=is_json)
        elif args.command == "scan":
            from txthumanizer.commands.scan_cmd import run_scan
            return run_scan(args, is_json=is_json)
        elif args.command in ("transform", "humanize"):
            from txthumanizer.commands.transform_cmd import run_transform
            return run_transform(args, is_json=is_json)
        elif args.command == "rules":
            from txthumanizer.commands.rules_cmd import run_rules
            return run_rules(args, is_json=is_json)
        elif args.command == "init-hook":
            from txthumanizer.commands.hook_cmd import run_hook
            return run_hook(args)
    except Exception as e:
        if is_json:
            print(json.dumps({"error": str(e)}))
        else:
            sys.stderr.write(red(f"Error: {e}\n"))
        return 2


if __name__ == "__main__":
    sys.exit(main())
