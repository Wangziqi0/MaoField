# Residual Transport / Holonomy Synthetic Harness

Date: 2026-06-24 CST

## Boundary

This is a Mode A synthetic harness for report (23)'s finite scale-lattice
residual transport proposal. It is not a MaoField experiment result.

It does not:

- read a MaoField aggregate;
- load checkpoints;
- run model inference;
- train;
- authorize a new loss;
- observe a residual, interaction, transport, or holonomy field.

The MaoField Mode B verdict remains:

```text
stable non-scalar residual object = insufficient_artifact
existing interaction smoke = smoke_conjecture_only
```

## Script

```text
scripts/residual_transport_holonomy_synthetic.py
```

The script builds small toy finite tables and implements four report(23)
definition checks:

```text
scale_square_holonomy
nuisance_functoriality_digest
rank1_angle_vacuity_guard
random_same_dim_angle_gap
```

## What It Tests

`scale_square_holonomy` compares two paths around a 4x4 -> 2x2 refinement
square. With product weights and additive nuisance at every scale, the square
should commute up to numerical noise. With deliberately non-functorial
intermediate nuisance, the two paths should diverge.

`nuisance_functoriality_digest` computes an edge defect

```text
D_rho(K) = C_rho P_s K - P_s' C_rho K
```

and verifies that a natural additive nuisance has near-zero defect while a bad
coarse nuisance produces a nonzero defect.

`rank1_angle_vacuity_guard` checks that repeated copies of one interaction
template are killed as a rank-1 shadow, while a two-direction synthetic object
clears the current design-review floor:

```text
sigma2 / sigma1 >= 0.25
```

`random_same_dim_angle_gap` checks that a known toy two-dimensional residual
subspace beats random same-dimension subspaces on a held-out vector.

## Allowed Interpretation

If all synthetic controls pass, the only allowed conclusion is:

```text
synthetic_harness_only_no_maofield_claim
```

This means the definitions are executable and the proposed kill tests have toy
positive and negative controls. It does not make any claim about real MaoField
data.

## Run Rule

Run from node36 SSD scratch, not directly in canonical:

```bash
SCR=/home/amd/codex-node36/tmp/residual-transport-holonomy-20260624
mkdir -p "$SCR"
cd "$SCR"
/home/amd/venv/bin/python \
  /media/amd/raid1/canonical/projects/MaoField/scripts/residual_transport_holonomy_synthetic.py \
  --out synthetic_harness_result.json \
  --random-draws 1000
```

Only promote small JSON/markdown summaries after verifying the result and
preserving the boundary above.

## First Verified Run

The first verified run is archived at:

```text
docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md
docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.json
```

All four synthetic controls passed, with strongest allowed verdict:

```text
synthetic_harness_only_no_maofield_claim
```
