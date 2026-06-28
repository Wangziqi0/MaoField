# Node22 Vector Refresh — Report(31) Final Order-Defect Package

Date: 2026-06-28 CST
Authority: node36
Temporary vector worker: node22

## Scope

This final report(31) refresh indexes the corrected `1734final` package state,
the guarded Formal v1.3 order-defect proof-audit materials, and the D628 17:37
`STATE.md` truth source.

Primary indexed context before the build included:

- report (31) archive and guarded adoption note;
- Formal v1.3 order-defect workplan and GPT-5.5 Pro proof-audit prompt;
- node19 package record for
  `MaoField_PRO_FoundationalResidualTransport_FormalV13_OrderDefectProof_Report31_20260628_1734final.zip`;
- updated `STATE.md`, `MD_CATALOG.md`, `GPT55_PRO_RESEARCH_INDEX_20260622.md`,
  and current README/navigation files;
- superseded `NODE22_VECTOR_REFRESH_REPORT31_ORDERDEFECT_20260628.md` marked
  as intermediate provenance.

## Method

Node36:

- generated file inventory and digest under SSD scratch first;
- generated canonical active markdown scope;
- chunked markdown, wrote FAISS and metadata, verified/promoted the final index;
- retained scope, logs, hashes, and smoke results under
  `docs/infra/rag_rebuild_20260622/`.

Node22:

- ran a temporary llama.cpp bge-m3 embedding HTTP worker only;
- did not own scope, manifests, promotion, or final verification;
- was stopped after use.

Final node22 worker status:

```text
stopped pid=2467191
not running port=18080
```

## Final Promoted Index

```text
active canonical markdown files: 428
chunks: 10074
kb.faiss sha256=ca498170f96ad7b09015194e688df92def0461d0607ed98c2dda2f60cfe82e2a
kb_meta.jsonl sha256=18efe1b9fda30663ed1dca63f54ee98be08caf20547f693b28224d4f321ab67d
canonical scope sha256=80ae320b75ade8334e6e86ed691e794c9cdcc459be6b006630275976ff86bca0
```

Candidate build stats:

```text
files=428
chunks=10074
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=95.301 text/s
```

Final artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260628_1737_report31final
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260628_1737_report31final
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260628_1737_report31final.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260628_1737_report31final.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260628_1737_report31final.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260628_1737_report31final.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260628_1737_report31final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_state_final_20260628_1737_report31final.txt
```

## Smoke And Direct Checks

Smoke query:

```text
D628 17:37 report31 1734final order defect proof audit 50421728
```

returned top hits including:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md` with the `1734final` package hash;
- `STATE.md` with the D628 17:37 stamp;
- `docs/infra/debranded_residual_transport/README.md`;
- `MD_CATALOG.md`.

Direct metadata grep of `/media/amd/raid1/rag/index/kb_meta.jsonl` confirmed
indexed chunks for:

- `STATE.md` D628 17:37 stamp;
- node19 `1734final` package path;
- zip sha256 `50421728ac178716074cf917208c3670e2d9202c8a3b37965456bc8addb0462c`;
- package record prompt sha256 `2450a5ef34e1730d4fe178a28fd6f72b9f7afe451d093f5342f1fc812795ffde`.

## Self-Reference Boundary

This final RAG record is written after the final index promotion, so the final
index can locate the corrected report(31) STATE/package context but may not
locate this record until a future refresh. Use this record as the canonical
post-build hash log.

## Evidence Boundary

RAG is a locator only. Claims still require primary files, code, JSON/JSONL,
logs, verdicts, or formal proofs. This refresh does not authorize full-panel,
training, new-loss, observed-field, glass-box, F3/LOSO-positive, or
completed-formal-system claims. Report (31) remains a guarded proof-audit plan,
not a completed theorem.
