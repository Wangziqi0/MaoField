# Node22 Vector Refresh - D708 Extra SubPro A/E Identity Check

## Scope

This refresh indexes the D708 extra SubPro A/E identity-check package and its
local agent/RAG claim-gate record.

New anchors include:

- `docs/infra/MAOFIELD_PRO_D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_PACKAGE_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_NODE19_DELIVERY_20260708.md`
- `docs/infra/recovery/D708_EXTRA_SUBPRO_AE_IDENTITY_CLAIM_GATE_AGENT_REPORT_20260708.md`
- `docs/infra/recovery/D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_TASKBOOK_20260708.md`
- `docs/infra/recovery/D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_PACKAGE_README_20260708.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_D708_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_PROMPT_20260708.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_D708_SUBPRO_E_REDTEAM_IDENTITY_CHECK_PROMPT_20260708.md`

This refresh does not upgrade the project to paper-ready, public-ready,
submission-ready, NMI-ready, empirical-positive, or broad-theory status.

## Build

- Date verified: `2026-07-08 12:54:07 CST`
- Host: node36 as pipeline authority
- Vector worker: node22 one-shot BGE-M3 compatible llama.cpp service on port
  `18080`
- Sidecar tag: `20260708_1245_extra_subpro_identity_check`
- Node36 scratch root:
  `/home/amd/codex-node36/tmp/rag_20260708_1245_extra_subpro_identity_check`
- Candidate index:
  `/home/amd/codex-node36/tmp/rag_20260708_1245_extra_subpro_identity_check/candidate_index`
- Remote node22 worker root:
  `/home/amd/codex-node22/tmp/maofield-rag-vector-20260708_1245_extra_subpro_identity_check`

Build command class:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python scripts/rag_build_index_node22_http.py \
  --file-list /home/amd/codex-node36/tmp/rag_20260708_1245_extra_subpro_identity_check/scope_include_maofield_active_md.txt \
  --index-dir /home/amd/codex-node36/tmp/rag_20260708_1245_extra_subpro_identity_check/candidate_index \
  --endpoint http://192.168.31.22:18080 \
  --model bge-m3-temp \
  --batch-size 32 \
  --target 450 \
  --overlap 60
```

Build stats:

```text
files=746
chunks=13557
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding seconds=179.6
embedding rate=75.470 text/s
dimension=1024
```

The active-md scope used the previous report40 scope as baseline and appended
the new D708 extra SubPro package/status/prompt records to avoid unrelated scan
churn.

## Candidate Verification

`candidate_verify_20260708_1245_extra_subpro_identity_check.txt` reports:

```text
faiss_ntotal=13557
faiss_dim=1024
meta_count=13557
ntotal_equals_meta=True
projects/MaoField/STATE.md=True
projects/MaoField/MD_CATALOG.md=True
docs/infra/MAOFIELD_PRO_D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_PACKAGE_20260708.md=True
docs/infra/MAOFIELD_PRO_D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_NODE19_DELIVERY_20260708.md=True
docs/infra/recovery/D708_EXTRA_SUBPRO_AE_IDENTITY_CLAIM_GATE_AGENT_REPORT_20260708.md=True
docs/infra/gpt_deep_research/GPT55_PRO_D708_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_PROMPT_20260708.md=True
docs/infra/gpt_deep_research/GPT55_PRO_D708_SUBPRO_E_REDTEAM_IDENTITY_CHECK_PROMPT_20260708.md=True
docs/infra/recovery/D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_TASKBOOK_20260708.md=True
docs/infra/recovery/D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_PACKAGE_README_20260708.md=True
docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md=True
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md=True
D708_EXTRA_SUBPRO_AE_IDENTITY_CHECK_PACKAGE_DELIVERED=True
finite metric-object identity audit analogue=True
PASS_FINITE_MATH_WITH_NOTES=True
PASS_REDTEAM_WITH_CLAIM_GUARDS=True
insufficient_artifact=True
proof by RAG=True
public-ready / paper-ready / submission-ready / NMI-ready=True
```

## Promoted Index

```text
05922e578c7f316e8d635f1d1f4bb5247d6a1dc7c14ec554b40b1c41483720d4  /media/amd/raid1/rag/index/kb.faiss
3156bae4f1fcd71766b6f7b13483d50a17c006767bd03e5ba22c6e586162f471  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata count:

```text
13557 /media/amd/raid1/rag/index/kb_meta.jsonl
```

## Node22 Stop Status

The initial stop command terminated the port-18080 process but returned ssh
code 255 because `pkill` matched the remote shell. The follow-up status is the
authoritative check:

```text
2026-07-08 12:53:23 CST
not running port=18080
```

Only a separate non-RAG node22 service on port 3000 remained; the temporary
embedding worker for this refresh was stopped.

## Smoke Queries

Smoke outputs:

```text
rag_smoke_20260708_1245_extra_subpro_identity_check_package.txt
rag_smoke_20260708_1245_extra_subpro_identity_check_identity_agent.txt
rag_smoke_20260708_1245_extra_subpro_identity_check_prompts.txt
```

The smokes locate:

- extra SubPro A/E package and node19 delivery records;
- the agent/RAG claim-gate record;
- SubPro A and SubPro E prompts;
- the finite metric-object identity analogue boundary;
- required verdict strings for both extra Pro sessions.

## Sidecars

- `scope_include_maofield_active_md_20260708_1245_extra_subpro_identity_check.txt`
- `scope_sha256_20260708_1245_extra_subpro_identity_check.txt`
- `rag_build_node22_candidate_20260708_1245_extra_subpro_identity_check.txt`
- `candidate_index_sha256_20260708_1245_extra_subpro_identity_check.txt`
- `candidate_verify_20260708_1245_extra_subpro_identity_check.txt`
- `backup_index_sha256_20260708_1245_extra_subpro_identity_check.txt`
- `promoted_index_sha256_20260708_1245_extra_subpro_identity_check.txt`
- `promoted_meta_count_20260708_1245_extra_subpro_identity_check.txt`
- `node22_status_before_20260708_1245_extra_subpro_identity_check.txt`
- `node22_start_20260708_1245_extra_subpro_identity_check.txt`
- `node22_ready_20260708_1245_extra_subpro_identity_check.txt`
- `node22_stop_20260708_1245_extra_subpro_identity_check.txt`
- `node22_status_after_stop_20260708_1245_extra_subpro_identity_check.txt`
- `rag_smoke_20260708_1245_extra_subpro_identity_check_package.txt`
- `rag_smoke_20260708_1245_extra_subpro_identity_check_identity_agent.txt`
- `rag_smoke_20260708_1245_extra_subpro_identity_check_prompts.txt`

RAG remains a locator, not proof authority.
