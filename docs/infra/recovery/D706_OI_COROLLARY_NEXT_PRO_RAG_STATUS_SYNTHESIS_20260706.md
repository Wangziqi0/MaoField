# D706 OI Corollary Next-Pro RAG/Status Synthesis

Date verified on node36: 2026-07-06 20:17:12 CST.

Status:

```text
RAG_LOCATOR_AND_STATUS_SYNTHESIS
```

This file records the node36 status/RAG/grep basis for preparing the next
zero-context GPT-5.5 Pro package. RAG locates candidate evidence only; the
primary files listed below remain the claim authority.

## Git And Local State

At preparation start:

```text
repo: /media/amd/raid1/canonical/projects/MaoField
branch: main
HEAD: 410a944
dirty status: ?? .codex/ and ?? AGENTS.md only
```

Those untracked files are not part of this package task.

## Current Status Basis

`STATE.md` says the live action is:

```text
D706_REPORT31_OI_COROLLARY_DECISION_ACCEPTED_AND_RAG_SYNCED
```

It also states that the next exact-math step, if PI continues, should be only a
bounded one-page corollary companion:

```text
OI^{op}_{N_add}(w)=0 iff w is product form
```

The same status forbids upgrading this step into a current V2.5 preprint patch
or a dynamic chart-sequence/collapse-object theory.

## RAG Query

Command run on node36:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "OI op N_add product form order independence corollary companion report31 v1.3 Proposition 1 2 3" --top-k 8 --project MaoField
```

Raw output saved in the package as:

```text
raw/rag_oi_corollary_companion_top8.txt
```

Top locator hits:

1. `docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md`
2. `docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md`
3. `STATE.md`
4. `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_repair_dual_pro_report7_20260630.md`
5. `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md`
6. `docs/infra/gpt_deep_research/deep_research_order_defect_boundary_locked_draft_v10_report15_20260701.md`
7. `docs/infra/gpt_deep_research/deep_research_metric_identity_oi_corollary_decision_report31_20260706.md`
8. `docs/infra/recovery/V2_5_SOURCE_MAP_AND_CHANGELOG_20260703.md`

## Targeted Grep

Raw targeted grep output saved in the package as:

```text
raw/grep_oi_corollary_candidate.txt
```

Key local evidence:

- `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` defines `C`, `A`, `B0`,
  `N_add`, `R_Q_then_B`, `R_B_then_Q`, and `D_w`.
- v1.3 Proposition 1 proves product weights iff `A` is orthogonal to `B0`.
- v1.3 Proposition 2 proves `D_w=0` iff product weights and order-independence
  iff product weights.
- v1.3 Proposition 3 proves the existential pure-main-effect no-go witness for
  non-product weights.
- Report31 and its adoption note classify the restricted OI candidate only as
  `FORMALIZABLE_NOW_AS_COROLLARY_COMPANION`.

## Claim Authority

Primary proof authority:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
scripts/debranded_residual_transport_exact_witness_v1_4.py
```

Current decision authority:

```text
docs/infra/gpt_deep_research/deep_research_metric_identity_oi_corollary_decision_report31_20260706.md
docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md
docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md
STATE.md
```

Boundary/context authority:

```text
docs/infra/gpt_deep_research/deep_research_metric_identity_nonidentity_unity_next_math_report30_20260706.md
docs/infra/gpt_deep_research/METRIC_IDENTITY_NONIDENTITY_UNITY_NEXT_MATH_REPORT30_ADOPTION_NOTE_20260706.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md
docs/infra/debranded_residual_transport/EXACT_GQ_FCR_V1_5_20260706.md
```

## Safe Next Prompt Target

Ask GPT-5.5 Pro to choose exactly one:

```text
DRAFT_ONE_PAGE_OI_COROLLARY_COMPANION
PATCH_DEFINITION_THEN_RECHECK
REJECT_OR_DEFER_DUE_TO_PROOF_GAP
REQUEST_NODE36_FILES
```

The package must not ask Pro to create a broad theory, claim empirical
MaoField findings, revise the Zenodo V2.5 preprint, or merge GQ-FCR into the
order-defect theorem spine.
