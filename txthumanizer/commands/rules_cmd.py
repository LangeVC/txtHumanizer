"""
Handler for 'rules' subcommand (Catalog criteria exploration).
"""
import sys
import os
import json
from txthumanizer.commands.check_cmd import parse_yaml_simple
from txthumanizer.formatter import bold, red, yellow, cyan, dim


def run_rules(args, is_json: bool = False) -> int:
    lang = args.lang or "de"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    crit_file = os.path.join(base_dir, "catalog", "languages", lang, "criteria.yaml")

    if not os.path.exists(crit_file):
        sys.stderr.write(f"Catalog for language '{lang}' not found.\n")
        return 2

    data = parse_yaml_simple(crit_file)
    criteria = data.get("criteria", [])

    if args.tier:
        criteria = [c for c in criteria if c.get("tier") == args.tier]

    if is_json or getattr(args, "json", False):
        print(json.dumps({"language": lang, "criteria": criteria}, ensure_ascii=False, indent=2))
        return 0

    print(f"\n{bold('txt-humanizer Catalog Rules:')} {lang.upper()} ({len(criteria)} criteria)")
    print(f"{'ID':<14} {'TIER':<8} {'WEIGHT':<8} {'NAME / DESCRIPTION'}")
    print("-" * 78)

    for c in criteria:
        cid = c.get("id", "")
        tier = c.get("tier", 2)
        weight = str(c.get("weight", 0.5))
        name = c.get("name", "")
        tier_str = red(f"Tier {tier}") if tier == 1 else (yellow(f"Tier {tier}") if tier == 2 else dim(f"Tier {tier}"))
        print(f"{bold(cid):<14} {tier_str:<17} {weight:<8} {name}")
        triggers = c.get("triggers", [])
        if triggers:
            sample_trig = ", ".join(f'"{t}"' for t in triggers[:4])
            if len(triggers) > 4:
                sample_trig += f" ... (+{len(triggers)-4} more)"
            print(f"  {dim('Triggers:')} {dim(sample_trig)}")

    print("-" * 78 + "\n")
    return 0
