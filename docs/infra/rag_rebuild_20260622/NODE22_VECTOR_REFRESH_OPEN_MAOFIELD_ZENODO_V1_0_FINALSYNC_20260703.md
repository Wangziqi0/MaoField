# Node22 Vector Refresh -- Open-MaoField Zenodo / v1.0.0 Finalsync

Date: 2026-07-03 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260703_1640_zenodo_v1_0_finalsync`

## Purpose

Refresh the canonical MaoField RAG index after the Zenodo / v1.0.0 metadata
preparation, `STATE.md`, `MD_CATALOG.md`, and the release-prep record were all
updated. This finalsync record is written before the build so it can be included
in the active markdown scope.

RAG remains a locator only. It is not proof, release authority, DOI authority,
arXiv/journal-submission authority, peer-review authority, or evidence for
MaoField empirical claims.

## Sidecars

Exact active-file count, chunk count, scope hash, build log, candidate hashes,
promoted hashes, smoke outputs, and node22 start/stop records are kept in
sidecars named with this tag:

```text
20260703_1640_zenodo_v1_0_finalsync
```

The important expected sidecars are:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/scope_hash_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260703_1640_zenodo_v1_0_finalsync.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/rag_smoke_zenodo_v1_public_route_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/rag_smoke_zenodo_v1_boundary_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/rag_smoke_zenodo_v1_modeb_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/node22_start_20260703_1640_zenodo_v1_0_finalsync.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260703_1640_zenodo_v1_0_finalsync.txt
```

## Build Route

Node36 owns scope generation, chunking, FAISS writing, hash verification,
promotion, and smoke queries. Node22 only serves temporary bge-m3 embeddings
through a llama.cpp OpenAI-compatible HTTP endpoint.

Temporary worker:

```text
host: amd@192.168.31.22
endpoint: http://192.168.31.22:18080
model alias: bge-m3-temp
embedding dim: 1024
HIP_VISIBLE_DEVICES=0
ROCR_VISIBLE_DEVICES=0
```

## Smoke Targets

Smoke queries must locate:

- `docs/infra/OPEN_MAOFIELD_ZENODO_V1_0_PREP_20260703.md`;
- `STATE.md` with the v1.0.0 / Zenodo waiting-for-human-enable status;
- `MD_CATALOG.md` current RAG pointer;
- no-Release/no-DOI boundary;
- Mode B `insufficient_artifact`;
- duplicate risk `MEDIUM`.

## Boundary

This refresh must not be treated as evidence that Zenodo integration has been
enabled, a GitHub Release exists, a Zenodo DOI exists, a preprint has been
posted, an arXiv/journal submission has occurred, peer review has occurred, a
full panel has run, training/inference occurred, or any MaoField residual,
interaction, transport, holonomy, glass-box, F3, or LOSO result has been
observed.
