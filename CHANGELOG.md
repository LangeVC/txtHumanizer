# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Repository Provenance**: Forgejo (`git.langevc.com/langevc/txt-humanizer`) is canonical.
> GitHub (`github.com/LangeVC/txtHumanizer`) is a read-only mirror.

---

## [0.6.0] - 2026-11-12

### Added
- **Project Configuration (`.txthumanizerrc.yaml`)**: Zero-dependency upward config discovery & stdlib YAML subset parser (`txthumanizer/config.py`) supporting custom `thresholds` (`review`, `suspect`), `disabled_rules`, `weight_overrides`, `default_lang`, `fail_on`, and `ignore_paths`, integrated into `check`, `scan`, `transform`, and `review`.
- **Local HTTP Server & Offline Web UI (`txt-humanizer serve`)**: Pure stdlib `ThreadingHTTPServer` bound to `127.0.0.1:8080` serving an offline single-page review UI at `/` plus JSON endpoints (`/api/health`, `/api/detect`, `/api/check`, `/api/transform`).
- **Vietnamese NFC & Syllable-Aware Boundary Tokenization**: Normalized NFD/NFC inputs and introduced `compile_phrase_pattern` / `find_phrase_matches` in `catalog/engine/detector.py` so multi-word compounds (`máy lạnh`, `xe hơi`, `fin de semaine`) match reliably without partial subword false positives.
- **Full 7-Language Evaluation in `check`**: Dynamically discovers all language catalogs (`de`, `en`, `fr`, `es`, `it`, `pt`, `vi`) instead of restricting evaluation to `de`/`en`.
- **CI Test & Version Parity Gate**: Added `pytest tests/` execution to `.github/workflows/ci.yml` alongside `tests/test_version_parity.py` verifying `.version.yaml`, `capability.yaml`, `txthumanizer/__init__.py`, `setup.py`, and `SKILL.md`.

### Performance
- **Adaptive Single-Process Fast Path (`scan`)**: Batches under 500 files under `--workers auto` bypass `ProcessPoolExecutor` spawn overhead while preserving multi-core execution for large trees, plus mtime-cached criteria loading (>100 files/sec sustained on macOS).

---

## [0.5.1] - 2026-11-10

### Fixed
- **Release Permissions in CI**: Resolved HTTP 403 Forbidden on GitHub Actions release step by adding explicit top-level `permissions: contents: write` and `id-token: write` to `.github/workflows/release.yml`.
- **Capacium Trusted Publishing (OIDC)**: Configured `Capacium/capacium-action-publish@v1` with `use_oidc: "true"` and `id-token: write` permissions, eliminating reliance on static registry secrets.
- **Capacium Manifest Registry Parity**: Aligned `capability.yaml` with `owner: LangeVC` and `name: txtHumanizer` matching the canonical GitHub repository `LangeVC/txtHumanizer` for clean `cap install LangeVC/txtHumanizer`.
- **Packaging Compatibility**: Ensured `cap package` outputs clean `.tar.gz` distribution packages without nested subdirectory collisions.
- **CLI Input & Transform Parsing**: Fixed non-TTY stdin shadowing on inline text (`detect`/`check`/`transform`) and extracted nested `replacements:` blocks in `parse_transforms_simple`.

---

## [0.5.0] - 2026-10-21

> **Release Note (Historical Lineage):** Git tag `v0.5.0` failed to publish a GitHub Release / Capacium artifact due to missing CI permissions (resolved in [`0.5.1`](#051---2026-11-10)). Users should install `v0.5.1` or newer.

### Added
- **5 New Language Catalogs**: Full support for French (`fr`), Spanish (`es`), Italian (`it`), Portuguese (`pt`), and Vietnamese (`vi`).
  - **French (`fr`)**: Metropolitan (`fr-FR`) vs Canadian (`fr-CA` Quebecois shields: *magasiner, courriel, char, fin de semaine*) + Argot & Verlan signals.
  - **Spanish (`es`)**: Peninsular (`es-ES`) vs Mexican (`es-MX`) vs Argentine (`es-AR` with *voseo*, *che*, *pileta*, *remera*, *laburo*) + Lunfardo signals.
  - **Italian (`it`)**: Standard Italian (`it-IT`) with North/South lexical protection + Romanesco and Neapolitan dialect signals.
  - **Portuguese (`pt`)**: Bidirectional variety shields for Brazilian (`pt-BR`: *celular, trem, ônibus*) and European (`pt-PT`: *telemóvel, comboio, autocarro*) + Nordestino signals.
  - **Vietnamese (`vi`)**: Northern (`vi-North` / Hanoi standard AI boilerplate detection) + Central (`vi-Central` / Nghệ Tĩnh & Huế: *mô, tê, răng, rứa, nỏ, chi*) + Southern (`vi-South` / Saigon & Mekong shields: *ly, máy lạnh, heo, bắp, nghen, hen, hổng, mần, xài*).
- **Interactive Terminal Review (`review`)**: Line-by-line CLI command (`txt-humanizer review <file>`) allowing human-in-the-loop inspection and acceptance (`[y/n/a/e/q]`) of suggested transformations with optional `--backup`.
- **High-Volume Multi-Core Tree Scanner**: `scan` command upgraded with `ProcessPoolExecutor` (`--workers auto|N`), gitignore awareness, and streaming file traversal, achieving >150 files/sec across massive codebases.
- **Native Pre-Commit Plugin**: Added `.pre-commit-hooks.yaml` in repo root for instant zero-dependency integration via standard `pre-commit`.
- **Multilingual Documentation & Navigation Badge Bar**: Localized READMEs (`README.en.md`, `README.fr.md`, `README.es.md`, `README.it.md`, `README.pt.md`, `README.vi.md`) with a unified button-style language navigation bar.

---

## [0.4.0] - 2026-10-21

> **Release Note (Historical Lineage):** Git tag `v0.4.0` failed to publish a GitHub Release / Capacium artifact due to missing CI permissions (resolved in [`0.5.1`](#051---2026-11-10)).

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
