# Node22 Vector Refresh -- Order-Defect Boundary-Locked Draft Review V11

Date: 2026-07-01 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField

## Purpose

Refresh the canonical MaoField RAG index after report(15) and the V11
boundary-locked draft-review package files were added. The final promoted
refresh is the `V11_FIX_20260701_1352` rerun after independent audit caught and
node36 fixed a stale `MD_CATALOG.md` pointer to the older D701 V9 prompt.

Report(15) returned:

```text
BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE
```

Node36 adopts this only as:

```text
RECEIVE_LOCAL_DRAFT_CANDIDATE_UNDER_LOCK_PREPARE_V11_REVIEW
```

RAG is a locator only. It is not proof, bibliography authority, package
authority, paper-ready authority, or evidence for MaoField empirical claims.

## Scope Policy

The V11 scope is based on the prior V10 authoritative scope plus the six
report(15)/V11 current files:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_boundary_locked_draft_v10_report15_20260701.md
docs/infra/gpt_deep_research/ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_V10_REPORT15_ADOPTION_NOTE_20260701.md
docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_TASKBOOK_20260701.md
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_PROMPT_20260701.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_20260701.md
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_20260701.md
```

Exact scope path, scope hash, promoted index hashes, build log, and smoke
outputs are stored in sidecars named with:

```text
20260701_1352_draftreview_v11_fix
```

Exact values are intentionally kept in sidecars and logs rather than this
self-referential Markdown record.

## Boundary

The refreshed index must be able to locate:

- report(15);
- report(15) adoption note;
- V11 taskbook;
- V11 prompt;
- V11 package record;
- current live labels;
- `BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`;
- `insufficient_artifact`.

It must not be treated as evidence that a paper is ready, a preprint is posted,
the emergency lock is lifted, a full panel has run, training/inference occurred,
or any MaoField residual/interactions/transport/holonomy field has been
observed.

## Node22 Lifecycle

Node36 owns scope, manifest, hash verification, and promotion. Node22 is only a
temporary embedding worker. Stop any temporary node22 service after the build
and record the stopped status in a sidecar.
