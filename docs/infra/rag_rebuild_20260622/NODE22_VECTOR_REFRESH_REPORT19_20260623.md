# Node22 Vector Refresh For Report 19 Quotient Residual Framework — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (19), adding the node36 adoption note, and adding a follow-up
GPT-5.5 Pro prompt for quotient-residual theorem/no-go work:

- `docs/infra/gpt_deep_research/deep_research_mode_a_quotient_residual_kill_framework_20260623.md`
- `docs/infra/gpt_deep_research/MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after the candidate index was built.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `3351840`
- Scope file: `canonical_scope_active_20260623_1642_report19.txt`
- Active scope: 337 markdown files
- MaoField active markdown scope: 232 files
- Recursive scan: 7813 files
- Candidate chunks: 8962
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report19-20260623_1642`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`
- Local ignored build log: `rag_build_node22_report19_20260623_1642.log`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       b4f65861adf31abf7a08d9b8095627bed115e484629187c9f3578b63a334a1f2
kb_meta.jsonl sha256:  5766c75ec71837b065d75746c7ec07041f2ad36a7f73153cbad3db93e69c1541
kb_meta.jsonl lines:   8962
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1642_report19
kb_meta.jsonl.bak_pre_20260623_1642_report19
```

Backup hashes:

```text
kb.faiss.bak sha256:       762ecd2f686d878b65df668b626f6e3ceaf67daea40d1f885c19321f441e824e
kb_meta.jsonl.bak sha256:  451bd9039f3e23584bf04187e5b39159e7003d62e23ae2660fdb1c32c049dcee
```

## Verification

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report19 quotient residual kill framework rank1 shadow insufficient_artifact" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE best object R_t Pi_N_perp" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT theorem no-go random subspace coarsening" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/deep_research_mode_a_quotient_residual_kill_framework_20260623.md`
- `docs/infra/gpt_deep_research/MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `MD_CATALOG.md`
- `STATE.md`

Node22 service status after refresh:

```text
not running port=18080
GPU0 use: 0%
GPU1 use: 0%
```

## Guardrail

The strongest allowed claim from this refresh is that report (19), its adoption
note, the follow-up Pro prompt, and updated guardrails are discoverable through
default RAG. This does not run or approve the full panel, does not produce a
scientific result, and does not authorize training, a new loss, `LOSO passed`,
`F3 positive`, `interaction field observed`, `residual field observed`,
`hypercube residual observed`, or `glass box broken`.
