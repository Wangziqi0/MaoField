# Node22 Vector Refresh - D707 Split-Loop Outputs

- Date verified: 2026-07-07 15:50 CST
- Node36 authority: `/media/amd/raid1/canonical/projects/MaoField`
- Scratch root: `/home/amd/codex-node36/tmp/rag_20260707_1550_split_loop_outputs`
- Sidecar tag: `20260707_1550_split_loop_outputs`
- Status: `PROMOTED_AND_NODE22_STOPPED_SPLIT_LOOP_OUTPUTS_READY_FOR_PRO`

## Scope

This refresh indexes the D707 split-loop outputs as internal Main Pro / Sub Pro A / Sub Pro E review input.

It does not promote the split-loop drafts into accepted mathematics, empirical evidence, NMI-ready material, or public-submission claims.

Primary new / updated project anchors:

- `STATE.md`
- `MD_CATALOG.md`
- `docs/infra/recovery/D707_SPLIT_LOOP_OUTPUTS_ADOPTION_NOTE_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/SESSION4_STATUS_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/MAIN_PRO_HANDOFF_PACKET_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_A_FINITE_MATH_PROMPT_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_E_REDTEAM_PROMPT_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/COMPOSITION_LEMMA_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/TELESCOPING_PROOF_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md`

## Build Summary

- Active markdown scope: 600 files
- FAISS vectors / metadata rows: 10541
- Embedding dimension: 1024
- Embedding worker: node22 one-shot BGE-M3 compatible service
- Node22 endpoint used during build: `http://192.168.31.22:18080`
- Batch size: 32
- Chunk target / overlap: 450 / 60
- Embedding runtime: 127.7 seconds
- Embedding rate: 82.553 text/s

Build command class:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python scripts/rag_build_index_node22_http.py \
  --file-list /home/amd/codex-node36/tmp/rag_20260707_1550_split_loop_outputs/scope_include_maofield_active_md.txt \
  --index-dir /home/amd/codex-node36/tmp/rag_20260707_1550_split_loop_outputs/candidate_index \
  --endpoint http://192.168.31.22:18080 \
  --model bge-m3-temp \
  --batch-size 32 \
  --target 450 \
  --overlap 60
```

## Promotion

Previous canonical index backup suffix:

- `bak_pre_node22_20260707_1550_split_loop_outputs`

Promoted canonical index hashes:

```text
f69644e6e747473073c75d0390b801d097371351e120ee5c5061c0f22f6ed752  /media/amd/raid1/rag/index/kb.faiss
2bf27a25f377506fddd8bb0a2ca9fe3d1e46e75eb797a734eac54ca4cd1f7fa4  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata rows:

```text
10541
```

## Candidate Verification

Candidate verification result:

```text
faiss_ntotal=10541
faiss_dim=1024
meta_count=10541
ntotal_equals_meta=True
```

Required path presence:

```text
STATE.md=True
MD_CATALOG.md=True
docs/infra/recovery/D707_SPLIT_LOOP_OUTPUTS_ADOPTION_NOTE_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SESSION4_STATUS_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/MAIN_PRO_HANDOFF_PACKET_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_A_FINITE_MATH_PROMPT_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_E_REDTEAM_PROMPT_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop3/COMPOSITION_LEMMA_LOOP3_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop4/TELESCOPING_PROOF_LOOP4_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md=True
```

Required phrase presence:

```text
D707_SPLIT_LOOP_OUTPUTS_READY_FOR_MANUAL_MAIN_PRO_SUBPRO_A_E_REVIEW_AND_RAG_SYNCED=True
ADOPT_AS_INTERNAL_PRO_REVIEW_HANDOFF_INPUT_ONLY=True
FINITE_PATH_CYCLE_DEFECT_PACKAGE_READY_FOR_PRO_REVIEW=True
READY_FOR_LOOP3=True
READY_FOR_LOOP4=True
READY_FOR_PRO_REVIEW_HANDOFF=True
READY_FOR_MAIN_PRO_AND_SUBPRO_A_E_REVIEW=True
SUBPRO_A_FINITE_MATH_PROMPT_20260707.md=True
SUBPRO_E_REDTEAM_PROMPT_20260707.md=True
Delta_{beta circ alpha} = T_beta Delta_alpha + Delta_beta U_alpha=True
Delta_{gamma,n}=True
proof-by-JSON=True
NMI-ready=True
dynamic-collapse theory=True
observed transport=True
local proof drafts for Pro review=True
```

