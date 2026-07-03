# GPT-5.5 Pro Zero-Context Prompt: MaoField Final Preprint Review V2.4

Use the uploaded zip as your only project evidence bundle. Do not use public
GitHub pages, raw.githubusercontent.com, search-engine results, or memory of
previous chats as evidence for the private/local MaoField repository. You may
use external scholarly sources only to spot-check bibliography metadata, and
you must mark any such external checks separately from bundle facts.

If the zip is missing, unreadable, or internally inconsistent, stop and return:

```text
INSUFFICIENT_BUNDLE
```

You are an external reviewer. Node36 and the human PI retain final authority.
Your output is not proof authority, bibliography authority, paper-ready
authority, posting authority, release authority, or submission authority.

## Current Task

Review the V2.4 under-lock preprint source:

```text
from_repo/docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_4_UNDER_LOCK_20260703.tex
```

The author metadata requested by the PI is:

```text
陈一凡 / Yifan Chen
```

The selected title is:

```text
Finite Projection Order Defects in Residual Metric Audits: A Mathematical Starting Point for Black-Box Evaluation
```

Your job is to decide whether this V2.4 source is acceptable for a final human
PI local release decision under lock, and to identify any required edits before
public release can even be considered.

## First Package Checks

Before reviewing the manuscript, verify that the bundle contains:

```text
PACKAGE_README.md
PACKAGE_FILE_LIST.txt
SHA256SUMS.txt
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_4_UNDER_LOCK_20260703.tex
from_repo/docs/infra/recovery/FORMAL_PREPRINT_V2_4_AUTHOR_TITLE_RELEASE_TASKBOOK_20260703.md
from_repo/docs/infra/recovery/BIBLIOGRAPHY_FINAL_METADATA_AUDIT_20260703.md
from_repo/docs/infra/recovery/FINAL_DUPLICATE_RISK_AND_FORBIDDEN_CLAIMS_REVIEW_20260703.md
```

If any of these are missing, return `INSUFFICIENT_BUNDLE`.

## Read These Files First

Read these files before judging the manuscript:

```text
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/AGENTS.md
from_repo/CLAUDE.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_4_UNDER_LOCK_20260703.tex
from_repo/docs/infra/recovery/FORMAL_PREPRINT_V2_4_AUTHOR_TITLE_RELEASE_TASKBOOK_20260703.md
from_repo/docs/infra/recovery/BIBLIOGRAPHY_FINAL_METADATA_AUDIT_20260703.md
from_repo/docs/infra/recovery/FINAL_DUPLICATE_RISK_AND_FORBIDDEN_CLAIMS_REVIEW_20260703.md
from_repo/docs/infra/gpt_deep_research/deep_research_formal_preprint_v2_2_strict_review_report23_20260703.md
from_repo/docs/infra/gpt_deep_research/FORMAL_PREPRINT_V2_2_STRICT_REVIEW_REPORT23_ADOPTION_NOTE_20260703.md
from_repo/docs/infra/recovery/FORMAL_PREPRINT_V2_2_REPORT23_LOCAL_VERIFICATION_20260703.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md
```

The package may include the uploaded V2.3 source/PDF as provenance only. The
V2.3 PDF is stale after V2.4 source edits and must not be treated as the final
V2.4 PDF.

## Mathematical Boundary

Review only the finite-dimensional object:

- finite positive weighted two-way table `X = Q x B`;
- weighted Hilbert space `L^2(w)`;
- constant subspace `C`;
- centered row-main-effect space `A`;
- centered column-main-effect space `B0`;
- additive nuisance space `N_add = C + A + B0`;
- weighted orthogonal projections;
- ordered stripping maps
  `R_Q_then_B = (I-P_B0)(I-P_A)(I-P_C)` and
  `R_B_then_Q = (I-P_A)(I-P_B0)(I-P_C)`;
- order-defect operator `D_w = R_Q_then_B - R_B_then_Q`;
- exact 2 x 2 rational witness with squared weighted norm `61/177408`.

Do not generalize this into a broad ANOVA theory, a broad dependent-input
decomposition theory, a broad noncommuting-projection theory, a sheaf/holonomy
theory, a transport-field theory, or a MaoField empirical result.

## Required Review Questions

Audit V2.4 for:

1. correctness of the product-weight iff `A` orthogonal to `B0` statement;
2. correctness of order-independence iff product weights;
3. whether the non-product witness is existential, not universal;
4. whether the manuscript distinguishes true additive residual
   `(I-P_N_add)K` from wrong-order sequential output;
5. whether the exact witness and `61/177408` norm are used correctly;
6. whether the deterministic harness is treated only as regression support;
7. whether author/title metadata are acceptable for a final PI local decision;
8. whether bibliography metadata, especially Böttcher/Boettcher/Bottcher,
   Lamboni 2026, Il Idrissi 2025, and arXiv version metadata, are acceptable;
9. whether duplicate risk remains `MEDIUM duplicate risk`;
10. whether the release-position language correctly blocks public release until
    human/admin action;
11. whether the MaoField programme section is phrased as future work only;
12. whether the manuscript contains any forbidden or overbroad claim.

## Forbidden Claims

Do not write or endorse any of the following:

```text
paper-ready
preprint-ready
posted
submitted
public-postable
submission-authorized
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
duplicate risk is low
no close work exists
```

## Required Output

Return exactly one verdict:

```text
ACCEPT_FOR_HUMAN_PI_LOCAL_RELEASE_DECISION_UNDER_LOCK
PATCH_V2_4_BEFORE_HUMAN_PI_LOCAL_RELEASE_DECISION
DO_NOT_RELEASE_EVIDENCE_OR_WORDING_BLOCKER
INSUFFICIENT_BUNDLE
```

If you choose `ACCEPT_FOR_HUMAN_PI_LOCAL_RELEASE_DECISION_UNDER_LOCK`, include:

- concise mathematical audit;
- remaining soft risks;
- exact public-release checklist for the human PI;
- a statement that this is still not paper-ready, preprint-ready, posted,
  submitted, public-postable, or submission-authorized.

If you choose `PATCH_V2_4_BEFORE_HUMAN_PI_LOCAL_RELEASE_DECISION`, give exact
line-level required edits and do not rewrite outside the stated boundary.

If you choose `DO_NOT_RELEASE_EVIDENCE_OR_WORDING_BLOCKER`, list only blockers
and evidence paths.

End with:

```text
This is a final zero-context review for a V2.4 under-lock local draft only. Node36 and the human PI retain final authority. No public release or submission is authorized by this review.
```
