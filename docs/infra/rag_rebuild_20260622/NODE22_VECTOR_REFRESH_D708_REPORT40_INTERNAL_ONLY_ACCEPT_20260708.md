# Node22 Vector Refresh - D708 Report40 Internal-Only Accept

## Scope

This refresh indexes the D708 repair-recheck result after Main Pro returned:

```text
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY
KEEP_INTERNAL_ONLY
```

Newly indexed anchors include:

- `docs/infra/gpt_deep_research/deep_research_d708_internal_v0_gate_repair_accept_report40_20260708.md`
- `docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REPAIR_ACCEPT_REPORT40_ADOPTION_NOTE_20260708.md`
- existing report39 repair package records and prompts;
- D707 internal v0 note and SubPro A/E review prompts.

This refresh does not promote the D707 internal v0 note into a public paper,
NMI-ready result, broad theory, empirical result, or proof-by-package claim.

## Build

- Date verified: `2026-07-08 12:27:00 CST`
- Host: node36 as pipeline authority
- Vector worker: node22 one-shot BGE-M3 compatible llama.cpp service on port
  `18080`
- Sidecar tag: `20260708_1218_report40_internal_only_accept`
- Node36 scratch root:
  `/home/amd/codex-node36/tmp/rag_20260708_1218_report40_internal_only_accept`
- Candidate index:
  `/home/amd/codex-node36/tmp/rag_20260708_1218_report40_internal_only_accept/candidate_index`
- Remote node22 worker root:
  `/home/amd/codex-node22/tmp/maofield-rag-vector-20260708_1218_report40_internal_only_accept`

Build command class:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python scripts/rag_build_index_node22_http.py \
  --file-list /home/amd/codex-node36/tmp/rag_20260708_1218_report40_internal_only_accept/scope_include_maofield_active_md.txt \
  --index-dir /home/amd/codex-node36/tmp/rag_20260708_1218_report40_internal_only_accept/candidate_index \
  --endpoint http://192.168.31.22:18080 \
  --model bge-m3-temp \
  --batch-size 32 \
  --target 450 \
  --overlap 60
```

Build stats:

```text
files=736
chunks=13496
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding seconds=179.0
embedding rate=75.386 text/s
dimension=1024
```

## Node22 Notes

The first service attempt selected the node22 integrated GPU (`gfx1036`) and the
build failed with a ROCm TensileLibrary error. The final service was restarted
with:

```text
HIP_VISIBLE_DEVICES=0
ROCR_VISIBLE_DEVICES=0
HSA_OVERRIDE_GFX_VERSION=12.0.1
--batch-size 4096
--ubatch-size 4096
```

The temporary worker was stopped after promotion.

## Candidate Verification

`candidate_verify_20260708_1218_report40_internal_only_accept.txt` reports:

```text
faiss_ntotal=13496
faiss_dim=1024
meta_count=13496
ntotal_equals_meta=True
projects/MaoField/STATE.md=True
projects/MaoField/MD_CATALOG.md=True
docs/infra/gpt_deep_research/deep_research_d708_internal_v0_gate_repair_accept_report40_20260708.md=True
docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REPAIR_ACCEPT_REPORT40_ADOPTION_NOTE_20260708.md=True
docs/infra/gpt_deep_research/deep_research_d708_internal_v0_gate_request_files_report39_20260708.md=True
docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REQUEST_FILES_REPORT39_ADOPTION_NOTE_20260708.md=True
docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_A_FINITE_MATH_PROMPT_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_E_REDTEAM_PROMPT_20260707.md=True
docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_GATE_REPAIR_PACKAGE_20260708.md=True
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY=True
KEEP_INTERNAL_ONLY=True
ACCEPT_REPORT40_KEEP_INTERNAL_ONLY=True
Report39 package/provenance blocker=True
internal v0 local note=True
prior-art/triviality risk=True
MEDIUM=True
insufficient_artifact=True
proof by RAG=True
public-ready / paper-ready / submission-ready / NMI-ready=True
```

## Promoted Index

```text
8c3283fcde357594cbed5ea08cb7b4c0854cd1d256de15d352c73d3fe93c6153  /media/amd/raid1/rag/index/kb.faiss
0eef18d09fcae982466a15c520db2ae320b6067ab94195199e63aed73de15358  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata count:

```text
13496 /media/amd/raid1/rag/index/kb_meta.jsonl
```

## Sidecars

- `rag_scan_20260708_1218_report40_internal_only_accept.txt`
- `scope_select_20260708_1218_report40_internal_only_accept.txt`
- `scope_count_20260708_1218_report40_internal_only_accept.txt`
- `scope_include_maofield_active_md_20260708_1218_report40_internal_only_accept.txt`
- `rag_build_node22_candidate_20260708_1218_report40_internal_only_accept.txt`
- `candidate_index_sha256_20260708_1218_report40_internal_only_accept.txt`
- `candidate_verify_20260708_1218_report40_internal_only_accept.txt`
- `backup_index_sha256_20260708_1218_report40_internal_only_accept.txt`
- `promoted_index_sha256_20260708_1218_report40_internal_only_accept.txt`
- `promoted_meta_count_20260708_1218_report40_internal_only_accept.txt`
- `node22_status_before_20260708_1218_report40_internal_only_accept.txt`
- `node22_start_20260708_1218_report40_internal_only_accept.txt`
- `node22_ready_20260708_1218_report40_internal_only_accept.txt`
- `node22_stop_20260708_1218_report40_internal_only_accept.txt`
- `node22_status_after_stop_20260708_1218_report40_internal_only_accept.txt`
- `rag_smoke_20260708_1218_report40_internal_only_accept_report40.txt`
- `rag_smoke_20260708_1218_report40_internal_only_accept_adoption.txt`
- `rag_smoke_20260708_1218_report40_internal_only_accept_subpro.txt`

## Smoke Queries

The promoted index was queried with:

```text
Report40 ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY KEEP_INTERNAL_ONLY
ACCEPT_REPORT40_KEEP_INTERNAL_ONLY prior-art triviality MEDIUM internal v0 local note
SubPro A finite math SubPro E redteam prompts D707 internal v0
```

The smoke results locate report40, the adoption note, the internal v0 note, the
report39 repair package context, and the SubPro A/E prompt locations.

## Boundary

RAG is a locator only. Evidence remains in primary repository files, reports,
adoption notes, scripts, exact certificates, JSON, package records, and explicit
Pro verdicts.

The current accepted state is internal-only:

```text
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY
KEEP_INTERNAL_ONLY
```

Forbidden upgrades remain: public-ready, paper-ready, submission-ready,
NMI-ready, MaoField empirical positive, observed residual/transport/holonomy/
gluing/collapse field, dynamic-collapse theory, broad ANOVA/dependent-input/
projection/sheaf/contextuality/path-closure theory, black-box mechanism solved,
or proof by JSON/harness/package/RAG/prompt/manifest/model output.
