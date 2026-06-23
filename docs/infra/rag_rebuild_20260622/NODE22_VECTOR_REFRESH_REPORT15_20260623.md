# Node22 Vector Refresh For Report(15) — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (15), the future math-object / weighted interaction-field audit:

- `docs/infra/gpt_deep_research/deep_research_future_math_objects_interaction_field_audit_20260623.md`
- `docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.json`
- updated `STATE.md`, `MD_CATALOG.md`, `GPT55_PRO_RESEARCH_INDEX_20260622.md`,
  `docs/infra/gpt_deep_research/README_20260622.md`, and
  `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after the candidate index was built.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `fcdf6a5`
- Scope file: `canonical_scope_active_20260623_1336_report15.txt`
- Active scope: 327 markdown files
- MaoField active markdown scope: 222 files
- Recursive scan: 7799 files
- Candidate chunks: 8843
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report15-20260623_1336`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`
- Local ignored build log: `rag_build_node22_report15_20260623_1336.log`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       869098306cf3b17424eb8240179c8349e74d62cdc18972e4290a50c6b12b996a
kb_meta.jsonl sha256:  acc697eed82306bde4148bbefeff74806d5fb09e0abc030a2fbd9850c27081a1
kb_meta.jsonl lines:   8843
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1336_report15
kb_meta.jsonl.bak_pre_20260623_1336_report15
```

## Verification

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report15 weighted product partition interaction field smoke_conjecture_only" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT interaction mean-null ratio sigma2 sigma1" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md`
- `docs/infra/gpt_deep_research/deep_research_future_math_objects_interaction_field_audit_20260623.md`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md`
- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/README_20260622.md`
- `docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md`

Node22 service status after refresh:

```text
not running port=18080
```

## Guardrail

The strongest allowed claim from this refresh is that report (15), its adoption
note, the local interaction-field smoke audit, and updated guardrails are
discoverable through default RAG. This does not run or approve the full panel,
does not produce a scientific result, and does not authorize training, a new
loss, `LOSO passed`, `F3 positive`, `residual field observed`,
`hypercube residual observed`, `hypercube interaction field observed`, or
`glass box broken`.
