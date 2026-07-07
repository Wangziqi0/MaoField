# Node22 Vector Refresh - D707 Report38 Internal V0

- Date verified: 2026-07-07 21:12 CST
- Node36 authority: `/media/amd/raid1/canonical/projects/MaoField`
- Scratch root: `/home/amd/codex-node36/tmp/rag_20260707_2101_report38_internal_v0`
- Sidecar tag: `20260707_2101_report38_internal_v0`
- Status: `PROMOTED_AND_NODE22_STOPPED_REPORT38_INTERNAL_V0`

## Scope

This refresh indexes the report38 internal-v0 decision and the node36 internal
v0 local draft.

Newly indexed anchors include:

- `docs/infra/gpt_deep_research/deep_research_d707_bounded_formal_note_v0_draft_report38_20260707.md`
- `docs/infra/gpt_deep_research/D707_BOUNDED_FORMAL_NOTE_V0_DRAFT_REPORT38_ADOPTION_NOTE_20260707.md`
- `docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md`
- `docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md`
- `STATE.md`
- `MD_CATALOG.md`

## Build Summary

- Repository scan: `scanned_files=9082`
- Active markdown scope: 614 files
- FAISS vectors / metadata rows: 10683
- Embedding dimension: 1024
- Embedding worker: node22 one-shot BGE-M3 compatible service
- Node22 endpoint used during build: `http://192.168.31.22:18080`
- Batch size: 32
- Chunk target / overlap: 450 / 60
- Embedding runtime: 129.2 seconds
- Embedding rate: 82.706 text/s

Promoted canonical index hashes:

```text
acb66ecb2150ef97974e892fbf5b8c5911f0a59774f94a1bb5736e308521657d  /media/amd/raid1/rag/index/kb.faiss
76637bc2046a3c3ddef24ffde38bd56a7e9291eb08d4a6fb1200ef7d7f6cfa57  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata rows:

```text
10683
```

Previous canonical index backup suffix:

```text
bak_pre_node22_20260707_2101_report38_internal_v0
```

Previous canonical index hashes:

```text
5da394076712a68e3e9edaba5e0df7d4cfdf3a2131e608747b69c637af5e6f99  /media/amd/raid1/rag/index/kb.faiss.bak_pre_node22_20260707_2101_report38_internal_v0
62261fb52bc7057264fcc8d5ecd62191813633e000f429dd49a681c11669f977  /media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_node22_20260707_2101_report38_internal_v0
```

## Candidate Verification

Candidate verification:

```text
faiss_ntotal=10683
faiss_dim=1024
meta_count=10683
ntotal_equals_meta=True
STATE.md=True
MD_CATALOG.md=True
docs/infra/gpt_deep_research/deep_research_d707_bounded_formal_note_v0_draft_report38_20260707.md=True
docs/infra/gpt_deep_research/D707_BOUNDED_FORMAL_NOTE_V0_DRAFT_REPORT38_ADOPTION_NOTE_20260707.md=True
docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md=True
docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md=True
docs/infra/gpt_deep_research/deep_research_d707_split_loop_bounded_formal_note_review_report37_20260707.md=True
docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_REVISION_TASKBOOK_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/MAIN_PRO_HANDOFF_PACKET_20260707.md=True
DRAFT_INTERNAL_V0_NOW=True
ACCEPT_REPORT38_DRAFT_INTERNAL_V0_NOW_AND_IMPLEMENT_INTERNAL_V0_NOTE=True
REVISE_BEFORE_FORMAL_NOTE=True
FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md=True
Delta_{gamma,n}=True
image-control=True
invariance=True
insufficient_artifact=True
MEDIUM=True
NMI-ready=True
proof-by-JSON=True
```

## Smoke Search Verdict

Verdict: `PASS_LOCATOR`.

Smoke observations:

- Report38 query locates `STATE.md`, `MD_CATALOG.md`, the report38 adoption note,
  report37, the internal v0 note, the taskbook, and local verification.
- Formal-note query locates the Loop4 cycle source files and the internal v0
  note, including the `Delta_{gamma,n}` and restricted-norm caveat context.
- Route query locates report38 at rank 1, the adoption note at rank 2, the
  report38 conclusion at rank 3, and the Session4 open blockers.

## Node22 Shutdown

Node22 temporary embedding worker was stopped after promotion.

Final stop output:

```text
stopped pid=3604891
```

Final port check:

```text
not running port=18080
```

## Sidecars

Promoted sidecars under `docs/infra/rag_rebuild_20260622/`:

- `backup_index_sha256_20260707_2101_report38_internal_v0.txt`
- `candidate_index_sha256_20260707_2101_report38_internal_v0.txt`
- `candidate_verify_20260707_2101_report38_internal_v0.txt`
- `node22_models_20260707_2101_report38_internal_v0.json`
- `node22_ready_20260707_2101_report38_internal_v0.txt`
- `node22_start_20260707_2101_report38_internal_v0.txt`
- `node22_status_after_stop_20260707_2101_report38_internal_v0.txt`
- `node22_status_before_20260707_2101_report38_internal_v0.txt`
- `node22_stop_20260707_2101_report38_internal_v0.txt`
- `promoted_index_sha256_20260707_2101_report38_internal_v0.txt`
- `promoted_meta_count_20260707_2101_report38_internal_v0.txt`
- `rag_build_node22_candidate_20260707_2101_report38_internal_v0.txt`
- `rag_scan_20260707_2101_report38_internal_v0.txt`
- `rag_smoke_20260707_2101_report38_internal_v0_formal_note.txt`
- `rag_smoke_20260707_2101_report38_internal_v0_report38.txt`
- `rag_smoke_20260707_2101_report38_internal_v0_route.txt`
- `scope_include_maofield_active_md_20260707_2101_report38_internal_v0.txt`
- `scope_include_maofield_all_nonarchive_md_20260707_2101_report38_internal_v0.txt`

## Claim Boundary

This RAG refresh is only for locating report38, the internal v0 local draft, and
their supporting chain. It is not proof, not peer review, not public readiness,
and not empirical evidence.

Still forbidden:

- MaoField empirical-positive claim
- proof-by-JSON / proof-by-harness / proof-by-artifact
- observed residual / interaction / transport / holonomy / gluing / collapse field
- dynamic-collapse theory
- black-box mechanism solved
- broad ANOVA / dependent-input / sheaf / contextuality / projection theory
- NMI-ready or submission-ready
- public/paper-ready promotion from report38 or the internal v0 note

Mode B remains:

```text
insufficient_artifact
```

Duplicate risk remains:

```text
MEDIUM
```

