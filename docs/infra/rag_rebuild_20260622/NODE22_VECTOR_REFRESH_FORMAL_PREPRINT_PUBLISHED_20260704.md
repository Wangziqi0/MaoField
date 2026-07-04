# Node22 Vector Refresh -- Formal Zenodo Preprint Published

Date: 2026-07-04 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260704_1830_formal_preprint_published_final`

## Purpose

Refresh the canonical MaoField RAG index after the formal Zenodo
`Publication -> Preprint` record was published and canonical status files were
updated.

RAG remains a locator only. It is not proof, peer review, arXiv/journal
submission authority, or evidence for MaoField empirical claims.

## Scope And Promotion

Sidecars for this refresh use the tag:

```text
20260704_1830_formal_preprint_published_final
```

Promoted hashes:

```text
kb.faiss sha256: 1a903bc152d44c417f5e6cc675d5885d9c575935715b08dd561b4421afdcf8d6
kb_meta.jsonl sha256: 0cd8e26d53af2b457c3065d69db426b2d7dcfcad0b888d633d7b19064d73a181
scope sha256: f77b6ad2096c3a1cbaf672e8e0c1f5071ca52a4bddfc537f2f131fb394ca68b4
active files: 592
chunks: 11983
```

Primary sidecars:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260704_1830_formal_preprint_published_final.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/smoke_queries_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/node22_start_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260704_1830_formal_preprint_published_final.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260704_1830_formal_preprint_published_final.txt
```

Node36 scratch candidate:

```text
/home/amd/codex-node36/tmp/rag_20260704_1830_formal_preprint_published_final/
```

Node22 temporary worker root:

```text
/home/amd/codex-node22/tmp/maofield-rag-vector-20260704_1830_formal_preprint_published_final/
```

## Smoke Targets

Smoke queries locate:

- `docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md`;
- superseded markers in `docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PREP_20260704.md`
  and `docs/infra/OPEN_MAOFIELD_ZENODO_PREPRINT_UPLOAD_GUIDE_20260704.md`;
- `MD_CATALOG.md` with the formal-preprint-published patch;
- `STATE.md` with `PUBLISHED_FORMAL_ZENODO_PREPRINT_AND_PUBLIC_DOI_BACKFILLED`;
- DOI `10.5281/zenodo.21190475`;
- concept DOI `10.5281/zenodo.21190474`;
- Mode B `insufficient_artifact`;
- duplicate risk `MEDIUM`;
- no-peer-review / no-arXiv / no-journal / no-MaoField-positive boundaries.

## Node22 Lifecycle

The temporary service was started on node22 port `18080`, used for the one-shot
embedding build, then stopped.

Final node22 checks:

```text
port 18080: not listening
KFD PIDs: none
GPU use: 0%
```

ROCm still reported stale-looking VRAM accounting (`GPU[0] VRAM 40%`) after the
process stopped, but `rocm-smi --showpids` showed no KFD processes and no
embedding service was listening.

## Boundary

This refresh must not be treated as evidence that peer review has occurred, an
arXiv/journal submission has occurred, a full panel has run, training/inference
occurred, or any MaoField residual, interaction, transport, holonomy, glass-box,
F3, or LOSO result has been observed.
