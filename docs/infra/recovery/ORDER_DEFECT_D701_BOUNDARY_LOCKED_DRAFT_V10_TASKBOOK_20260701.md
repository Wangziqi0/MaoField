# Order-Defect D701 Boundary-Locked Draft V10 Taskbook

Date: 2026-07-01 CST
Authority: node36
Task class: local short-note draft candidate under lock

## Current Verdict Chain

```text
report(12): POST_V6_DECISION_GATE_ACCEPTED_KEEP_LOCK
report(13): HUMAN_DECISION_UNDER_LOCK_ACCEPTED
report(14): DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED
node36 local action: PREPARE_SEPARATE_BOUNDARY_LOCKED_SHORT_NOTE_DRAFTING_PROMPT
```

The emergency lock remains active. V10 only prepares a package and prompt for a
separate external model to draft a local short-note candidate under lock.

## Live Labels

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall status: BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY
Mode B MaoField empirical status: insufficient_artifact
```

## Mathematical Boundary

V10 may only discuss this finite-dimensional object:

- finite positive weighted two-way table `X = Q x B`;
- weighted Hilbert space with inner product `<f,g>_w`;
- constant subspace `C`;
- centered row/main-effect space `A`;
- centered column/main-effect space `B0`;
- additive nuisance space `N_add = C + A + B0`;
- weighted orthogonal projections onto these subspaces;
- ordered stripping operators
  `R_Q_then_B = (I-P_B0)(I-P_A)(I-P_C)` and
  `R_B_then_Q = (I-P_A)(I-P_B0)(I-P_C)`;
- order-defect operator `D_w = R_Q_then_B - R_B_then_Q`;
- exact 2 x 2 rational witness with norm value `61/177408`.

## Safe Draft Scope

If package checks pass, V10 may ask Pro for a local short-note draft candidate
containing:

- title and abstract, explicitly marked local draft candidate;
- setup and notation for the finite weighted table only;
- propositions with `COMPLETE_LOCAL_DRAFT` labels;
- proof sketches tied to the local proof files, not to Pro authority;
- exact 2 x 2 witness section;
- deterministic harness boundary section;
- related-work and duplicate-risk section;
- limitations and forbidden-claim ledger;
- final node36/PI decision checklist.

The draft must remain local and locked. It must not call itself ready for
posting, submission, arXiv, journal upload, or public release.

## Required First Checks In V10 Prompt

The Pro model must first read:

```text
PACKAGE_README.md
SHA256SUMS.txt
PACKAGE_FILE_MANIFEST.sha256
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_draft_authorization_v9_report14_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md
```

If any required file is missing or unreadable, it must return:

```text
INSUFFICIENT_BUNDLE
```

## Forbidden Outputs

V10 must not output or endorse:

```text
emergency lock lifted
paper-ready
preprint-ready
posted
submission authorized
completed formal system
broad new ANOVA theory
broad new dependent-input decomposition theory
broad new noncommuting-projection theory
MaoField empirical positive result
full panel has run
16-cell aggregate exists
checkpoint loading
inference
training
new loss
MaoField residual observed
interaction observed
quotient-residual observed
transport field observed
holonomy field observed
glass box broken
F3 positive
LOSO passed
JSON floats prove theorem
harness proves theorem
```

## Accepted V10 Outcomes

The Pro model must choose exactly one:

```text
BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE
PATCH_BEFORE_LOCAL_DRAFT
STOP_DO_NOT_DRAFT
INSUFFICIENT_BUNDLE
```

Only the first outcome may include local draft prose. Even then, the output
must include an explicit boundary ledger and a final statement that node36 and
the human PI keep final authority.

## Nonblocking Hygiene Risk

Report(14) identified stale line references inside archived report(13) to V9
`PACKAGE_README.md`. This is not a blocker for V10 because the current
authorization basis is independently carried by primary files. V10 should not
cite those stale line references as proof.
