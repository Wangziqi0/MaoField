# Order-Defect D703 Formal Preprint Draft Gate Taskbook

Date: 2026-07-03 CST
Node: node36
Previous current state: `PI_LOCAL_REVIEW_ONLY_KEEP_LOCK_CONFIRMED`
New local action: `PREPARE_FORMAL_PREPRINT_DRAFT_GATE_UNDER_LOCK`
Source report: `docs/infra/gpt_deep_research/deep_research_order_defect_english_preprint_candidate_v1_report20_20260703.md`
Node36 adoption note: `docs/infra/gpt_deep_research/ORDER_DEFECT_ENGLISH_PREPRINT_CANDIDATE_V1_REPORT20_ADOPTION_NOTE_20260703.md`

## Purpose

This taskbook opens a local formal preprint drafting gate for the narrow
order-defect note. It is a drafting gate, not a public-release gate.

The gate exists because report(20) produced a narrow English V1 candidate for
local review and did not identify a mathematical hard blocker inside the finite
positive weighted two-way-table object. The next step is to transform that
candidate into a clean standalone draft while preserving every evidence and
wording boundary.

## Inputs

Required current inputs:

- `STATE.md`
- `MD_CATALOG.md`
- report(20) and this adoption note
- report(18) adoption note
- report(17) path-hygiene rule
- `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`
- `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md`
- `docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`
- `docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`
- `scripts/debranded_residual_transport_exact_witness_v1_4.py`
- `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`
- `docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`
- `scripts/debranded_residual_transport_harness_v1_3.py`
- `docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`
- `docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`
- `docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT15_PATH_HYGIENE_NOTE_20260701.md`

## Drafting Objective

Produce a standalone English draft candidate with this working title:

```text
Order Defect in Sequential Main-Effect Stripping for Finite Positive Weighted Two-Way Tables
```

The draft should target a compact 4-6 page mathematical note plus an exact
certificate appendix. It should be written as a finite-dimensional cautionary
artifact note, not as a broad theory paper.

## Required Mathematical Spine

The draft must contain:

1. finite positive weighted table setup `X = Q x B`;
2. weighted inner product and marginal definitions;
3. constant, row-main-effect, and column-main-effect spaces `C`, `A`, and
   `B0`;
4. additive nuisance space `N_add = C + A + B0`;
5. Proposition 1: product weights iff `A` is orthogonal to `B0`;
6. Proposition 2: order-independence iff product weights;
7. Proposition 3: for non-product weights, an existential pure-main-effect
   witness can generate a nonzero wrong-order sequential artifact while the
   true additive residual remains zero;
8. the exact `2 x 2` rational witness with
   `||R_Q_then_B K||_w^2 = 61/177408`;
9. a short related-work and duplicate-risk section anchored to
   `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`;
10. the canonical harness-boundary sentence:

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

## Hard Boundaries

The draft gate must not:

- call the result paper-ready, preprint-ready, posted, submitted, or
  submission-authorized;
- promote external model reports to proof authority or bibliography authority;
- treat deterministic harness output or JSON floats as proof;
- claim a broad new ANOVA theory, broad dependent-input decomposition theory,
  or broad noncommuting-projection theory;
- claim MaoField empirical evidence, full panel, checkpoint inference,
  training, new loss, observed residual, observed interaction, observed
  transport, observed holonomy, F3 positive, LOSO passed, glass-box broken, or
  completed formal system;
- use report(15)'s archived `/tmp/orderdefect_v10/rerun/harness.json` path in
  draft-facing or package-facing text;
- soften `MEDIUM duplicate risk`;
- change Mode B beyond `insufficient_artifact`.

## Required Local Checks Before Any Release Gate

Before any later release/preprint gate exists, node36 must run and archive:

1. exact witness rerun under `/home/amd/codex-node36/tmp/<task>/`;
2. deterministic harness rerun under `/home/amd/codex-node36/tmp/<task>/`;
3. forbidden-claims scan over the standalone draft;
4. bibliography metadata spot-check;
5. source-map check from draft claims to canonical files;
6. RAG refresh and smoke queries after the draft candidate is promoted to
   canonical.

## Allowed Next Outputs

The next local pass may output exactly one of:

```text
STANDALONE_PREPRINT_DRAFT_CANDIDATE_UNDER_LOCK
REQUEST_BIBLIOGRAPHY_PATCH_BEFORE_DRAFT
REQUEST_PROOF_WORDING_PATCH_BEFORE_DRAFT
STOP_OR_PARK_DRAFT_GATE
```

None of these outputs authorizes public posting or submission by itself.
