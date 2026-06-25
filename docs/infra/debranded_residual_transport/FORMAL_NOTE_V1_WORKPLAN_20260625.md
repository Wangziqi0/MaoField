# Formal Note v1 Workplan — Finite Weighted Residual Transport

Date: 2026-06-25 CST

Status: Mode A mathematical workplan. This is not a MaoField empirical result.

Primary source:

```text
docs/infra/gpt_deep_research/FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_ADOPTION_NOTE_20260625.md
```

## Boundary

The v1 note must preserve the current evidence boundary:

- MaoField remains a negative-centered empirical pilot and measurement-audit
  case.
- No full panel has run.
- No 16-cell full-panel aggregate exists.
- No residual, interaction, quotient-residual, transport, or holonomy field
  has been observed.
- No LOSO / F3 / glass-box / training / new-loss claim is authorized.

Strongest current local verdict:

```text
definitions_and_harness_viable_only
```

## v1 Target

Write the project as an operator/no-go note:

```text
finite weighted Hilbert systems
weighted quotient residual representatives
fixed scale transports
edge commutators
square holonomy no-go
rank/random/gluing/product-weight kill gates
```

The note should succeed even if it proves only that apparent structure is a
projection, coordinate, scale, rank, or nuisance artifact.

## Required Definitions

1. Admissible finite weighted system:

```text
(X_s, w_s, N_s)
H_s = L^2(X_s, w_s)
<f,g>_s = sum_x w_s(x) f(x) g(x)
P_s = Pi_{N_s^perp,w_s}
```

2. Source-fixed nuisance:

```text
N_s = span(phi_{s,1}, ..., phi_{s,d_s})
```

Every `phi` must be determined by axes, weights, templates, transports, or
other pre-outcome structure. Outcome-derived directions are invalid.

3. Transport system:

```text
G = finite directed scale graph
C_rho: H_s -> H_t for rho: s -> t
C_p = C_{rho_m} ... C_{rho_1}
```

4. Projected path transport:

```text
Chat_p = P_{s_m} C_{rho_m} P_{s_{m-1}} ... P_{s_1} C_{rho_1} P_{s_0}
```

5. Edge and square defects:

```text
E_rho = C_rho P_s - P_t C_rho
D_rho(K) = E_rho K
Omega_{p,q} = Chat_p - Chat_q
H_{p,q}(K) = Omega_{p,q} K
```

## Required Lemmas / No-Gos

1. Weighted projection lemma:
   `Q = A(A^T W A)^+ A^T W` is a weighted orthogonal projection onto `N`.

2. Quotient representative lemma:
   `P_N K` is the minimum-norm representative of the quotient class `K + N`.

3. Outcome-derived nuisance vacuity:
   if `N` can be chosen after seeing `K`, residual claims become arbitrary.

4. Edge commutation lemma:

```text
C_rho P_s = P_t C_rho
iff
C_rho(N_s) <= N_t and C_rho(N_s^perp) <= N_t^perp
```

5. Square holonomy no-go:
   if all edge commutators vanish and raw path transports agree, square
   holonomy vanishes.

6. Rank-1 shadow vacuity:
   rank-1 stacked residuals are scalar brightness paths along one template.

7. Random same-dimensional subspace guard:
   named residual subspaces must beat random equal-dimensional subspaces in the
   same weighted residual Hilbert space.

8. Gluing absorption no-go:
   overlap mismatch absorbed by allowed local nuisance is not a gluing
   obstruction.

9. Non-product-weight counterexample:
   construct a positive non-product weight table where observed weighted
   projection residual differs from product-reference Hoeffding interaction.

10. Product-reweighting separation:
    product-reweighted Hoeffding analysis lives in a different `L^2` geometry
    from the observed weighted residual object.

## Harness v1 Additions

Keep the existing seven blocks:

- non-product weighted projection;
- edge defect;
- square holonomy;
- rank-shadow guard;
- random-subspace guard;
- gluing absorption;
- commutator obstruction.

Add these controls before treating the harness as v1-complete:

- exact product-weight equality control;
- transport-stable multidirectional positive control;
- raw-path-equality square control;
- outcome-derived nuisance invalidation;
- equal-cell-count random axes;
- within-axis shuffle;
- bad-axis label control;
- rank-1 plus noise-floor trap;
- product-reweighting separation;
- coarsening non-naturality trap.

## Verdict Map

Allowed synthetic/formal verdicts:

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

Forbidden verdicts from this line:

```text
observed_field
glass_box_broken
training_authorized
new_loss_authorized
```

## Next Local Work

1. Draft `FORMAL_NOTE_V1_20260625.md` from this workplan.
2. Keep all examples finite, zero-GPU, and synthetic.
3. If code changes are needed, add a separate v1 harness script instead of
   mutating the v0 result.
4. Run any scripts under `/home/amd/codex-node36/tmp/<task>/`.
5. Promote only small source, JSON, and verdict artifacts after node36
   verification.
