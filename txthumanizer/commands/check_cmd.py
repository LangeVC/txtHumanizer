"""
Handler for 'check' and 'analyze' subcommands.
"""
import sys
import os
import re
import json
from functools import lru_cache
from catalog.engine.detector import detect_language, find_phrase_matches, normalize_text
from txthumanizer.config import load_config
from txthumanizer.formatter import box, bold, red, yellow, green, cyan, dim, score_badge


@lru_cache(maxsize=16)
def _get_supported_languages_cached(lang_dir: str, required_file: str, dir_mtime_ns: int) -> tuple:
    langs = sorted(
        d for d in os.listdir(lang_dir)
        if os.path.isdir(os.path.join(lang_dir, d))
        and os.path.isfile(os.path.join(lang_dir, d, required_file))
    )
    return tuple(langs) if langs else ("de", "en")


def get_supported_languages(required_file: str = "criteria.yaml") -> list:
    """Discover supported language catalog codes under catalog/languages/."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    lang_dir = os.path.join(base_dir, "catalog", "languages")
    if not os.path.isdir(lang_dir):
        return ["de", "en"]
    return list(_get_supported_languages_cached(lang_dir, required_file, os.stat(lang_dir).st_mtime_ns))


def resolve_effective_language(
    explicit_lang: str,
    config: dict,
    detected_lang: str,
    supported_langs: list,
) -> str:
    """Resolve effective language: explicit arg > config default_lang > detected > 'de'."""
    if isinstance(explicit_lang, str):
        norm_explicit = explicit_lang.strip().lower()
        if norm_explicit in supported_langs:
            return norm_explicit

    cfg_lang = config.get("default_lang") if isinstance(config, dict) else None
    if isinstance(cfg_lang, str):
        norm_cfg = cfg_lang.strip().lower()
        if norm_cfg in supported_langs:
            return norm_cfg

    if isinstance(detected_lang, str) and detected_lang in supported_langs:
        return detected_lang

    return "de" if "de" in supported_langs else supported_langs[0]


@lru_cache(maxsize=32)
def _parse_yaml_cached(abs_path: str, mtime_ns: int) -> dict:
    """Parse and cache criteria YAML keyed by resolved path and mtime."""
    try:
        import yaml
        with open(abs_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        pass

    # Fallback regex-based extraction of criteria
    criteria_list = []
    with open(abs_path, "r", encoding="utf-8") as f:
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


def parse_yaml_simple(path: str) -> dict:
    """Lightweight pure-python parser for txt-humanizer criteria files."""
    abs_path = os.path.abspath(path)
    return _parse_yaml_cached(abs_path, os.stat(abs_path).st_mtime_ns)


def evaluate_text(text: str, lang: str = None, config: dict = None) -> dict:
    cfg = load_config() if config is None else config
    supported_langs = get_supported_languages("criteria.yaml")

    normalized_text = normalize_text(text)
    det = detect_language(normalized_text)
    detected_lang = resolve_effective_language(
        lang,
        cfg,
        det.get("language"),
        supported_langs,
    )

    # Base directory resolution
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    crit_file = os.path.join(base_dir, "catalog", "languages", detected_lang, "criteria.yaml")

    data = parse_yaml_simple(crit_file)
    criteria = data.get("criteria", [])

    disabled_rules = set(cfg.get("disabled_rules") or [])
    weight_overrides = cfg.get("weight_overrides") or {}

    lines = normalized_text.splitlines()
    matches = []
    score = 0.0

    for crit in criteria:
        crit_id = crit.get("id")
        if crit_id in disabled_rules:
            continue

        triggers = crit.get("triggers", [])
        crit_name = crit.get("name")
        crit_tier = crit.get("tier", 2)
        if crit_id in weight_overrides:
            crit_weight = float(weight_overrides[crit_id])
        else:
            crit_weight = float(crit.get("weight", 0.5))

        matched_quotes = []
        for line_no, line in enumerate(lines, 1):
            for trig in triggers:
                for m in find_phrase_matches(line, trig):
                    start = max(0, m.start() - 20)
                    end = min(len(line), m.end() + 40)
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

    thresholds = cfg.get("thresholds") or {"review": 1.0, "suspect": 2.5}
    review_threshold = float(thresholds.get("review", 1.0))
    suspect_threshold = float(thresholds.get("suspect", 2.5))

    if final_score < review_threshold:
        verdict = "clean"
    elif final_score < suspect_threshold:
        verdict = "review"
    else:
        verdict = "suspect"

    return {
        "verdict": verdict,
        "score": final_score,
        "raw_penalty": round(score, 2),
        "human_offset": round(human_offset, 2),
        "language": detected_lang,
        "variety": det.get("variety", "standard"),
        "human_signals": det.get("human_signals", []),
        "matches_count": len(matches),
        "matches": matches
    }


def run_check(args, is_json: bool = False) -> int:
    input_path = args.input
    if input_path == "-":
        text = sys.stdin.read()
        target_name = "stdin"
        config = load_config()
    elif os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        target_name = os.path.basename(input_path)
        config = load_config(start_path=input_path)
    else:
        text = input_path
        target_name = "inline_text"
        config = load_config()

    if not text.strip():
        if is_json:
            print(json.dumps({"error": "Empty input"}))
        else:
            sys.stderr.write("Error: Empty input text.\n")
        return 2

    res = evaluate_text(text, lang=getattr(args, "lang", None), config=config)

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

    # Determine exit code based on threshold or fail-on (CLI overrides config)
    threshold = getattr(args, "threshold", None)
    cli_fail_on = getattr(args, "fail_on", None)
    fail_on = cli_fail_on if cli_fail_on is not None else (None if threshold is not None else config.get("fail_on"))

    exit_code = 0
    if threshold is not None and res["score"] >= threshold:
        exit_code = 1
    elif fail_on == "suspect" and res["verdict"] == "suspect":
        exit_code = 1
    elif fail_on == "review" and res["verdict"] in ("review", "suspect"):
        exit_code = 1

    return exit_code
