# Node22 Vector Refresh -- Order-Defect PI Local Review Decision V13

Date: 2026-07-01 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField

## Purpose

Refresh the canonical MaoField RAG index after report(17), V13 taskbook, V13
prompt, V13 package record, and the report(17) adoption note were added.

Report(17) returned:

```text
RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
```

Node36 adopts this only as:

```text
PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
```

RAG is a locator only. It is not proof, bibliography authority, package
authority, paper-ready authority, or evidence for MaoField empirical claims.

## Scope Policy

The V13 scope is based on the prior V12 authoritative scope plus the six
report(17)/V13 current files:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_pi_decision_gate_v12_report17_20260701.md
docs/infra/gpt_deep_research/ORDER_DEFECT_PI_DECISION_V12_REPORT17_ADOPTION_NOTE_20260701.md
docs/infra/recovery/ORDER_DEFECT_D701_PI_LOCAL_REVIEW_DECISION_V13_TASKBOOK_20260701.md
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PI_LOCAL_REVIEW_DECISION_V13_PROMPT_20260701.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PI_LOCAL_REVIEW_DECISION_V13_20260701.md
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PI_LOCAL_REVIEW_DECISION_V13_20260701.md
```

Exact scope path, scope hash, promoted index hashes, build log, and smoke
outputs are stored in sidecars named with:

```text
20260701_2028_pilocalreview_v13
```

Exact values are intentionally kept in sidecars and logs rather than this
self-referential Markdown record.

## Boundary

The refreshed index must be able to locate:

- report(17);
- report(17) adoption note;
- V13 taskbook;
- V13 prompt;
- V13 package record;
- current live labels;
- `RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`;
- `PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`;
- `BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`;
- `insufficient_artifact`.

It must not be treated as evidence that a paper is ready, a preprint is posted,
the emergency lock is lifted, an English draft is authorized, a full panel has
run, training/inference occurred, or any MaoField
residual/interactions/transport/holonomy field has been observed.

## Node22 Lifecycle

Node36 owns scope, manifest, hash verification, and promotion. Node22 is only a
temporary embedding worker. Stop any temporary node22 service after the build
and record the stopped status in a sidecar.
