# Node22 Vector Refresh -- Order-Defect PI Local Review Confirmed Report18

Date: 2026-07-02 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField

## Purpose

Refresh the canonical MaoField RAG index after report(18), its adoption note,
and the D702 `STATE.md` / `MD_CATALOG.md` status updates were added.

Report(18) returned:

```text
CONFIRM_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
```

Node36 adopts this only as:

```text
PI_LOCAL_REVIEW_ONLY_KEEP_LOCK_CONFIRMED
```

Local next action:

```text
ASK_PI_DIRECTION_AFTER_V13
```

RAG is a locator only. It is not proof, bibliography authority, package
authority, paper-ready authority, posting authority, submission authority, or
evidence for MaoField empirical claims.

## Scope Policy

The report(18) scope is based on the prior V13 authoritative scope plus the
report(18) current files:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_pi_local_review_decision_v13_report18_20260702.md
docs/infra/gpt_deep_research/ORDER_DEFECT_PI_LOCAL_REVIEW_DECISION_V13_REPORT18_ADOPTION_NOTE_20260702.md
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PI_LOCAL_REVIEW_CONFIRMED_REPORT18_20260702.md
```

Exact scope path, scope hash, promoted index hashes, build log, and smoke
outputs are stored in sidecars named with:

```text
20260702_1003_report18_pilocalreview_confirmed
```

Exact values are intentionally kept in sidecars and logs rather than this
self-referential Markdown record.

## Boundary

The refreshed index must be able to locate:

- report(18);
- report(18) adoption note;
- `CONFIRM_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`;
- `PI_LOCAL_REVIEW_ONLY_KEEP_LOCK_CONFIRMED`;
- `ASK_PI_DIRECTION_AFTER_V13`;
- `BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`;
- `insufficient_artifact`;
- the absence of any active next-Pro prompt/package until PI choice.

It must not be treated as evidence that a paper is ready, a preprint is posted,
the emergency lock is lifted, an English draft is authorized, a full panel has
run, training/inference occurred, or any MaoField
residual/interactions/transport/holonomy field has been observed.

## Node22 Lifecycle

Node36 owns scope, manifest, hash verification, and promotion. Node22 is only a
temporary embedding worker. Stop any temporary node22 service after the build
and record the stopped status in a sidecar.
