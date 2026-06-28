# Node22 Vector Refresh — Report(31) Final Order-Defect Package

Date: 2026-06-28 CST
Authority: node36
Temporary vector worker: node22

## Scope

This final report(31) refresh record now tracks the corrected `1758fixed`
package state, the guarded Formal v1.3 order-defect proof-audit materials, and
the D628 17:58 `STATE.md` truth source.

Primary indexed context before the build included:

- report (31) archive and guarded adoption note;
- Formal v1.3 order-defect workplan and GPT-5.5 Pro proof-audit prompt;
- node19 package record for
  `MaoField_PRO_FoundationalResidualTransport_FormalV13_OrderDefectProof_Report31_20260628_1758fixed.zip`;
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
stopped pid=2473121
not running port=18080
```

## Final Promoted Index

```text
active canonical markdown files: 429
chunks: 10083
kb.faiss sha256=ed25e1035ea6f90b1b6ede669a26a351528a1dc443579a538b8e9185550bd0d1
kb_meta.jsonl sha256=5905def22115073bbda1cb33e68bc9deb309d20f9ef6c83245f9e69b7f9b7276
canonical scope sha256=1a78578f215fe3771f37e9c9f2e4a743e0e2a0b023f1877ac871d373ad5a5309
```

Candidate build stats:

```text
files=429
chunks=10083
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=95.359 text/s
```

Final artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260628_1824_packagefix_final2
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260628_1824_packagefix_final2
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260628_1824_packagefix_final2.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260628_1824_packagefix_final2.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260628_1824_packagefix_final2.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260628_1824_packagefix_final2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_state_packagefix_20260628_1824_packagefix_final2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_package_record_20260628_1824_packagefix_final2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_math_guardrails_20260628_1824_packagefix_final2.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260628_1824_packagefix_final2.txt
```

## Smoke And Direct Checks

Smoke query:

```text
D628 17:58 report31 1758fixed order defect proof audit 3780b31e
```

returned top hits including:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md` with the `1758fixed` package hash;
- `STATE.md` with the D628 17:58 stamp;
- `docs/infra/debranded_residual_transport/README.md`;
- `MD_CATALOG.md`.

Direct metadata grep of `/media/amd/raid1/rag/index/kb_meta.jsonl` confirmed
indexed chunks for:

- `STATE.md` D628 17:58 stamp;
- node19 `1758fixed` package path;
- zip sha256 `3780b31e6f420c7dbf07d9378849f348c3ee151680c20e14aa84ee3ba4a6f7bb`;
- package record prompt sha256 `2450a5ef34e1730d4fe178a28fd6f72b9f7afe451d093f5342f1fc812795ffde`.

## Self-Reference Boundary

This final RAG record is updated after the final index promotion, so the final
index can locate the corrected report(31) STATE/package context and may locate
a pre-final version of this record, but the current hash lines in this file are
primary-file truth. Use this record as the canonical post-build hash log.

## Evidence Boundary

RAG is a locator only. Claims still require primary files, code, JSON/JSONL,
logs, verdicts, or formal proofs. This refresh does not authorize full-panel,
training, new-loss, observed-field, glass-box, F3/LOSO-positive, or
completed-formal-system claims. Report (31) remains a guarded proof-audit plan,
not a completed theorem.
