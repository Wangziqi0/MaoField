# README For GPT-5.5 Pro Formal v1.3 Order-Defect Implementation Audit Package

Date: 2026-06-28 CST

This package is for a zero-context GPT-5.5 Pro audit of the local Formal v1.3
order-defect proof note and deterministic zero-GPU harness after report (32).

## Primary Task

Ask Pro to audit:

```text
FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
scripts/debranded_residual_transport_harness_v1_3.py
SYNTHETIC_HARNESS_V1_3_20260628.md
synthetic_harness_v1_3_20260628.json
```

The audit should decide whether the local v1.3 proof note and harness pass, or
whether a minor revision is needed.

## Evidence Boundary

This is Mode A finite-dimensional mathematics only. It is not MaoField
empirical validation.

Strongest allowed local verdict:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status:

```text
insufficient_artifact
```

## Critical Mathematical Guardrails

- `N_add = C direct-sum A direct-sum B0` is algebraic in general, not
  automatically orthogonal.
- `P_C`, `P_A`, and `P_B0` are weighted orthogonal projections onto individual
  subspaces. `P_N` is the weighted orthogonal projection onto the whole
  additive nuisance space.
- `P_N = P_C + P_A + P_B0` is valid only after product-form orthogonality is
  established.
- `D_w != 0` means the ordered operators are unequal and some witness signal
  shows order dependence; it does not mean every input differs.
- The non-product wrong-order output is a `sequential stripping artifact` or
  `interaction-like artifact`, not a true interaction residual.

## Arithmetic Correction To Audit

Report (32)'s main `B0` witness was correct:

```text
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
```

Report (32)'s optional symmetric `A` witness had an 11x arithmetic slip. The
local v1.3 note and harness use the corrected vector:

```text
R_B_then_Q K' = (1/42, -1/84, 5/224, -3/224)
```

Pro should verify these exact rational coordinates and check whether any
similar scaling mistakes remain.

## Forbidden Upgrades

Do not claim:

- full panel has run;
- 16-cell aggregate exists;
- checkpoint loading, inference, training, or new loss is authorized;
- MaoField residual / interaction / quotient-residual / transport / holonomy
  field has been observed;
- glass box broken;
- LOSO passed;
- F3 positive;
- completed formal system;
- theorem stack complete;
- Formal v1.3 completed as a whole system.

## Recommended Use

Upload the zip, then paste the standalone prompt:

```text
GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_IMPLEMENTATION_AUDIT_PROMPT_20260628.md
```

The prompt asks Pro for a strict PASS/WARN/FAIL audit of definitions, T1, T2,
T3, exact rational coordinates, harness/script/JSON, and claim boundary.
