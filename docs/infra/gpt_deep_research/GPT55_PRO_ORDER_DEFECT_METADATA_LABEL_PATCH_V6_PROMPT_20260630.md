# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Metadata/Label Patch V6

Use the uploaded zip as the only evidence bundle. Do not use public web
browsing, public GitHub pages, raw.githubusercontent.com, search-engine
results, GitHub connector content outside the uploaded bundle, or memory of
previous chats. If the zip is missing or unreadable, stop and say
`INSUFFICIENT_BUNDLE`.

You are an external, non-authoritative audit model. Node36 keeps final
authority. Your output is advisory only and must not be treated as proof
authority, bibliography authority, paper-ready authority, or posting authority.

## Current Task

Node36 adopted report(10) as:

```text
PATCH_METADATA_OR_LABELS_AGAIN
```

The V6 bundle is intended to repair report(10)'s metadata/label blockers only.
It must not change the mathematical claim boundary.

Current live state remains:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
KEEP_LOCK_AND_FIX
```

Do not draft a paper body. Do not produce a preprint. Do not claim that the
emergency lock is lifted.

## First Package Checks

Before substantive analysis:

1. read `PACKAGE_README.md`;
2. inspect `SHA256SUMS.txt` and `PACKAGE_FILE_MANIFEST.sha256`;
3. confirm the bundle contains the V5 package record:

```text
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_LOCAL_DRAFT_LOCK_V5_20260630.md
```

4. confirm the bundle contains the V6 package record:

```text
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_METADATA_LABEL_PATCH_V6_20260630.md
```

5. confirm the bundle contains the report(9) label erratum:

```text
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT9_LABEL_ERRATUM_20260630.md
```

6. if any of those are missing, return `PATCH_METADATA_OR_LABELS_AGAIN`.

Do not infer missing file contents.

## Read These Files First

Read these files in order from the uploaded zip:

```text
PACKAGE_README.md
SHA256SUMS.txt
PACKAGE_FILE_MANIFEST.sha256
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_local_draft_lock_audit_v5_report10_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_LOCAL_DRAFT_LOCK_AUDIT_V5_REPORT10_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_METADATA_LABEL_PATCH_V6_TASKBOOK_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT9_LABEL_ERRATUM_20260630.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_proof_repair_recheck_report9_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_LOCAL_DRAFT_LOCKED_TASKBOOK_20260630.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_LOCAL_DRAFT_LOCK_V5_20260630.md
from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_METADATA_LABEL_PATCH_V6_20260630.md
from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_METADATA_LABEL_PATCH_V6_20260630.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md
```

## Correct Live Labels

Audit whether all current live files use or preserve exactly these labels:

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

The raw report(9) label table is provenance only where it conflicts with these
live labels. The report(9) label erratum is the node36 guard for that drift.

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
decomposition theory, or a broad noncommuting-projection theory.

## Audit Questions

Answer with file and line references where possible:

1. Does V6 fix report(10)'s three metadata/label blockers?
2. Does the zip include V5 package record, V6 package record, and internal
   `SHA256SUMS.txt`?
3. Does the report(9) erratum clearly supersede the raw over-wide label table?
4. Are `STATE.md`, `MD_CATALOG.md`, adoption notes, taskbooks, verification,
   package records, and RAG record aligned?
5. Is the self-hash policy sound: zip container hash external; package-content
   hashes internal; live RAG hashes external sidecars; RAG only locator?
6. Are exact witness and deterministic harness roles still bounded as
   `CERTIFICATE` and `HARNESS_ONLY`?
7. Are bibliography and duplicate-risk boundaries still conservative?
8. Is there any forbidden claim in the controlled bundle?

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
METADATA_LABEL_PATCH_ACCEPTED_KEEP_LOCK
PATCH_METADATA_OR_LABELS_AGAIN
KEEP_LOCK_AND_FIX
DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT
```

2. `Identity Chain`: package identity, internal manifest/SHA256SUMS status, and
   whether report(10)'s V5 package-record criticism is fixed.

3. `Label Drift`: whether report(9)'s raw label table is safely superseded by
   live labels and the erratum.

4. `Status Consistency`: whether current status files agree.

5. `Proof Labels`: label Proposition 1, Proposition 2, Proposition 3, exact
   witness, deterministic harness, bibliography.

6. `Remaining Blockers`: exact files and line references. If none, say
   `no metadata/label blocker for local draft, emergency lock still active`.

7. `Forbidden-Claim Scan`: any risky wording found in the controlled bundle.

8. `Recommended Node36 Action`: choose one:

```text
KEEP_LOCAL_DRAFT_LOCKED_AND_PREPARE_USER_DECISION
PATCH_AND_REPACKAGE
STOP_EVIDENCE_INSUFFICIENT
```

Do not draft the note. Do not lift the emergency lock. Do not promote Mode B.

