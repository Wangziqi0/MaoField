# Formal Note v1.1 Workplan

Date: 2026-06-25 CST

Status: Mode A mathematical patch plan. This is not a MaoField empirical
result.

Source audit:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_strict_audit_20260625.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md
```

## Boundary

Formal v1.1 must keep the same evidence boundary as v1:

- no full panel;
- no checkpoint loading or model inference;
- no MaoField observed residual, interaction, quotient, transport, or holonomy
  field;
- no LOSO / F3 / glass-box / training / new-loss claim;
- toy harnesses are synthetic design checks only.

Strongest allowed verdict:

```text
definitions_and_harness_viable_only
```

## Patch Goal

Turn Formal Note v1 from a good finite-dimensional draft into a stricter
operator/no-go note by filling the missing quotient, commutator, null, and
gluing machinery. The goal is not a positive MaoField result. A clean no-go or
absorption theorem is an acceptable success.

## Formal Patches

### 1. Quotient Descent

Add a proposition:

```text
C:H_s -> H_t induces \bar C:H_s/N_s -> H_t/N_t
iff C(N_s) <= N_t.
```

Then separate quotient descent from the stronger residual-representative
naturality condition:

```text
C P_s = P_t C.
```

### 2. Projection-Evolution Commutator

Add a theorem for one weighted Hilbert space:

```text
P T = T P
iff
T(N) <= N and T(N^{perp,w}) <= N^{perp,w}.
```

Also state the equivalent weighted-adjoint form when useful:

```text
T(N) <= N and T^{*,w}(N) <= N.
```

The theorem should define the leakage object:

```text
[P,T] = P T - T P
```

and explain that nonzero commutator is a leakage/no-go diagnostic, not a
discovery by itself.

### 3. Square Holonomy Decomposition

Keep the v1 no-go, then add a decomposition that separates:

- raw path mismatch;
- transported edge projection defects;
- endpoint projection effects.

This should make nonzero square holonomy diagnosable instead of only
pass/fail.

### 4. Transported Invariants

Define a common ambient space before claiming invariance of:

- residual norms;
- residual stack singular values;
- principal angles;
- edge-defect norms;
- square-holonomy norms.

Acceptable constructions include a selected base vertex, a path-transported
ambient space, or a weighted direct-sum space. The construction must be stated
before any spectrum or angle statement.

### 5. Random-Subspace Null

Replace or supplement Monte Carlo-only language with a finite-dimensional null:
after whitening the residual Hilbert space, the squared capture of a fixed
unit vector by a uniform random `k`-plane should have an analytic distribution
or a documented deterministic calibration fallback.

If a closed-form law is not included in v1.1, the note must say that the
current random-subspace block is a Monte Carlo design gate only.

### 6. Rank-1 Shadow Perturbation

Add a near-rank-1 statement:

```text
M = a v^T + E
```

and bound the second singular value / multidirectional evidence in terms of
`||E||`. The existing `sigma2/sigma1 >= 0.25` threshold must remain a
registered review floor, not a theorem.

### 7. Finite Gluing Complex

Move beyond pairwise gluing absorption by adding at least one finite
three-chart example:

- local spaces and overlaps;
- pairwise overlap maps;
- triple-overlap consistency condition;
- allowed nuisance absorption;
- obstruction residual after nuisance removal.

The v1 pairwise absorption guard remains a necessary screen, not a sufficient
sheaf theorem.

### 8. Product-Weight Equivalence Boundary

State the positive theorem:

```text
under exact product weights and additive main-effect nuisance,
weighted residual equals product-measure Hoeffding interaction.
```

Then keep the v1 non-product counterexample showing that observed non-product
weighted residuals and product-reweighted Hoeffding interactions live in
different `L^2` geometries.

## Harness v1.1 Patches

The v1.1 harness should remain a separate script or a clearly versioned mode.
Do not mutate the v1 JSON result.

Required additions:

1. restore a standalone `commutator_obstruction` block;
2. add a bad-edge-defect block alongside the good edge/naturality control;
3. write all pass/fail thresholds into JSON;
4. write environment metadata into JSON;
5. record discarded random draw counts;
6. convert within-axis shuffle into a null distribution, not a single shuffle;
7. add a harder random-subspace heldout case not fully constructed from the
   named true subspace;
8. add a finite three-overlap gluing/cocycle toy case;
9. keep product-weight equality and non-product separation controls.

## Exit Gate

v1.1 can be called a formal patch only if all of these hold:

- `py_compile` passes for any new or patched script;
- synthetic outputs are generated under `/home/amd/codex-node36/tmp/<task>/`;
- promoted JSON validates with `python -m json.tool`;
- formal note, harness summary, and JSON agree on test names and verdicts;
- forbidden empirical phrases remain blocked;
- no MaoField data, checkpoints, inference, training, or new loss are invoked.

If any gate fails, the correct status is:

```text
formal_v1_1_blocked_or_incomplete
```
