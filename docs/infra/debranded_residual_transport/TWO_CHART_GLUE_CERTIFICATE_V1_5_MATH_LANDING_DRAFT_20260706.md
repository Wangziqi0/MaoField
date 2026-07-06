# Two-Chart Glue Certificate v1.5 Math Landing Draft

Date verified on node36: 2026-07-06 11:40:43 CST

Status:

```text
DRAFT_FOR_PRO_REVIEW_NOT_CERTIFICATE
```

This file is a direct mathematical landing draft prepared after an internet
prior-art scan. It is not yet the final formal note, not an exact script output,
and not paper authorization.

## Name

Use the conservative name:

```text
Gauge-Quotiented Finite Consistency Radius
```

Internal shorthand:

```text
GQ-FCR
```

This name acknowledges nearby prior art on sheaf consistency radius while
preserving the MaoField specialization: finite residual-audit objects, declared
gauge/nuisance subspaces, and exact rational certificates.

## Data

Let `I_1`, `I_2`, and `O_12` be finite sets. Work over rational vectors for
certificates and over real vectors for projection language:

```text
H_i = Q^{I_i}
V_12 = Q^{O_12}
```

Given:

```text
rho_i : H_i -> V_12
```

restriction maps, positive rational weights

```text
w_12(o) > 0
```

on `O_12`, and a declared overlap gauge/nuisance subspace

```text
Gamma_12 subset V_12.
```

For local sections `s_i in H_i`, define the raw overlap mismatch:

```text
m_12(s_1,s_2) = rho_1 s_1 - rho_2 s_2.
```

Define the weighted inner product:

```text
<u,v>_{w_12} = sum_{o in O_12} w_12(o) u(o)v(o).
```

Let `P_Gamma` be the weighted orthogonal projection onto `Gamma_12`.

## Definition

The gauge-quotiented finite consistency radius squared is:

```text
Delta^2_12(s_1,s_2; Gamma_12)
  = min_{gamma in Gamma_12}
      ||m_12(s_1,s_2) - gamma||^2_{w_12}
  = ||(I - P_Gamma)m_12(s_1,s_2)||^2_{w_12}.
```

The unsquared radius is:

```text
Delta_12 = sqrt(Delta^2_12).
```

For exact rational certificates, store `Delta^2_12` as the primary value.

## Compatibility Theorem

### Statement

For fixed finite data and fixed declared gauge `Gamma_12`:

```text
Delta^2_12(s_1,s_2; Gamma_12) = 0
```

if and only if there exists `gamma in Gamma_12` such that:

```text
rho_1 s_1 - rho_2 s_2 = gamma.
```

Equivalently, the two local sections are compatible on the overlap modulo the
declared gauge.

### Proof

By definition, `Delta^2_12` is the squared weighted distance from the mismatch
`m_12` to the subspace `Gamma_12`. Since all weights are positive, the weighted
inner product is positive definite. Distance to a subspace is zero if and only
if the vector belongs to the subspace. Therefore `Delta^2_12=0` exactly when
`m_12 in Gamma_12`.

## No-Pasting Corollary

If a two-chart pasted object is defined to mean a pair of gauge-adjusted local
sections whose restrictions agree on `O_12`, then:

```text
Delta^2_12 > 0
```

implies no pasted object exists inside the declared gauge class.

This corollary is semantic: it depends on the declared meaning of "pasted
object." Do not add stronger global regularity conditions unless they are
explicitly placed in the finite data.

## Gauge Monotonicity

If:

```text
Gamma_12 subset Gamma'_12
```

then:

```text
Delta^2_12(s_1,s_2; Gamma'_12)
  <= Delta^2_12(s_1,s_2; Gamma_12).
```

Proof: minimization over a larger subspace cannot increase the minimum.

Consequently, an obstruction is always relative to the declared gauge. If
enlarging the gauge absorbs it, the old obstruction was a certificate only
relative to the narrower gauge, not an absolute structural contradiction.

## Exact 2x2 Controls

Use overlap order:

```text
(q1,b1), (q1,b2), (q2,b1), (q2,b2).
```

Use uniform weights:

```text
w = (1/4, 1/4, 1/4, 1/4).
```

Use additive gauge:

```text
Gamma = span{
  1 = (1,1,1,1),
  q = (-1,-1,1,1),
  b = (-1,1,-1,1)
}.
```

### Positive Control

Let:

```text
m_plus = (1, 2, 3/2, 5/2).
```

Then:

```text
m_plus = (7/4) * 1 + (1/4) * q + (1/2) * b.
```

Thus:

```text
m_plus in Gamma
Delta^2(m_plus; Gamma) = 0.
```

### Negative Control

Let:

```text
m_minus = (1, -1, -1, 1).
```

Then under the uniform weighted inner product:

```text
<m_minus, 1>_w = 0
<m_minus, q>_w = 0
<m_minus, b>_w = 0.
```

Therefore `m_minus` is orthogonal to `Gamma`, so:

```text
(I - P_Gamma)m_minus = m_minus
Delta^2(m_minus; Gamma) = ||m_minus||^2_w = 1.
```

## Relation To Existing MaoField Order Defect

The order-defect certificate handles same-carrier procedural non-identity:

```text
wrong-order stripping output != true residual.
```

The GQ-FCR handles overlap non-identity:

```text
two local residual-like sections fail to paste modulo declared gauge.
```

The shared principle is:

```text
do not promote raw mismatch; first quotient or project away declared nuisance.
```

## Prior-Art Boundary

This draft must be positioned against:

- Robinson's sheaf consistency radius;
- cellular sheaf global-section/cohomology literature;
- Abramsky-Brandenburger contextuality/global-section obstruction;
- dependent-input ANOVA/Hoeffding-Sobol work;
- classical two-projection theory.

Safe novelty, if any, is narrow:

```text
an exact rational residual-audit specialization with declared additive gauge,
paired controls, and integration with the finite order-defect spine.
```

Unsafe novelty:

```text
broad sheaf theory, broad consistency radius theory, broad contextuality,
broad ANOVA, or broad projection theory.
```

## Proposed Final Artifact Paths

If Pro approves this draft, node36 should convert it into:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md
scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py
docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json
docs/infra/debranded_residual_transport/EXACT_GQ_FCR_V1_5_20260706.md
```

## Required Exact Script Assertions

- all weights are positive rational strings;
- gauge basis is rank checked;
- Gram matrix on an independent gauge basis is invertible;
- positive control has exact projected residual zero;
- negative control has exact projected residual `m_minus`;
- negative control has exact norm squared `1`;
- gauge monotonicity is tested with an enlarged gauge containing checkerboard;
- JSON stores rational strings and declares `fractions.Fraction`;
- no float is used as proof authority.
