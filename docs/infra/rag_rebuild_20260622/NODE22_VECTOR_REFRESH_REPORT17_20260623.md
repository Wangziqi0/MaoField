# Node22 Vector Refresh For Report(17) — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (17), the math-ore quotient residual strict audit:

- `docs/infra/gpt_deep_research/deep_research_math_ore_quotient_residual_strict_audit_20260623.md`
- `docs/infra/gpt_deep_research/MATH_ORE_QUOTIENT_RESIDUAL_ADOPTION_NOTE_20260623.md`
- `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md`
- updated `STATE.md`, `MD_CATALOG.md`, `GPT55_PRO_RESEARCH_INDEX_20260622.md`,
  and `docs/infra/gpt_deep_research/README_20260622.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after the candidate index was built.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `68c4ac7`
- Scope file: `canonical_scope_active_20260623_1509_report17.txt`
- Active scope: 331 markdown files
- MaoField active markdown scope: 226 files
- Recursive scan: 7804 files
- Candidate chunks: 8898
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report17-20260623_1509`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`
- Local ignored build log: `rag_build_node22_report17_20260623_1509.log`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       38a48da42432bfb39f50fe0a00635bf0905277fb4d09fe7504a5408c78778bab
kb_meta.jsonl sha256:  634dea15b9d29291ca2ea7a092a6a2050e4e95cd12988998cf39c34bed62434d
kb_meta.jsonl lines:   8898
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1509_report17
kb_meta.jsonl.bak_pre_20260623_1509_report17
```

## Verification

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report17 math ore quotient residual stable non-scalar structure smoke_conjecture_only" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "Hypercube Interaction Analysis Prereg Design Kill Suite invalid_artifact killed_by_random_axis" \
  --top-k 10 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/MATH_ORE_QUOTIENT_RESIDUAL_ADOPTION_NOTE_20260623.md`
- `docs/infra/gpt_deep_research/deep_research_math_ore_quotient_residual_strict_audit_20260623.md`
- `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md`
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/README_20260622.md`
- `docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md`

Node22 service status after refresh:

```text
not running port=18080
GPU0 use: 0%
GPU1 use: 0%
```

## Guardrail

The strongest allowed claim from this refresh is that report (17), its adoption
note, the local zero-GPU prereg design, and updated guardrails are discoverable
through default RAG. This does not run or approve the full panel, does not
produce a scientific result, and does not authorize training, a new loss,
`LOSO passed`, `F3 positive`, `residual field observed`,
`hypercube residual observed`, `hypercube interaction field observed`, or
`glass box broken`.
