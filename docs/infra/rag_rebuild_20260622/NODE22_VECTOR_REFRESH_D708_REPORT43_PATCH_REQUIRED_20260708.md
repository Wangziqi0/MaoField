# Node22 Vector Refresh - D708 Report43 Patch Required

## Status

- Date verified on node36: `2026-07-08 14:10 CST`
- Scope owner: node36
- GPU/vector worker: node22, one-shot temporary embedding service
- Sidecar tag: `20260708_1410_report43_patch_required`
- Purpose: sync RAG after SubPro E repair recheck Report43 and node36 adoption.
- Claim boundary: RAG is locator support only. It does not prove theorems,
  publication readiness, MaoField empirical claims, observed fields, broad
  theory, or prior-art novelty.

## Scope

- Scope file:
  `docs/infra/rag_rebuild_20260622/scope_include_maofield_active_md_20260708_1410_report43_patch_required.txt`
- Active markdown files in scope: `759`

New anchors included:

- `docs/infra/gpt_deep_research/deep_research_d708_subpro_e_repair_recheck_report43_20260708.md`
- `docs/infra/gpt_deep_research/D708_SUBPRO_E_REPAIR_RECHECK_REPORT43_ADOPTION_NOTE_20260708.md`
- updated `STATE.md`
- updated `MD_CATALOG.md`

## Build

Node22 worker:

- endpoint: `http://192.168.31.22:18080`
- model label: `bge-m3-temp`
- worker status after stop:
  `docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260708_1410_report43_patch_required.txt`

Build output:

```text
files=759
chunks=13681
dim=1024
embed_seconds=163.3
rate=83.774 text/s
faiss=/home/amd/codex-node36/tmp/rag_20260708_1410_report43_patch_required/candidate_index/kb.faiss
meta=/home/amd/codex-node36/tmp/rag_20260708_1410_report43_patch_required/candidate_index/kb_meta.jsonl
```

Candidate verification:

```text
faiss_ntotal=13681
faiss_dim=1024
meta_count=13681
ntotal_equals_meta=True
```

## Promoted Index

Promoted canonical RAG index:

```text
6b276371dde2cab01a5d7ccd84a6a4bd5534bd799830ac045b999dd8b0660e8c  /media/amd/raid1/rag/index/kb.faiss
717d0cef50e438f5965342846aa36aab2da76cb02e63541a93ae9fdda0672a48  /media/amd/raid1/rag/index/kb_meta.jsonl
13681 /media/amd/raid1/rag/index/kb_meta.jsonl
```

Sidecar records:

- `docs/infra/rag_rebuild_20260622/backup_index_sha256_20260708_1410_report43_patch_required.txt`
- `docs/infra/rag_rebuild_20260622/candidate_index_sha256_20260708_1410_report43_patch_required.txt`
- `docs/infra/rag_rebuild_20260622/candidate_verify_20260708_1410_report43_patch_required.txt`
- `docs/infra/rag_rebuild_20260622/promoted_index_sha256_20260708_1410_report43_patch_required.txt`
- `docs/infra/rag_rebuild_20260622/promoted_meta_count_20260708_1410_report43_patch_required.txt`
- `docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260708_1410_report43_patch_required.txt`

## Verification

Required anchors were found in candidate metadata:

```text
projects/MaoField/STATE.md=True
projects/MaoField/MD_CATALOG.md=True
docs/infra/gpt_deep_research/deep_research_d708_subpro_e_repair_recheck_report43_20260708.md=True
docs/infra/gpt_deep_research/D708_SUBPRO_E_REPAIR_RECHECK_REPORT43_ADOPTION_NOTE_20260708.md=True
PATCH_REQUIRED_OVERCLAIM_OR_PRIOR_ART=True
PATCH_RHETORIC_AND_PRIOR_ART_BOUNDARY=True
finite metric-object identity audit analogue=True
public-ready=True
paper-ready=True
insufficient_artifact=True
```

The `public-ready` and `paper-ready` hits are in forbidden / boundary contexts,
not claim upgrades.

Smoke query outputs:

- `docs/infra/rag_rebuild_20260622/rag_smoke_20260708_1410_report43_patch_required_report.txt`
- `docs/infra/rag_rebuild_20260622/rag_smoke_20260708_1410_report43_patch_required_status.txt`

## Result

RAG now locates Report43's controlling verdict:

```text
PATCH_REQUIRED_OVERCLAIM_OR_PRIOR_ART
```

Current action:

```text
PATCH_RHETORIC_AND_PRIOR_ART_BOUNDARY
```

This refresh does not change the project claim boundary:

- current math remains finite analogue / internal bookkeeping under declared
  finite objects only;
- Mode B MaoField empirical status remains `insufficient_artifact`;
- still forbidden: public-ready, paper-ready, NMI-ready, MaoField
  empirical-positive, observed field, broad black-box or identity theory, and
  proof-by-RAG/JSON/harness/package/prompt/model-output.
