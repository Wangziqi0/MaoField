# Node22 Vector Refresh -- Order-Defect Paper Draft v1.6 Final

Date: 2026-06-29 CST
Authority: node36
Temporary vector worker: node22

## Scope

This final refresh closes the RAG/state skew observed after the intermediate
v1.6 paper-draft package refresh. It indexes the v1.6 wording lock, paper-draft
prompt, package record, updated `STATE.md`, updated `MD_CATALOG.md`, and the
RAG/package records that existed before this build.

Primary indexed context before the build included:

- `STATE.md`;
- `MD_CATALOG.md`;
- `docs/infra/gpt_deep_research/deep_research_order_defect_v1_5_final_gate_audit_20260629.md`;
- `docs/infra/gpt_deep_research/ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md`;
- `docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`;
- `docs/infra/debranded_residual_transport/README_FOR_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_20260629.md`;
- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PAPERDRAFT_V16_20260629.md`;
- updated harness markdown, JSON, and script files.

## Method

Node36:

- regenerated the MaoField file inventory and digest under SSD scratch;
- rebuilt `layer_map.tsv`;
- generated the active canonical markdown scope;
- chunked markdown, called the node22 HTTP embedding worker, wrote candidate
  FAISS and metadata, verified hashes, backed up the prior runtime index, and
  promoted the final index;
- copied scope, logs, hashes, smoke results, and this record into
  `docs/infra/rag_rebuild_20260622/`.

Node22:

- ran a temporary llama.cpp bge-m3 embedding HTTP worker on port 18080;
- did not own scope, manifests, promotion, or final verification;
- was stopped after use.

Final node22 worker status:

```text
stopped pid=2611335
not running port=18080
```

## Final Promoted Index

```text
scanned MaoField files: 8011
active canonical markdown files: 461
chunks: 10466
kb.faiss sha256=8ea8eaadaa4b015f239bf7821665db84daecc9928c9d533a6e29da968d861510
kb_meta.jsonl sha256=5c9a5015c534778a36ddf6a805b01527915b25f408146871a943e3c6e5e71ed0
canonical scope sha256=5ca9b31e1e09928dd4655d036e79130b583bfdeea9a5b66b4bb246e080a023a8
```

Candidate build stats:

```text
files=461
chunks=10466
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=95.332 text/s
```

Final artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260629_1601_v16final
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260629_1601_v16final
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260629_1601_v16final.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v16_final_state_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v16_paper_prompt_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v16_node19_package_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260629_1601_v16final.txt
docs/infra/rag_rebuild_20260622/maofield_file_inventory.tsv
docs/infra/rag_rebuild_20260622/maofield_scan_summary.json
docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md
docs/infra/rag_rebuild_20260622/scope_include_maofield_active_md.txt
docs/infra/rag_rebuild_20260622/scope_include_maofield_all_nonarchive_md.txt
```

## Smoke Checks

Smoke query:

```text
OrderDefect v1.6 paper draft STATE 15:53 wording lock
```

returned top hits including:

- `WORDING_LOCK_V1_6_20260629.md`;
- `NODE22_VECTOR_REFRESH_ORDERDEFECT_PAPERDRAFT_V16_20260629.md`;
- `ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md`;
- `MD_CATALOG.md`;
- `GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md`.

Smoke query:

```text
GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT gate-conditioned paper draft 4-6 page
```

returned top hits including:

- `README_FOR_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_20260629.md`;
- `DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PAPERDRAFT_V16_20260629.md`;
- `README.md`;
- `STATE.md`.

Smoke query:

```text
MaoField_PRO_OrderDefect_PaperDraft_V16_20260629_1550final zip sha256 node19 package record
```

returned top hits including:

- `DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PAPERDRAFT_V16_20260629.md`;
- `MD_CATALOG.md`.

## Self-Reference Boundary

This record is written after final index promotion. The promoted index can
locate the v1.6 prompt, wording lock, package record, `STATE.md`,
`MD_CATALOG.md`, and related files. It may not locate this exact refresh record
until a future refresh. The hash lines in this file and
`promoted_hashes_20260629_1601_v16final.txt` are the primary post-build truth
for this refresh.

The final node19 zip hash is intentionally not embedded in the `STATE.md` and
`MD_CATALOG.md` snapshots inside that zip. The authoritative zip hash is the
external package record
`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PAPERDRAFT_V16_20260629.md`.
Because the package record and this boundary note are post-promotion primary
files, RAG may still retrieve intermediate package snippets for semantically
similar package-hash queries. Treat RAG as a locator; resolve the final package
truth from the primary package record and node19 hash readback.

## Evidence Boundary

RAG is a locator only. Claims still require primary files, code, JSON/JSONL,
logs, verdicts, or formal proofs. This refresh does not authorize full-panel,
training, new-loss, observed-field, glass-box, F3/LOSO-positive, posted
preprint, paper acceptance, or completed-formal-system claims. The order-defect
materials remain Mode A finite-dimensional proof/harness material with the
strongest local verdict `definitions_and_harness_viable_only`; MaoField Mode B
remains `insufficient_artifact`.
