# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Repository Provenance**: Forgejo (`git.langevc.com/langevc/txt-humanizer`) is canonical.
> GitHub (`github.com/LangeVC/txtHumanizer`) is a read-only mirror.

---

## [0.4.0] - 2026-10-21

### Added
- **Unified CLI Suite (`txt-humanizer`)**:
  - `detect`: Sub-millisecond identification of primary language (`de`, `en`), varieties (`de-DE`, `de-AT`, `de-CH`, `en-US`, `en-GB`, `en-hybrid`), and dialectal Human Signals.
  - `check` (alias: `analyze`): Evidence-based evaluation of Tier 1–3 criteria with exact line numbers and quotation snippets.
  - `scan`: Recursive batch auditing of directories containing Markdown and text files with tabular summaries.
  - `transform` (alias: `humanize`): Rule-based deterministic text transformation with colorized unified diff previews (`--diff`).
  - `rules`: Terminal catalog inspection tool displaying criteria, weights, and triggers by language and tier.
  - `init-hook`: One-click Git Pre-Commit Hook installer to automatically block high-score AI drafts.
- **Zero-Dependency Core**: Pure Python 3.10+ standard library implementation with zero external package requirements.
- **Dual Usability Interface**:
  - Human Ergonomics: ANSI terminal styling with auto-detected TTY disabling, Unicode box rendering, and visual score badges.
  - Agent & CI/CD Ergonomics: Machine-readable JSON output (`--json` / `-j`), silent execution mode (`--silent` / `-q`), and deterministic exit codes (`0` clean, `1` suspect, `2` error).
- **Capacium v1.0 Manifest Hardening**: Full validation conformance with `Capacium/capacium-action-validate@v1` in strict mode (`name: LangeVC/txt-humanizer`, `canonical_source_url`, `bin` declaration, framework tags including `openclaude`, `claude-desktop`, `codex`).
- **Integration Test Suite**: `tests/test_cli.py` covering all CLI subcommands and pipe operations.

### Changed
- Standardized package architecture with `txthumanizer` module, `setup.py`, and executable wrapper `bin/txt-humanizer`.
- Updated `SKILL.md` to reference the local CLI engine for zero-token background evaluations by coding agents.

---

## [0.3.0] - 2026-10-21

### Added
- **Multilingual Support**: First-class support for English (`en`) based on *Wikipedia:Signs of AI writing (WP:AISIGNS)* alongside German (`de`).
- **Tiered Scoring Architecture**:
  - Tier 1 (1.0 weight): Falsifiable hard evidence, hallucinated sources, chatbot leaks, zero-width space artifacts.
  - Tier 2 (0.5 weight): Strong stylistic indicators (puffery, AI vocabulary density, superficial *-ing* codas, copula avoidance, triads, negative parallelisms).
  - Tier 3 (0.15 weight): Weak contextual signals (cadence, excessive errorlessness, title case headings).
- **Historic Marker Decay**: Dynamic decay factors (`<= 0.15`) for obsolete LLM tells (e.g. em-dash clustering, outdated knowledge cutoffs).
- **Regional Standard Varieties**:
  - DACH: False-positive protection for Swiss Standard German (`de-CH`, Helvetisms, no `ß`) and Austrian German (`de-AT`, Austriacisms, regional syntax).
  - English: Distinction between American (`en-US`) and British (`en-GB`) English with active detection of "Style Bleed" hybrid inconsistencies.
- **Dialectal Human Signals**: Authentic German regional dialects (Bairisch, Alemannisch, Kölsch, Plattdeutsch) actively reduce AI suspicion scores.
- **Modular YAML Catalog Structure**: Extensible directory schema under `catalog/core/`, `catalog/languages/de/`, and `catalog/languages/en/`.
- **Deterministic Detector Engine**: `catalog/engine/detector.py` providing sub-millisecond language and variety classification.

---

## [0.0.2] - 2026-07-28

### Added
- **Explicit Operating Modes**:
  - Automatikmodus: Transparent one-pass execution (Analyse → Recommend → Finetune) with disclosed style derivations.
  - Guide-Modus: Interactive stepwise process with confirmation checkpoints.
- Automatic style-regler inference heuristics based on source text domain.
- Seven single-choice style-regler configuration flow.

---

## [0.0.1] - 2026-07-28

### Added
- Initial three-stage system: ANALYSE → RECOMMEND → FINETUNE.
- Top 10 AI indicators adapted from German Wikipedia Schnelltest v1.35 (K1–K10).
- German linguistic additions (K11–K14) and Longlist deep inspection (A1–D4).
- 7 configurable style-reglers for text humanization.
