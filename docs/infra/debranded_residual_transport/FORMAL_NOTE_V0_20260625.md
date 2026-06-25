# Finite Weighted Residual Transport — Formal Note v0

Date: 2026-06-25 CST

Status: first debranded formal note. This is not a MaoField empirical result.

## 0. Boundary

This note starts the new mathematics direction while staying inside the
MaoField repository. The boundary is strict:

- no full MaoField panel has run;
- no 16-cell aggregate exists;
- no residual, interaction, quotient-residual, transport, or holonomy field has
  been observed in MaoField data;
- no LOSO, F3, glass-box, training, or new-loss claim is authorized;
- MaoField remains a negative-centered empirical pilot and measurement-audit
  case.

The object below can produce a definition, a counterexample, or a no-go theorem
without producing a positive MaoField empirical claim.

## 1. Finite Weighted Systems

An admissible finite weighted system is a triple

```text
(X, w, N)
```

where:

- `X` is a finite set;
- `w: X -> R_{>0}` is a positive weight;
- `H = L^2(X,w)` has inner product
  `<f,g>_w = sum_{x in X} w(x) f(x) g(x)`;
- `N <= H` is a pre-outcome nuisance subspace.

If a matrix `A` has columns spanning `N`, the weighted projection onto `N` is

```text
Q_N = A (A^T W A)^+ A^T W
```

where `W = diag(w)` and `+` is the Moore-Penrose inverse. The residual
projection is

```text
P_N = I - Q_N.
```

For a signal `K in H`, define the local residual

```text
R(K) = P_N K.
```

`R(K)` is the minimum-norm representative of the quotient class `K + N`.

## 2. Scale Graphs And Transport

A residual transport system consists of:

- a finite directed scale graph `G`;
- an admissible system `(X_s,w_s,N_s)` at every vertex `s`;
- a fixed linear map `C_rho: H_s -> H_t` at every edge `rho: s -> t`.

Each `C_rho` must be fixed before reading outcomes. Typical examples are
weighted block averages, pullbacks, or explicitly registered adjoints.

For an edge `rho: s -> t`, define the edge defect

```text
D_rho(K_s) = C_rho P_s K_s - P_t C_rho K_s.
```

It is exactly the commutator between nuisance removal and scale transport.

## 3. Edge No-Go Lemma

For one edge `rho: s -> t`, the identity

```text
C_rho P_s = P_t C_rho
```

holds if and only if both subspace conditions hold:

```text
C_rho(N_s) <= N_t
C_rho(N_s^perp) <= N_t^perp.
```

Proof sketch: apply the operator identity to vectors in `N_s` and
`N_s^perp`; conversely decompose any vector as `n+r` and use the two inclusions.

Therefore a stable nonzero edge defect is not automatically a discovery. It
first means the chosen nuisance family and transport map do not form a natural
quotient operation.

## 4. Square Holonomy No-Go

For a square with two paths from `s0` to `s2`, define projected path operators

```text
T_A = P_2 C_b P_a C_a P_0
T_B = P_2 C_d P_c C_c P_0
```

and define

```text
H_square(K) = T_A K - T_B K.
```

If every edge on the square commutes with its endpoint projections and the raw
transport maps have the same terminal composition, then

```text
H_square(K) = 0 for all K.
```

Thus square holonomy is a path-dependence obstruction only after raw transport,
projection choices, and nuisance subspaces have all been fixed. It is not a
name for any arbitrary discrepancy.

## 5. Rank-1 Shadow No-Go

Let residual vectors from multiple conditions be stacked as rows of a matrix
`M`. If

```text
rank(M) = 1
```

then every residual is only a scalar multiple of one template. Principal-angle
stability or transport stability is then a one-template brightness path, not a
non-scalar structure. Current design-review floor:

```text
sigma_2 / sigma_1 >= 0.25
```

This floor is a guardrail, not a positive discovery threshold.

## 6. Random Subspace Guard

A named residual subspace must beat random same-dimensional subspaces inside
the same weighted residual Hilbert space. Otherwise it has no coordinate-free
content and should be treated as a coordinate choice.

The guard must use the same ambient residual dimension, the same weight, and a
fixed random seed recorded in the result artifact.

## 7. Gluing Absorption Guard

Local residual models can fail to agree on overlaps. Let `m` be the mismatch on
an overlap and let `N_overlap` be the allowed local nuisance there.

- If `P_{N_overlap} m = 0`, the mismatch is fully absorbed by nuisance and is
  not a gluing obstruction.
- If `P_{N_overlap} m` remains large, the mismatch is a candidate local-global
  obstruction.

This prevents ordinary nuisance mismatch from being renamed as sheaf-theoretic
content.

## 8. Product-Weight Boundary

Classical product-measure Hoeffding / functional ANOVA language is legal only
when the reference weight is explicitly product-form:

```text
w(x_1,...,x_d) = product_j w_j(x_j).
```

For a positive non-product weight, weighted orthogonal projection still exists,
but the legal phrase is:

```text
non-product weighted hierarchical projection / residual program
```

Current q4 x tokenpos4 material is non-product weighted. This note therefore
uses projection language by default.

## 9. First Formal Start

The v0 deliverable is intentionally modest:

1. define the operator package cleanly;
2. run a seven-block toy harness with positive and negative controls;
3. allow only `definitions_and_harness_viable_only`;
4. keep MaoField empirical claims blocked until future primary artifacts exist.

The companion harness is:

```text
scripts/debranded_residual_transport_harness.py
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V0_20260625.md
```
