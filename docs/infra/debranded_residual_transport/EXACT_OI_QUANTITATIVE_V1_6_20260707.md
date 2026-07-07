# Exact Quantitative OI Norm Support v1.6

Date: 2026-07-07 CST

Status: synthetic-only exact rational support for the v1.6
quantitative OI norm companion. This is not a MaoField empirical
result and is not proof authority.

## Artifact

```text
exact_oi_quantitative_v1_6_20260707.json
sha256=14b84dde306af6bb455e4aa7fce5d4ced901f7da0ad7587380d6796ce4812b13
```

## Boundary

Mode B MaoField empirical status:

```text
insufficient_artifact
```

The mathematical claim is carried by the analytic finite-dimensional
proof in `FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md`, not by
this JSON/Markdown support artifact.

## Exact Checks

- `witness_strictly_positive`: pass
- `witness_probability_sum_one`: pass
- `witness_tau_exact`: pass
- `witness_rho_squared_exact`: pass
- `witness_oi_operator_norm_squared_exact`: pass
- `old_v1_4_fixed_witness_norm_squared_exact`: pass
- `operator_norm_not_fixed_witness_norm`: pass
- `operator_to_fixed_witness_ratio_exact`: pass
- `product_control_tau_zero`: pass
- `product_control_rho_squared_zero`: pass
- `product_control_oi_squared_zero`: pass

Overall:

```text
all_checks_passed=True
```

## v1.3 Witness Table

```text
w = (1/11) [[1,2],
            [3,5]]
tau = -1/121
rho^2 = 1/672
(OI^op_N_add)^2 = 671/451584
```

## Normalization Guard

```text
v1.6 operator norm squared = 671/451584
v1.4 fixed witness artifact norm squared = 61/177408
ratio = 121/28
```

These are different quantities. The v1.6 value is an operator norm
after input normalization. The v1.4 value is the output norm of one
fixed witness.

## Product Control

```text
w = [[1/6, 1/3],
     [1/6, 1/3]]
tau = 0
rho^2 = 0
(OI^op_N_add)^2 = 0
```

## Forbidden Upgrades

Do not use this support artifact to claim empirical positives,
observed residual fields, broad projection theory, or proof by JSON.
