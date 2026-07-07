# Node22 Vector Refresh -- D707 Report35/36 Split-Loop Prompts

Date verified on node36: 2026-07-07 13:28 CST.

Status:

```text
PROMOTED_AND_NODE22_STOPPED_REPORT35_36_SPLIT_LOOP_PROMPTS
```

This refresh covers the local adoption of Report35/36 and the split-loop prompt
package for the path-closure recheck sequence:

```text
Loop0 -> Loop3 -> Loop4 -> Session4 -> Main Pro/SubPro A/E
```

## Newly Indexed / Updated Files

```text
STATE.md
MD_CATALOG.md
docs/infra/gpt_deep_research/deep_research_path_closure_review_report35_20260707.md
docs/infra/gpt_deep_research/deep_research_path_closure_revision_report36_20260707.md
docs/infra/recovery/MAOFIELD_SPLIT_MAIN_AND_4_SESSIONS_PROMPTS_20260707.md
docs/infra/gpt_deep_research/PATH_CLOSURE_REPORT35_36_ADOPTION_NOTE_20260707.md
docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md
docs/infra/debranded_residual_transport/MATERIAL_RELATION_PATH_CLOSURE_PROGRAMME_BRIEF_20260707.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md
```

## Scope And Index Counts

```text
active markdown files=573
candidate chunks=10358
promoted meta rows=10358
faiss dim=1024
```

Promoted hashes:

```text
dab04126e8383c44c6d9f15c10bfc0c7b6923a2e8eb35b77b6fc98558a6f068c  /media/amd/raid1/rag/index/kb.faiss
99e60eaeb62dbcd4b7b50c69a5c9a206cdaaab4fe17f8912ad2898ffb2b0c0f6  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Backups were created with suffix:

```text
bak_pre_node22_20260707_1320_report35_36_split_loop
```

## Sidecars

Exact scope, hashes, candidate verification, smoke output, and node22 logs are
stored in non-Markdown sidecars with tag:

```text
20260707_1320_report35_36_split_loop
```

Key sidecars:

```text
docs/infra/rag_rebuild_20260622/scope_include_maofield_active_md_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/scope_sha256_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/candidate_verify_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/candidate_index_sha256_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/promoted_index_sha256_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/rag_smoke_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/rag_smoke_hits_20260707_1320_report35_36_split_loop.txt
docs/infra/rag_rebuild_20260622/node22_start_20260707_1320_report35_36_split_loop.log
docs/infra/rag_rebuild_20260622/node22_stop_20260707_1320_report35_36_split_loop.log
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260707_1320_report35_36_split_loop.log
```

## Candidate Verification

Candidate verification passed:

```text
faiss_ntotal=10358
faiss_dim=1024
meta_count=10358
ntotal_equals_meta=True
```

Required paths present:

```text
STATE.md :: True
MD_CATALOG.md :: True
deep_research_path_closure_review_report35_20260707.md :: True
deep_research_path_closure_revision_report36_20260707.md :: True
MAOFIELD_SPLIT_MAIN_AND_4_SESSIONS_PROMPTS_20260707.md :: True
PATH_CLOSURE_REPORT35_36_ADOPTION_NOTE_20260707.md :: True
MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md :: True
MATERIAL_RELATION_PATH_CLOSURE_PROGRAMME_BRIEF_20260707.md :: True
FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md :: True
```

Required phrases present:

```text
PATCH_DEFINITIONS_THEN_RECHECK :: True
ADOPT_PATCH_DEFINITIONS_THEN_RECHECK_AND_SPLIT_LOOP_EXECUTION :: True
Loop 0 :: True
Loop 3 :: True
Loop 4 :: True
READY_FOR_LOOP3 :: True
READY_FOR_LOOP4 :: True
READY_FOR_MAIN_PRO_AND_SUBPRO_A_E_REVIEW :: True
metric-object identity is unlicensed unless declared transport and path-closure hold :: True
Identity is not naming; identity is path closure under declared material relations :: True
proof-by-JSON :: True
NMI-ready :: True
dynamic-collapse theory :: True
```

The last three phrases are indexed as forbidden-boundary text, not as allowed
claims.

## Smoke

Smoke queries:

```text
MaoField Report35 Report36 PATCH_DEFINITIONS_THEN_RECHECK path closure split loop
MaoField Loop 0 Loop 3 Loop 4 Session 4 READY_FOR_MAIN_PRO_AND_SUBPRO_A_E_REVIEW
metric-object identity unlicensed declared transport path-closure hold proof-by-JSON NMI-ready dynamic-collapse forbidden
Identity is not naming identity is path closure under declared material relations
```

Smoke verdict:

```text
PASS_LOCATOR
```

The smoke locates the loop-goals doc, STATE/MD_CATALOG updates, Report35/36
adoption note, split-loop source, Report35 archive, and forbidden-boundary
sections.

## Node22 Stop

```text
stopped pid=3588920
not running port=18080
```

The `rocm-smi` output after stop still showed GPU use from other node22
services; the temporary port-18080 bge worker for this refresh was stopped.

## Claim Boundary

This refresh does not authorize:

- MaoField empirical positive claims;
- Loop6/Loop7 real black-box or empirical audit;
- NMI-ready / paper-ready claims for the path-closure line;
- observed residual, transport, holonomy, interaction, gluing, or collapse
  fields;
- broad ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof-by-JSON or proof-by-deterministic-harness wording.

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

RAG remains a locator only. Report35/36 and split prompts are task-source and
claim-boundary artifacts, not proof authority.
