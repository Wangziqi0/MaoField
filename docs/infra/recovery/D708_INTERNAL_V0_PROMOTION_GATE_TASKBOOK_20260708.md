# D708 Internal V0 Promotion Gate Taskbook

- Date verified on node36: 2026-07-08 10:01 CST
- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Current HEAD before D708 package edits: `b356c0b`
- Current status source: `STATE.md`

## Purpose

Prepare the next zero-context Pro review round for the D707 internal v0 note:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md
```

The question is not whether MaoField is empirically positive, not whether the
programme is public-ready, and not whether a paper should be written. The narrow
question is:

```text
Is the internal v0 finite chart/path/cycle defect note mathematically correct,
well-scoped, and safe to keep as an internal bounded formal note after patching
any remaining local issues?
```

## Inputs

Read first:

1. `STATE.md`
2. `docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md`
3. `docs/infra/gpt_deep_research/deep_research_d707_bounded_formal_note_v0_draft_report38_20260707.md`
4. `docs/infra/gpt_deep_research/D707_BOUNDED_FORMAL_NOTE_V0_DRAFT_REPORT38_ADOPTION_NOTE_20260707.md`
5. `docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md`

Then inspect the source chain:

- report37 and its adoption note;
- D707 v0 revision taskbook;
- Loop0 claim ledger and forbidden-claims checklist;
- Loop3 typed definitions and composition lemma;
- Loop4 cycle definitions, telescoping proof, norm bounds, and boundary guards;
- Session4 main handoff, open blockers, and SubPro A/E prompts;
- latest RAG record.

## Required Review Questions

Pro must answer all of the following:

1. Are all chart, path, and cycle domains/codomains correct?
2. Is the empty-path convention coherent?
3. Is the path-defect composition lemma correct?
4. Is the cycle telescoping proof correct for every finite `n>=1`?
5. Is the finite-horizon global norm bound correct?
6. Is the restricted-norm caveat sufficient?
7. Does any line incorrectly replace global `||Delta_gamma||` with
   `||Delta_gamma|_S||` without image-control or invariance?
8. Does the note overclaim novelty, public readiness, broad theory, or empirical
   meaning?
9. Does the note need prior-art/triviality language strengthened?
10. Is the right next action to keep, patch, reject, or stop-park this internal
    v0 note?

## Allowed Verdicts

Pro must choose exactly one:

```text
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY
PATCH_INTERNAL_V0_THEN_RECHECK
REJECT_OR_STOP_PARK
REQUEST_NODE36_FILES
```

Meaning:

- `ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY`: the note is safe as an internal
  bounded formal note only; no public/paper/NMI upgrade.
- `PATCH_INTERNAL_V0_THEN_RECHECK`: the note has fixable math, notation, or
  boundary issues; list exact patches.
- `REJECT_OR_STOP_PARK`: the note is too trivial, too duplicative, too
  ambiguous, or too risky even as an internal note.
- `REQUEST_NODE36_FILES`: the package is missing required local evidence; list
  exact file paths or content classes.

## Forbidden Outputs

Pro must not:

- write a paper;
- claim public-ready, paper-ready, submission-ready, or NMI-ready status;
- upgrade Mode B beyond `insufficient_artifact`;
- claim MaoField empirical-positive results;
- claim observed residual, interaction, transport, holonomy, gluing, or collapse
  fields;
- claim black-box mechanism solved;
- claim dynamic-collapse theory;
- claim broad ANOVA, dependent-input, projection, sheaf, contextuality, or
  path-closure theory;
- treat RAG, JSON, harness, prompt, handoff, manifest, or model output as proof.

## Expected Output Shape

Pro should produce:

1. The exact verdict.
2. A line-by-line finite-math audit.
3. A boundary/overclaim audit.
4. Prior-art/triviality risk assessment.
5. Exact blockers, if any.
6. Exact patch instructions, if any.
7. Minimal safe wording for the note, if accepted.
8. A final recommendation among:

```text
KEEP_INTERNAL_ONLY
PATCH_AND_RECHECK
STOP_PARK
REQUEST_MORE_FILES
```
