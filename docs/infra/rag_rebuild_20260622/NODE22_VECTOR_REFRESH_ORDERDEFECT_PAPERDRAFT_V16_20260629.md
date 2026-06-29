# Node22 Vector Refresh -- Order-Defect Paper Draft v1.6

Date: 2026-06-29 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh records the post-v1.6 state after archiving the Pro v1.5
final-gate audit, adopting it as a wording WARN, adding the v1.6 wording lock,
canonicalizing the harness boundary sentence, rerunning the v1.3 deterministic
harness, adding the gate-conditioned paper-draft prompt, and updating
`STATE.md`, `MD_CATALOG.md`, and debranded residual transport navigation.

Primary indexed context before the build included:

- `deep_research_order_defect_v1_5_final_gate_audit_20260629.md`;
- `ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md`;
- `WORDING_LOCK_V1_6_20260629.md`;
- `GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md`;
- `README_FOR_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_20260629.md`;
- updated `README.md`, `PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`,
  `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`;
- updated `SYNTHETIC_HARNESS_V1_3_20260628.md` and
  `synthetic_harness_v1_3_20260628.json`;
- updated `scripts/debranded_residual_transport_harness_v1_3.py`;
- `scripts/rag_build_index_node22_http.py`.

## Method

Node36:

- regenerated the MaoField file inventory and digest under SSD scratch;
- regenerated the active canonical markdown scope after rebuilding
  `layer_map.tsv`;
- chunked markdown, called the node22 HTTP embedding worker, wrote candidate
  FAISS and metadata, verified hashes, and promoted the final index;
- retained scope, logs, hashes, smoke results, and this record under
  `docs/infra/rag_rebuild_20260622/`.

Node22:

- ran a temporary llama.cpp bge-m3 embedding HTTP worker on port 18080;
- did not own scope, manifests, promotion, or final verification;
- was stopped after use.

Final node22 worker status:

```text
stopped pid=2608147
not running port=18080
```

## Final Promoted Index

```text
active canonical markdown files: 459
chunks: 10445
kb.faiss sha256=753ac8154ed389dfb75b3e60c89b7a4eb5a8572720d19e8c8843ecb4cddcafa1
kb_meta.jsonl sha256=12145d484ac4b52a078d6631cc15050f947e478f085596086451a8f1014fa828
canonical scope sha256=c73ca51ab3afeba97e6cceb53ed1bf26a68b487be388691c30e5955bfb09262c
```

Candidate build stats:

```text
files=459
chunks=10445
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=95.123 text/s
```

Final artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260629_1540_v16paper
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260629_1540_v16paper
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260629_1540_v16paper.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v16_wording_lock_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v16_paper_prompt_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v15_final_gate_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260629_1540_v16paper.txt
docs/infra/rag_rebuild_20260622/maofield_file_inventory.tsv
docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md
docs/infra/rag_rebuild_20260622/maofield_scan_summary.json
```

## Smoke Checks

Smoke query:

```text
v1.6 wording lock floating-point harness JSON floats paper draft
```

returned top hits including:

- `docs/infra/debranded_residual_transport/README.md`;
- `STATE.md`;
- `MD_CATALOG.md`;
- `ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md`;
- `GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md`;
- `deep_research_order_defect_v1_5_final_gate_audit_20260629.md`.

Smoke query:

```text
GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT gate-conditioned short note
```

returned top hits including:

- `docs/infra/debranded_residual_transport/README.md`;
- `README_FOR_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_20260629.md`;
- `STATE.md`.

Smoke query:

```text
deep_research_order_defect_v1_5_final_gate short_note_requires_minor_wording
```

returned top hits including:

- `deep_research_order_defect_v1_5_final_gate_audit_20260629.md`;
- `STATE.md`;
- `ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md`;
- `MD_CATALOG.md`;
- `WORDING_LOCK_V1_6_20260629.md`.

## Self-Reference Boundary

This record is written after final index promotion.  The promoted index can
locate the v1.6 prompt, wording lock, adoption note, STATE, MD_CATALOG, and
related files, but it may not locate this refresh record or any later package
record until a future refresh.  The hash lines in this file and
`promoted_hashes_20260629_1540_v16paper.txt` are the primary post-build truth
for this refresh.

## Evidence Boundary

RAG is a locator only.  Claims still require primary files, code, JSON/JSONL,
logs, verdicts, or formal proofs.  This refresh does not authorize full-panel,
training, new-loss, observed-field, glass-box, F3/LOSO-positive, posted
preprint, paper acceptance, or completed-formal-system claims.  The
order-defect materials remain Mode A finite-dimensional proof/harness material
with the strongest local verdict `definitions_and_harness_viable_only`;
MaoField Mode B remains `insufficient_artifact`.
