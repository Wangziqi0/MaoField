# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Human Decision Under Lock V8

Use the uploaded zip as the only evidence bundle. Do not use public web
browsing, public GitHub pages, raw.githubusercontent.com, search-engine
results, GitHub connector content outside the uploaded bundle, or memory of
previous chats. If the zip is missing or unreadable, stop and say
`INSUFFICIENT_BUNDLE`.

You are an external, non-authoritative audit model. Node36 keeps final
authority. Your output is advisory only and must not be treated as proof
authority, bibliography authority, paper-ready authority, or posting authority.

## Current Task

The previous V7 decision-gate audit returned:

```text
POST_V6_DECISION_GATE_ACCEPTED_KEEP_LOCK
```

Node36 adopted this only as:

```text
PREPARE_HUMAN_DECISION_UNDER_LOCK
```

Your task is to help prepare the human PI decision under the still-active
emergency lock. Decide whether the materials support asking the human PI to
authorize a separate future boundary-locked short-note drafting prompt, or
whether more proof, bibliography, package, status, or boundary repair is still
needed first.

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
3. confirm the bundle contains report(12):

```text
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md
```

4. confirm the bundle contains the report(12) adoption note:

```text
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md
```

5. confirm the bundle contains the V8 taskbook and V8 package record:

```text
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_HUMAN_DECISION_UNDER_LOCK_V8_20260630.md
```

If any required file is missing, return
`PATCH_PACKAGE_OR_STATUS_BEFORE_HUMAN_DECISION`.

Do not infer missing file contents.

## Read These Files First

Read these files in order from the uploaded zip:

```text
PACKAGE_README.md
SHA256SUMS.txt
PACKAGE_FILE_MANIFEST.sha256
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_HUMAN_DECISION_UNDER_LOCK_V8_20260630.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_metadata_label_patch_v6_report11_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_METADATA_LABEL_PATCH_V6_REPORT11_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_POST_V6_DECISION_GATE_V7_TASKBOOK_20260630.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_local_draft_lock_audit_v5_report10_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_LOCAL_DRAFT_LOCK_AUDIT_V5_REPORT10_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT9_LABEL_ERRATUM_20260630.md
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

## Human-Decision Questions

Answer with file and line references where possible:

1. Does report(12) validly support `PREPARE_HUMAN_DECISION_UNDER_LOCK`?
2. Is there any remaining package identity, status-chain, or RAG-locator blocker?
3. Are Proposition 1/2/3 still only local-draft claims inside the controlled
   finite weighted two-way-table object?
4. Is the exact 2 x 2 witness correctly limited to `CERTIFICATE`?
5. Is the deterministic floating-point harness correctly limited to
   `HARNESS_ONLY`?
6. Is bibliography/positioning still conservative enough, including duplicate
   risk and online/publisher metadata caveats?
7. Are forbidden claims absent as endorsed claims, even if listed in negative
   scan contexts?
8. If the answer is favorable, what exact human decision should node36 ask the
   PI to make next?
9. If the answer is unfavorable, what exact patch must happen before another
   Pro round?

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
HUMAN_DECISION_UNDER_LOCK_ACCEPTED
PATCH_PROOF_OR_BIBLIO_BEFORE_HUMAN_DECISION
PATCH_PACKAGE_OR_STATUS_BEFORE_HUMAN_DECISION
DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT
```

2. `Package and Status Chain`: whether the V8 bundle and status files are
   coherent.

3. `Proof Boundary`: Proposition 1/2/3 status and any proof gap that still
   blocks a human decision.

4. `Certificate and Harness Boundary`: exact witness and deterministic harness
   roles.

5. `Bibliography and Duplicate Risk`: conservative status and what not to
   claim.

6. `Forbidden-Claim Scan`: any risky wording found in the controlled bundle.

7. `Human Decision Memo`: a short decision memo for node36 and the human PI.
   It may list allowed claims, forbidden claims, risks, and decision options.
   It must not contain paper prose.

8. `Remaining Blockers`: exact files and line references. If none, say
   `no human-decision blocker found; emergency lock still active`.

9. `Recommended Node36 Action`: choose one:

```text
ASK_PI_FOR_SEPARATE_DRAFT_AUTHORIZATION_UNDER_LOCK
PATCH_FIRST_THEN_RECHECK
STOP_DO_NOT_DRAFT
```

## Final Reminder

This is a decision-support audit, not a drafting session. If you find yourself
writing publishable paragraphs, stop and replace them with a claim ledger or a
decision memo.
