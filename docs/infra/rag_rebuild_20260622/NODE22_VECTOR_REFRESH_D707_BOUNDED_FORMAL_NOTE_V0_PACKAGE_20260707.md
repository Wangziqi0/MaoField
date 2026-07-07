# Node22 Vector Refresh - D707 Bounded Formal Note V0 Package

- Date verified: 2026-07-07 17:30 CST
- Node36 authority: `/media/amd/raid1/canonical/projects/MaoField`
- Scratch root: `/home/amd/codex-node36/tmp/rag_20260707_1730_bounded_note_v0_package`
- Sidecar tag: `20260707_1730_bounded_note_v0_package`
- Status: `PROMOTED_AND_NODE22_STOPPED_BOUNDED_NOTE_V0_PACKAGE`

## Scope

This refresh indexes the next GPT-5.5 Pro prompt/package for the D707 bounded internal v0 formal-note decision.

Newly indexed anchors include:

- `docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_RAG_STATUS_SYNTHESIS_20260707.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_D707_BOUNDED_FORMAL_NOTE_V0_MAIN_PROMPT_20260707.md`
- `docs/infra/MAOFIELD_PRO_D707_BOUNDED_FORMAL_NOTE_V0_PACKAGE_20260707.md`
- `docs/infra/MAOFIELD_PRO_D707_BOUNDED_FORMAL_NOTE_V0_NODE19_DELIVERY_20260707.md`
- `docs/infra/recovery/D707_SPLIT_LOOP_OUTPUTS_ADOPTION_NOTE_20260707.md`

## Build Summary

- Repository scan: `scanned_files=9055`
- Active markdown scope: 609 files
- FAISS vectors / metadata rows: 10630
- Embedding dimension: 1024
- Embedding worker: node22 one-shot BGE-M3 compatible service
- Node22 endpoint used during build: `http://192.168.31.22:18080`
- Batch size: 32
- Chunk target / overlap: 450 / 60
- Embedding runtime: 129.0 seconds
- Embedding rate: 82.415 text/s

Promoted canonical index hashes:

```text
5da394076712a68e3e9edaba5e0df7d4cfdf3a2131e608747b69c637af5e6f99  /media/amd/raid1/rag/index/kb.faiss
62261fb52bc7057264fcc8d5ecd62191813633e000f429dd49a681c11669f977  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Promoted metadata rows:

```text
10630
```

Previous canonical index backup suffix:

```text
bak_pre_node22_20260707_1730_bounded_note_v0_package
```

## Candidate Verification

Candidate verification:

```text
faiss_ntotal=10630
faiss_dim=1024
meta_count=10630
ntotal_equals_meta=True
STATE.md=True
MD_CATALOG.md=True
docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_RAG_STATUS_SYNTHESIS_20260707.md=True
docs/infra/gpt_deep_research/GPT55_PRO_D707_BOUNDED_FORMAL_NOTE_V0_MAIN_PROMPT_20260707.md=True
docs/infra/MAOFIELD_PRO_D707_BOUNDED_FORMAL_NOTE_V0_PACKAGE_20260707.md=True
docs/infra/MAOFIELD_PRO_D707_BOUNDED_FORMAL_NOTE_V0_NODE19_DELIVERY_20260707.md=True
docs/infra/recovery/D707_SPLIT_LOOP_OUTPUTS_ADOPTION_NOTE_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/session4/MAIN_PRO_HANDOFF_PACKET_20260707.md=True
docs/infra/recovery/d707_split_loop_outputs/loop0/CLAIM_LEDGER_LOOP0_20260707.md=True
docs/infra/gpt_deep_research/D707_SPLIT_LOOP_BOUNDED_FORMAL_NOTE_REVIEW_REPORT37_ADOPTION_NOTE_20260707.md=True
GPT55_PRO_D707_BOUNDED_FORMAL_NOTE_V0_MAIN_PROMPT_20260707.md=True
MaoField_PRO_D707_BoundedFormalNoteV0_20260707_1727_bounded_note_v0_fix.zip=True
DRAFT_INTERNAL_V0_NOW=True
REVISE_BEFORE_FORMAL_NOTE=True
PATCH_DEFINITIONS_THEN_RECHECK=True
Loop0 -> Loop3 -> Loop4 -> Session4 -> Main Pro/SubPro A/E=True
metric-object identity is unlicensed unless declared transport and path-closure hold=True
finite chart/path/cycle defect calculus under declared transports=True
Mode B remains `insufficient_artifact`=True
NMI-ready=True
proof-by-JSON=True
```

## Smoke Search Verdict

Verdict: `PASS_LOCATOR`.

Smoke observations:

- Package query locates the package record, report37, main prompt, `MD_CATALOG.md`, node19 delivery record, adoption note, and taskbook.
- Delivery query locates the node19 delivery record and package record.
- Report37 route query locates the main prompt, synthesis, SubPro E prompt, review artifact index, `MD_CATALOG.md`, and prior report37 RAG record.
- Core-claim query locates Loop0 state lock, main prompt, Loop0 claim ledger, synthesis, split-loop goals, split-loop prompt source, and Loop4 finite-cycle definitions.

## Node22 Shutdown

Node22 temporary embedding worker was stopped after promotion.

Final stop output:

```text
stopped pid=3598219
```

Final port check:

```text
not running port=18080
```

## Claim Boundary

This RAG refresh is only for locating the next Pro package and prompt. It is not proof, not peer review, not public readiness, and not empirical evidence.

Still forbidden:

- MaoField empirical-positive claim
- proof-by-JSON / proof-by-harness / proof-by-artifact
- observed residual / interaction / transport / holonomy / gluing / collapse field
- dynamic-collapse theory
- black-box mechanism solved
- broad ANOVA / dependent-input / sheaf / contextuality / projection theory
- NMI-ready or submission-ready
- public/paper-ready promotion from report37 or this package

Mode B remains:

```text
insufficient_artifact
```

Duplicate risk remains:

```text
MEDIUM
```
