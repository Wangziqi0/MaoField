# Debranded Residual Transport / Holonomy — First Formal Note Outline

Date: 2026-06-25 CST

This outline is the local D625 landing of GPT/Pro report (25). It is not a
MaoField evidence upgrade. It is a formal-note scaffold for the debranded
finite weighted residual transport / holonomy / operator no-go project.

## 0. Boundary

The note must begin with the negative boundary:

- MaoField remains a negative-centered empirical pilot and measurement-audit
  case.
- No full panel has run.
- No 16-cell aggregate exists.
- No residual, interaction, quotient-residual, transport, or holonomy field
  has been observed.
- No LOSO / F3 / glass-box / training / new-loss claim is authorized.

The mathematical project can succeed without a positive MaoField empirical
result.

## 1. Admissible Systems

For each finite scale `s`, define an admissible triple:

```text
(X_s, w_s, N_s)
```

where:

- `X_s` is a finite table;
- `w_s(x) > 0` is a fixed positive weight;
- `H_s = L^2(X_s, w_s)`;
- `N_s` is a pre-outcome, outcome-independent nuisance subspace;
- `P_s = Pi_{N_s_perp,w_s}` is the weighted orthogonal projection.

The nuisance subspace may include constants, main effects, registered slopes,
registered smooth trends, matched mean/slope templates, and coarse-scale
pullbacks. It may not include outcome-derived directions.

## 2. Local Residuals

For a signal `K_s in H_s`, define:

```text
R_s(K) = P_s K_s
```

`R_s(K)` is the minimum-norm representative of the quotient class of `K_s`
modulo `N_s`.

## 3. Transport Maps

For a coarsening/refinement edge `rho: s -> s'`, define a fixed linear map:

```text
C_rho: H_s -> H_s'
```

Typical choices should be weighted block averages or their explicitly defined
weighted adjoints / pullbacks. The map must be fixed before outcomes are read.

The edge defect is:

```text
D_rho(K) = C_rho P_s K_s - P_s' C_rho K_s
```

It measures the failure of nuisance removal to commute with scale transport.

## 4. Square Holonomy

For a scale square with two paths from `s0` to `s2`, define:

```text
H_square(K) = path_A(K) - path_B(K)
```

where each path is a composition of fixed transport maps and fixed projections.
The defect lives in the terminal Hilbert space. It is a path-dependence test,
not a claim of an observed MaoField field.

## 5. Equivalence

Use two equivalence layers:

1. Nuisance-gauge equivalence:
   `K_s - K_s' in N_s` at each scale.

2. Transport-isomorphism equivalence:
   weighted isometries `U_s` satisfying:

```text
U_s N_s = N_tilde_s
U_s' C_rho = C_tilde_rho U_s
```

Only invariants under these equivalences should be used as project claims.

## 6. Invariants

Candidate invariants:

- residual norm profiles;
- stacked-residual singular spectra;
- principal-angle profiles;
- edge-defect norms;
- square-holonomy norms;
- random same-dimensional subspace capture quantiles;
- transport-stable rank.

## 7. Product-Weight Boundary

Classical product-measure Hoeffding / functional ANOVA language is allowed only
when the reference weight is explicitly product-form:

```text
w(x_1,...,x_d) = product_j w_j(x_j)
```

For current q4 x tokenpos4 material, node36 already verified non-product
weights. Therefore the current legal language is:

```text
non-product weighted hierarchical projection / residual program
```

unless a future exact product measure or explicit product reweighting is
introduced and clearly labeled as a different reference geometry.

## 8. Theorem / No-Go Targets

1. Rank-1 shadow vacuity:
   if stacked residuals have rank 1, apparent stability is only a scalar
   brightness path along one template.

2. Random same-dimensional subspace indistinguishability:
   if a named residual subspace does not beat the random Grassmann control, it
   has no coordinate-invariant content.

3. Coarsening/projection commutation:
   characterize when `C_rho P_s = P_s' C_rho`.

4. Square-holonomy no-go:
   if all edge commutators vanish around a compatible square, holonomy must
   vanish.

5. Projection/evolution commutator leakage:
   characterize when `[P,T]` is zero or represents nuisance/residual leakage.

6. Gluing absorption no-go:
   if overlap mismatch can be absorbed by allowed local nuisance expansion, it
   is not a gluing obstruction.

7. Non-product-weight counterexample:
   construct a positive non-product weight table where weighted projection
   residual differs from product-reference Hoeffding interaction.

## 9. Seven-Block Synthetic Harness

The next zero-GPU harness should use small finite matrices and include:

- non-product weighted projection;
- edge defect;
- square holonomy;
- rank-shadow guard;
- random-subspace guard;
- gluing absorption;
- commutator obstruction.

Each block needs positive and negative controls. Passing the harness means only:

```text
definitions_and_harness_viable_only
```

## 10. Fail-Closed Empirical Gate

Before any future empirical upgrade, require:

- provenance check;
- schema check;
- source-only weights;
- matched mean/slope removal;
- random equal-size axes;
- within-axis shuffles;
- bad-axis labels;
- same-dimensional random subspaces;
- rank/noise floor;
- coarsening/refinement naturality;
- seed/generation holdout;
- gluing sanity.

If any high-priority kill gate fires, stop explanation. Do not append a weak
positive narrative.

Strongest empirical-design verdict remains:

```text
eligible_for_next_design_review_only
```

## 11. Junior-High Explanation

The old MaoField story had many attractive shapes. Strict checking showed that
most could be caused by simpler things: one-number metrics, coordinate choices,
low-rank templates, or smoothing trends.

The new project asks a cleaner question. After every easy-to-fake mark is
wiped away, is there still a shape that survives changes of scale and path? If
yes, define it. If no, prove why the apparent structure was an artifact.
