# Debranded Residual Transport Synthetic Harness v1.1

Date: 2026-06-25 CST

## Boundary

This is a zero-GPU synthetic harness for the debranded mathematics
direction. It is not a MaoField empirical result and does not authorize
training, checkpoint loading, full-panel generation, model inference,
or a new loss.

Strongest allowed verdict:

```text
definitions_and_harness_viable_only
```

## Artifact

```text
docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json
```

## v1.1 Blocks

- `exact_product_weight_equality_control`: pass
- `product_reweighting_separation`: pass
- `outcome_derived_nuisance_invalidation`: pass (invalid_artifact)
- `transport_stable_multidirectional_positive_control`: pass
- `bad_edge_defect_control`: pass
- `projection_evolution_commutator_obstruction`: pass
- `raw_path_equality_square_control`: pass
- `coarsening_non_naturality_trap`: pass (killed_by_coarsening)
- `rank1_plus_noise_floor_trap`: pass (killed_by_rank1_shadow)
- `random_subspace_in_residual_space`: pass
- `equal_cell_count_random_axes`: pass
- `within_axis_shuffle_null_distribution`: pass
- `gluing_absorption`: pass (killed_by_gluing_absorption)
- `triple_overlap_gluing_cocycle`: pass

All synthetic controls passed:

```text
true
```

## Selected Metrics

```text
exact_product_weight_equality_control.product_weight_max_abs_error = 0
exact_product_weight_equality_control.residual_difference_norm_under_observed_weight = 0
product_reweighting_separation.max_abs_diff = 0.0869800839995
product_reweighting_separation.observed_raw_weight_norm_diff = 0.127651515989
outcome_derived_nuisance_invalidation.source_fixed_residual_norm = 1
outcome_derived_nuisance_invalidation.outcome_derived_residual_norm = 0
transport_stable_multidirectional_positive_control.max_edge_relative_defect_norm = 2.33979226107e-15
transport_stable_multidirectional_positive_control.coarse_residual_sigma2_over_sigma1 = 0.648672714086
bad_edge_defect_control.good_edge_relative_defect_norm = 1.63653433704e-15
bad_edge_defect_control.bad_edge_relative_defect_norm = 0.463621974123
projection_evolution_commutator_obstruction.good_commutator_fro_norm = 0
projection_evolution_commutator_obstruction.bad_commutator_fro_norm = 0.612372435696
projection_evolution_commutator_obstruction.bad_signal_leakage_norm = 0.875
raw_path_equality_square_control.raw_path_max_abs_diff = 0
raw_path_equality_square_control.square_holonomy_norm = 1.92296268638e-16
coarsening_non_naturality_trap.raw_path_max_abs_diff = 0
coarsening_non_naturality_trap.path_dependent_bad_nuisance_holonomy_norm = 1.19444444444
rank1_plus_noise_floor_trap.rank1_noise_sigma2_over_sigma1 = 6.2366828602e-05
rank1_plus_noise_floor_trap.multidirectional_sigma2_over_sigma1 = 0.274114060349
random_subspace_in_residual_space.true_subspace_capture_ratio = 0.982280123544
random_subspace_in_residual_space.random_capture_p99 = 0.859050072162
equal_cell_count_random_axes.named_axis_capture_ratio = 1
equal_cell_count_random_axes.random_equal_cell_axis_capture_p99 = 0.755928946018
within_axis_shuffle_null_distribution.within_axis_shuffle_capture_p99 = 0.801783725737
within_axis_shuffle_null_distribution.bad_axis_label_capture_ratio = 8.32667268469e-17
gluing_absorption.absorbed_mismatch_residual_norm = 4.4408920985e-16
gluing_absorption.obstruction_mismatch_residual_norm = 1
triple_overlap_gluing_cocycle.absorbed_cycle_residual_norm = 0
triple_overlap_gluing_cocycle.obstruction_cycle_residual_norm = 2.1
```

## Interpretation

The v1.1 harness keeps the v1 product, nuisance, square, rank,
random-axis, and gluing controls while adding explicit bad-edge,
projection-evolution commutator, shuffle-null, tougher random-subspace,
triple-overlap gluing, threshold-contract, and environment metadata
checks. Passing these toy controls supports formal design review only.

Blocked interpretations:

```text
full_panel_has_run
sixteen_cell_full_panel_aggregate_exists
residual_field_observed
interaction_field_observed
quotient_residual_field_observed
transport_field_observed
holonomy_field_observed
glass_box_broken
LOSO_passed
F3_positive
training_authorized
new_loss_authorized
```
