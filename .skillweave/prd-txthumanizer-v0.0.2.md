# Product Requirements Document: txtHumanizer v0.0.2 Extended Modes

## 1. Executive Summary

txtHumanizer v0.0.2 extends the existing German text humanization skill with two explicit operating modes:

1. **Automatikmodus**: Fast one-pass execution with transparent automatic style selection.
2. **Guide-Modus**: Stepwise guided execution through Analyse, Recommend, style-regler selection, optional Finetune, and final output.

The existing three-stage system remains intact:

```text
ANALYSE -> RECOMMEND -> FINETUNE
```

The extension resolves a workflow ambiguity in v0.0.1: the skill currently says style controls should be queried, but it also allows direct humanization. v0.0.2 makes that behavior explicit and predictable.

## 2. Problem Statement

In v0.0.1, the user flow for direct humanization is underspecified. If no style-regler values are provided, an agent may either:

- ask for all style-regler values before continuing, or
- infer them silently and produce a humanized text.

Both behaviors can be reasonable in isolation, but without mode rules the result feels inconsistent. Users need a clear way to choose between speed and control.

## 3. Target Users

### Primary users

- German-speaking writers, coaches, consultants, and business users who want to make AI-shaped text sound more natural.
- AI agents using the skill instructions to produce reproducible analyses and transformations.

### Secondary stakeholders

- Skill maintainers packaging txtHumanizer through Capacium and similar skill registries.
- Reviewers validating that the skill behavior is deterministic, transparent, and versioned.

## 4. Solution Overview

v0.0.2 introduces explicit mode routing:

- No mode parameter means **Automatikmodus**.
- `guide`, `guided`, `geführt`, `schrittweise`, `stepwise`, or `interactive` means **Guide-Modus**.
- Explicit style-regler values can be passed directly and override inferred values.

The Automatikmodus must disclose its inferred configuration. The Guide-Modus must stop at defined checkpoints and wait for user confirmation.

## 5. Functional Requirements

### FR-001: Version metadata update

Update all visible project metadata from `0.0.1` to `0.0.2` where the current skill version is declared or displayed.

Acceptance criteria:

- `SKILL.md` frontmatter uses `version: 0.0.2`.
- The system title in `SKILL.md` says `v0.0.2`.
- `capability.yaml` uses `version: 0.0.2`.
- `README.md` version badge references `0.0.2`.
- `SKILL.md` version history includes a v0.0.2 entry.

### FR-002: Automatikmodus

Document a default mode that applies when no guide/stepwise parameter is present.

Acceptance criteria:

- `SKILL.md` defines Automatikmodus as the default when no mode parameter is present.
- Automatikmodus explicitly runs Analyse, Recommend, and Finetune in one pass.
- Automatikmodus requires visible disclosure of all seven style-regler values.
- Automatikmodus requires a concrete justification for inferred style values.
- Automatikmodus forbids hidden random style selection.
- Automatikmodus forbids adding new facts unless the user explicitly asks for free rewriting.

### FR-003: Automatic style-regler inference rules

Define deterministic heuristics for selecting all seven style-regler values from the source text.

Acceptance criteria:

- `SKILL.md` documents inference rules for Domäne.
- `SKILL.md` documents inference rules for Formalität.
- `SKILL.md` documents inference rules for Persönlichkeit.
- `SKILL.md` documents inference rules for Texttreue.
- `SKILL.md` documents inference rules for Satzbau-Variation.
- `SKILL.md` documents inference rules for Kreativität.
- `SKILL.md` documents inference rules for Seele.
- `SKILL.md` defines a fallback configuration when inference is uncertain.

### FR-004: Guide-Modus

Document a guided workflow activated by mode aliases.

Acceptance criteria:

- `SKILL.md` lists guide aliases: `guide`, `guided`, `geführt`, `schrittweise`, `stepwise`, `interactive`.
- Guide-Modus starts with Stufe 1 Analyse.
- Guide-Modus stops after Analyse and asks whether to continue to Empfehlungen.
- Guide-Modus stops after Empfehlungen and asks whether to continue to style-regler selection.
- Guide-Modus supports `automatik` / `mach du` as a way to switch remaining decisions to transparent automatic selection.

### FR-005: Seven-step style-regler selection

Define a simple single-choice interaction for all seven style-reglers.

Acceptance criteria:

- Each style-regler is asked separately.
- Each style-regler presents lettered options.
- Each style-regler includes a `custom` option.
- Custom entries are documented in the final configuration.
- After step 7, the selected configuration is summarized before final humanization.

### FR-006: Optional Finetune

Allow the user to perform, preview-plan, skip, or adjust Finetune after style selection.

Acceptance criteria:

- `SKILL.md` defines direct finalization.
- `SKILL.md` defines an optional Finetune plan.
- `SKILL.md` defines ways to stop before humanization.
- `SKILL.md` defines a path to change the selected configuration.

### FR-007: README usage documentation

Update the README to make both modes discoverable.

Acceptance criteria:

- README describes Automatikmodus.
- README describes Guide-Modus.
- README shows at least one Automatik example.
- README shows at least one Guide example.
- README states that automatic style selection is disclosed and justified.

## 6. Non-Functional Requirements

- Preserve the existing German-language tone and structure of the skill.
- Do not alter the underlying KI detection criteria K1-K14 or Longlist A1-D4.
- Keep the skill self-contained in Markdown.
- Keep instructions deterministic enough for AI agents to follow reproducibly.
- Do not introduce scripts or runtime dependencies.

## 7. Scope

### In scope

- `SKILL.md` updates for v0.0.2 mode behavior.
- `README.md` updates for user-facing mode documentation.
- `capability.yaml` metadata update.
- SkillWeave PRD and execution artifacts under `.skillweave/`.

### Out of scope

- Changing KI detection criteria.
- Adding a command-line application.
- Adding tests that require a new runtime.
- Publishing a release or pushing the branch.

## 8. Success Metrics

- Metadata grep verifies no stale `0.0.1` version remains except historical v0.0.1 changelog entries.
- `SKILL.md` contains the required Automatikmodus and Guide-Modus sections.
- `README.md` documents both modes.
- `capability.yaml` remains valid YAML.
- Git diff is limited to intentional files plus existing untracked files left untouched.

## 9. Assumptions

- The v0.0.2 extension is documentation/instruction behavior, not executable code.
- The current package format supports a nonstandard `version` frontmatter field in `SKILL.md`, as it already exists in v0.0.1.
- The existing `perplexity.log` untracked file is unrelated and must not be modified.

## 10. Execution Recommendation

Recommended sequence type: `build`

Recommended execution mode: `ralph_attended`

Reason:

- The work mutates repository files.
- The implementation is small but touches public skill behavior and version metadata.
- Binary verification gates are useful and lightweight.
