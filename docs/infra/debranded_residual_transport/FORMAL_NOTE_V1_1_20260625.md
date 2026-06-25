# Finite Weighted Residual Transport — Formal Note v1.1

Date: 2026-06-25 CST

Status: Mode A mathematical patch note. This is not a MaoField empirical
result.

Source workplan and audit:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_WORKPLAN_20260625.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md
```

## 0. Boundary

This note patches Formal Note v1. It keeps the same evidence boundary:

- no full MaoField panel has run;
- no 16-cell aggregate exists;
- no residual, interaction, quotient-residual, transport, or holonomy field has
  been observed in MaoField data;
- no LOSO, F3, glass-box, checkpoint-loading, model-inference, training, or
  new-loss claim is authorized;
- every example below is finite, synthetic, and zero-GPU.

Allowed ceiling:

```text
definitions_and_harness_viable_only
```

## 1. Quotient Descent

Let `(H_s,N_s)` and `(H_t,N_t)` be finite real vector spaces with nuisance
subspaces. A linear map `C:H_s -> H_t` descends to the quotient if

```text
bar C([h]) = [C h]
```

is well-defined as a map

```text
H_s / N_s -> H_t / N_t.
```

### Proposition 1. Quotient Descent Criterion

`C` descends to `bar C` if and only if

```text
C(N_s) <= N_t.
```

Proof. If `h` and `h+n` represent the same source coset, then well-definedness
requires `C(h+n)-Ch = Cn` to lie in `N_t` for every `n in N_s`. Conversely, if
`C(N_s) <= N_t`, replacing `h` by `h+n` changes `Ch` only by an element of
`N_t`, so the target coset is unchanged.

This is weaker than residual-representative naturality. With weighted
orthogonal residual projections `P_s` and `P_t`, the stronger condition is

```text
C P_s = P_t C.
```

Quotient descent says the coset map exists. Residual naturality says the
chosen minimum-norm representatives are compatible with `C`.

## 2. Projection-Evolution Commutator

Let `(H,w,N)` be one finite weighted Hilbert space. Let `Q` be the weighted
orthogonal projection onto `N`, and let

```text
P = I - Q
```

be the projection onto `N^{perp,w}`. For a source-fixed linear operator
`T:H -> H`, define

```text
[P,T] = P T - T P.
```

### Proposition 2. Commutator Criterion

The following are equivalent:

```text
P T = T P
```

and

```text
T(N) <= N
T(N^{perp,w}) <= N^{perp,w}.
```

Equivalently, using the weighted adjoint `T^{*,w}`,

```text
T(N) <= N
T^{*,w}(N) <= N.
```

Proof. If `PT=TP`, then for `n in N`, `Pn=0`, so `P T n = T P n = 0`; hence
`Tn in N`. For `r in N^{perp,w}`, `Pr=r`, so `PTr=TPr=Tr`; hence
`Tr in N^{perp,w}`. Conversely, decompose any `h=n+r`. If both subspaces are
invariant, both `PT` and `TP` return `Tr`. The adjoint form is equivalent
because `T(N^{perp,w}) <= N^{perp,w}` iff `<Tr,n>_w=0` for all `r in N^perp`
and `n in N`, iff `<r,T^{*,w}n>_w=0` for all such `r`, iff `T^{*,w}N <= N`.

Interpretation. A nonzero commutator is an operator leakage diagnostic. It is
not by itself an observed field, a glass-box result, or a training signal.

## 3. Square Holonomy Decomposition

For a path `p:s -> t`, let raw transport be `C_p` and projected path transport
be `Chat_p` as in Formal Note v1. Define the path projection defect

```text
Delta_p = Chat_p - P_t C_p P_s.
```

For two paths `p,q:s -> t`, the projected square holonomy decomposes exactly as

```text
Omega_{p,q}
= Chat_p - Chat_q
= P_t (C_p - C_q) P_s + Delta_p - Delta_q.
```

Thus every nonzero square holonomy has at least one of these sources:

1. raw path mismatch: `C_p != C_q`;
2. projection/transport non-naturality along `p`;
3. projection/transport non-naturality along `q`.

Formal Note v1's no-go is the special case where all three terms vanish. This
decomposition prevents a raw transport mismatch from being mislabeled as a
projection or nuisance obstruction.

## 4. Common Ambient Space For Invariants

Residual vectors at different vertices do not automatically live in one vector
space. Before using singular values, principal angles, or named residual
subspaces across vertices, choose one of:

1. a base vertex and registered transports into that base vertex;
2. a weighted direct sum `oplus_s H_s`;
3. a declared common coordinate space with weighted isometries from each
   vertex.

Only after this choice are the following meaningful:

- residual-stack singular spectra;
- principal angles between named subspaces;
- edge-defect norms across multiple edges;
- square-holonomy norms across comparable squares.

Without a registered common ambient construction, these are diagnostics, not
invariants.

## 5. Random Subspace Null

After whitening `N^{perp,w}`, let the residual space be `R^d`. For a fixed unit
vector `u` and a uniformly random `k`-plane `S`, the squared capture

```text
||Pi_S u||^2
```

has distribution

```text
Beta(k/2, (d-k)/2).
```

This is the analytic null for one fixed vector. Finite harnesses may still use
Monte Carlo quantiles when they avoid extra dependencies, but they must record:

- residual-space dimension `d`;
- random-plane dimension `k`;
- draw count;
- discarded degenerate draws;
- calibration statistic and threshold.

Failure to beat this null only means the named subspace has not beaten the
registered statistic. It does not prove absolute absence of all possible
structure.

## 6. Rank-1 Shadow Perturbation

Let a residual stack be

```text
M = a v^T + E.
```

The first term has rank at most one. By Weyl's singular-value inequality,

```text
sigma_2(M) <= ||E||_2.
```

Therefore a small second singular value can be explained by a near-rank-1
template plus perturbation. The current review floor

```text
sigma_2 / sigma_1 >= 0.25
```

remains a source-fixed design-review guard, not a theorem and not a universal
constant.

## 7. Finite Gluing Complex

Use finite overlap language unless a full sheaf object has been defined.

For three charts `U_1,U_2,U_3`, let pairwise overlap mismatches be

```text
m_12, m_23, m_31.
```

Let `P_ij` remove registered nuisance on pairwise overlaps. Pairwise absorption

```text
P_ij m_ij = 0
```

only says the pairwise mismatch is killed locally. A three-overlap obstruction
requires a registered cycle/cocycle check, for example a residualized cycle

```text
P_123 (m_12 + m_23 + m_31) != 0
```

under a predeclared threshold. Pairwise nonzero mismatch is not sufficient for
sheaf language, and pairwise absorption is not a full gluing theorem.

## 8. Product-Weight Equivalence Boundary

If the weight is exact product form

```text
w(q,b) = w_Q(q) w_B(b)
```

and `N` is the additive main-effect subspace

```text
span{1, q-main effects, b-main effects},
```

then the weighted residual `P_N K` is exactly the product-measure two-factor
Hoeffding interaction component of `K`.

If the observed weight is not exact product form, the object is instead a
non-product weighted projection residual. Product-reweighted Hoeffding lives in
a different `L^2` geometry. Formal Note v1's `2 x 2` counterexample remains
the guardrail.

## 9. v1.1 Harness Contract

The v1.1 synthetic harness must be treated as a fail-closed contract:

- script: `scripts/debranded_residual_transport_harness_v1_1.py`;
- JSON: `docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json`;
- summary: `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md`.

Required additions over v1:

1. standalone bad-edge defect control;
2. standalone projection-evolution commutator obstruction control;
3. tougher random-subspace heldout not lying exactly in the named true
   subspace;
4. within-axis shuffle null distribution, not one shuffle;
5. finite three-overlap gluing/cocycle toy check;
6. JSON threshold contract;
7. JSON environment metadata;
8. discarded random draw counts.

Passing this harness supports only:

```text
definitions_and_harness_viable_only
```

It does not observe a MaoField field and does not authorize training, model
inference, checkpoint loading, a full panel, or a new loss.

## 10. What v1.1 Adds Over v1

v1.1 patches the exact holes identified by report (26):

1. quotient descent is separated from residual-representative naturality;
2. `[P,T]` is promoted to an explicit finite-dimensional theorem;
3. square holonomy is decomposed into raw path mismatch and path projection
   defects;
4. invariants require a common ambient space;
5. random-subspace language gets an analytic null plus recorded fallback;
6. rank-shadow language gets a perturbation bound;
7. gluing language gets a finite three-overlap/cocycle screen;
8. the harness records thresholds and environment instead of hiding gates only
   in Python source.

This is a formal patch only. It does not change MaoField empirical status.
