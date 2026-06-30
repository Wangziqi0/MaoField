# Node22 Vector Refresh -- Order-Defect Post-V6 Decision Gate V7

Date: 2026-06-30 CST
Authority: node36

## Purpose

Refresh the canonical MaoField RAG index after report(11) and the V7
post-V6 decision-gate materials were added.

This refresh is a locator update only. It is not proof, not bibliography
authority, not paper-ready authority, and not evidence for MaoField Mode B.

## Scope Policy

Node36 owns:

- canonical scope selection;
- scope manifest;
- candidate artifact hash verification;
- promotion decision;
- RAG smoke checks;
- node22 stop verification.

Node22 is used only as a temporary GPU embedding worker.

## Sidecar Files

Exact live hashes, scope size, build output, and smoke results are kept in
sidecars to avoid Markdown/RAG self-hash loops:

```text
canonical_scope_active_20260630_1755_post_v6_decision_gate_v7.txt
scope_hash_20260630_1755_post_v6_decision_gate_v7.txt
candidate_hashes_20260630_1755_post_v6_decision_gate_v7.txt
promoted_hashes_20260630_1755_post_v6_decision_gate_v7.txt
backup_hashes_20260630_1755_post_v6_decision_gate_v7.txt
rag_build_node22_candidate_20260630_1755_post_v6_decision_gate_v7.log
node22_status_after_stop2_20260630_1755_post_v6_decision_gate_v7.txt
rag_smoke_post_v6_report11_20260630_1755.txt
rag_smoke_post_v6_prompt_20260630_1755.txt
rag_smoke_post_v6_package_record_20260630_1755.txt
rag_smoke_post_v6_boundary_20260630_1755.txt
```

## Expected Smoke Coverage

Smoke queries must locate:

- report(11) raw audit;
- report(11) adoption note;
- V7 prompt;
- V7 package record;
- `METADATA_LABEL_PATCH_ACCEPTED_KEEP_LOCK`;
- `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK`;
- `LOCKED_NO_PAPER_BODY`;
- Mode B `insufficient_artifact`.

## Boundary

This refresh does not authorize paper-body drafting, paper-ready wording,
preprint-ready wording, emergency-lock lifting, full panel, checkpoint
inference, training, new loss, observed residual/interaction/transport/holonomy
fields, F3/LOSO/glass-box claims, or completed formal system wording.
