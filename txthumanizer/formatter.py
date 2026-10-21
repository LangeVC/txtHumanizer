"""
ANSI Terminal Formatter & Visual Utilities for txt-humanizer CLI.
Zero external dependencies. Auto-disables colors when stdout is not a TTY.
"""
import sys
import os

# Check if colors should be enabled
USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def c(text: str, code: str) -> str:
    if not USE_COLOR:
        return str(text)
    return f"\033[{code}m{text}\033[0m"


def bold(text: str) -> str:
    return c(text, "1")


def dim(text: str) -> str:
    return c(text, "2")


def red(text: str) -> str:
    return c(text, "31")


def green(text: str) -> str:
    return c(text, "32")


def yellow(text: str) -> str:
    return c(text, "33")


def blue(text: str) -> str:
    return c(text, "34")


def magenta(text: str) -> str:
    return c(text, "35")


def cyan(text: str) -> str:
    return c(text, "36")


def score_badge(score: float) -> str:
    """Format an AI suspicion score with visual color & verdict."""
    if score < 1.0:
        return green(f"● {score:.1f} (Clean / Natural)")
    elif score < 2.5:
        return yellow(f"▲ {score:.1f} (Review / Moderate tells)")
    else:
        return red(f"✖ {score:.1f} (Suspect / High AI density)")


def box(title: str, lines: list, color_func=cyan) -> str:
    """Draw a clean Unicode box around lines."""
    width = max(len(title) + 4, max((len(l) for l in lines), default=40)) + 4
    width = min(width, 78)

    top = color_func("┌─ ") + bold(title) + color_func(" " + "─" * (width - len(title) - 4) + "┐")
    bottom = color_func("└" + "─" * (width - 1) + "┘")

    body = []
    for line in lines:
        body.append(color_func("│ ") + line + " " * max(0, width - len(line) - 3) + color_func("│"))

    return "\n".join([top] + body + [bottom])
