# Exact Witness Certificate v1.4 -- Order Defect

Date: 2026-06-29 CST

Status: synthetic-only exact rational certificate for the v1.3
finite weighted order-defect note. This is not a MaoField empirical
result and is not a completed formal system claim.

## Artifact

```text
exact_witness_v1_4_20260629.json
sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
```

## Boundary

Allowed ceiling:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status:

```text
insufficient_artifact
```

## Exact Checks

- `main_b0_true_additive_residual_zero`: pass
- `main_b0_zero_order_residual_zero`: pass
- `main_b0_artifact_vector_exact`: pass
- `main_b0_artifact_norm_sq_exact`: pass
- `symmetric_a_true_additive_residual_zero`: pass
- `symmetric_a_zero_order_residual_zero`: pass
- `symmetric_a_artifact_vector_exact`: pass
- `order_defect_equals_commutator_exact`: pass
- `order_defect_nonzero`: pass

All checks passed: `true`

## Main B0 Witness

```text
K = ['7/11', '-4/11', '7/11', '-4/11']
(I-P_N)K = ['0', '0', '0', '0']
R_B_then_Q K = ['0', '0', '0', '0']
R_Q_then_B K = ['1/32', '5/168', '-1/96', '-1/84']
||R_Q_then_B K||_w^2 = 61/177408
```

## Symmetric A Witness

```text
K' = ['8/11', '8/11', '-3/11', '-3/11']
R_Q_then_B K' = ['0', '0', '0', '0']
R_B_then_Q K' = ['1/42', '-1/84', '5/224', '-3/224']
```

## Interpretation

This certificate upgrades the displayed 2x2 witness from float-based
regression support to exact rational arithmetic. It does not replace
the analytic proof and does not authorize empirical MaoField claims.
