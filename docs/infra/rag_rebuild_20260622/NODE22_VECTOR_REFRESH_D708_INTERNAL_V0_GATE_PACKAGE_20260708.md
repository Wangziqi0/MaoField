# Node22 Vector Refresh - D708 Internal V0 Gate Package

## Scope

This refresh indexes the final warning-cleaned D708 internal-v0 promotion-gate
package prepared for manual GPT-5.5 Pro review.

Newly indexed anchors include:

- `docs/infra/recovery/D708_INTERNAL_V0_PROMOTION_GATE_TASKBOOK_20260708.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PROMPT_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_NODE19_DELIVERY_20260708.md`
- `docs/infra/package_outputs/d708_internal_v0_promotion_gate_20260708_1001/`
- D707 split-loop ancillary files:
  - `docs/infra/recovery/d707_split_loop_outputs/loop3/ARTIFACT_MANIFEST_LOOP3_20260707.md`
  - `docs/infra/recovery/d707_split_loop_outputs/loop4/ARTIFACT_MANIFEST_LOOP4_20260707.md`
  - `docs/infra/recovery/d707_split_loop_outputs/session4/CLAIM_DIFF_AFTER_LOOPS_20260707.md`

This is an internal gate-review sync only. It does not promote the D707
internal v0 formal note into a public paper, NMI-ready result, broad theory,
MaoField empirical positive result, or proof-by-artifact claim.

The earlier same-day tag `20260708_1005_d708_internal_v0_gate_package` is
superseded by this final tag after warning cleanup and node19 redelivery.

## Build

- Date verified: `2026-07-08 10:24:43 CST`
- Host: node36 as pipeline authority
- Vector worker: node22 one-shot BGE-M3 service on port `18080`
- Sidecar tag: `20260708_1020_d708_internal_v0_gate_package_final`
- Node36 scratch root:
  `/home/amd/codex-node36/tmp/rag_20260708_1020_d708_internal_v0_gate_package_final`
- Candidate index:
  `/home/amd/codex-node36/tmp/rag_20260708_1020_d708_internal_v0_gate_package_final/candidate_index`
- Remote node22 worker root:
  `/home/amd/codex-node22/tmp/maofield-rag-vector-20260708_1020_d708_internal_v0_gate_package_final`

Build sidecars:

- `rag_scan_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `rag_build_node22_candidate_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `candidate_verify_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `candidate_index_sha256_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `promoted_index_sha256_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `promoted_meta_count_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `node22_status_before_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `node22_start_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `node22_ready_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `node22_stop_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `node22_status_after_stop_20260708_1020_d708_internal_v0_gate_package_final.txt`
- `rag_smoke_20260708_1020_d708_internal_v0_gate_package_final_package.txt`
- `rag_smoke_20260708_1020_d708_internal_v0_gate_package_final_prompt.txt`
- `rag_smoke_20260708_1020_d708_internal_v0_gate_package_final_delivery.txt`

## Candidate Verification

`candidate_verify_20260708_1020_d708_internal_v0_gate_package_final.txt`
reports:

```text
faiss_ntotal=10754
faiss_dim=1024
meta_count=10754
ntotal_equals_meta=True
STATE.md=True
MD_CATALOG.md=True
docs/infra/recovery/D708_INTERNAL_V0_PROMOTION_GATE_TASKBOOK_20260708.md=True
docs/infra/gpt_deep_research/GPT55_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PROMPT_20260708.md=True
docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_20260708.md=True
docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_NODE19_DELIVERY_20260708.md=True
docs/infra/package_outputs/d708_internal_v0_promotion_gate_20260708_1001/START_HERE_MAIN_PROMPT_20260708_1001_internal_v0_gate.md=True
docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md=True
docs/infra/gpt_deep_research/deep_research_d707_bounded_formal_note_v0_draft_report38_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop3/ARTIFACT_MANIFEST_LOOP3_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop4/ARTIFACT_MANIFEST_LOOP4_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/CLAIM_DIFF_AFTER_LOOPS_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_A_FINITE_MATH_PROMPT_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_E_REDTEAM_PROMPT_20260707.md=True
D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_TO_19_READY_RAG_REFRESH_PENDING=True
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY=True
PATCH_INTERNAL_V0_THEN_RECHECK=True
REJECT_OR_STOP_PARK=True
REQUEST_NODE36_FILES=True
MaoField_PRO_D708_InternalV0PromotionGate_20260708_1001.zip=True
START_HERE_MAIN_PROMPT_20260708_1001_internal_v0_gate.md=True
2cf1a9117a1c521fb60be7f99014b62715b033090e17d7973e8fc651cd55965a=True
6b42193d6259465f4aa57402f5acc73980ab49b54bf0bfaac6c2894808c8cd8b=True
Delta_{gamma,n}=True
image-control=True
insufficient_artifact=True
proof-by-artifact=True
```

## Promoted Index

```text
da3c560fadbfb09488de3341d10ef0036e10a618402413fa061870a302e63ad2  /media/amd/raid1/rag/index/kb.faiss
76bd90f674436de9f309940170d75882f84f826661527564537babc15e0e6a40  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata count:

```text
10754 /media/amd/raid1/rag/index/kb_meta.jsonl
```

The previous index was backed up with suffix:

```text
bak_pre_node22_20260708_1020_d708_internal_v0_gate_package_final
```

## Node22 Stop Status

`node22_stop_20260708_1020_d708_internal_v0_gate_package_final.txt` reports:

```text
stopped pid=3627880
```

`node22_status_after_stop_20260708_1020_d708_internal_v0_gate_package_final.txt`
reports the temporary port is not running:

```text
not running port=18080 log=/home/amd/codex-node22/tmp/maofield-rag-vector-20260708_1020_d708_internal_v0_gate_package_final/bge-m3-llama-18080.log
```

## Smoke Queries

The promoted index was queried with:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "D708 internal v0 promotion gate final package 2cf1a911" --top-k 8 --project MaoField
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "D708 Pro prompt SubPro A SubPro E artifact manifest claim diff" --top-k 8 --project MaoField
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "MaoField_PRO_D708_InternalV0PromotionGate node19 delivery 2CF1A911" --top-k 8 --project MaoField
```

Smoke results locate the final D708 package record, prompt, taskbook, node19
delivery record, final zip hash, the D707 SubPro A/E review files, and the
ancillary artifact-manifest / claim-diff files.

## Boundary

RAG is a locator only. Evidence still comes from primary repository files,
scripts, exact certificates, JSON, audit notes, package records, and explicit
Pro verdicts.

The current gate remains:

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
