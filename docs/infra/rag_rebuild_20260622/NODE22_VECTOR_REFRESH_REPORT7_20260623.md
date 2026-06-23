# Node22 Vector Refresh For Report(7) — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (7):

- `docs/infra/gpt_deep_research/deep_research_q4_object_strict_math_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_OBJECT_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after promotion.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Scope file: `canonical_scope_active_20260623_091046.txt`
- Active scope: 311 markdown files
- Candidate chunks: 8603
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-refresh-report7-20260623_091046`
- Build log: `rag_build_node22_report7_20260623_091046.log`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:     6c03beb1ac728bba193876a39392854fc9ce71cb710be9a9be987e37500b085c
kb_meta.jsonl sha256: 8fe186b6161184e62442c6d4951826608d8924908a22061a0d72b55234d114e1
kb_meta.jsonl lines: 8603
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_report7_20260623_091046
kb_meta.jsonl.bak_pre_report7_20260623_091046
```

## Verification

Exact metadata path checks passed for:

- `docs/infra/gpt_deep_research/deep_research_q4_object_strict_math_audit_20260623.md`
  - chunks: 29
- `docs/infra/gpt_deep_research/Q4_OBJECT_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
  - chunks: 7
- `STATE.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Default `kb_search.py` smoke query passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report7 q4 object strict math audit fold-local q4 mean-null residual current implemented artifact not mathematical advance" \
  --top-k 8 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `Q4_OBJECT_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`
- `STATE.md`
- `deep_research_q4_object_strict_math_audit_20260623.md`

Node22 service status after refresh:

```text
not running port=18080
GPU use: 0%
```

## Guardrail

The strongest allowed claim from this refresh is that report (7), its adoption
note, and updated project pointers are discoverable through default RAG. This
does not approve full-panel generation, does not produce a new experiment
result, and does not establish `LOSO passed`, `F3 positive`, `mean-null vector
field survives`, or `glass box broken`.
