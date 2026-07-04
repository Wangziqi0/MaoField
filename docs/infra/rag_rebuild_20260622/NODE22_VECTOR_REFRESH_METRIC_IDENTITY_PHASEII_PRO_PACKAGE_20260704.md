# Node22 Vector Refresh -- Metric-Identity Phase II Pro Package

Date: 2026-07-04 CST

Authority: node36

Worker: node22 one-shot GPU embedding service

Project: MaoField

Tag: `20260704_2212_metric_identity_phaseii_final_package`

## Purpose

Refresh the canonical MaoField RAG index after node36 built the Phase-II
metric-identity Pro polling package, updated `STATE.md` / `MD_CATALOG.md`, and
added the following durable records:

```text
docs/infra/MAOFIELD_PRO_METRIC_IDENTITY_PHASEII_PACKAGE_20260704.md
docs/infra/recovery/MAOFIELD_D704_METRIC_IDENTITY_PHASEII_PRO_TASKBOOK_20260704.md
docs/infra/gpt_deep_research/GPT55_PRO_METRIC_IDENTITY_PHASEII_POLLING_PROMPT_20260704.md
```

RAG remains a locator only. It is not proof, empirical evidence, peer review,
or authority to expand claims.

## Scope And Promotion

Sidecars for this refresh use the tag:

```text
20260704_2212_metric_identity_phaseii_final_package
```

Promoted hashes:

```text
kb.faiss sha256: e45bafbb4fb6a6b014fab232a100d1d7bd09b7fbe1ccf00c21bff4ae34c6c540
kb_meta.jsonl sha256: f9350c05be7ae209574e14c6cec5e75df5982382c849cb73ee5ce1cf144c0c98
scope sha256: see scope_hash_20260704_2212_metric_identity_phaseii_final_package.txt
active files: 599
chunks: 12083
faiss vectors: 12083
faiss dim: 1024
```

Primary sidecars:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260704_2212_metric_identity_phaseii_final_package.log
docs/infra/rag_rebuild_20260622/rag_scan_20260704_2212_metric_identity_phaseii_final_package.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/faiss_verify_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/smoke_queries_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/node22_start_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/node22_ready_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260704_2212_metric_identity_phaseii_final_package.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260704_2212_metric_identity_phaseii_final_package.txt
```

Node36 scratch candidate:

```text
/home/amd/codex-node36/tmp/rag_20260704_2212_metric_identity_phaseii_final_package/
```

Node22 temporary worker root:

```text
/home/amd/codex-node22/tmp/maofield-rag-vector-20260704_2212_metric_identity_phaseii_final_package/
```

## Smoke Targets

Smoke queries locate:

- `MaoField_PRO_MetricIdentity_PhaseII_Polling_FINAL_20260704_2208`;
- final ZIP sha256 `cf5b7aba71e549fb0b51886d861c05da2abf713d082df2b77c63266cab5cfd69`;
- `REQUEST_TO_NODE36_CODEX`;
- `metric-object identity finite evaluation charts`;
- `GPT55_PRO_METRIC_IDENTITY_PHASEII`;
- node19 desktop delivery and hashes;
- current `STATE.md` and `MD_CATALOG.md` package references.

## Node22 Lifecycle

The temporary service was started on node22 port `18080`, used for the one-shot
embedding build, then stopped.

Final node22 checks:

```text
port 18080: not listening
KFD PIDs: none
GPU use: 0%
```

ROCm still reported stale-looking VRAM accounting after the process stopped,
but `rocm-smi --showpids` showed no KFD processes and no embedding service was
listening.

## Boundary

This refresh must not be treated as evidence that the package contents are
mathematical proof, empirical result, peer review, arXiv/journal submission, or
a broad theory. It only makes the Phase-II package and prompt discoverable in
RAG. Primary files remain the authority.
