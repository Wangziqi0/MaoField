# Debranded Residual Transport Synthetic Harness v0

Date: 2026-06-25 CST

## Boundary

This is a zero-GPU toy harness for the debranded mathematics direction.
It is not a MaoField empirical result and does not authorize training,
checkpoint loading, full-panel generation, or a new loss.

Strongest allowed verdict:

```text
definitions_and_harness_viable_only
```

## Artifact

```text
docs/infra/debranded_residual_transport/synthetic_harness_v0_20260625.json
sha256=d999ae147b9a7a641ea1adff297e2582b5dfd7b16c28568dd688abbd34df89af
```

Script:

```text
scripts/debranded_residual_transport_harness.py
```

Run location:

```text
/home/amd/codex-node36/tmp/debranded-residual-transport-20260625_v0
```

## Seven Blocks

- `non_product_weighted_projection`: pass
- `edge_defect`: pass
- `square_holonomy`: pass
- `rank_shadow_guard`: pass
- `random_subspace_guard`: pass
- `gluing_absorption`: pass
- `commutator_obstruction`: pass

All synthetic controls passed:

```text
true
```

## Key Metrics

```text
non_product_weighted_projection.observed_minus_product_max_abs = 0.0225
non_product_weighted_projection.residual_difference_norm_under_observed_weight = 0.0271321227928
edge_defect.natural_relative_defect_norm = 1.63653433704e-15
edge_defect.bad_nuisance_relative_defect_norm = 0.463621974123
square_holonomy.natural_square_holonomy_norm = 3.14018491737e-16
square_holonomy.bad_nuisance_square_holonomy_norm = 1.19444444444
rank_shadow_guard.rank1_sigma2_over_sigma1 = 9.73734454048e-17
rank_shadow_guard.multidirectional_sigma2_over_sigma1 = 0.25286504479
random_subspace_guard.true_subspace_capture_ratio = 1
random_subspace_guard.random_capture_p95 = 0.585855425307
gluing_absorption.absorbed_mismatch_residual_norm = 4.4408920985e-16
gluing_absorption.obstruction_mismatch_residual_norm = 1
commutator_obstruction.good_operator_commutator_norm = 0
commutator_obstruction.bad_operator_commutator_norm = 0.406201920232
```

## Interpretation

The operator definitions are executable on small finite weighted systems and
the seven kill controls have toy positive and negative cases. This supports
continuing formalization only.

Blocked interpretations:

```text
residual_field_observed
interaction_field_observed
quotient_residual_field_observed
transport_field_observed
holonomy_field_observed
glass_box_broken
training_authorized
new_loss_authorized
```
