# Node22 Vector Refresh - D708 SubPro E Repair Recheck

## Status

- Date verified on node36: `2026-07-08 13:41 CST`
- Scope owner: node36
- GPU/vector worker: node22, one-shot temporary embedding service
- Sidecar tag: `20260708_1340_subpro_e_repair`
- Current purpose: sync RAG after SubPro A Report41, SubPro E Report42, and the SubPro E repair/recheck package.
- Claim boundary: RAG is locator support only. It does not prove theorems, paper readiness, MaoField empirical claims, observed fields, broad theory, or publication suitability.

## Scope

- Scope file:
  `docs/infra/rag_rebuild_20260622/scope_include_maofield_active_md_20260708_1340_subpro_e_repair.txt`
- Active markdown files in scope: `757`

Included new anchors:

- `docs/infra/gpt_deep_research/deep_research_d708_subpro_a_finite_math_identity_check_report41_20260708.md`
- `docs/infra/gpt_deep_research/D708_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_REPORT41_ADOPTION_NOTE_20260708.md`
- `docs/infra/gpt_deep_research/deep_research_d708_subpro_e_redteam_identity_check_blocked_report42_20260708.md`
- `docs/infra/gpt_deep_research/D708_SUBPRO_E_REDTEAM_IDENTITY_CHECK_REPORT42_ADOPTION_NOTE_20260708.md`
- `docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md`
- `docs/infra/recovery/D708_SUBPRO_E_REPAIR_RECHECK_TASKBOOK_20260708.md`
- `docs/infra/recovery/D708_SUBPRO_E_REPAIR_RECHECK_PACKAGE_README_20260708.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_D708_SUBPRO_E_REPAIR_RECHECK_PROMPT_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_SUBPRO_E_REPAIR_RECHECK_PACKAGE_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_SUBPRO_E_REPAIR_RECHECK_NODE19_DELIVERY_20260708.md`

## Build

Node22 worker:

- endpoint: `http://192.168.31.22:18080`
- model label: `bge-m3-temp`
- worker status after stop:
  `docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260708_1340_subpro_e_repair.txt`

Build output:

```text
files=757
chunks=13652
dim=1024
embed_seconds=181.0
rate=75.444 text/s
faiss=/home/amd/codex-node36/tmp/rag_20260708_1340_subpro_e_repair/candidate_index/kb.faiss
meta=/home/amd/codex-node36/tmp/rag_20260708_1340_subpro_e_repair/candidate_index/kb_meta.jsonl
```

Candidate verification:

```text
faiss_ntotal=13652
faiss_dim=1024
meta_count=13652
ntotal_equals_meta=True
```

## Promoted Index

Promoted canonical RAG index:

```text
995c5a8db129d69e365af8047d04c24103113579bc2473aa08d47d4d1a855f65  /media/amd/raid1/rag/index/kb.faiss
ea8ce9530e985694b122ad74688536a3d4a76f43179e38b2bb0320814eb8a57a  /media/amd/raid1/rag/index/kb_meta.jsonl
13652 /media/amd/raid1/rag/index/kb_meta.jsonl
```

Sidecar hash records:

- `docs/infra/rag_rebuild_20260622/candidate_index_sha256_20260708_1340_subpro_e_repair.txt`
- `docs/infra/rag_rebuild_20260622/promoted_index_sha256_20260708_1340_subpro_e_repair.txt`
- `docs/infra/rag_rebuild_20260622/promoted_meta_count_20260708_1340_subpro_e_repair.txt`
- `docs/infra/rag_rebuild_20260622/backup_index_sha256_20260708_1340_subpro_e_repair.txt`

## Verification

Verification file:

```text
docs/infra/rag_rebuild_20260622/candidate_verify_20260708_1340_subpro_e_repair.txt
```

Required anchors were found in promoted metadata:

```text
projects/MaoField/STATE.md=True
projects/MaoField/MD_CATALOG.md=True
docs/infra/gpt_deep_research/deep_research_d708_subpro_a_finite_math_identity_check_report41_20260708.md=True
docs/infra/gpt_deep_research/D708_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_REPORT41_ADOPTION_NOTE_20260708.md=True
docs/infra/gpt_deep_research/deep_research_d708_subpro_e_redteam_identity_check_blocked_report42_20260708.md=True
docs/infra/gpt_deep_research/D708_SUBPRO_E_REDTEAM_IDENTITY_CHECK_REPORT42_ADOPTION_NOTE_20260708.md=True
docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md=True
docs/infra/MAOFIELD_PRO_D708_SUBPRO_E_REPAIR_RECHECK_PACKAGE_20260708.md=True
docs/infra/MAOFIELD_PRO_D708_SUBPRO_E_REPAIR_RECHECK_NODE19_DELIVERY_20260708.md=True
docs/infra/gpt_deep_research/GPT55_PRO_D708_SUBPRO_E_REPAIR_RECHECK_PROMPT_20260708.md=True
PASS_FINITE_MATH_WITH_NOTES=True
BLOCKED_MISSING_ARTIFACTS=True
WAIT_FOR_SUBPRO_E_REPAIR_RECHECK=True
MaoField_PRO_D708_SubProE_RepairRecheck_20260708_1340.zip=True
HIGH=True
insufficient_artifact=True
```

Smoke query outputs:

- `docs/infra/rag_rebuild_20260622/rag_smoke_20260708_1340_subpro_e_repair_reports.txt`
- `docs/infra/rag_rebuild_20260622/rag_smoke_20260708_1340_subpro_e_repair_repair.txt`

## Result

RAG now locates the SubPro A pass, SubPro E missing-artifact blocker, the repaired package that includes the missing D707 loop-goals file, and the current `WAIT_FOR_SUBPRO_E_REPAIR_RECHECK` status.

This refresh does not change the project claim boundary:

- SubPro A: `PASS_FINITE_MATH_WITH_NOTES`
- SubPro E: `BLOCKED_MISSING_ARTIFACTS`
- Current node36 action: `WAIT_FOR_SUBPRO_E_REPAIR_RECHECK`
- Still forbidden: public-ready, paper-ready, NMI-ready, MaoField empirical-positive, observed field, broad black-box or identity theory, and proof-by-RAG/JSON/harness/package/prompt/model-output.
