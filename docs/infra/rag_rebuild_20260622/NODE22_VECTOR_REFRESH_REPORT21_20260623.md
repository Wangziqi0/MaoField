# Node22 Vector Refresh For Report 21 Finite ANOVA Formalization — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (21) and adding the node36 adoption note:

- `docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`
- `docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after the candidate index was built.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `bd6c428`
- Scope file: `canonical_scope_active_20260623_1733_report21.txt`
- Active scope: 340 markdown files
- MaoField active markdown scope: 235 files
- Recursive scan: 7817 files
- Candidate chunks: 9006
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report21-20260623_1733`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`
- Local ignored build log: `rag_build_node22_report21_20260623_1733.log`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       e522eccb5ed21554f33a9ec9fe567fb3821664c7eb2ec20419ce49535ee090d2
kb_meta.jsonl sha256:  2920ce4dcf36eeda9c813d128fd5805a61c87491afc36ecac49ff301a65c391b
kb_meta.jsonl lines:   9006
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1733_report21
kb_meta.jsonl.bak_pre_20260623_1733_report21
```

Backup hashes:

```text
kb.faiss.bak sha256:       b4f65861adf31abf7a08d9b8095627bed115e484629187c9f3578b63a334a1f2
kb_meta.jsonl.bak sha256:  5766c75ec71837b065d75746c7ec07041f2ad36a7f73153cbad3db93e69c1541
```

## Verification

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report21 finite weighted ANOVA admissible triple quotient residual no-go" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE admissible triple product weight Hoeffding insufficient_artifact" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`
- `docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md`
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

The strongest allowed claim from this refresh is that report (21), its adoption
note, and updated guardrails are discoverable through default RAG. This does not
run or approve the full panel, does not produce a scientific result, and does
not authorize training, a new loss, `LOSO passed`, `F3 positive`,
`interaction field observed`, `residual field observed`,
`hypercube residual observed`, or `glass box broken`.
