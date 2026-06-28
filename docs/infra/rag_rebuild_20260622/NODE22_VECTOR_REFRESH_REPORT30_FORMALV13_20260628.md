# Node22 Vector Refresh — Report(30) / Formal v1.3 Package

Date: 2026-06-28 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh promotes the report (30) acceptance materials and the Formal v1.3
theorem-strengthening prompt/package metadata into the default node36 RAG
locator.

Primary additions before the final build included:

- `deep_research_formal_residual_transport_v1_2_report29_minor_revision_audit_20260628.md`;
- `FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`;
- `GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PROMPT_20260628.md`;
- `README_FOR_PRO_FORMALV13_THEOREM_STRENGTHENING_20260628.md`;
- `DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_FORMALV13_THEOREM_STRENGTHENING_20260628.md`;
- updated `STATE.md`, `MD_CATALOG.md`, `GPT55_PRO_RESEARCH_INDEX_20260622.md`,
  and current README/navigation files.

## Method

Node36:

- generated file inventory and digest under SSD scratch first;
- promoted durable scan outputs into `docs/infra/rag_rebuild_20260622/`;
- generated canonical active markdown scope;
- chunked markdown, wrote FAISS and metadata, and verified/promoted the final
  index.

Node22:

- ran a temporary llama.cpp bge-m3 embedding HTTP worker only;
- did not own scope, manifests, promotion, or final verification;
- was stopped after use.

Final node22 worker status:

```text
stopped pid=2430062
not running port=18080
```

## Final Promoted Index

```text
active canonical markdown files: 421
chunks: 9992
kb.faiss sha256=47b7603da21cb325af9e78e0efc0ea004bb741d7529f37929278e5e2a0411fc4
kb_meta.jsonl sha256=3fdf961fb521c5f615f306340e933871082a1a4c64982b876261fc454b5487cd
canonical scope sha256=0ba199ec3e2c529865b1d90196f8473966eca8a9022f4b6c180c370468922fef
```

Candidate build stats:

```text
files=421
chunks=9992
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=96.215 text/s
```

Final artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260628_1152_report30final2
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260628_1152_report30final2
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260628_1152_report30final2.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260628_1152_report30final2.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260628_1152_report30final2.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260628_1152_report30final2.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260628_1152_report30final2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_report30_v13_20260628_1152_report30final2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_state_d628_20260628_1152_report30final2.txt
```

## Smoke Queries

The first smoke query:

```text
D628 report30 accepted after minor revision Formal v1.3 theorem strengthening node19 package
```

returned top hits including:

- `docs/infra/debranded_residual_transport/README.md`;
- `GPT55_PRO_RESEARCH_INDEX_20260622.md` section 4.31;
- `STATE.md` D628 stamp;
- `FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`.

The second smoke query:

```text
MaoField current state D628 report30 node19 v1.3 prompt insufficient_artifact
```

returned top hits including:

- `deep_research_formal_residual_transport_v1_2_report29_minor_revision_audit_20260628.md`;
- `DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md` D628 section;
- `STATE.md`;
- `FORMAL_NOTE_V1_2_20260627.md` boundary section.

## Self-Reference Boundary

This refresh record itself was written after final index promotion. Therefore
the final RAG index can locate the report (30) materials, package metadata,
prompt, and updated status/navigation files, but this record may require the
next refresh to be discoverable as an indexed chunk. Use this record as the
canonical post-build hash log.

## Evidence Boundary

RAG is a locator only. Claims still require primary files, code, JSON/JSONL,
logs, verdicts, or formal proofs. This refresh does not authorize full-panel,
training, new-loss, observed-field, glass-box, F3/LOSO-positive, or
completed-formal-system claims.
