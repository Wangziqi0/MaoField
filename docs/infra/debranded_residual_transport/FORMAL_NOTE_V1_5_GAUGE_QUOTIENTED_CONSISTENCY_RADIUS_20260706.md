# Formal Note v1.5 -- Gauge-Quotiented Finite Consistency Radius

Date verified on node36: 2026-07-06 12:51:36 CST

Status:

```text
MODE_A_FINITE_EXACT_CERTIFICATE_NOTE
```

This note implements the D706 Pro decision
`APPROVE_NODE36_IMPLEMENT_V1_5_GQ_FCR` in a deliberately narrow form. It is a
finite-dimensional residual-audit certificate, not a MaoField empirical result,
not paper authorization, and not a broad theory of sheaves, consistency radius,
contextuality, dependent-input ANOVA, or noncommuting projections.

## Data

Let `I_1`, `I_2`, and `O_12` be finite sets. Work over rational vectors for
certificates:

```text
H_i = Q^{I_i}
V_12 = Q^{O_12}
```

Given rational linear restriction maps

```text
rho_i : H_i -> V_12,
```

strictly positive rational overlap weights `w_12(o) > 0`, and a declared
overlap gauge/nuisance subspace

```text
Gamma_12 subset V_12,
```

define the raw overlap mismatch of local sections `s_i in H_i` by

```text
m_12(s_1,s_2) = rho_1 s_1 - rho_2 s_2.
```

The weighted inner product is

```text
<u,v>_w = sum_{o in O_12} w_12(o) u(o)v(o).
```

Because all weights are strictly positive, this is a positive-definite inner
product on the finite vector space `V_12`.

## Core Definition

Let `P_Gamma` be the weighted orthogonal projection onto `Gamma_12`. The
gauge-quotiented finite consistency radius squared is

```text
Delta^2_12(s_1,s_2; Gamma_12)
  = min_{gamma in Gamma_12}
      ||m_12(s_1,s_2) - gamma||^2_w
  = ||(I - P_Gamma)m_12(s_1,s_2)||^2_w.
```

The squared value `Delta^2_12` is the certificate-level value. The unsquared
radius can be taken afterward, but is not needed for exact rational auditing.

If `Gamma_12` is represented by an independent gauge basis matrix `G` whose
columns are basis vectors in row-major overlap coordinates, and
`W = diag(w_12)`, then

```text
P_Gamma = G (G^T W G)^(-1) G^T W.
```

All exact artifacts for this note use `fractions.Fraction`, not floating point
arithmetic.

## Core Compatibility Theorem

For fixed finite data and fixed declared gauge `Gamma_12`,

```text
Delta^2_12(s_1,s_2; Gamma_12) = 0
```

if and only if

```text
rho_1 s_1 - rho_2 s_2 in Gamma_12.
```

Equivalently, the two local sections are compatible on the overlap modulo the
declared overlap gauge.

Proof: Let `m = m_12(s_1,s_2)`. In a finite-dimensional positive-definite
weighted Hilbert space there is a unique orthogonal decomposition

```text
m = P_Gamma m + (I - P_Gamma)m
```

with `P_Gamma m in Gamma_12` and `(I - P_Gamma)m` orthogonal to `Gamma_12`.
Therefore the closest vector in `Gamma_12` is `P_Gamma m`, and the squared
distance to `Gamma_12` is `||(I - P_Gamma)m||^2_w`. This distance is zero if
and only if `(I - P_Gamma)m = 0`, equivalently `m in Gamma_12`.

## Conditional Realized-Gauge Corollary

The core theorem is a quotient-overlap statement. It does not, by itself,
assert the existence or nonexistence of realized gauge-adjusted local sections.

To make that stronger semantic statement, add local gauge parameter spaces
`G_1`, `G_2` and overlap transfer maps

```text
lambda_1 : G_1 -> V_12
lambda_2 : G_2 -> V_12
```

with the declared overlap gauge realized as

```text
Gamma_12 = im(lambda_1) - im(lambda_2).
```

Under this additional data, there exist gauge parameters `g_1, g_2` such that

```text
rho_1 s_1 - lambda_1 g_1 = rho_2 s_2 - lambda_2 g_2
```

if and only if `Delta^2_12(s_1,s_2; Gamma_12)=0`. Thus `Delta^2_12>0` excludes
realized-gauge pasting only under this realized-gauge hypothesis. Without this
extra data, the safe claim is only failure of compatibility modulo the declared
overlap gauge.

## Gauge Monotonicity

If

```text
Gamma_12 subset Gamma'_12,
```

then

```text
Delta^2_12(s_1,s_2; Gamma'_12)
  <= Delta^2_12(s_1,s_2; Gamma_12).
```

Proof: the minimum over a larger subspace cannot be larger. Hence every
obstruction is relative to the declared gauge. If an enlarged gauge absorbs the
mismatch, the original obstruction was only an obstruction relative to the
narrower declared gauge.

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
  one = (1,1,1,1),
  q   = (-1,-1,1,1),
  b   = (-1,1,-1,1)
}.
```

Positive control:

```text
m_plus = (1, 2, 3/2, 5/2)
       = (7/4) one + (1/4) q + (1/2) b.
```

Therefore `m_plus in Gamma` and `Delta^2(m_plus; Gamma)=0`.

Negative control:

```text
m_minus = (1, -1, -1, 1).
```

Under the uniform weighted inner product,

```text
<m_minus, one>_w = 0
<m_minus, q>_w   = 0
<m_minus, b>_w   = 0.
```

Therefore `(I-P_Gamma)m_minus = m_minus` and

```text
Delta^2(m_minus; Gamma) = ||m_minus||^2_w = 1.
```

Enlarged-gauge monotonicity control:

```text
Gamma' = span{one, q, b, m_minus}.
```

Then `Delta^2(m_minus; Gamma')=0 <= 1=Delta^2(m_minus; Gamma)`.

The exact script and certificate are:

```text
scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py
docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json
docs/infra/debranded_residual_transport/EXACT_GQ_FCR_V1_5_20260706.md
```

## Relation To v1.3/v1.4 Order Defect

The v1.3/v1.4 order-defect spine concerns same-carrier weighted projections
and order-dependent stripping artifacts. This v1.5 object concerns two local
sections and their overlap mismatch modulo a declared gauge.

The relation is adjacency, not identity:

- v1.3/v1.4: same-carrier order defect under finite weighted projection
  procedures;
- v1.5: two-chart overlap mismatch after quotienting declared overlap gauge.

Both enforce the same discipline: do not promote raw mismatch before removing
declared nuisance structure. But v1.5 does not prove the v1.3 product-weight
theorem, does not state a new projection theorem, and does not broaden the
existing order-defect result.

## Claim Boundary

Authorized:

```text
Given finite carriers, rational restriction maps, positive rational overlap
weights, and a declared overlap gauge subspace, Delta^2 is the exact squared
weighted distance of the overlap mismatch to that declared gauge. In the 2x2
uniform additive-gauge controls, m_plus has Delta^2=0 and m_minus has
Delta^2=1 by exact rational arithmetic.
```

Not authorized:

```text
broad sheaf theory
broad consistency-radius theory
broad contextuality theory
broad dependent-input ANOVA theory
broad noncommuting projection theory
MaoField empirical positive result
observed residual/transport/holonomy/gluing field
full panel / training / inference / new loss
paper-ready, peer-reviewed, arXiv, or journal status
proof by JSON floats or deterministic harness
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```
