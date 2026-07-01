# GPT-5.5 Pro Zero-Context Prompt: PI Decision And English Rewrite Gate V12

Use the uploaded zip as the only evidence bundle. Do not use public web
browsing, public GitHub pages, raw.githubusercontent.com, search-engine
results, GitHub connector content outside the uploaded bundle, or memory of
previous chats. If the zip is missing or unreadable, stop and say
`INSUFFICIENT_BUNDLE`.

You are an external, non-authoritative reviewer. Node36 and the human PI retain
final authority. Your output is not proof authority, bibliography authority,
paper-ready authority, posting authority, or submission authority.

## Current Task

The previous V11 review returned:

```text
DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW
```

Node36 adopts this only as:

```text
DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW_BUT_KEEP_LOCK
```

Your V12 task is to help node36 and the human PI make a locked local decision:

1. keep report(15) as a Chinese local-review artifact only;
2. request minor hygiene patches before PI review;
3. recommend a boundary-locked English short-note rewrite candidate for local
   review only; or
4. stop/park the note because the residual risks are too high.

You must not claim the draft is paper-ready, preprint-ready, posted,
submission-authorized, release-approved, or ready for public use.

## First Package Checks

Before reviewing or rewriting any prose, read and verify these files:

```text
PACKAGE_README.md
SHA256SUMS.txt
PACKAGE_FILE_MANIFEST.sha256
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_draft_candidate_review_v11_report16_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_CANDIDATE_REVIEW_V11_REPORT16_ADOPTION_NOTE_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT15_PATH_HYGIENE_NOTE_20260701.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D701_PI_DECISION_AND_ENGLISH_REWRITE_GATE_V12_TASKBOOK_20260701.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PI_DECISION_ENGLISH_REWRITE_GATE_V12_20260701.md
```

If any required file is missing, unreadable, or inconsistent with the claimed
V12 task, return exactly:

```text
INSUFFICIENT_BUNDLE
```

Do not infer missing file contents.

## Read These Files Before Judgment

Read these files in order:

```text
PACKAGE_README.md
SHA256SUMS.txt
PACKAGE_FILE_MANIFEST.sha256
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_draft_candidate_review_v11_report16_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_CANDIDATE_REVIEW_V11_REPORT16_ADOPTION_NOTE_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT15_PATH_HYGIENE_NOTE_20260701.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D701_PI_DECISION_AND_ENGLISH_REWRITE_GATE_V12_TASKBOOK_20260701.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_boundary_locked_draft_v10_report15_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_V10_REPORT15_ADOPTION_NOTE_20260701.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_TASKBOOK_20260701.md
from_repo/docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_PROMPT_20260701.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_proof_repair_recheck_report9_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md
from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md
from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md
from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md
from_repo/docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md
```

## Mathematical Object Boundary

Review only this finite-dimensional object:

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
- exact `2 x 2` rational witness.

Do not generalize this into a broad ANOVA theory, a broad dependent-input
decomposition theory, a broad noncommuting-projection theory, a sheaf/holonomy
theory, or a MaoField empirical result.

## Required Live Labels

Preserve these labels exactly:

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

## Required Review

Audit the report(16) acceptance and the report(15) local draft candidate for:

1. whether node36/PI local review can proceed under lock;
2. whether the `/tmp/orderdefect_v10/rerun/harness.json` reference must be
   replaced by stable bundle paths before any local rewrite;
3. whether an English short-note rewrite candidate is advisable, or whether the
   duplicate-risk and boundary overhead make it wiser to stop/park;
4. mathematical correctness of Proposition 1, Proposition 2, and Proposition 3;
5. preservation of existential, not universal, wording for the non-product
   pure-main-effect witness;
6. correct distinction between true additive residual `(I-P_N)K` and
   wrong-order sequential stripping output;
7. exact `2 x 2` witness values, including `61/177408`;
8. deterministic harness being treated as regression support only;
9. bibliography/positioning staying at `MEDIUM duplicate risk`;
10. absence of all forbidden claims.

## Forbidden Claims

Do not write or endorse any of the following:

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

## Required Output

Return exactly one recommendation:

```text
RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
RECOMMEND_MINOR_HYGIENE_PATCH_THEN_PI_LOCAL_REVIEW
RECOMMEND_BOUNDARY_LOCKED_ENGLISH_REWRITE_CANDIDATE
RECOMMEND_STOP_OR_PARK
INSUFFICIENT_BUNDLE
```

Then include:

- a concise reasoned audit;
- remaining hard blockers, if any;
- remaining soft risks;
- a PI decision checklist;
- three short questions for the human PI about the draft direction and style.

If and only if you choose
`RECOMMEND_BOUNDARY_LOCKED_ENGLISH_REWRITE_CANDIDATE`, you may provide a
boundary-locked English short-note rewrite candidate for node36/PI local review
only. It must be rewritten from the formal notes, exact witness, harness
boundary, and bibliography files, not translated line-by-line from report(15).
Label it exactly:

```text
BOUNDARY_LOCKED_ENGLISH_DRAFT_CANDIDATE_FOR_NODE36_PI_LOCAL_REVIEW_ONLY
```

If you provide such a candidate, also provide:

- a one-paragraph scope statement;
- theorem statements with the same narrow labels;
- proof sketches tied to the listed files;
- exact witness summary;
- harness disclaimer using the canonical wording-lock sentence;
- bibliography positioning paragraph that keeps `MEDIUM duplicate risk`;
- a forbidden-claim self-scan.

End by stating:

```text
This remains a boundary-locked PI decision and local rewrite gate only. Node36
and the human PI retain final authority. This is not paper-ready,
preprint-ready, posted, or submission-authorized.
```
