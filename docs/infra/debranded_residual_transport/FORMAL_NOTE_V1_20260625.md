# Finite Weighted Residual Transport — Formal Note v1

Date: 2026-06-25 CST

Status: Mode A mathematical note. This is not a MaoField empirical result.

Source workplan:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_WORKPLAN_20260625.md
docs/infra/gpt_deep_research/FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_ADOPTION_NOTE_20260625.md
```

## 0. Boundary

This note formalizes a finite-dimensional operator package. It does not
promote MaoField empirical claims.

Blocked:

- no full MaoField panel has run;
- no 16-cell aggregate exists;
- no residual, interaction, quotient-residual, transport, or holonomy field has
  been observed in MaoField data;
- no LOSO, F3, glass-box, training, checkpoint-loading, model-inference, or
  new-loss claim is authorized;
- external references in GPT/Pro reports remain unverified until a separate
  node36 literature pass.

Allowed ceiling:

```text
definitions_and_harness_viable_only
```

The note can succeed by producing definitions, lemmas, counterexamples, and
kill gates. It does not need a positive MaoField empirical result.

## 1. Algebraic Setting

All vector spaces in this note are real and finite-dimensional.

An admissible finite weighted system is a triple

```text
A = (X, w, N)
```

where:

- `X` is finite;
- `w: X -> R_{>0}` is fixed before reading outcomes;
- `H = L^2(X,w)` is the real vector space of functions `X -> R`;
- `<f,g>_w = sum_{x in X} w(x) f(x) g(x)`;
- `N <= H` is a pre-outcome nuisance subspace.

For a chosen ordering of `X`, let `W = diag(w)`. If the columns of a matrix
`A_N` span `N`, define

```text
Q_N = A_N (A_N^T W A_N)^+ A_N^T W
P_N = I - Q_N
```

where `+` is the Moore-Penrose inverse. Rank-deficient column lists are allowed.

### Lemma 1. Weighted Projection

`Q_N` is the weighted orthogonal projection onto `N`: it is idempotent, its
range is `N`, and it is self-adjoint for the weighted inner product:

```text
Q_N^2 = Q_N
<Q_N f, g>_w = <f, Q_N g>_w.
```

Consequently, `P_N` is the weighted orthogonal projection onto
`N^{perp,w}`.

Proof sketch. Let `B = W^{1/2} A_N`. The Euclidean orthogonal projection onto
`col(B)` is `Pi_B = B (B^T B)^+ B^T`. Then

```text
Q_N = W^{-1/2} Pi_B W^{1/2}.
```

Idempotence and weighted self-adjointness follow from the ordinary projection
properties of `Pi_B`.

### Lemma 2. Quotient Representative

For `K in H`, the vector

```text
R(K) = P_N K
```

is the unique element of `(K + N) cap N^{perp,w}` and the minimum-norm
representative of the coset `K + N`:

```text
P_N K = argmin_{h in K+N} ||h||_w.
```

Equivalently, the nuisance correction is

```text
-Q_N K = argmin_{n in N} ||K + n||_w,
```

and `K + (-Q_N K) = P_N K`.

Proof sketch. Since `P_N K - K = -Q_N K in N`, `P_N K` lies in `K + N`. For
any `n in N`,

```text
K + n = P_N K + (Q_N K + n)
```

with the two terms weighted-orthogonal. The norm is minimized by choosing
`n = -Q_N K`.

## 2. Source-Fixed Nuisance

A nuisance specification is source-fixed when there is pre-outcome metadata
`M` and a registered rule `F` such that

```text
N = F(M)
```

where `M` may include axes, weights, declared templates, constants, main
effects, registered slopes, smooth trend templates, matched mean/slope
templates, and registered transport structure.

Invalid: choosing any of the following after seeing the outcome signal `K`:

```text
axes
weights
dimension d = dim(N)
templates
hyperparameters
subspace basis
transport maps
thresholds
```

When post-outcome tuning happens, the object may still be a diagnostic, but it
is not an admissible residual claim.

### Lemma 3. Outcome-Derived Nuisance Vacuity

If `K != 0` and `N` may be chosen after observing `K`, then choosing

```text
N = span(K)
```

makes `P_N K = 0`. More generally, for finitely many signals
`K_1, ..., K_m`, choosing `N = span(K_1, ..., K_m)` kills every residual.

Therefore any claim based on an outcome-derived nuisance subspace is invalid
unless it is explicitly labeled as post-selection diagnostics.

## 3. Transport Systems

A finite residual transport system consists of:

- a finite directed graph `G`;
- an admissible system `(X_s, w_s, N_s)` at each vertex `s`;
- a fixed linear map `C_rho: H_s -> H_t` for each edge `rho: s -> t`.

The map `C_rho` must be fixed before outcomes. Algebraically it need only be
linear. If weighted adjoints are used, the adjoint is

```text
C_rho^* = W_s^{-1} C_rho^T W_t.
```

Coarsening maps, pullbacks, and adjoints must be declared separately; do not
hide empirical axis choices inside the word "transport."

For an edge `rho: s -> t`, define the edge operator and its application to a
signal:

```text
E_rho = C_rho P_s - P_t C_rho
D_rho(K_s) = E_rho K_s
```

Here `P_s = Pi_{N_s^{perp,w_s}}` and `P_t = Pi_{N_t^{perp,w_t}}`.

### Lemma 4. Edge Commutation

For `rho: s -> t`,

```text
C_rho P_s = P_t C_rho
```

if and only if

```text
C_rho(N_s) <= N_t
C_rho(N_s^{perp,w_s}) <= N_t^{perp,w_t}.
```

Proof sketch. If the operator identity holds, apply it to `n in N_s` and to
`r in N_s^{perp,w_s}`. Conversely, decompose every `h in H_s` as `h = n + r`;
the two inclusions make both sides equal to `C_rho r`.

Boundary. A nonzero `D_rho(K)` is not a discovery by itself. It first says the
registered nuisance family and the registered transport do not commute.

## 4. Path Transport And Holonomy No-Go

For a path

```text
p: s_0 --rho_1--> s_1 --rho_2--> ... --rho_m--> s_m
```

define raw and projected path transports:

```text
C_p = C_{rho_m} ... C_{rho_1}
Chat_p = P_{s_m} C_{rho_m} P_{s_{m-1}} ... P_{s_1} C_{rho_1} P_{s_0}
```

For two paths `p,q: s -> t`, define the terminal-space holonomy operator:

```text
Omega_{p,q} = Chat_p - Chat_q
H_{p,q}(K) = Omega_{p,q} K.
```

### Lemma 5. Path Reduction

If every edge on `p` satisfies `C_rho P_u = P_v C_rho`, then

```text
Chat_p = P_t C_p P_s.
```

Proof sketch. Move each projection across the next edge by edge commutation
and use `P_u^2 = P_u`.

### Lemma 6. Square Holonomy No-Go

If `p,q: s -> t`, every edge on both paths commutes with endpoint projections,
and the raw path transports agree,

```text
C_p = C_q,
```

then

```text
Omega_{p,q} = 0
H_{p,q}(K) = 0 for all K.
```

Boundary. If raw paths already differ, a nonzero terminal difference is not
evidence of a projection or nuisance obstruction. It may be only raw transport
non-functoriality.

## 5. Invariance Under Transport Isomorphism

Two transport systems are isomorphic if each vertex has a weighted isometry

```text
U_s: H_s -> H'_s
```

such that

```text
<U_s f, U_s g>_{w'_s} = <f,g>_{w_s}
```

and

```text
U_s N_s = N'_s
U_t C_rho = C'_rho U_s
```

for each edge `rho: s -> t`.

Under such an isomorphism:

- residual norms are preserved;
- singular spectra of consistently transported residual stacks are preserved;
- edge-defect norms are preserved;
- square-holonomy norms are preserved;
- principal angles between named residual subspaces are preserved.

These are invariants only under this stated equivalence. Without the isometry
and commuting diagram, call them diagnostics, not invariants.

## 6. Rank-1 Shadow Guard

Let residual vectors be represented in a common weighted residual Hilbert space
and stacked as rows after the declared whitening or normalization. If the stack
has rank one, then all across-condition variation is only scalar brightness
along one template:

```text
r_i = a_i v.
```

The template `v` may itself be internally non-scalar, but the family
`{r_i}` has no multidirectional structure.

The current design-review floor

```text
sigma_2 / sigma_1 >= 0.25
```

is not a theorem and not a canonical mathematical constant. It is only a
fail-closed guardrail for deciding whether a synthetic or future empirical
artifact is worth the next review stage.

## 7. Random Subspace Guard

A named residual subspace must beat random same-dimensional subspaces in the
same weighted residual Hilbert space.

The null must be generated after whitening and after restriction to
`N^{perp,w}`. One admissible construction:

1. choose an orthonormal basis of `N^{perp,w}`;
2. sample a Gaussian matrix in that coordinate system;
3. orthonormalize it to obtain a random `k`-plane;
4. compare capture, projection norm, or angle statistics against the named
   subspace.

If the named subspace is indistinguishable from this random null, it has no
coordinate-invariant content.

## 8. Gluing Absorption Guard

Use finite language unless a full sheaf object is explicitly defined.

Let `{U_i}` be a finite cover of a finite table, with registered restriction
maps to overlaps `U_ij`. Let local residual sections be `r_i`, and define the
overlap mismatch

```text
m_ij = r_i|_{U_ij} - r_j|_{U_ij}.
```

Let `N_ij` be the allowed nuisance subspace on the overlap and `P_ij` the
weighted projection away from it.

If

```text
P_ij m_ij = 0
```

then the mismatch is absorbed by allowed nuisance and is not a gluing
obstruction. A candidate obstruction requires nonzero residual mismatch after
registered nuisance removal, with a predeclared normalized threshold.

## 9. Product-Weight Boundary

Classical product-measure Hoeffding or functional-ANOVA language is allowed
only under an explicitly product reference weight:

```text
w(x_1,...,x_d) = product_j w_j(x_j).
```

For non-product weights, the correct default language is:

```text
non-product weighted hierarchical projection / residual program
```

Product-reweighted Hoeffding analysis is a different `L^2` geometry from the
observed weighted residual object.

### Counterexample. Non-Product Projection Is Not Product Hoeffding

Use a `2 x 2` table ordered as `(0,0),(0,1),(1,0),(1,1)`.

Observed non-product weights:

```text
w_obs = [1, 2, 3, 5]
```

The row marginals are `[3,8]`, the column marginals are `[4,7]`, and the
same-total product reference is:

```text
w_prod = [12/11, 21/11, 32/11, 56/11]
```

Take signal:

```text
K = [0, 1, 2, 6].
```

Project away the additive nuisance span:

```text
N = span{1, row_main_effect, col_main_effect}.
```

The weighted additive residuals are:

```text
R_obs  = [ 1.475409836066, -0.737704918033, -0.491803278689,  0.295081967213]
R_prod = [ 1.388429752066, -0.793388429752, -0.520661157025,  0.297520661157]
```

Difference:

```text
R_obs - R_prod = [0.086980083999, 0.055683511719, 0.028857878336, -0.002438693944]
max_abs_diff = 0.086980083999
observed_weight_norm_diff = 0.127651515989
```

Therefore the observed weighted projection residual is not identical to the
product-reference Hoeffding residual, even when the product reference uses the
same row and column marginals.

## 10. Kill Gates For Future Artifacts

Before any future artifact can move beyond formal design, all choices below
must be source-fixed:

```text
axes
weights
nuisance basis
transport maps
thresholds
random seeds
rank floor
holdout scheme
```

Fail-closed gates:

- exact product-weight equality control;
- outcome-derived nuisance invalidation;
- transport-stable multidirectional positive control;
- raw-path-equality square control;
- random equal-cell-count axes;
- within-axis shuffle;
- bad-axis label control;
- random same-dimensional subspace null;
- rank-1 plus noise-floor trap;
- gluing absorption check;
- product-reweighting separation;
- coarsening non-naturality trap.

Allowed verdicts remain:

```text
invalid_artifact
killed_by_rank1_shadow
killed_by_random_axis
killed_by_coarsening
killed_by_gluing_absorption
insufficient_artifact
definitions_and_harness_viable_only
eligible_for_next_design_review_only
```

Forbidden verdicts remain:

```text
observed_field
glass_box_broken
training_authorized
new_loss_authorized
```

## 11. What v1 Adds Over v0

v1 tightens v0 in five ways:

1. projection and quotient statements are written as finite Hilbert-space
   lemmas;
2. nuisance admissibility is formalized as a source-fixed rule;
3. edge and path holonomy no-go statements have explicit quantifiers;
4. rank, random-subspace, and gluing language is separated from discovery
   language;
5. the product-weight boundary has an explicit finite counterexample.

This completes a formal-note pass only. It does not change MaoField empirical
status.
