# Exact GQ-FCR Certificate v1.5

Date: 2026-07-06 CST

Status: synthetic-only exact rational certificate for the v1.5
Gauge-Quotiented Finite Consistency Radius formal note. This is not a
MaoField empirical result and is not a broad consistency-radius, sheaf,
contextuality, ANOVA, or projection-theory claim.

## Artifact

```text
exact_gq_fcr_v1_5_20260706.json
sha256=01d3d452da17b0b7d1d1ad7b169c30a2b26d9098a4d1060703cc51cf9a856231
```

## Boundary

Allowed ceiling:

```text
definitions_and_exact_certificate_viable_only
```

Mode B MaoField empirical status:

```text
insufficient_artifact
```

## Exact Definition Checked

```text
Delta^2_12(s_1,s_2; Gamma_12)
  = min_{gamma in Gamma_12} ||rho_1 s_1 - rho_2 s_2 - gamma||^2_w
  = ||(I - P_Gamma)(rho_1 s_1 - rho_2 s_2)||^2_w
```

All arithmetic is exact `fractions.Fraction`; JSON stores rationals as
strings. In the controls, `I_1 = I_2 = O_12`, `rho_1 = rho_2 = I`,
and `s_2 = 0`, so each raw mismatch is `s_1`.

## Exact Checks

- `weights_strictly_positive`: pass
- `gauge_gram_invertible`: pass
- `projection_idempotent`: pass
- `projection_weighted_self_adjoint`: pass
- `complement_annihilates_gauge_basis`: pass
- `positive_control_coefficients_exact`: pass
- `positive_control_residual_zero`: pass
- `positive_control_delta_squared_zero`: pass
- `negative_control_orthogonal_to_gauge`: pass
- `negative_control_residual_equals_mismatch`: pass
- `negative_control_delta_squared_one`: pass
- `enlarged_gauge_gram_invertible`: pass
- `enlarged_gauge_projection_is_identity`: pass
- `enlarged_gauge_absorbs_checkerboard`: pass
- `gauge_monotonicity_exact`: pass

All checks passed: `true`

## Positive Control

```text
m_plus = ['1', '2', '3/2', '5/2']
gauge coefficients [one,q,b] = ['7/4', '1/4', '1/2']
(I-P_Gamma)m_plus = ['0', '0', '0', '0']
Delta^2(m_plus; Gamma) = 0
```

## Negative Control

```text
m_minus = ['1', '-1', '-1', '1']
weighted inner products = {'one': '0', 'q': '0', 'b': '0'}
(I-P_Gamma)m_minus = ['1', '-1', '-1', '1']
Delta^2(m_minus; Gamma) = 1
```

## Gauge Monotonicity Witness

```text
Gamma' = span{one, q, b, checkerboard}
Delta^2(m_minus; Gamma) = 1
Delta^2(m_minus; Gamma') = 0
```

## Interpretation

`Delta^2 = 0` certifies compatibility modulo the declared overlap gauge.
A stronger statement about realized gauge-adjusted local sections requires
extra local gauge parameter spaces and overlap transfer maps. This
certificate does not include or claim that stronger data.
