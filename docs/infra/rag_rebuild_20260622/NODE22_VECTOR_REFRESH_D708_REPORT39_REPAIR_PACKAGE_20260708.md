# Node22 Vector Refresh - D708 Report39 Repair Package

## Scope

This refresh indexes the D708 report39 repair/recheck package after Main Pro
returned `REQUEST_NODE36_FILES`.

Newly indexed anchors include:

- `docs/infra/gpt_deep_research/deep_research_d708_internal_v0_gate_request_files_report39_20260708.md`
- `docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REQUEST_FILES_REPORT39_ADOPTION_NOTE_20260708.md`
- `docs/infra/recovery/D708_INTERNAL_V0_GATE_REPAIR_PACKAGE_TASKBOOK_20260708.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_D708_INTERNAL_V0_GATE_REPAIR_RECHECK_PROMPT_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_GATE_REPAIR_PACKAGE_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_GATE_REPAIR_NODE19_DELIVERY_20260708.md`
- `docs/infra/package_outputs/d708_internal_v0_gate_repair_20260708_1130/`
- missing-file blockers requested by report39:
  - `docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md`
  - `docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md`
  - `docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md`

This is an internal package/provenance repair sync only. It does not promote the
D707 internal v0 formal note into a public paper, NMI-ready result, broad theory,
MaoField empirical positive result, or proof-by-package claim.

## Build

- Date verified: `2026-07-08 11:51:17 CST`
- Host: node36 as pipeline authority
- Vector worker: node22 one-shot BGE-M3 service on port `18080`
- Sidecar tag: `20260708_1146_d708_report39_repair_package`
- Node36 scratch root:
  `/home/amd/codex-node36/tmp/rag_20260708_1146_d708_report39_repair_package`
- Candidate index:
  `/home/amd/codex-node36/tmp/rag_20260708_1146_d708_report39_repair_package/candidate_index`
- Remote node22 worker root:
  `/home/amd/codex-node22/tmp/maofield-rag-vector-20260708_1146_d708_report39_repair_package`

Build sidecars:

- `rag_scan_20260708_1146_d708_report39_repair_package.txt`
- `rag_build_node22_candidate_20260708_1146_d708_report39_repair_package.txt`
- `candidate_verify_20260708_1146_d708_report39_repair_package.txt`
- `candidate_index_sha256_20260708_1146_d708_report39_repair_package.txt`
- `promoted_index_sha256_20260708_1146_d708_report39_repair_package.txt`
- `promoted_meta_count_20260708_1146_d708_report39_repair_package.txt`
- `node22_status_before_20260708_1146_d708_report39_repair_package.txt`
- `node22_start_20260708_1146_d708_report39_repair_package.txt`
- `node22_ready_20260708_1146_d708_report39_repair_package.txt`
- `node22_stop_20260708_1146_d708_report39_repair_package.txt`
- `node22_status_after_stop_20260708_1146_d708_report39_repair_package.txt`
- `rag_smoke_20260708_1146_d708_report39_repair_package_report39.txt`
- `rag_smoke_20260708_1146_d708_report39_repair_package_delivery.txt`
- `rag_smoke_20260708_1146_d708_report39_repair_package_prompt.txt`

## Candidate Verification

`candidate_verify_20260708_1146_d708_report39_repair_package.txt` reports:

```text
faiss_ntotal=10829
faiss_dim=1024
meta_count=10829
ntotal_equals_meta=True
STATE.md=True
MD_CATALOG.md=True
docs/infra/gpt_deep_research/deep_research_d708_internal_v0_gate_request_files_report39_20260708.md=True
docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REQUEST_FILES_REPORT39_ADOPTION_NOTE_20260708.md=True
docs/infra/recovery/D708_INTERNAL_V0_GATE_REPAIR_PACKAGE_TASKBOOK_20260708.md=True
docs/infra/gpt_deep_research/GPT55_PRO_D708_INTERNAL_V0_GATE_REPAIR_RECHECK_PROMPT_20260708.md=True
docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_GATE_REPAIR_PACKAGE_20260708.md=True
docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_GATE_REPAIR_NODE19_DELIVERY_20260708.md=True
docs/infra/package_outputs/d708_internal_v0_gate_repair_20260708_1130/START_HERE_D708_REPAIR_RECHECK_PROMPT_20260708_1130.md=True
docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md=True
D708_REPORT39_REPAIR_PACKAGE_TO_19_READY_RAG_REFRESH_PENDING=True
REQUEST_NODE36_FILES=True
b3206ecf59b636d2eb17ba3a510ea1b348fa518a60668d714d87c455d1729b52=True
7b29b8eef5770ca05a7a83e47542cbd72349cd218db4c3db26f8db3d5253ac78=True
MaoField_PRO_D708_InternalV0GateRepair_20260708_1130.zip=True
START_HERE_D708_REPAIR_RECHECK_PROMPT_20260708_1130.md=True
d3993191822d430b25832d7c9c82ee9b0bff182efa004bbca18ba873d5abc038=True
d73d2a317ae96572fcd622dcd9e7e58d519238997dbb2877b3e4063ea50bda43=True
07a623ffb333e639b8a0ce6a8aa45632ac759daea0234633cd2afab329dd15bb=True
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY=True
PATCH_INTERNAL_V0_THEN_RECHECK=True
REJECT_OR_STOP_PARK=True
Delta_{gamma,n}=True
insufficient_artifact=True
proof-by-package=True
```

## Promoted Index

```text
d94d5fc9128cef203e492a17a79008b5c30cf6a9a7bec835c288e1ee08445749  /media/amd/raid1/rag/index/kb.faiss
1bba933f98b49908596fd8647d389a26d7829e38aa6b5bfaba333b12a89ba53d  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata count:

```text
10829 /media/amd/raid1/rag/index/kb_meta.jsonl
```

## Node22 Stop Status

`node22_stop_20260708_1146_d708_report39_repair_package.txt` reports:

```text
stopped pid=3630566
```

`node22_status_after_stop_20260708_1146_d708_report39_repair_package.txt`
reports the temporary port is not running:

```text
not running port=18080 log=/home/amd/codex-node22/tmp/maofield-rag-vector-20260708_1146_d708_report39_repair_package/bge-m3-llama-18080.log
```

## Smoke Queries

The promoted index was queried with:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "Report39 REQUEST_NODE36_FILES D708 repair package loop status" --top-k 8 --project MaoField
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "MaoField_PRO_D708_InternalV0GateRepair b3206ecf node19 delivery" --top-k 8 --project MaoField
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "D708 repair recheck prompt proof-by-package Delta gamma n" --top-k 8 --project MaoField
```

Smoke results locate report39, adoption note, repair package record, node19
delivery, repair zip hash, repair prompt, loop status files, and boundary terms.

## Boundary

RAG is a locator only. Evidence still comes from primary repository files,
scripts, exact certificates, JSON, audit notes, package records, and explicit
Pro verdicts.

The current repair gate remains:

```text
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY
PATCH_INTERNAL_V0_THEN_RECHECK
REJECT_OR_STOP_PARK
REQUEST_NODE36_FILES
```

Forbidden upgrades remain: public-ready, paper-ready, NMI-ready, MaoField
empirical positive, observed residual/transport/holonomy/gluing/collapse field,
dynamic-collapse theory, broad ANOVA/dependent-input/projection/sheaf theory,
black-box mechanism solved, or proof by JSON/harness/package.
