# Node22 Vector Refresh For Mode A Prompt / Mode B Skeleton — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after adding:

- `docs/infra/gpt_deep_research/GPT55_PRO_MODE_A_MATH_DISCOVERY_PROMPT_20260623.md`
- `scripts/q4_hypercube_interaction_prereg_analysis.py`
- updated `GPT55_PRO_RESEARCH_INDEX_20260622.md`, `MD_CATALOG.md`, `STATE.md`,
  `docs/infra/gpt_deep_research/README_20260622.md`, and
  `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after the candidate index was built.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `73cf9c8`
- Scope file: `canonical_scope_active_20260623_1556_modea.txt`
- Active scope: 333 markdown files
- MaoField active markdown scope: 228 files
- Recursive scan: 7808 files
- Candidate chunks: 8916
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-modea-20260623_1556`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`
- Local ignored build log: `rag_build_node22_modea_20260623_1556.log`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       762ecd2f686d878b65df668b626f6e3ceaf67daea40d1f885c19321f441e824e
kb_meta.jsonl sha256:  451bd9039f3e23584bf04187e5b39159e7003d62e23ae2660fdb1c32c049dcee
kb_meta.jsonl lines:   8916
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1556_modea
kb_meta.jsonl.bak_pre_20260623_1556_modea
```

## Verification

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "GPT55 Pro Mode A mathematical discovery prompt deflated MaoField conceptual ore quotient residual" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "q4_hypercube_interaction_prereg_analysis eligible_for_next_design_review_only old aggregate invalid_artifact" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/GPT55_PRO_MODE_A_MATH_DISCOVERY_PROMPT_20260623.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md`
- `docs/infra/gpt_deep_research/MATH_ORE_QUOTIENT_RESIDUAL_ADOPTION_NOTE_20260623.md`
- `MD_CATALOG.md`
- `STATE.md`

Node22 service status after refresh:

```text
not running port=18080
GPU0 use: 0%
GPU1 use: 0%
```

## Guardrail

The strongest allowed claim from this refresh is that the Mode A GPT-5.5 Pro
prompt, the Mode B skeleton pointers, and updated guardrails are discoverable
through default RAG. This does not run or approve the full panel, does not
produce a scientific result, and does not authorize training, a new loss,
`LOSO passed`, `F3 positive`, `interaction field observed`,
`residual field observed`, `hypercube residual observed`, or
`glass box broken`.
