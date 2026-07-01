# Order-Defect D701 Boundary-Locked Draft Review V11 Taskbook

Date: 2026-07-01 CST
Authority: node36
Task class: review of local short-note draft candidate under lock

## Current Verdict Chain

```text
report(12): POST_V6_DECISION_GATE_ACCEPTED_KEEP_LOCK
report(13): HUMAN_DECISION_UNDER_LOCK_ACCEPTED
report(14): DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED
report(15): BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE
node36 local action: RECEIVE_LOCAL_DRAFT_CANDIDATE_UNDER_LOCK_PREPARE_V11_REVIEW
```

The emergency lock remains active. V11 reviews report(15)'s local draft
candidate. It does not convert the candidate into a paper, preprint, public
release, or submission.

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

## V11 Purpose

V11 must perform a strict review of report(15)'s draft candidate:

1. verify the package and manifest context;
2. verify that report(15)'s boundary labels were preserved;
3. check every mathematical proposition against the primary proof files;
4. check the exact witness values and role;
5. check that the deterministic harness is not treated as proof;
6. check bibliography and duplicate-risk wording;
7. scan for forbidden or overbroad claims;
8. identify required patches before any local PI paper decision.

## Mathematical Boundary

V11 may only discuss this finite-dimensional object:

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

V11 must not generalize this into a broad ANOVA theory, a broad
dependent-input decomposition theory, a broad noncommuting-projection theory,
a sheaf/holonomy theory, or a MaoField empirical result.

## Required V11 Checks

The review must answer:

- Does report(15) keep the object finite, weighted, positive, and two-way?
- Does it keep the propositions at `COMPLETE_LOCAL_DRAFT`, not proven-public
  or final-submission status?
- Does it preserve the existential quantifier in the non-product witness claim?
- Does it describe wrong-order output as a sequential stripping artifact, not a
  true interaction residual?
- Does it avoid treating JSON floats or deterministic harness outputs as
  theorem proof?
- Does it preserve `MEDIUM duplicate risk` for bibliography/positioning?
- Does it avoid MaoField empirical upgrades and all Mode B claims?
- Does it preserve the final lock disclaimer?

## Accepted V11 Outcomes

The Pro model must choose exactly one:

```text
DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW
PATCH_DRAFT_CANDIDATE_BEFORE_LOCAL_REVIEW
STOP_DO_NOT_USE_DRAFT
INSUFFICIENT_BUNDLE
```

If the verdict is `DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW`, it
must still say that this is only a local review status, not paper-ready,
preprint-ready, posted, or submission-authorized.

If the verdict is `PATCH_DRAFT_CANDIDATE_BEFORE_LOCAL_REVIEW`, it may provide a
patched local draft candidate only if every patch stays within the boundary.

If the verdict is `STOP_DO_NOT_USE_DRAFT`, it must list exact blockers and
avoid rewriting the draft.

## Forbidden Outputs

V11 must not output or endorse:

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

## Node36 Decision Rule

Even if V11 returns `DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW`,
node36 must treat that only as an input to local PI review. Any public paper,
preprint, arXiv, journal, or release action requires a later explicit human
decision and a fresh gate.
