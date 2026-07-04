# Node22 Vector Refresh -- Metric-Identity Programme

Date: 2026-07-04 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260704_2045_metric_identity_programme`

## Purpose

Refresh the canonical MaoField RAG index after PI supplied the metric-identity
programme note and node36 adopted its core framing into `STATE.md`.

New canonical programme files:

```text
docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md
docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md
```

RAG remains a locator only. It is not proof, empirical evidence, peer review,
or authority to expand claims.

## Scope And Promotion

Sidecars for this refresh use the tag:

```text
20260704_2045_metric_identity_programme
```

Promoted hashes:

```text
kb.faiss sha256: 32b99f6d998e0aed822e68136345cf1a1898d84bf517225f06d74192bb0b5b79
kb_meta.jsonl sha256: 7b3c0b06d84004018865c907eb7fa1fc485bb3e85186386a58f80b443a2cbb36
scope sha256: 74ef43a359b6f1fa81944cf23f46755459ea784aa8291ca02580c769ca232d7c
active files: 594
chunks: 12034
```

Primary sidecars:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260704_2045_metric_identity_programme.log
docs/infra/rag_rebuild_20260622/rag_scan_20260704_2045_metric_identity_programme.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/smoke_queries_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/node22_start_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260704_2045_metric_identity_programme.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260704_2045_metric_identity_programme.txt
```

Node36 scratch candidate:

```text
/home/amd/codex-node36/tmp/rag_20260704_2045_metric_identity_programme/
```

Node22 temporary worker root:

```text
/home/amd/codex-node22/tmp/maofield-rag-vector-20260704_2045_metric_identity_programme/
```

## Smoke Targets

Smoke queries locate:

- `measurement-object identity problem`;
- `metric-form fetishism`;
- `evaluation chart` / `identity condition` / `defect certificate`;
- audit-order instability `OI(w)`;
- `MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`;
- `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`;
- `STATE.md` with the Phase-II metric-identity adoption;
- Mode B `insufficient_artifact`;
- duplicate risk `MEDIUM`.

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

This refresh must not be treated as evidence that the programme note is a proof,
an empirical result, peer review, arXiv/journal submission, or a broad theory.
It only makes the adopted direction discoverable in RAG.
