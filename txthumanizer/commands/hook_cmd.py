"""
Handler for 'init-hook' subcommand (Git Pre-Commit Hook installation).
"""
import sys
import os
from txthumanizer.formatter import bold, green, yellow, dim

HOOK_SCRIPT = """#!/usr/bin/env bash
# txt-humanizer Git Pre-Commit Hook
# Automatically blocks commits containing text with high AI suspicion scores.

set -e

# Find staged markdown and text files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.(md|txt)$' || true)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

echo "🔍 Running txt-humanizer pre-commit check on staged documents..."
FAILED=0

for FILE in $STAGED_FILES; do
    if [ -f "$FILE" ]; then
        if ! txt-humanizer check "$FILE" --fail-on {fail_on} -q; then
            echo "❌ [BLOCKED] $FILE exceeded AI suspicion threshold ({fail_on})"
            FAILED=1
        fi
    fi
done

if [ $FAILED -ne 0 ]; then
    echo "🚨 Commit blocked by txt-humanizer. Run 'txt-humanizer check <file>' to inspect."
    exit 1
fi

exit 0
"""


def run_hook(args) -> int:
    fail_on = args.fail_on or "suspect"
    script_content = HOOK_SCRIPT.replace("{fail_on}", fail_on)

    hook_dir = os.path.join(".git", "hooks")
    hook_path = os.path.join(hook_dir, "pre-commit")

    try:
        if os.path.isdir(hook_dir):
            with open(hook_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            os.chmod(hook_path, 0o755)
            print(green(f"✔ Successfully installed pre-commit hook to {hook_path}"))
            print(dim(f"Hook will block commits on {fail_on} level."))
            return 0
    except Exception as e:
        pass

    # If .git is read-only or in sandbox, print the script to stdout
    print(yellow("ℹ Could not write directly to .git/hooks/pre-commit (repository may be sandboxed)."))
    print(bold("\nTo install manually, save the following script as '.git/hooks/pre-commit' and make it executable (chmod +x):\n"))
    print(dim("----------------------------------------------------------------------"))
    print(script_content.strip())
    print(dim("----------------------------------------------------------------------\n"))
    return 0
