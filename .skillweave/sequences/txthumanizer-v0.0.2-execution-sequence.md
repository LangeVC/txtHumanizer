# SkillWeave PromptChain: txtHumanizer v0.0.2 Extended Modes

## Metadata

- Sequence ID: `txthumanizer-v0.0.2-extended-modes`
- Sequence type: `build`
- Execution mode: `ralph_attended`
- Source PRD: `.skillweave/prd-txthumanizer-v0.0.2.json`
- Risk mode: `medium`

## Objective

Implement txtHumanizer v0.0.2 by adding explicit Automatikmodus and Guide-Modus behavior to the skill instructions, updating user-facing documentation, and aligning package metadata.

## Success Criteria

- `SKILL.md` declares v0.0.2 and documents both modes.
- Automatikmodus requires transparent inferred style-regler disclosure.
- Guide-Modus enforces stepwise checkpoints.
- README documents both modes with examples.
- `capability.yaml` declares v0.0.2 and mentions both modes.
- Verification checks pass.

## Inputs Required

- Requirements: `/Users/andrelange/workspaces/_local-temp/txtHumanizer-modi-anforderungen.md`
- Repository root: `/Users/andrelange/Documents/repositories/github/LangeVC/txtHumanizer`
- PRD JSON: `.skillweave/prd-txthumanizer-v0.0.2.json`

## Execution Batches

### Batch 1: Skill instruction update

- Included tasks: `DOC-001`
- Critical path: Update `SKILL.md`
- Write surfaces: `SKILL.md`
- Verification:
  - `rtk grep -n "version: 0.0.2|Automatikmodus|Guide-Modus|Stil-Regler-Abfrage|AUTOMATISCHE STILWAHL" SKILL.md`
- Gate:
  - Pass only if v0.0.2 metadata and both mode sections are present.

### Batch 2: README and metadata update

- Included tasks: `DOC-002`, `META-001`
- Critical path: Align public docs and package metadata with the updated skill behavior.
- Write surfaces:
  - `README.md`
  - `capability.yaml`
- Verification:
  - `rtk grep -n "0.0.2|Automatikmodus|Guide-Modus|guide" README.md capability.yaml`
  - Parse `capability.yaml` as YAML.
- Gate:
  - Pass only if README and capability metadata reflect v0.0.2 behavior.

### Batch 3: Final verification

- Included tasks: `VERIFY-001`
- Critical path: Verify consistency and review diff.
- Write surfaces: none.
- Verification:
  - Grep required terms in changed files.
  - Parse JSON/YAML artifacts.
  - Review `rtk git diff -- SKILL.md README.md capability.yaml .skillweave/prd-txthumanizer-v0.0.2.md .skillweave/prd-txthumanizer-v0.0.2.json .skillweave/sequences/txthumanizer-v0.0.2-execution-sequence.md`.
  - Confirm existing untracked `perplexity.log` remains untouched.
- Gate:
  - Pass only if all checks are conclusive.

## Failure Handling

- If a required section is missing, patch the narrow section only and rerun grep.
- If YAML or JSON parsing fails, fix syntax only and rerun parse checks.
- If unrelated files change, stop and inspect before continuing.

## Final Deliverable Format

Report:

- Files changed
- Verification commands and results
- Known limitations
- Branch name
