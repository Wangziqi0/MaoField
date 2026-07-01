# Node22 Vector Refresh -- Order-Defect Draft Authorization Under Lock V9

Date: 2026-07-01 CST
Authority: node36 controls scope, manifests, verification, and promotion.
Node22 role: temporary one-shot GPU vector worker only.

## Purpose

Refresh the MaoField RAG index after report(13) and the V9 draft-authorization
under-lock package material are added to canonical.

This refresh is for locator support only. RAG is not evidence and does not
promote claims. Primary evidence remains the canonical files, package manifests,
scripts, JSON, and audit reports.

## Current V9 Files To Locate

```text
docs/infra/gpt_deep_research/deep_research_order_defect_human_decision_v8_report13_20260701.md
docs/infra/gpt_deep_research/ORDER_DEFECT_HUMAN_DECISION_V8_REPORT13_ADOPTION_NOTE_20260701.md
docs/infra/recovery/ORDER_DEFECT_D701_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_TASKBOOK_20260701.md
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_PROMPT_20260701.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_DRAFT_AUTHORIZATION_UNDER_LOCK_V9_20260701.md
```

## Self-Hash-Safe Policy

Exact live index hashes, scope file counts, chunk counts, node22 status, and
smoke outputs are intentionally kept in sidecar files and the build log. This
Markdown does not embed final live hashes to avoid self-hash drift after the
index is rebuilt.

Expected sidecar names:

```text
canonical_scope_active_20260701_1050_draftauth_v9.txt
scope_hash_20260701_1050_draftauth_v9.txt
candidate_hashes_20260701_1050_draftauth_v9.txt
promoted_hashes_20260701_1050_draftauth_v9.txt
backup_hashes_20260701_1050_draftauth_v9.txt
rag_build_node22_candidate_20260701_1050_draftauth_v9.log
node22_status_after_stop2_20260701_1050_draftauth_v9.txt
rag_smoke_report13_20260701_1050.txt
rag_smoke_v9_prompt_20260701_1050.txt
rag_smoke_v9_package_record_20260701_1050.txt
rag_smoke_v9_boundary_20260701_1050.txt
```

## Required Smoke Queries

After promotion, run at least these node36 RAG locator checks:

```text
report13 HUMAN_DECISION_UNDER_LOCK_ACCEPTED ASK_PI_FOR_SEPARATE_DRAFT_AUTHORIZATION_UNDER_LOCK
V9 draft authorization under lock prompt package node19
LOCKED_NO_PAPER_BODY insufficient_artifact DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED
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
