# Node22 Vector Refresh -- Order-Defect Human Decision Under Lock V8

Date: 2026-06-30 CST
Authority: node36 controls scope, manifests, verification, and promotion.
Node22 role: temporary one-shot GPU vector worker only.

## Purpose

Refresh the MaoField RAG index after report(12) and the V8 human-decision
under-lock package material are added to canonical.

This refresh is for locator support only. RAG is not evidence and does not
promote claims. Primary evidence remains the canonical files, package manifests,
scripts, JSON, and audit reports.

## Current V8 Files To Locate

```text
docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md
docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md
docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_HUMAN_DECISION_UNDER_LOCK_V8_PROMPT_20260630.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_HUMAN_DECISION_UNDER_LOCK_V8_20260630.md
```

## Self-Hash-Safe Policy

Exact live index hashes, scope file counts, chunk counts, node22 status, and
smoke outputs are intentionally kept in sidecar files and the build log. This
Markdown does not embed final live hashes to avoid self-hash drift after the
index is rebuilt.

Expected sidecar names:

```text
canonical_scope_active_20260630_2005_humandecision_v8.txt
scope_hash_20260630_2005_humandecision_v8.txt
candidate_hashes_20260630_2005_humandecision_v8.txt
promoted_hashes_20260630_2005_humandecision_v8.txt
backup_hashes_20260630_2005_humandecision_v8.txt
rag_build_node22_candidate_20260630_2005_humandecision_v8.log
node22_status_after_stop2_20260630_2005_humandecision_v8.txt
rag_smoke_report12_20260630_2005.txt
rag_smoke_v8_prompt_20260630_2005.txt
rag_smoke_v8_package_record_20260630_2005.txt
rag_smoke_v8_boundary_20260630_2005.txt
```

## Required Smoke Queries

After promotion, run at least these node36 RAG locator checks:

```text
report12 POST_V6_DECISION_GATE_ACCEPTED_KEEP_LOCK PREPARE_HUMAN_DECISION_UNDER_LOCK
V8 human decision under lock prompt package node19
LOCKED_NO_PAPER_BODY insufficient_artifact HUMAN_DECISION_UNDER_LOCK_ACCEPTED
```

Smoke success means the relevant files can be located. It does not mean the
claims are proven.

## Boundary

The refresh must preserve:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
KEEP_LOCK_AND_FIX
LOCKED_NO_PAPER_BODY
Mode B: insufficient_artifact
RAG: locator only, not evidence
```

Node22 temporary service must be stopped after the one-shot build. Node36 must
verify the returned candidate hashes before promoting to `/media/amd/raid1/rag`.
