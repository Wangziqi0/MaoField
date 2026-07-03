# Node22 Vector Refresh -- Open-MaoField Zenodo / v1.0.0 Prep

Date: 2026-07-03 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260703_1632_zenodo_v1_0_prep`

## Purpose

Refresh the canonical MaoField RAG index after the public `Open-MaoField`
repository was prepared for Zenodo / v1.0.0 metadata and canonical status files
were updated.

RAG remains a locator only. It is not proof, release authority, DOI authority,
arXiv/journal-submission authority, peer-review authority, or evidence for
MaoField empirical claims.

## Scope

Scope sidecar:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260703_1632_zenodo_v1_0_prep.txt
```

Active files:

```text
578
```

Scope hash:

```text
b15afaa5cc8daf6bd29cb5410ba36badcd3ec7d482186ae3a27fd231440cc653
```

The active scope includes:

- `STATE.md`;
- `MD_CATALOG.md`;
- `docs/infra/OPEN_MAOFIELD_ZENODO_V1_0_PREP_20260703.md`;
- the prior V2.5 public-route and release-gate records.

This RAG refresh record itself was written after promotion as a durable record
of the run. It is a primary file, but it is not self-indexed in this refresh.

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
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260703_1632_zenodo_v1_0_prep.log
```

Build summary:

```text
files=578
chunks=11888
vectors=11888
dim=1024
```

## Promoted Hashes

Promoted sidecar:

```text
docs/infra/rag_rebuild_20260622/promoted_hashes_20260703_1632_zenodo_v1_0_prep.txt
```

Current promoted hashes:

```text
c2232f38112e00191d821eaf6381f5979db34e1043ff645aa7d62ba12895eaf8  /media/amd/raid1/rag/index/kb.faiss
dc6b931ca9c8984469f8eb64995c58154523aac3dd92759ef1ea7dd9b1e6dc9a  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Candidate hashes are stored in:

```text
docs/infra/rag_rebuild_20260622/candidate_hashes_20260703_1632_zenodo_v1_0_prep.txt
```

Previous canonical index backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260703_1632_zenodo_v1_0_prep
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260703_1632_zenodo_v1_0_prep
```

## Smoke Queries

Smoke query outputs:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_zenodo_v1_public_route_20260703_1632_zenodo_v1_0_prep.txt
docs/infra/rag_rebuild_20260622/rag_smoke_zenodo_v1_boundary_20260703_1632_zenodo_v1_0_prep.txt
docs/infra/rag_rebuild_20260622/rag_smoke_zenodo_v1_modeb_20260703_1632_zenodo_v1_0_prep.txt
```

Smoke results locate the Zenodo/v1.0.0 preparation record, `STATE.md`,
`MD_CATALOG.md`, the no-Release/no-DOI boundary, Mode B
`insufficient_artifact`, and duplicate risk `MEDIUM`.

## Node22 Lifecycle

Node22 start and stop records:

```text
docs/infra/rag_rebuild_20260622/node22_start_20260703_1632_zenodo_v1_0_prep.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260703_1632_zenodo_v1_0_prep.txt
```

The temporary service was stopped after promotion, and port `18080` was
verified as not listening.

Node36 scratch candidate artifacts:

```text
/home/amd/codex-node36/tmp/rag_20260703_1632_zenodo_v1_0_prep/
```

## Boundary

This refresh must not be treated as evidence that Zenodo integration has been
enabled, a GitHub Release exists, a Zenodo DOI exists, a preprint has been
posted, an arXiv/journal submission has occurred, peer review has occurred, a
full panel has run, training/inference occurred, or any MaoField residual,
interaction, transport, holonomy, glass-box, F3, or LOSO result has been
observed.
