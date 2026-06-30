# Order-Defect D630 Proof Repair Taskbook

Date: 2026-06-30 CST
Authority: node36
Purpose: prevent context drift after Pro report (8) proof/bibliography repair
audit.

## Current Verdict

```text
PATCH_PROOFS_THEN_RECHECK
```

This verdict is a subtask under the broader lock:

```text
KEEP_LOCK_AND_FIX
```

## Allowed Activity

```text
proof_repair_candidate
proof_repair_audit
bibliography_conservatism_check
claim_boundary_audit
status_catalog_rag_sync
package_for_next_pro_recheck
```

## Forbidden Activity

```text
paper_body_drafting
claim_promotion
proof_authority_promotion_without_recheck
bibliography_authority_promotion_without_metadata_limits
MaoField_empirical_positive_claim
new_theory_expansion
training_or_new_loss_authorization
```

## Inputs

```text
docs/infra/gpt_deep_research/deep_research_order_defect_proof_biblio_repair_audit_report8_20260630.md
docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
scripts/debranded_residual_transport_exact_witness_v1_4.py
docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
```

## Current Proof Labels

Preserve these labels until the next recheck:

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: PROOF_REPAIR_CANDIDATE
Proposition 3: PROOF_REPAIR_CANDIDATE
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
```

## Completion Criteria For This Round

This round is complete only after:

1. report (8) is archived with sha256;
2. adoption note is written;
3. proof-repair candidate is written;
4. `STATE.md` and `MD_CATALOG.md` point to the candidate and preserve the lock;
5. exact witness and deterministic harness smoke checks still pass;
6. RAG is refreshed through node22 one-shot vectorization and node22 is stopped;
7. a next Pro prompt and light zip are generated and copied to node19 desktop;
8. the independent verification thread has been asked to review the updated
   status/RAG/prompt/zip;
9. intentional files are committed and pushed from node36.

## Boundary

This taskbook does not authorize paper drafting. It only creates and packages a
proof-repair candidate for external recheck.
