# Node22 Vector Rebuild Record — 2026-06-22

## Boundary

This record documents a node36-controlled RAG rebuild that used node22 only as a
temporary external vector worker. Node36 generated scope, scan outputs, metadata,
FAISS promotion, and verification. Node22 ran a temporary `llama.cpp`
`bge-m3-f16.gguf` embedding service on port `18080`, then the service was
stopped after use.

RAG remains a locator. It is not primary evidence for MaoField claims.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Scope file: `canonical_scope_active_20260622_230118.txt`
- Active scope: 309 markdown files
- Candidate chunks: 8562
- Project scan summary: `maofield_scan_summary.json`
- Data digest: `maofield_data_digest_20260622.md`

## Vector Worker

- Worker: node22 `192.168.31.22`
- GPU: RX 9070 XT / `gfx1201`
- Temporary service script in node22 scratch:
  `/home/amd/codex-node22/tmp/maofield-rag-vector-20260622/node22_bge_temp_service.sh`
- Temporary 36-side builder in scratch:
  `/home/amd/codex-node36/tmp/maofield-rag-rebuild-20260622_223448/build_index_node22_http.py`
- Embedding backend: `llama.cpp` + `/home/amd/models/bge-m3-f16.gguf`
- HTTP endpoint during build: `http://192.168.31.22:18080/v1/embeddings`
- Service status after build: stopped

## Outputs

Promoted to `/media/amd/raid1/rag/index` during the D622 post-q4 rebuild. Check current
runtime hashes directly with:

```bash
sha256sum /media/amd/raid1/rag/index/kb.faiss \
  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-rebuild backups are kept next to the runtime index as
`kb.faiss.bak_pre_node22_*` and `kb_meta.jsonl.bak_pre_node22_*`.

Representative final build stats:

- files: 309
- chunks/vectors: 8562
- embedding seconds: 88.0
- rate: 97.269 text/s
- dimension: 1024

## Verification

Exact metadata path checks passed for:

- `docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md`
- `docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md`
- `docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_NEGATIVE_SMOKE_20260622.md`
- `docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md`
- `docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md`

Default `kb_search.py` smoke queries passed for:

- report(6) / full-panel-not-approved / fold-local q4 analysis path
- fail-fast negative smokes / schema-builder-source-q4-bin mismatches
- multi-checkpoint smoke / seed1-gen0, seed2-gen5, seed42-gen9

## Guardrail

The strongest allowed claim from this rebuild is that latest q4/report markdown
is now discoverable through default RAG. It does not approve full-panel
generation, does not produce a new experiment result, and does not establish
`LOSO passed`, `F3 positive`, `mean-null vector field survives`, or `glass box
broken`.
