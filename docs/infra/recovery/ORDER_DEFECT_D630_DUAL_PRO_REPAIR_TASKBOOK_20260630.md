# Order-Defect D630 Dual-Pro Repair Taskbook

Date: 2026-06-30 CST
Authority: node36
Purpose: prevent context drift after receiving two independent Pro recovery
repair reports.

## Current Binding

Current verdict:

```text
KEEP_LOCK_AND_FIX
```

Allowed activity:

```text
recovery_audit
proof_repair_audit
bibliography_conservatism_repair
status_and_index_repair
```

Forbidden activity while the external-model emergency lock remains active:

```text
paper_body_drafting
proof_authority_promotion
bibliography_authority_promotion
claim_promotion
posting_or_ready_decision
```

## Evidence Inputs

- `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_repair_dual_pro_report6_20260630.md`
- `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_repair_dual_pro_report7_20260630.md`
- `docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`
- `docs/infra/recovery/ORDER_DEFECT_D630_TASKBOOK_NEXT_PRO_20260630.md`
- `docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`
- `docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`
- `docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`

## Required Repair Scope

This round is deliberately small:

1. Archive both Pro reports with sha256.
2. Patch `docs/infra/debranded_residual_transport/README.md` so the active next
   step is D630 recovery repair, not v1.6 paper drafting.
3. Patch `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` so Lamboni 2026 is
   treated as DOI / publisher online record status only for current drafting.
4. Update `STATE.md`, `MD_CATALOG.md`, and recovery index notes so they reflect
   dual-Pro verdict `KEEP_LOCK_AND_FIX`.
5. Refresh RAG through node22 one-shot vectorization and stop node22.

## Proof-Risk Labels

Preserve these labels unless a later proof-repair audit changes them:

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: PLAUSIBLE_LOCAL_DRAFT
Proposition 3: PLAUSIBLE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
```

## Forbidden Claims

Do not claim:

- full panel has run;
- 16-cell aggregate exists;
- checkpoint loading, inference, training, or new loss authorization;
- observed MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- glass box broken;
- F3 positive;
- LOSO passed;
- completed formal system;
- paper-ready or posted preprint;
- JSON floats or deterministic harness prove theorem;
- broad new ANOVA, dependent-input decomposition, or noncommuting projection
  theory.

## Completion Criteria

This taskbook is complete only when:

- both reports are archived;
- the adoption note exists;
- README and Lamboni wording are patched;
- status/catalog/recovery pointers are updated;
- exact/harness smoke checks pass locally;
- RAG refresh and smoke search pass;
- node22 temporary service is stopped;
- git commit is made from node36 with only intentional files.
