# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Proof-Repair Recheck V4

Use the uploaded zip as the only evidence bundle. Do not use public web
browsing, public GitHub pages, raw.githubusercontent.com, search-engine results,
or memory of previous chats. If the zip is missing or unreadable, stop and say
`INSUFFICIENT_BUNDLE`.

You are an external, non-authoritative audit model. The node36 repository keeps
the final authority. Your output is advisory only and must not be treated as
proof authority, bibliography authority, paper-ready authority, or posting
authority.

## Current Local Verdict To Audit

The current local state is:

```text
KEEP_LOCK_AND_FIX
```

Report (8) narrowed the next local action to:

```text
PATCH_PROOFS_THEN_RECHECK
```

Your task is to recheck the proof-repair candidate. Do not draft a paper body.
Do not produce a preprint. Do not claim that the emergency lock is lifted.

## Read These Files First

Read these files in this order from the uploaded zip:

```text
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_proof_biblio_repair_audit_report8_20260630.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md
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
from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md
```

If a file is missing, report it exactly. Do not infer its contents.

## Mathematical Object

Audit only the following finite-dimensional object:

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

## Claims To Recheck

Classify each item as:

```text
COMPLETE_LOCAL_DRAFT
PROOF_REPAIR_CANDIDATE
PLAUSIBLE_BUT_GAP
NOT_PROVED
CONTRADICTED
```

### Proposition 1

Finite positive weights are product weights if and only if centered row and
column main-effect spaces are orthogonal.

Check whether the centered-cell-indicator proof is complete.

### Proposition 2 Repair Candidate

The proof-repair candidate claims the following equivalences:

```text
w is product form
A is orthogonal to B0
D_w = 0
R_Q_then_B = R_B_then_Q
```

and, when these hold:

```text
R_Q_then_B = R_B_then_Q = I - P_N
```

Audit the exact step:

```text
D_w=0 => P_A|_{B0}=0 => A orthogonal B0 => product weights.
```

In particular, verify or reject:

- `A cap B0 = {0}`;
- `D_w = P_B0 P_A - P_A P_B0`;
- for `b in B0`, `D_w b = 0` implies `P_A b = P_B0 P_A b`;
- therefore `P_A b in A cap B0`;
- self-adjointness gives `<a,b>_w = <a,P_A b>_w`;
- degenerate one-row or one-column cases are harmless.

If any step depends on a hidden assumption, state the assumption and label the
claim accordingly.

### Proposition 3 Repair Candidate

For non-product weights, the candidate claims an existential pure-main-effect
witness:

```text
exists K in B0 such that
K in N_add
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K != 0
```

Audit the exact logic:

- non-product weights imply `A` is not orthogonal to `B0`;
- therefore there exists `K in B0` with `P_A K != 0`;
- `R_B_then_Q K = 0`;
- if `R_Q_then_B K = 0`, then `P_AK in A cap B0`, contradiction;
- the nonzero wrong-order output is a sequential stripping artifact, not a true
  interaction residual.

Confirm that the statement is existential only. Reject any universal reading
that every non-product input differs under the two stripping orders.

## Exact Witness Recheck

The exact 2 x 2 rational witness should remain the certificate-level example:

```text
w = (1/11) [[1,2],
            [3,5]]
K = (7/11, -4/11, 7/11, -4/11)
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

Check whether the Markdown, JSON, and script are mutually consistent. Do not
call JSON floats or deterministic harness output a proof.

## Bibliography And Positioning Recheck

Audit only conservative positioning:

- Hooker 2007;
- Chastaing, Gamboa, Prieur 2012 and 2014/2015;
- Owen and Prieur 2017;
- Iooss and Prieur 2019;
- Il Idrissi et al. 2025;
- Lamboni 2026;
- Bottcher and Spitkovsky 2010;
- Corach and Maestripieri;
- Halmos 1969.

For Lamboni 2026, keep DOI / publisher-online-record / online-first wording if
that is all the bundle supports. Do not infer final print metadata from the
bundle.

Classify duplicate risk as `LOW`, `MEDIUM`, `HIGH`, or `UNKNOWN`, but keep the
scope narrow: this is a finite illustrative artifact unless the files prove
more.

## Forbidden Claims

Do not write or endorse any of the following:

```text
paper body drafted
paper-ready
preprint-ready
posted
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
PROOF_REPAIR_ACCEPTED_FOR_LOCAL_DRAFT_ONLY
PATCH_PROOFS_AGAIN
KEEP_LOCK_AND_FIX
DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT
```

2. `Claim Labels`: label Proposition 1, Proposition 2, Proposition 3, exact
   witness, deterministic harness, bibliography.

3. `Blocking Issues`: exact file paths and line references where possible.

4. `Proof Details`: line-by-line assessment of the Proposition 2 and
   Proposition 3 repair steps.

5. `Exact Witness Consistency`: Markdown/JSON/script status and any mismatch.

6. `Bibliography Risks`: conservative metadata notes and duplicate-risk class.

7. `Forbidden-Claim Scan`: any risky wording found in the controlled bundle.

8. `Next Node36 Action`: choose one:

```text
KEEP_AS_PROOF_REPAIR_CANDIDATE
PATCH_CANDIDATE_THEN_RECHECK
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
STOP_EVIDENCE_INSUFFICIENT
```

Do not draft the note. Do not lift the emergency lock. Do not promote Mode B.
