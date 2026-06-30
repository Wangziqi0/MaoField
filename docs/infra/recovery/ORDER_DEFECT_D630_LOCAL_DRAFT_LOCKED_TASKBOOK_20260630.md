# Order-Defect D630 Local-Draft Locked Taskbook

Date: 2026-06-30 CST
Authority: node36
Purpose: prevent context drift after Pro report (9) accepted the proof-repair
candidate for local draft only.

## Current Verdict

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
```

This verdict is still under the broader recovery lock:

```text
KEEP_LOCK_AND_FIX
```

## What Changed

Report (9) rechecked the V4 proof-repair package and judged the repaired
finite-dimensional proof stack acceptable at local-draft level:

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
```

This supersedes the report(8)-era action:

```text
PATCH_PROOFS_THEN_RECHECK
```

but only for the controlled finite positive weighted two-way-table object.

## Still Locked

The following remain locked:

```text
paper_body_drafting
paper_ready_or_preprint_ready_status
posting_or_submission
completed_formal_system
broad_new_ANOVA_theory
broad_new_dependent_input_decomposition_theory
broad_new_noncommuting_projection_theory
MaoField_empirical_positive_claim
full_panel
checkpoint_loading
inference
training
new_loss
observed_residual_or_interaction_or_transport_or_holonomy_field
glass_box_broken
F3_positive
LOSO_passed
JSON_floats_as_proof
harness_as_proof
```

## Authoritative Inputs

```text
docs/infra/gpt_deep_research/deep_research_order_defect_proof_repair_recheck_report9_20260630.md
docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md
docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
scripts/debranded_residual_transport_exact_witness_v1_4.py
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
scripts/debranded_residual_transport_harness_v1_3.py
docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md
```

## Label Reconciliation

Historical report(8) language such as `PLAUSIBLE_LOCAL_DRAFT` and
`PROOF_REPAIR_CANDIDATE` remains provenance. Current live status after report
(9) is:

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall paper status: LOCKED_NO_PAPER_BODY
```

## Package Identity Fix

The next package must include the package record Markdown inside the zip so a
zero-context Pro session can close the identity chain without relying on an
external file. Include `PACKAGE_FILE_MANIFEST.sha256` and `SHA256SUMS.txt`.

## Completion Criteria For This Round

This round is complete only after:

1. report (9) is archived with sha256;
2. this taskbook and the adoption note are written;
3. `STATE.md` and `MD_CATALOG.md` point to report (9) and the locked local-draft
   state;
4. exact witness and deterministic harness smoke checks still pass in SSD
   scratch;
5. RAG is refreshed through node22 one-shot vectorization and node22 is stopped;
6. RAG search retrieves report (9), this taskbook, the V5 prompt, and the
   `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK` boundary;
7. a V5 zero-context prompt and light package are copied to node19 desktop;
8. the independent verification thread is asked to review updated status, RAG,
   prompt, package, and mainline consistency;
9. intentional files are committed from node36.
