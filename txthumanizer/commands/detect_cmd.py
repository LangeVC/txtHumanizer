"""
Handler for 'detect' subcommand.
"""
import sys
import os
import json
from catalog.engine.detector import detect_language
from txthumanizer.formatter import box, bold, cyan, green, yellow, dim


def get_input_text(input_arg: str) -> str:
    if input_arg == "-" or not sys.stdin.isatty() and not os.path.exists(input_arg):
        return sys.stdin.read()
    if os.path.exists(input_arg):
        with open(input_arg, "r", encoding="utf-8") as f:
            return f.read()
    return input_arg


def run_detect(args, is_json: bool = False) -> int:
    raw_text = get_input_text(args.input)
    if not raw_text.strip():
        if is_json:
            print(json.dumps({"error": "Empty input text"}))
        else:
            sys.stderr.write("Error: Empty input text.\n")
        return 2

    res = detect_language(raw_text)

    if is_json or getattr(args, "json", False):
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    lines = [
        f"{bold('Primary Language:')} {res['language'].upper()} ({res['confidence']} confidence)",
        f"{bold('Standard Variety:')} {res['variety']} – {res['variety_details'].get('name', '')}",
    ]

    ev = res['variety_details'].get('evidence', [])
    if ev:
        lines.append(f"{bold('Lexical Anchors:')} {', '.join(ev)}")

    warning = res['variety_details'].get('warning')
    if warning:
        lines.append(f"{yellow('Warning:')} {warning}")

    signals = res.get('human_signals', [])
    if signals:
        for s in signals:
            lines.append(f"{green('Human Signal:')} {s['name'].capitalize()} ({', '.join(s['evidence'])})")
    else:
        lines.append(f"{dim('Human Signals:')} None detected")

    lines.append(f"{dim('Latency:')} {res['elapsed_ms']}ms")

    print(box(f"txt-humanizer Language & Variety Analysis", lines))
    return 0
