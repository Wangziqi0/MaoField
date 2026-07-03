# Node22 Vector Refresh -- Order-Defect Report20 Formal Preprint Draft Gate

Date: 2026-07-03 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260703_1053_report20_formal_preprint_draft_gate`

## Purpose

Refresh the canonical MaoField RAG index after report(20), its node36 adoption
note, local verification, D703 formal-preprint-draft taskbook, and D703
`STATE.md` / `MD_CATALOG.md` status updates were added.

Report(20) produced:

```text
independent English preprint candidate V1 for local review only
```

Node36 adopts it only as:

```text
ENGLISH_PREPRINT_CANDIDATE_V1_INTERNAL_REVIEW_ACCEPTED_PREPARE_FORMAL_DRAFT_GATE
```

Local next action:

```text
PREPARE_FORMAL_PREPRINT_DRAFT_GATE_UNDER_LOCK
```

RAG is a locator only. It is not proof, bibliography authority, package
authority, paper-ready authority, preprint-ready authority, posting authority,
submission authority, or evidence for MaoField empirical claims.

## Scope Policy

The report(20) scope is based on the current active canonical MaoField markdown
scope plus the D703 current files:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_english_preprint_candidate_v1_report20_20260703.md
docs/infra/gpt_deep_research/ORDER_DEFECT_ENGLISH_PREPRINT_CANDIDATE_V1_REPORT20_ADOPTION_NOTE_20260703.md
docs/infra/recovery/ORDER_DEFECT_D703_REPORT20_LOCAL_VERIFICATION_20260703.md
docs/infra/recovery/ORDER_DEFECT_D703_FORMAL_PREPRINT_DRAFT_GATE_TASKBOOK_20260703.md
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_REPORT20_FORMAL_PREPRINT_DRAFT_GATE_20260703.md
STATE.md
MD_CATALOG.md
```

Scope sidecar:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260703_1053_report20_formal_preprint_draft_gate.txt
```

Exact scope hash, active file count, promoted index hashes, and chunk count are
stored in sidecars named with the tag above. They are intentionally not repeated
here to avoid self-referential hash drift when this record itself enters the RAG
scope.

## Build Route

Node36 owned scope generation, chunking, FAISS writing, hash verification,
promotion, and smoke queries. Node22 only served temporary bge-m3 embeddings
through a llama.cpp OpenAI-compatible HTTP endpoint.

The temporary worker used:

```text
host: amd@192.168.31.22
endpoint: http://192.168.31.22:18080
model alias: bge-m3-temp
embedding dim: 1024
```

The first HTTP build attempt failed because the general bge service on port
8080 had `--batch-size 512`, which rejected a 523-token embedding input. The
repeatable build path was corrected by using the existing node22 temporary
service script on port 18080 with a larger physical batch size, and by adding
`--max-input-chars` to `scripts/rag_build_index_node22_http.py`. Metadata keeps
the original chunk text; only the text sent to the HTTP embedding server is
truncated for embedding parity with the CPU path's max-length behavior.

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260703_1053_report20_formal_preprint_draft_gate.log
```

## Promoted Hashes

Promoted sidecar:

```text
docs/infra/rag_rebuild_20260622/promoted_hashes_20260703_1053_report20_formal_preprint_draft_gate.txt
```

Use that sidecar for exact `kb.faiss`, `kb_meta.jsonl`, scope hash, active file
count, and chunk count.

Candidate hashes are stored in:

```text
docs/infra/rag_rebuild_20260622/candidate_hashes_20260703_1053_report20_formal_preprint_draft_gate.txt
```

Previous canonical index backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260703_1053_report20_formal_preprint_draft_gate
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260703_1053_report20_formal_preprint_draft_gate
```

## Smoke Queries

Smoke query outputs:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_report20_candidate_20260703_1053_report20_formal_preprint_draft_gate.txt
docs/infra/rag_rebuild_20260622/rag_smoke_d703_state_boundary_20260703_1053_report20_formal_preprint_draft_gate.txt
docs/infra/rag_rebuild_20260622/rag_smoke_d703_forbidden_boundary_20260703_1053_report20_formal_preprint_draft_gate.txt
```

The smoke queries located report(20), the report(20) adoption note, the D703
taskbook, the local verification note, `STATE.md`, `MD_CATALOG.md`,
`FORMAL_PREPRINT_DRAFT_GATE_UNDER_LOCK`, `PREPARE_FORMAL_PREPRINT_DRAFT_GATE_UNDER_LOCK`,
`MEDIUM duplicate risk`, harness-as-regression-support wording, and Mode B
`insufficient_artifact`.

## Boundary

The refreshed index must not be treated as evidence that a paper is ready, a
preprint is ready, a preprint is posted, a submission is authorized, the
emergency lock is lifted, a full panel has run, training/inference occurred,
or any MaoField residual/interactions/transport/holonomy field has been
observed.

## Node22 Lifecycle

Node22 temporary service status is recorded in:

```text
docs/infra/rag_rebuild_20260622/node22_stop_20260703_1053_report20_formal_preprint_draft_gate.txt
```

The temporary service was stopped after promotion. Node36 retains scratch
candidate artifacts under:

```text
/home/amd/codex-node36/tmp/rag_20260703_1053_report20_formal_preprint_draft_gate/
```
