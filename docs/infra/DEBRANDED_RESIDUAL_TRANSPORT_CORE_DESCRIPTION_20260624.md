# Debranded Residual Transport / Holonomy Project Core Description

Date: 2026-06-24 CST

## One-Sentence Description

A finite-dimensional mathematics project studying whether stable non-scalar
residual structure survives after scalar metrics, main effects, nuisance
subspaces, decode artifacts, smooth trends, and coordinate freedom are removed.

## Why This Exists

MaoField's empirical line has been deflated into a negative-centered pilot and
measurement-audit case. That is valuable, but it should not be inflated into a
positive glass-box claim.

The material still suggests a sharper mathematical problem: when observations
live on weighted finite tables across scales, can there be a residual object
whose identity survives projection, coarsening, random-axis controls,
rank-shadow guards, and local-to-global gluing tests?

## Separation From MaoField

This project is debranded:

- it does not claim MaoField broke the glass box;
- it does not depend on dialectical-materialist wording as evidence;
- it does not treat smoke tests as discoveries;
- it does not require a MaoField full panel before definitions and no-go tests
  are formalized;
- it can end in a no-go theorem and still succeed.

MaoField remains the empirical ore. This project is the mathematical extraction
and kill framework.

## Core Object

For each finite scale `s`, define an admissible triple:

```text
(X_s, w_s, N_s)
```

where:

- `X_s` is a finite coordinate table;
- `w_s` is a positive weight vector or measure;
- `N_s` is a pre-outcome nuisance subspace;
- `H_s = L^2(X_s, w_s)`;
- `P_s = Pi_{N_s_perp,w_s}` is the weighted orthogonal projection away from
  nuisance.

For a signal `K_s in H_s`, define:

```text
R_s(K) = P_s K_s
```

For a coarsening or refinement edge `rho: s -> s'` with linear map
`C_rho: H_s -> H_s'`, define:

```text
D_rho(K) = C_rho P_s K_s - P_s' C_rho K_s
```

For a square in the scale lattice, define `H_square(K)` as the difference
between the two projection/coarsening paths around the square.

## Main Questions

1. Residual existence:
   Does `R_s(K)` survive after registered nuisance removal?

2. Transport stability:
   Are edge defects `D_rho(K)` small or structurally meaningful across scales?

3. Holonomy obstruction:
   Does a refinement square fail to commute after nuisance removal, and is the
   failure not absorbed by local nuisance?

4. Rank-shadow guard:
   Is the residual more than a rank-1 scalar template?

5. Random-subspace guard:
   Does the residual beat random same-dimensional subspaces?

6. No-go value:
   If all structure dies under controls, what theorem explains why the old
   apparent complexity was a scalar, coordinate, or projection artifact?

## Required Kill Suite

Before any empirical upgrade, the project must pass or explicitly fail these
zero-GPU tests:

- matched mean/slope removal;
- random equal-size axes;
- bad-axis labels such as `audit_block_id`;
- within-axis shuffles;
- same-dimension random subspace comparisons;
- rank-1 shadow guard with `sigma2/sigma1 >= 0.25` as the current design-review
  floor;
- coarsening/refinement naturality checks;
- projection/evolution commutator checks;
- gluing absorption checks.

Passing every test means only:

```text
eligible_for_next_design_review_only
```

It never means:

```text
residual_field_observed
interaction_field_observed
glass_box_broken
training_authorized
new_loss_authorized
```

## Success Conditions

The project succeeds if it produces any of:

- a clean finite-dimensional definition with invariants;
- a theorem explaining when residual structure is impossible;
- a counterexample showing why a dashboard metric can fake structure;
- a no-go classification for rank-1, random-axis, coarsening, or gluing
  artifacts;
- a preregistered, fail-closed measurement contract for future data.

It does not need a positive MaoField empirical result to be valuable.

## D625 Formal Note Agenda

The first formal note should be written as an operator/no-go note, not as a
MaoField finding. Its minimum structure is now:

1. admissible finite weighted systems `(X_s,w_s,N_s)`;
2. local residuals `R_s(K)=P_sK_s`;
3. fixed coarsening/refinement maps `C_rho`;
4. edge defects `D_rho(K)=C_rho P_sK_s - P_s' C_rho K_s`;
5. square holonomy defects as terminal-space path differences;
6. nuisance-gauge and transport-isomorphism equivalences;
7. invariants: residual norms, singular spectra, principal angles, edge
   defects, square holonomy, random-subspace quantiles, and transport-stable
   rank;
8. no-go targets for rank-1 shadows, random subspaces, coarsening
   non-naturality, square holonomy, commutator leakage, gluing absorption, and
   non-product weights.

The companion outline is:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_FORMAL_NOTE_OUTLINE_20260625.md
```

## First Work Items

1. Formalize admissible triples `(X,w,N)` and allowed maps.
2. Extend the synthetic harness to non-product weighted hierarchical
   projection.
3. Prove or falsify rank-shadow and random-subspace no-go propositions.
4. Define square holonomy and gluing obstruction in finite weighted Hilbert
   spaces.
5. Only after these definitions are stable, decide whether any future MaoField
   aggregate is worth PI-approved generation.
