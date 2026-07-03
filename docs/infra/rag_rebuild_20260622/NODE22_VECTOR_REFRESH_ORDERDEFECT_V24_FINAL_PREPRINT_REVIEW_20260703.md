# Node22 Vector Refresh -- V2.4 Final Preprint Review

Date: 2026-07-03 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260703_1438_v24_final_preprint_review`

## Purpose

Refresh the canonical MaoField RAG index after the V2.4 final Pro review
source, author/title/release taskbook, bibliography metadata audit,
duplicate-risk/forbidden-claim review, final Pro prompt, `STATE.md`, and
`MD_CATALOG.md` navigation updates were added.

RAG is a locator only. It is not proof, bibliography authority, package
authority, paper-ready authority, preprint-ready authority, posting authority,
submission authority, or evidence for MaoField empirical claims.

## Scope

Scope sidecar:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260703_1438_v24_final_preprint_review.txt
```

Scope hash:

```text
6cb617846908d074dc88a14c5d446c94acdcbdff38f5efbc472e02eea41adb04
```

Active file count:

```text
569
```

## Build Route

Node36 owned scope generation, chunking, FAISS writing, hash verification,
promotion, and smoke queries. Node22 only served temporary bge-m3 embeddings
through a llama.cpp OpenAI-compatible HTTP endpoint.

Temporary worker:

```text
host: amd@192.168.31.22
endpoint: http://192.168.31.22:18080
model alias: bge-m3-temp
embedding dim: 1024
```

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260703_1438_v24_final_preprint_review.log
```

## Promoted Hashes

Promoted sidecar:

```text
docs/infra/rag_rebuild_20260622/promoted_hashes_20260703_1438_v24_final_preprint_review.txt
```

Current promoted hashes:

```text
0c9f8b18d5f7de0456241698ffee5ddd52ca6ff119eeca8953e0269516ddc9e6  /media/amd/raid1/rag/index/kb.faiss
dd5a6082711cfd297a9170fa9f89629a66313f5dd75b2ad6421ff376e354c725  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Chunk count:

```text
11827
```

Previous canonical index backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260703_1438_v24_final_preprint_review
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260703_1438_v24_final_preprint_review
```

## Smoke Queries

Smoke query outputs:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_v24_title_author_20260703_1438_v24_final_preprint_review.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v24_bibliography_20260703_1438_v24_final_preprint_review.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v24_boundaries_20260703_1438_v24_final_preprint_review.txt
```

Smoke results locate the V2.4 final-review taskbook, bibliography metadata
audit, final Pro prompt, duplicate-risk/forbidden-claim review, `STATE.md`, and
`MD_CATALOG.md`. RAG also still returns older Lamboni caution records, which is
acceptable because V2.4 explicitly updates Lamboni metadata from the current
Crossref record while retaining `MEDIUM duplicate risk`.

## Node22 Lifecycle

Node22 temporary service status:

```text
docs/infra/rag_rebuild_20260622/node22_stop_20260703_1438_v24_final_preprint_review.txt
```

The temporary service was stopped after promotion. Node36 scratch candidate
artifacts:

```text
/home/amd/codex-node36/tmp/rag_20260703_1438_v24_final_preprint_review/
```

## Boundary

This refresh must not be treated as evidence that a paper is ready, a preprint
is ready, a preprint is posted, a submission is authorized, the lock is lifted,
a full panel has run, training/inference occurred, or any MaoField residual,
interaction, transport, holonomy, glass-box, F3, or LOSO result has been
observed.
