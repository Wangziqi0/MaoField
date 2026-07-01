# Order-Defect D701 PI Decision And English Rewrite Gate V12 Taskbook

Date: 2026-07-01 CST
Node: node36
Previous package: `MaoField_PRO_OrderDefect_BoundaryLockedDraftReview_V11_FIX_20260701_1352.zip`
Previous Pro verdict: `DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW`
Node36 local action: `PREPARE_PI_DECISION_AND_ENGLISH_REWRITE_GATE_V12`

## Purpose

V12 is not a release gate. V12 prepares a zero-context Pro review package for a
human PI decision under lock:

1. Should the current Chinese local draft candidate remain only a local review
   artifact?
2. Should node36/PI authorize a boundary-locked English short-note rewrite
   candidate for local review?
3. What exact hygiene, wording, proof, and duplicate-risk constraints must be
   preserved before any further drafting?

## Inputs

Required current inputs:

- report(16): `deep_research_order_defect_draft_candidate_review_v11_report16_20260701.md`
- report(16) adoption note:
  `ORDER_DEFECT_DRAFT_CANDIDATE_REVIEW_V11_REPORT16_ADOPTION_NOTE_20260701.md`
- path hygiene note:
  `ORDER_DEFECT_REPORT15_PATH_HYGIENE_NOTE_20260701.md`
- report(15) local draft candidate and report(15) adoption note
- V11 taskbook, V11 prompt, and V11 package record
- formal notes, proof-repair candidate, exact witness, deterministic harness,
  wording lock, bibliography, recovery audits, and forbidden-claim scan
- `STATE.md` and `MD_CATALOG.md`

## Hard Boundaries

V12 must not:

- lift the emergency lock;
- call anything paper-ready, preprint-ready, posted, submission-authorized, or
  public-use ready;
- promote Pro into proof authority, bibliography authority, posting authority,
  or submission authority;
- upgrade Mode B beyond `insufficient_artifact`;
- claim full panel, checkpoint inference, training, new loss, observed residual,
  observed interaction, observed transport, observed holonomy, F3 positive,
  LOSO passed, glass-box broken, or completed formal system;
- treat deterministic harness or JSON floats as proof.

## Required Output From Next Pro

The next Pro review should return one recommendation:

```text
RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
RECOMMEND_MINOR_HYGIENE_PATCH_THEN_PI_LOCAL_REVIEW
RECOMMEND_BOUNDARY_LOCKED_ENGLISH_REWRITE_CANDIDATE
RECOMMEND_STOP_OR_PARK
INSUFFICIENT_BUNDLE
```

If it recommends an English rewrite candidate, the candidate must be explicitly
marked:

```text
BOUNDARY_LOCKED_ENGLISH_DRAFT_CANDIDATE_FOR_NODE36_PI_LOCAL_REVIEW_ONLY
```

This label still means not paper-ready, not preprint-ready, not posted, and not
submission-authorized.

## Human PI Questions To Preserve

Ask the human PI to decide after V12:

1. preferred path: local Chinese review only, English rewrite candidate under
   lock, or park the note because duplicate risk is too high;
2. preferred tone if English rewrite is authorized: terse theorem note,
   methodological cautionary note, or appendix-style certificate note;
3. tolerance for `MEDIUM duplicate risk`: proceed narrowly, wait for more
   bibliography review, or stop.
