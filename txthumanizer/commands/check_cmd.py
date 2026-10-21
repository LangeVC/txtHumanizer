"""
Handler for 'check' and 'analyze' subcommands.
"""
import sys
import os
import re
import json
from catalog.engine.detector import detect_language
from txthumanizer.formatter import box, bold, red, yellow, green, cyan, dim, score_badge


def parse_yaml_simple(path: str) -> dict:
    """Lightweight pure-python parser for txt-humanizer criteria files."""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        pass

    # Fallback regex-based extraction of criteria
    criteria_list = []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\s*-\s+id:\s*", content)
    for b in blocks[1:]:
        lines = b.splitlines()
        crit_id = lines[0].strip().strip('"\'')
        name_m = re.search(r"name:\s*\"?([^\n\"]+)\"?", b)
        tier_m = re.search(r"tier:\s*(\d+)", b)
        weight_m = re.search(r"weight:\s*([0-9.]+)", b)
        triggers = []
        if "triggers:" in b:
            trig_block = b[b.find("triggers:"):].split("\n\n")[0]
            triggers = [t.strip().strip('"\'') for t in re.findall(r"-\s*\"?([^\n\"]+)\"?", trig_block)]

        criteria_list.append({
            "id": crit_id,
            "name": name_m.group(1) if name_m else crit_id,
            "tier": int(tier_m.group(1)) if tier_m else 2,
            "weight": float(weight_m.group(1)) if weight_m else 0.5,
            "triggers": triggers
        })
    return {"criteria": criteria_list}


def evaluate_text(text: str, lang: str = None) -> dict:
    det = detect_language(text)
    detected_lang = lang if lang in ("de", "en") else det["language"]
    if detected_lang not in ("de", "en"):
        detected_lang = "de"

    # Base directory resolution
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    crit_file = os.path.join(base_dir, "catalog", "languages", detected_lang, "criteria.yaml")

    data = parse_yaml_simple(crit_file)
    criteria = data.get("criteria", [])

    lines = text.splitlines()
    matches = []
    score = 0.0

    for crit in criteria:
        triggers = crit.get("triggers", [])
        crit_id = crit.get("id")
        crit_name = crit.get("name")
        crit_tier = crit.get("tier", 2)
        crit_weight = float(crit.get("weight", 0.5))

        matched_quotes = []
        for line_no, line in enumerate(lines, 1):
            for trig in triggers:
                if trig.lower() in line.lower():
                    # Extract quote snippet
                    start = max(0, line.lower().find(trig.lower()) - 20)
                    end = min(len(line), start + len(trig) + 40)
                    snippet = line[start:end].strip()
                    matched_quotes.append({"line": line_no, "trigger": trig, "snippet": snippet})

        if matched_quotes:
            # Score contribution
            penalty = crit_weight * min(len(matched_quotes), 3) # Cap repeat penalty
            score += penalty
            matches.append({
                "id": crit_id,
                "name": crit_name,
                "tier": crit_tier,
                "weight": crit_weight,
                "count": len(matched_quotes),
                "penalty": round(penalty, 2),
                "evidence": matched_quotes[:3]
            })

    # Offset by human signals (e.g. authentic dialects)
    human_offset = 0.0
    for sig in det.get("human_signals", []):
        human_offset += 0.5

    final_score = max(0.0, round(score - human_offset, 2))

    if final_score < 1.0:
        verdict = "clean"
    elif final_score < 2.5:
        verdict = "review"
    else:
        verdict = "suspect"

    return {
        "verdict": verdict,
        "score": final_score,
        "raw_penalty": round(score, 2),
        "human_offset": round(human_offset, 2),
        "language": detected_lang,
        "variety": det["variety"],
        "human_signals": det.get("human_signals", []),
        "matches_count": len(matches),
        "matches": matches
    }


def run_check(args, is_json: bool = False) -> int:
    input_path = args.input
    if input_path == "-" or not sys.stdin.isatty() and not os.path.exists(input_path):
        text = sys.stdin.read()
        target_name = "stdin"
    elif os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        target_name = os.path.basename(input_path)
    else:
        text = input_path
        target_name = "inline_text"

    if not text.strip():
        if is_json:
            print(json.dumps({"error": "Empty input"}))
        else:
            sys.stderr.write("Error: Empty input text.\n")
        return 2

    res = evaluate_text(text, lang=args.lang)

    if is_json or getattr(args, "json", False):
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif not getattr(args, "silent", False):
        print(f"\n{bold('Checked:')} {target_name} ({res['language'].upper()} · {res['variety']})")
        print(f"{bold('Score:')}   {score_badge(res['score'])}")

        if res["human_signals"]:
            for sig in res["human_signals"]:
                print(f"{green('Human Signal:')} {sig['name'].capitalize()} (-{res['human_offset']} offset)")

        if res["matches"]:
            print(f"\n{bold('Detected Patterns (' + str(len(res['matches'])) + '):')}")
            for m in res["matches"]:
                tier_color = red if m["tier"] == 1 else (yellow if m["tier"] == 2 else dim)
                print(f"  {tier_color('[Tier ' + str(m['tier']) + ']')} {bold(m['name'])} ({m['id']}) – +{m['penalty']} pts")
                for ev in m["evidence"]:
                    print(f"    {dim('L' + str(ev['line']) + ':')} \"...{ev['snippet']}...\"")
        else:
            print(green("  No conspicuous AI pattern triggers detected."))
        print()

    # Determine exit code based on threshold or fail-on
    exit_code = 0
    if args.threshold is not None and res["score"] >= args.threshold:
        exit_code = 1
    elif args.fail_on == "suspect" and res["verdict"] == "suspect":
        exit_code = 1
    elif args.fail_on == "review" and res["verdict"] in ("review", "suspect"):
        exit_code = 1

    return exit_code
