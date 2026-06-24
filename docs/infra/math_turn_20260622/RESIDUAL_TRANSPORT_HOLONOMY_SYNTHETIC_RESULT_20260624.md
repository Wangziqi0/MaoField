# Residual Transport / Holonomy Synthetic Result

Date: 2026-06-24 CST

## Boundary

This is a zero-GPU synthetic result for the report(23) finite scale-lattice
residual transport / holonomy proposal. It is not a MaoField empirical result.

It did not read MaoField aggregates, load checkpoints, run model inference,
train, or authorize a new loss.

Strongest allowed verdict:

```text
synthetic_harness_only_no_maofield_claim
```

Blocked interpretations:

```text
transport_field_observed
holonomy_field_observed
interaction_field_observed
quotient_residual_field_observed
glass_box_broken
training_authorized
new_loss_authorized
```

## Artifact

```text
docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.json
sha256=5c0d9586f31c60512a645020d4b1f0ee0a516a2fa8437c10db30e7f59f8884fd
```

Script:

```text
scripts/residual_transport_holonomy_synthetic.py
```

Run location:

```text
/home/amd/codex-node36/tmp/residual-transport-holonomy-20260624_1640
```

## Results

All synthetic controls passed:

```text
scale_square_holonomy                    pass
nuisance_functoriality_digest            pass
rank1_angle_vacuity_guard                pass
random_same_dim_angle_gap                pass
```

Key metrics:

```text
natural_square_holonomy_norm        = 3.14e-16
bad_nuisance_square_holonomy_norm   = 1.1944
natural_edge_relative_defect        = 1.64e-15
bad_nuisance_edge_relative_defect   = 0.4636
rank1_sigma2_over_sigma1            = 9.74e-17
multidirectional_sigma2_over_sigma1 = 0.2529
random_subspace_true_capture        = 1.0
random_subspace_p95_capture         = 0.5965
```

## Interpretation

The definitions are executable on toy finite tables, and the proposed kill
tests have both positive and negative controls:

- natural product/additive coarsening closes the refinement square up to
  numerical noise;
- deliberately non-functorial nuisance creates visible path dependence;
- repeated one-template residuals are killed as rank-1 shadows;
- a known two-dimensional toy residual subspace beats random same-dimension
  subspaces.

This supports continuing Mode A formalization. It does not upgrade MaoField
Mode B beyond:

```text
stable non-scalar residual object = insufficient_artifact
existing interaction smoke = smoke_conjecture_only
```
