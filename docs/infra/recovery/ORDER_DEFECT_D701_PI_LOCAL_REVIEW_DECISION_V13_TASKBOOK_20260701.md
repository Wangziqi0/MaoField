# Order-Defect D701 PI Local Review Decision V13 Taskbook

Date: 2026-07-01 CST
Node: node36
Previous package: `MaoField_PRO_OrderDefect_PIDecisionEnglishRewriteGate_V12_FINAL_20260701_1810.zip`
Previous Pro verdict: `RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`
Node36 local action: `PREPARE_PI_LOCAL_REVIEW_DECISION_V13`

## Purpose

V13 is not a release gate and not an English drafting gate. V13 prepares a
zero-context Pro review package for a human PI local-review decision under
lock:

1. confirm that report(15) remains only a Chinese locked local-review artifact;
2. preserve the exact mathematical and evidence boundaries before PI review;
3. make explicit what the human PI must decide before any future English rewrite
   gate exists;
4. prevent path-hygiene, duplicate-risk, harness/proof, and forbidden-claim
   drift.

## Inputs

Required current inputs:

- report(17): `deep_research_order_defect_pi_decision_gate_v12_report17_20260701.md`
- report(17) adoption note:
  `ORDER_DEFECT_PI_DECISION_V12_REPORT17_ADOPTION_NOTE_20260701.md`
- report(16) and report(16) adoption note
- report(15) local draft candidate, report(15) adoption note, and path hygiene
  note
- V12 taskbook, V12 prompt, and V12 package record
- formal notes, proof-repair candidate, exact witness, deterministic harness,
  wording lock, bibliography, recovery audits, and forbidden-claim scan
- `STATE.md` and `MD_CATALOG.md`

## Hard Boundaries

V13 must not:

- lift the emergency lock;
- call anything paper-ready, preprint-ready, posted, submission-authorized, or
  public-use ready;
- produce an English paper draft or English short-note rewrite candidate;
- promote Pro into proof authority, bibliography authority, posting authority,
  or submission authority;
- upgrade Mode B beyond `insufficient_artifact`;
- claim full panel, checkpoint inference, training, new loss, observed residual,
  observed interaction, observed transport, observed holonomy, F3 positive,
  LOSO passed, glass-box broken, or completed formal system;
- treat deterministic harness or JSON floats as proof;
- soften `MEDIUM duplicate risk`.

## Required Output From Next Pro

The next Pro review should return exactly one recommendation:

```text
CONFIRM_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
REQUEST_HYGIENE_PATCH_BEFORE_PI_LOCAL_REVIEW
RECOMMEND_SEPARATE_ENGLISH_REWRITE_GATE_AFTER_PI_CHOICE
RECOMMEND_PARK_OR_STOP
INSUFFICIENT_BUNDLE
```

The next Pro review must not provide an English draft. If it recommends a
future English rewrite gate, it must say that a separate PI authorization and a
separate package are required.

## Human PI Questions To Preserve

Ask the human PI to decide after V13:

1. keep report(15) as Chinese locked local review only, or authorize a later
   separate English rewrite gate;
2. if a later English rewrite gate is authorized, choose terse theorem note,
   methodological cautionary note, or appendix-style certificate note;
3. decide whether `MEDIUM duplicate risk` allows narrow proceed, requires more
   bibliography review first, or means stop/park.
