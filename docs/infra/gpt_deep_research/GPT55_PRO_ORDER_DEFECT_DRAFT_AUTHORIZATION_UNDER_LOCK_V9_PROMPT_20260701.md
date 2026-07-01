# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Draft Authorization Under Lock V9

Use the uploaded zip as the only evidence bundle. Do not use public web
browsing, public GitHub pages, raw.githubusercontent.com, search-engine
results, GitHub connector content outside the uploaded bundle, or memory of
previous chats. If the zip is missing or unreadable, stop and say
`INSUFFICIENT_BUNDLE`.

You are an external, non-authoritative audit model. Node36 keeps final
authority. Your output is advisory only and must not be treated as proof
authority, bibliography authority, paper-ready authority, or posting authority.

## Current Task

The previous V8 human-decision audit returned:

```text
HUMAN_DECISION_UNDER_LOCK_ACCEPTED
```

Node36 adopted this only as:

```text
ASK_PI_FOR_SEPARATE_DRAFT_AUTHORIZATION_UNDER_LOCK
```

Your task is to help the human PI decide whether to authorize a separate future
boundary-locked short-note drafting prompt. This V9 task is still not a paper
drafting task.

Do not draft a paper body. Do not write an abstract. Do not write introduction
prose. Do not write theorem exposition for a paper. Do not write proof prose
for a paper. Do not claim that the emergency lock is lifted.

Current live state remains:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
KEEP_LOCK_AND_FIX
LOCKED_NO_PAPER_BODY
```

## First Package Checks

Before substantive analysis:

1. read `PACKAGE_README.md`;
2. inspect `SHA256SUMS.txt` and `PACKAGE_FILE_MANIFEST.sha256`;
3. confirm the bundle contains report(13):

```text
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_human_decision_v8_report13_20260701.md
```

4. confirm the bundle contains the report(13) adoption note:

```text
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_HUMAN_DECISION_V8_REPORT13_ADOPTION_NOTE_20260701.md
```

5. confirm the bundle contains the V9 taskbook, V9 prompt, and V9 package record:

```text
from_repo/docs/infra/recovery/ORDER_DEFECT_D701_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_TASKBOOK_20260701.md
from_repo/docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_PROMPT_20260701.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_20260701.md
```

If any required file is missing, return `INSUFFICIENT_BUNDLE`.

Do not infer missing file contents.

## Read These Files First

Read these files in order from the uploaded zip:

```text
PACKAGE_README.md
SHA256SUMS.txt
PACKAGE_FILE_MANIFEST.sha256
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_human_decision_v8_report13_20260701.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_HUMAN_DECISION_V8_REPORT13_ADOPTION_NOTE_20260701.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D701_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_TASKBOOK_20260701.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_20260701.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md
from_repo/docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_HUMAN_DECISION_UNDER_LOCK_V8_PROMPT_20260630.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_HUMAN_DECISION_UNDER_LOCK_V8_20260630.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_proof_repair_recheck_report9_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_LOCAL_DRAFT_LOCKED_TASKBOOK_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md
from_repo/docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md
```

## Mathematical Object Boundary

Audit only this finite-dimensional object:

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
- order-defect operator `D_w = R_Q_then_B - R_B_then_Q`.

Do not generalize this into a broad ANOVA theory, a broad dependent-input
decomposition theory, a broad noncommuting-projection theory, a sheaf/holonomy
theory, or a MaoField empirical result.

## Correct Live Labels

Audit whether all current live files preserve exactly these labels:

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall paper status: LOCKED_NO_PAPER_BODY
Mode B MaoField empirical status: insufficient_artifact
```

## Authorization-Gate Questions

Answer with file and line references where possible:

1. Does report(13) validly support asking the PI for a separate future drafting
   authorization under lock?
2. Is there any remaining package identity, status-chain, RAG-locator, proof,
   bibliography, or forbidden-claim blocker that should prevent asking for
   authorization?
3. Are Proposition 1/2/3 still only local-draft claims inside the controlled
   finite weighted two-way-table object?
4. Is the exact 2 x 2 witness correctly limited to `CERTIFICATE`?
5. Is the deterministic floating-point harness correctly limited to
   `HARNESS_ONLY`?
6. Is bibliography/positioning still conservative enough, including duplicate
   risk and online/publisher metadata caveats?
7. Are forbidden claims absent as endorsed claims, even if listed in negative
   scan contexts?
8. If favorable, what exact decision should the PI make, and what exact
   boundaries must bind the later separate drafting prompt?
9. If unfavorable, what exact patch must happen before authorization?

## Forbidden Claims

Do not write or endorse any of the following:

```text
paper body drafted
paper-ready
preprint-ready
posted
emergency lock lifted
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

Return a concise audit report with this structure:

1. `Verdict`: choose exactly one:

```text
DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED
PATCH_PROOF_BIBLIO_OR_PACKAGE_BEFORE_AUTHORIZATION
STOP_DO_NOT_DRAFT
INSUFFICIENT_BUNDLE
```

2. `Package and Status Chain`: whether the V9 bundle and status files are
   coherent.

3. `Authorization Basis`: whether report(13) and the canonical evidence support
   asking the PI for a separate future drafting authorization.

4. `Proof Boundary`: Proposition 1/2/3 status and any proof gap that blocks
   authorization.

5. `Certificate and Harness Boundary`: exact witness and deterministic harness
   roles.

6. `Bibliography and Duplicate Risk`: conservative status and what not to
   claim.

7. `Forbidden-Claim Scan`: any risky wording found in the controlled bundle.

8. `PI Decision Memo`: a short decision memo for the human PI. It may list
   allowed claims, forbidden claims, risks, and decision options. It must not
   contain paper prose.

9. `Future Drafting Prompt Constraints`: if and only if the verdict is
   `DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED`, provide constraints for a later
   separate drafting prompt. Do not write that prompt's paper content.

10. `Remaining Blockers`: exact files and line references. If none, say
    `no draft-authorization blocker found; emergency lock still active`.

11. `Recommended Node36 Action`: choose one:

```text
ASK_PI_TO_AUTHORIZE_SEPARATE_BOUNDARY_LOCKED_DRAFTING_PROMPT
PATCH_FIRST_THEN_RECHECK
STOP_DO_NOT_DRAFT
```

## Final Reminder

This is an authorization-gate session, not a drafting session. If you find
yourself writing publishable paragraphs, stop and replace them with a claim
ledger or a decision memo.
