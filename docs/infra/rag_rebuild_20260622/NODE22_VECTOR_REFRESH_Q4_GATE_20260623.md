# Node22 Vector Refresh For q4 Gate — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after committing
the D623 q4 implementation gate:

- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `scripts/q4_full_panel_foldlocal_analysis.py`
- updated `STATE.md`, `MD_CATALOG.md`, and `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- updated `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after promotion.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `d4eaed0`
- Scope file: `canonical_scope_active_20260623_095411.txt`
- Active scope: 313 markdown files
- Candidate chunks: 8615
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-q4-gate-20260623_095411`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`

The stable node36 CPU rebuild was started first and interrupted during embedding
after it proved too slow for this small refresh. Its scan and scope outputs were
reused; the runtime index was not promoted until the node22 candidate completed.

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       ab63caba9ad6a6be3a6989d90c7e70f6fc2c383d08f33086db8cc55f5954e712
kb_meta.jsonl sha256:  224a1d37ac689a159bce9d7ab29b419112690115f4bcdb078bddad479e7986b2
kb_meta.jsonl lines:   8615
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_095411_q4gate
kb_meta.jsonl.bak_pre_20260623_095411_q4gate
```

The interrupted CPU rebuild also created `bak_pre_rebuild_20260623_095411`
backups before embedding was stopped; those backups predate this q4-gate
promotion.

## Verification

Candidate metadata checks found chunks for:

- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `scripts/q4_full_panel_foldlocal_analysis.py` as a pointer in active markdown

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "q4 implementation gate full-panel dry-run approval-token fold-local analysis no checkpoint loaded" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Node22 service status after refresh:

```text
not running port=18080
GPU use: 0%
```

## Guardrail

The strongest allowed claim from this refresh is that the q4 implementation gate
and updated project pointers are discoverable through default RAG. This does not
run or approve the full panel, does not produce a new experiment result, and
does not establish `LOSO passed`, `F3 positive`, `mean-null vector field
survives`, or `glass box broken`.
