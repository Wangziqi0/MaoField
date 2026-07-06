# Finite Audit-Order Instability on Additive Nuisance

Date: 2026-07-06 CST

Status: bounded Mode A corollary companion to v1.3. This is not a MaoField
empirical result and does not patch the current Zenodo V2.5 preprint.

Source decision:

```text
docs/infra/gpt_deep_research/deep_research_oi_corollary_companion_report32_20260706.md
docs/infra/gpt_deep_research/OI_COROLLARY_COMPANION_REPORT32_ADOPTION_NOTE_20260706.md
```

Primary proof source:

```text
FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
```

## 0. Boundary

This companion records one finite-dimensional corollary:

```text
OI^{op}_{N_add}(w) = 0 iff w is product form
```

It does not introduce a broad ANOVA, dependent-input, projection, sheaf,
contextuality, consistency-radius, or dynamic-collapse theory. It does not
observe any residual, interaction, transport, holonomy, or gluing field in
MaoField data. Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## 1. Setting

Let `Q` and `B` be finite sets, let `X = Q x B`, and let `w(q,b)>0` with

```text
sum_{q,b} w(q,b) = 1.
```

Use the weighted inner product

```text
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b).
```

As in v1.3, define

```text
C  = span{1}
A  = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

and the ordered stripping maps

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q.
```

The v1.3 note proves equivalently that

```text
D_w = P_B0 P_A - P_A P_B0.
```

## 2. Restricted Audit-Order Instability

Define the restricted operator quantity

```text
OI^{op}_{N_add}(w)
  = || D_w restricted to N_add ||_(N_add, ||.||_w) -> L2(w).
```

This measures the maximum order-dependent sequential-stripping output that can
be generated from signals that live in the additive nuisance space. It does not
measure true interaction residual size.

## 3. Corollary

For finite positive weights on `Q x B`,

```text
OI^{op}_{N_add}(w) = 0 iff w(q,b) = w_Q(q) w_B(b) for all q,b.
```

Equivalently, the restricted audit-order instability on additive nuisance
vanishes exactly in the product-weight case.

## 4. Proof

Assume first that `w` is product form. By v1.3 Proposition 2,

```text
D_w = 0
R_Q_then_B = R_B_then_Q = I - P_N.
```

Therefore the restriction of `D_w` to `N_add` is also the zero map, so

```text
OI^{op}_{N_add}(w) = 0.
```

Conversely, assume

```text
OI^{op}_{N_add}(w) = 0.
```

Since the space is finite-dimensional, this means `D_w K = 0` for every
`K in N_add`. Suppose for contradiction that `w` is not product form. By v1.3
Proposition 3, there exists a pure main-effect witness `K in A` or `K in B0`
such that:

```text
K in N_add
(I - P_N)K = 0
one ordered stripping residual is zero
the opposite ordered stripping residual is nonzero.
```

Hence

```text
D_w K = R_Q_then_B K - R_B_then_Q K != 0,
```

contradicting the zero restricted operator assumption. Therefore `w` must be
product form.

The implication from non-product weights is existential: it only says that at
least one additive-nuisance witness has nonzero order defect. It does not say
that every input is order-sensitive.

## 5. Artifact Guard

For the witness supplied by v1.3 Proposition 3, the true additive residual is
zero:

```text
(I - P_N)K = 0.
```

The nonzero wrong-order output is therefore a sequential stripping artifact,
not a true interaction residual.

The v1.4 exact rational witness and deterministic harness may illustrate the
phenomenon, but they are not proof authority for this corollary. The proof
authority is the analytic v1.3 proposition chain plus elementary
finite-dimensional operator facts.

## 6. Forbidden Upgrades

Do not use this corollary to claim:

- MaoField empirical positive results;
- full panel, checkpoint loading, inference, training, or new loss;
- observed residual, interaction, transport, holonomy, or gluing field;
- F3 positive, LOSO passed, or glass-box success;
- broad new ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof by deterministic harness or JSON floats;
- paper-ready, peer-reviewed, arXiv-submitted, or journal-submitted status.
