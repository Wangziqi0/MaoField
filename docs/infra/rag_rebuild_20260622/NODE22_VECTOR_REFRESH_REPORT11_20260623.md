# Node22 Vector Refresh For Report(11) — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (11) and adding the q4 hypercube zero-GPU feasibility artifacts:

- `docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- `scripts/build_hypercube_schema_20260623.py`
- `scripts/q4_hypercube_zero_gpu_audit.py`
- `docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.{json,md}`
- updated `STATE.md`, `MD_CATALOG.md`, and `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after promotion.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `276f5f2`
- Scope file: `canonical_scope_active_20260623_1148_report11.txt`
- Active scope: 320 markdown files
- Candidate chunks: 8734
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report11-20260623_1148`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       964e05a02c4c6a5ff5b31d122e3cbf5304839f3897fea7fb2e292b45d27bdfdb
kb_meta.jsonl sha256:  f275d96aa19fc02ae504bba3dae005050cb18a71b4e3405860d6826870bf60b0
kb_meta.jsonl lines:   8734
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1148_report11
kb_meta.jsonl.bak_pre_20260623_1148_report11
```

## Verification

Candidate metadata checks found chunks for:

- `docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `docs/infra/gpt_deep_research/README_20260622.md`

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report11 q4 hypercube extension formal prereg only token_pos4" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "Q4_HYPERCUBE_ZERO_GPU_AUDIT formal_prereg_only q4 token_pos4 not full panel" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `STATE.md`
- `docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md`

Node22 service status after refresh:

```text
not running port=18080
ROCm status sample after stop: GPU0 busy 0%, GPU1 busy 0%
```

## Guardrail

The strongest allowed claim from this refresh is that report (11), its adoption
note, and the q4 hypercube zero-GPU feasibility artifacts are discoverable
through default RAG. This does not run or approve the full panel, does not
produce a new experiment result, and does not establish `LOSO passed`, `F3
positive`, `residual field observed`, `hypercube field observed`, or `glass box
broken`.
