# Node22 Vector Refresh For Report(13) — 2026-06-23

## Boundary

This record documents a node36-controlled default RAG refresh after archiving
GPT/PRO report (13), the current-repo q4 hypercube strict audit:

- `docs/infra/gpt_deep_research/deep_research_q4_hypercube_current_repo_strict_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_HYPERCUBE_CURRENT_REPO_STRICT_AUDIT_ADOPTION_NOTE_20260623.md`
- updated `STATE.md`, `MD_CATALOG.md`, `GPT55_PRO_RESEARCH_INDEX_20260622.md`,
  `docs/infra/gpt_deep_research/README_20260622.md`, and
  `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`

Node22 was used only as a temporary external vector worker. Node36 generated
scope, chunks, metadata, FAISS promotion, and verification. Node22 ran the
temporary `llama.cpp` bge-m3 embedding service on port `18080`, then the service
was stopped after promotion.

RAG remains a locator, not primary evidence.

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git head at scan: `b0b4720`
- Scope file: `canonical_scope_active_20260623_1250_report13.txt`
- Active scope: 323 markdown files
- MaoField active markdown scope: 218 files
- Candidate chunks: 8780
- Build scratch: `/home/amd/codex-node36/tmp/maofield-rag-report13-20260623_1250`
- Node22 endpoint during build: `http://192.168.31.22:18080/v1/embeddings`

## Runtime Index After Promotion

Promoted to `/media/amd/raid1/rag/index` on 2026-06-23.

```text
kb.faiss sha256:       2a40df24ac47eaf2db2742bb86400b36470979029f47709f66fc48dacbc1ecac
kb_meta.jsonl sha256:  63c51366785e1a101fc03a1f36a8ba18d4e8b64b5331593bdaac22075bda61c5
kb_meta.jsonl lines:   8780
```

Pre-refresh backups were created next to the runtime index:

```text
kb.faiss.bak_pre_20260623_1250_report13
kb_meta.jsonl.bak_pre_20260623_1250_report13
```

## Verification

Candidate metadata checks found chunks for:

- `docs/infra/gpt_deep_research/deep_research_q4_hypercube_current_repo_strict_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_HYPERCUBE_CURRENT_REPO_STRICT_AUDIT_ADOPTION_NOTE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/README_20260622.md`
- `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`

Default `kb_search.py` smoke queries passed:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report13 current repo hypercube zero GPU formal prereg no code authorization" \
  --top-k 8 --project MaoField

HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "Q4 Hypercube Current-Repo Strict Audit Adoption Note future-only gates no code change authorized" \
  --top-k 8 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/deep_research_q4_hypercube_current_repo_strict_audit_20260623.md`
- `docs/infra/gpt_deep_research/Q4_HYPERCUBE_CURRENT_REPO_STRICT_AUDIT_ADOPTION_NOTE_20260623.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/README_20260622.md`

Node22 service status after refresh:

```text
not running port=18080
ROCm status sample after stop: GPU0 busy 0%, GPU1 busy 0%
```

## Guardrail

The strongest allowed claim from this refresh is that report (13), its adoption
note, and current-repo hypercube guardrails are discoverable through default
RAG. This does not run or approve the full panel, does not produce a new
experiment result, and does not authorize `q4_hypercube_foldlocal_analysis.py`,
training, a new loss, `LOSO passed`, `F3 positive`, `residual field observed`,
`hypercube residual observed`, or `glass box broken`.
