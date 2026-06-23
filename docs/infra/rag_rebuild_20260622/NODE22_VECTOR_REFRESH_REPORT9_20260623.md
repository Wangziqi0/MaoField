# Node22 Vector Refresh For Report(9) — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (9) and incorporating the residual-field q4 analysis guard:

- `docs/infra/gpt_deep_research/deep_research_q4_residual_field_strict_math_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- updated `scripts/q4_full_panel_foldlocal_analysis.py`
- updated `scripts/math_turn_loso_audit.py`
- updated `STATE.md`, `MD_CATALOG.md`, and `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after promotion.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `e47bc88`
- Scope file: `canonical_scope_active_20260623_1054_report9.txt`
- Active scope: 316 markdown files
- Candidate chunks: 8674
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report9-20260623_1054`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       072fa57a86c480a95f6e7cf360cc547c625e7204ff5a19a511a1f54c48c327d8
kb_meta.jsonl sha256:  f9335ca9fe80d020b7e23c8fad6f9ee7a444c4e89dd88610b25fc59c3c3bba11
kb_meta.jsonl lines:   8674
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1054_report9
kb_meta.jsonl.bak_pre_20260623_1054_report9
```

## Verification

Candidate metadata checks found chunks for:

- `docs/infra/gpt_deep_research/deep_research_q4_residual_field_strict_math_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report9 q4 residual field r_i u_i v random projection multiplicity guard" \
  --top-k 8 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`

Node22 service status after refresh:

```text
not running port=18080
GPU use: 0%
```

## Guardrail

The strongest allowed claim from this refresh is that report (9), its adoption
note, and the residual-field q4 analysis pointers are discoverable through
default RAG. This does not run or approve the full panel, does not produce a new
experiment result, and does not establish `LOSO passed`, `F3 positive`,
`mean-null vector field survives`, or `glass box broken`.
