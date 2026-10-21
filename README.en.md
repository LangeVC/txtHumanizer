# txtHumanizer

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.5.0-blue)](https://github.com/LangeVC/txtHumanizer/releases/tag/v0.5.0)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/LangeVC/txtHumanizer)
[![Capacium](https://img.shields.io/badge/Capacium-Install%20via%20cap-0B1020?style=flat-square)](https://github.com/Capacium/capacium)
[![CI](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml)

[ ![Deutsch](https://img.shields.io/badge/🇩🇪-Deutsch-0969da?style=flat-square) ](README.md)
[ ![English](https://img.shields.io/badge/🇬🇧-English-238636?style=flat-square) ](README.en.md)
[ ![Français](https://img.shields.io/badge/🇫🇷-Français-0969da?style=flat-square) ](README.fr.md)
[ ![Español](https://img.shields.io/badge/🇪🇸-Español-0969da?style=flat-square) ](README.es.md)
[ ![Italiano](https://img.shields.io/badge/🇮🇹-Italiano-0969da?style=flat-square) ](README.it.md)
[ ![Português](https://img.shields.io/badge/🇵🇹-Português-0969da?style=flat-square) ](README.pt.md)
[ ![Tiếng Việt](https://img.shields.io/badge/🇻🇳-Tiếng%20Việt-0969da?style=flat-square) ](README.vi.md)

Modular, multilingual, variety-sensitive AI writing detection and humanization framework with full **Terminal CLI** capabilities. Evidence-based pattern removal adhering to guidelines from **English Wikipedia** (*Signs of AI writing / WP:AISIGNS*) and **German Wikipedia** (*Anzeichen für KI-generierte Inhalte*).

---

## ⚡ CLI Quickstart

The framework includes a zero-dependency CLI (**0 external packages**, pure Python 3.10+ standard library):

```bash
# Direct execution
./bin/txt-humanizer --help

# Or install in your virtual environment
pip install -e .
```

### The Core Commands

```bash
# 1. Identify language, regional variety (en-US, en-GB, etc.), and human signals
txt-humanizer detect "We analyze the behavior whilst maintaining consistency."

# 2. Check document with full score, metric breakdown, and quote citations
txt-humanizer check draft.md

# 3. CI/CD Gate: Exit code 1 when score indicates AI generation
txt-humanizer check draft.md --fail-on suspect -q

# 4. Recursive directory scan with summary table and JSON report
txt-humanizer scan ./docs/ --ext md,txt --report-file scan-report.json

# 5. Rule-based transformation preview with unified color diff
txt-humanizer transform article.md --diff

# 6. Inspect criteria catalog, triggers, and tier classifications
txt-humanizer rules --lang en --tier 1

# 7. Initialize pre-commit hook in your git repository
txt-humanizer init-hook
```

---

## 🤖 Agent Agnostic / Machine Interoperability

Engineered for autonomous LLM agents (Claude Code, Antigravity, OpenClaude, Cursor) and automated CI/CD runners:

```bash
# Stdin pipe: check input and return structured JSON
cat article.md | txt-humanizer check - --format json
```

### Exit Codes for CI/CD Gates
- `0`: Clean (Human text, score < 2.5)
- `1`: Suspect (AI signals detected, score >= 2.5)
- `2`: Error (Invalid arguments or unreadable file)

---

## 🌍 Supported Languages & Varieties

- **German (`de`):** `de-DE`, `de-AT` (Austriacisms protected), `de-CH` (Helvetisms protected), Dialects (Bavarian, Alemannic, Cologne, Low German as positive human signals).
- **English (`en`):** `en-US`, `en-GB`, Style Bleed cross-variant detection.
- **Coming in v0.5.0:** French (`fr-FR`, `fr-CA`), Spanish (`es-ES`, `es-MX`, `es-AR`), Italian (`it-IT`), Portuguese (`pt-BR`, `pt-PT`), Vietnamese (`vi-North`, `vi-Central`, `vi-South`).

---

## 📜 License

Licensed under the [Apache License, Version 2.0](LICENSE).
