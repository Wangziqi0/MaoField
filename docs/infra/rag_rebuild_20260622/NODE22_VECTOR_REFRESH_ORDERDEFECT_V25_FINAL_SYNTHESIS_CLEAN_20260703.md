# Node22 Vector Refresh -- V2.5 Final Synthesis Clean

Date: 2026-07-03 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260703_1612_v25_final_synthesis_final`

## Purpose

Refresh the canonical MaoField RAG index after the V2.5 final-synthesis
manuscript package was adopted into the private canonical repository, the
sanitized `Open-MaoField` public draft repository was updated, and the promoted
V2.5 source-map/changelog wording was cleaned to avoid publication-status
ambiguity.

RAG remains a locator only. It is not proof, bibliography authority, release
authority, DOI authority, arXiv/journal-submission authority, peer-review
authority, or evidence for MaoField empirical claims.

## Scope

Scope sidecar:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260703_1612_v25_final_synthesis_final.txt
```

The active scope includes the V2.5 markdown adoption records, the public-route
record, this V2.5 RAG refresh record, `STATE.md`, and `MD_CATALOG.md`. Exact
scope hash, active file count, and chunk count are stored in the sidecars named
with the tag above, rather than repeated here, to avoid self-referential hash
drift in this markdown. The
TeX/PDF/PNG artifacts are preserved as primary files but are not directly
embedded by the markdown-only default RAG scope.

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
HIP_VISIBLE_DEVICES=0
ROCR_VISIBLE_DEVICES=0
```

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260703_1612_v25_final_synthesis_final.log
```

## Promoted Hashes

Promoted sidecar:

```text
docs/infra/rag_rebuild_20260622/promoted_hashes_20260703_1612_v25_final_synthesis_final.txt
```

Candidate hashes are stored in:

```text
docs/infra/rag_rebuild_20260622/candidate_hashes_20260703_1612_v25_final_synthesis_final.txt
```

Previous canonical index backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260703_1612_v25_final_synthesis_final
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260703_1612_v25_final_synthesis_final
```

## Smoke Queries

Smoke query outputs:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_v25_public_draft_20260703_1612_v25_final_synthesis_final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v25_adoption_exact_20260703_1612_v25_final_synthesis_final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v25_public_route_20260703_1612_v25_final_synthesis_final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v25_modeb_boundary_20260703_1612_v25_final_synthesis_final.txt
```

Smoke results locate the V2.5 adoption record, V2.5 release-gate note,
Open-MaoField public-route record, `STATE.md`, `MD_CATALOG.md`, Mode B
`insufficient_artifact`, the exact-witness boundary, and the no-Release /
no-Zenodo / no-submission status.

## Node22 Lifecycle

Node22 start and stop records:

```text
docs/infra/rag_rebuild_20260622/node22_start_20260703_1612_v25_final_synthesis_final.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260703_1612_v25_final_synthesis_final.txt
```

The temporary service was stopped after promotion, and port `18080` was verified
as not listening.

Node36 scratch candidate artifacts:

```text
/home/amd/codex-node36/tmp/rag_20260703_1612_v25_final_synthesis_final/
```

## Boundary

This refresh must not be treated as evidence that a GitHub Release exists, a
Zenodo DOI exists, a preprint has been posted, an arXiv/journal submission has
occurred, peer review has occurred, a full panel has run, training/inference
occurred, or any MaoField residual, interaction, transport, holonomy,
glass-box, F3, or LOSO result has been observed.