## Smoke Search Verdict

Verdict: `PASS_LOCATOR_WITH_NOTE`.

Observed smoke behavior:

- Direct status/adoption queries locate `STATE.md`, `MD_CATALOG.md`, the adoption note, `REVIEW_ARTIFACT_INDEX_20260707.md`, and `SESSION4_STATUS_20260707.md`.
- Math queries locate `COMPOSITION_LEMMA_LOOP3_20260707.md` and `TELESCOPING_PROOF_LOOP4_20260707.md`.
- Sub Pro E semantic queries locate `SUBPRO_E_REDTEAM_PROMPT_20260707.md` directly.
- Sub Pro A semantic queries more often locate earlier Sub Pro A prompt context and finite-math proof artifacts; candidate verification confirms the exact Sub Pro A prompt file is indexed, and `STATE.md`, the adoption note, and `REVIEW_ARTIFACT_INDEX_20260707.md` all point to it.
- Forbidden-boundary queries locate blocked-context files such as `CLAIM_DIFF_AFTER_LOOPS_20260707.md`, `FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md`, and `MAIN_PRO_HANDOFF_PACKET_20260707.md`.

## Sidecars

Promoted sidecars under `docs/infra/rag_rebuild_20260622/`:

- `backup_index_sha256_20260707_1550_split_loop_outputs.txt`
- `candidate_index_sha256_20260707_1550_split_loop_outputs.txt`
- `candidate_meta_count_20260707_1550_split_loop_outputs.txt`
- `candidate_verify_20260707_1550_split_loop_outputs.txt`
- `node22_models_20260707_1550_split_loop_outputs.json`
- `node22_port_verify_20260707_1550_split_loop_outputs.txt`
- `node22_ready_20260707_1550_split_loop_outputs.txt`
- `node22_start_20260707_1550_split_loop_outputs.txt`
- `node22_status_after_stop_20260707_1550_split_loop_outputs.txt`
- `node22_status_before_20260707_1550_split_loop_outputs.txt`
- `node22_stop_20260707_1550_split_loop_outputs.txt`
- `promoted_index_sha256_20260707_1550_split_loop_outputs.txt`
- `promoted_meta_count_20260707_1550_split_loop_outputs.txt`
- `rag_build_node22_candidate_20260707_1550_split_loop_outputs.txt`
- `rag_scan_20260707_1550_split_loop_outputs.txt`
- `rag_smoke_20260707_1550_split_loop_outputs.txt`
- `rag_smoke_final_20260707_1550_split_loop_outputs.txt`
- `rag_smoke_hits_20260707_1550_split_loop_outputs.txt`
- `required_scope_20260707_1550_split_loop_outputs.txt`
- `scope_counts_20260707_1550_split_loop_outputs.txt`
- `scope_include_maofield_active_md_20260707_1550_split_loop_outputs.txt`
- `scope_sha256_20260707_1550_split_loop_outputs.txt`
- `smoke_queries_20260707_1550_split_loop_outputs.txt`

## Node22 Shutdown

Node22 temporary embedding worker was stopped after candidate promotion.

Final port check:

```text
not running port=18080
```

## Claim Boundary

This RAG refresh is only an index and locator update. It must not be cited as proof or empirical evidence.

Still forbidden:

- MaoField empirical-positive claim
- proof-by-JSON / proof-by-harness / proof-by-artifact
- observed residual / interaction / transport / holonomy / gluing / collapse field
- dynamic-collapse theory
- black-box mechanism solved
- broad ANOVA / dependent-input / sheaf / contextuality / projection theory
- NMI-ready or submission-ready
- revived first-DM / first-reflexive-AI / paradigm-shift / C1-C4 positive claims
