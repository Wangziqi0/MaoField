# Formal Note v1.2 Workplan

Date: 2026-06-26 CST

Status: Mode A minimal mathematical patch plan after the strict audit of Formal
v1.1. This is not a MaoField empirical result.

Source audit:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md
```

## Boundary

v1.2 must keep the same evidence boundary as v1.1:

- no full panel;
- no checkpoint loading;
- no model inference;
- no training;
- no new loss;
- no observed MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- no glass-box, LOSO, F3, or empirical-positive language.

Strongest allowed local verdict remains:

```text
definitions_and_harness_viable_only
```

## Patch Goal

Turn Formal v1.1 from an accepted patch into a tighter finite-dimensional
formal note by closing the four report (27) partial repairs:

1. common ambient definitions;
2. random-subspace analytic-null / harness-statistic alignment;
3. product-weight positive theorem proof;
4. fail-closed threshold contract.

The goal is a small precise patch, not a new research program.

## Required Formal Patches

### 1. Common Ambient Registration

Choose at least one registered ambient construction before using spectrum,
angle, stack, transported norm, or invariant language.

Minimum acceptable form:

```text
select a base vertex b;
define registered maps A_s:H_s -> H_b or A_s:H_s -> E;
define registered residuals \tilde R_s = A_s P_s K_s;
define stack, angles, norms, and spectra only after registration.
```

The note must state which quantities are registration-dependent diagnostics
and which, if any, are invariant under a stated equivalence.

### 2. Random-Subspace Null Closure

Align the formal statistic with the harness statistic.

Preferred patch:

```text
Z = ||Pi_S u||^2 / ||u||^2
Z ~ Beta(k/2, (d-k)/2)
```

after whitening, for a fixed nonzero `u` and a Haar-uniform random `k`-plane
`S` in `R^d`, with explicit nondegenerate domain `0 < k < d`.

The harness should either:

- compare squared capture to the Beta law; or
- clearly label Monte Carlo norm-ratio gates as monotone diagnostic gates, not
  direct Beta-calibrated tests.

### 3. Product-Weight Hoeffding Equivalence

State and prove the positive theorem internally:

```text
under exact product weights and additive main-effect nuisance,
the weighted residual equals the product-measure Hoeffding interaction term.
```

The theorem must define:

- product space;
- product weights;
- additive main-effect nuisance;
- conditional expectation / product projection;
- interaction component;
- the relevant weighted `L^2` inner product.

Then keep the v1/v1.1 non-product counterexample as the boundary case.

### 4. Square Holonomy Telescoping Defect

Keep v1.1's path-level identity, then add a per-edge telescoping expression
that isolates projection/transport leakage along a path.

Minimum acceptable form:

```text
Chat_p - P_t C_p P_s
= sum of transported local terms involving P_{i+1} C_i P_i - P_{i+1} C_i
  or equivalent commutator/leakage terms.
```

The statement may be a proposition for finite paths with explicitly named
operators. It does not need to become a sheaf theory.

### 5. Threshold Contract As Single Source

All pass/fail tests in the v1.2 harness must read thresholds from one
registered object. The JSON output must be a serialization of that object.

Add a meta-test:

```text
runtime_threshold_contract == json_threshold_contract
```

If a block uses hard-coded constants outside the contract, v1.2 should fail
the harness-contract audit.

## Required Harness Patches

The v1.2 harness should be versioned separately. Do not mutate v1.1 JSON.

Minimum additions or repairs:

1. `quotient_descent_control`
2. `common_ambient_registration_control`
3. `rank1_perturbation_bound_control`
4. `random_subspace_beta_squared_capture_control`
5. `threshold_contract_single_source_control`
6. optional `square_holonomy_telescoping_control`

Existing v1.1 blocks may remain as regression controls, but the v1.2 summary
must clearly distinguish:

- theorem-backed tests;
- regression examples;
- review-floor heuristics;
- Monte Carlo diagnostics.

## Exit Gate

v1.2 may be called a formal patch only if:

- a v1.2 note, harness summary, harness JSON, and script agree on test names;
- `py_compile` passes for the script;
- JSON validates with `python -m json.tool`;
- all thresholds are driven from the single contract;
- no MaoField data, checkpoints, inference, training, or new loss are invoked;
- forbidden empirical and completed-system claims remain blocked.

If these gates fail, use:

```text
formal_v1_2_blocked_or_incomplete
```
