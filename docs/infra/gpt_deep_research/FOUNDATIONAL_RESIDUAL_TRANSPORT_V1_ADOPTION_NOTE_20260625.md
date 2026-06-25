# Foundational Residual Transport v1 Audit — Adoption Note

Date: 2026-06-25 CST (`date` verified on node36 at 14:50 CST).

Source report:

```text
docs/infra/gpt_deep_research/deep_research_foundational_residual_transport_v1_20260625.md
sha256=f65db589ba39c23f5d5137cd36d18981962f6196c36f1edcc04d1411e99bfe11
```

## Verdict

The report completed the requested Mode A task.

Accepted local interpretation:

```text
keep_the_math_project_kill_the_empirical_positive_story
```

The finite weighted residual transport / holonomy / operator no-go package is
worth continuing as a mathematical project. It still does not create a MaoField
empirical result.

Strongest allowed local verdict remains:

```text
definitions_and_harness_viable_only
```

## Accepted

The report is accepted as a Formal Note v1 workplan source for these items:

1. Promote the projection formula to a weighted Hilbert-space lemma:
   `Q = A(A^T W A)^+ A^T W` is the weighted orthogonal projection onto `N`.
2. Formalize the quotient representative:
   `P_N K` is the minimum-norm representative of `K + N`.
3. Define admissible nuisance as pre-outcome / source-fixed, and add a no-go:
   outcome-derived nuisance makes residual claims vacuous.
4. Promote the edge commutation lemma:
   `C_rho P_s = P_t C_rho` iff `C_rho(N_s) <= N_t` and
   `C_rho(N_s^perp) <= N_t^perp`.
5. Promote the square holonomy no-go:
   if edge defects vanish and raw path transports agree, projected holonomy
   vanishes.
6. Add rank-1 shadow vacuity:
   rank-1 stacked residuals are scalar brightness paths, not non-scalar
   structure.
7. Add same-dimensional random-subspace indistinguishability as a coordinate
   guard.
8. Add gluing absorption no-go:
   overlap mismatch absorbed by allowed nuisance is not a sheaf/gluing
   obstruction.
9. Add a non-product-weight counterexample showing that observed weighted
   residual projection is not automatically product-measure Hoeffding
   interaction.
10. Add projection/evolution commutator leakage and multiscale non-naturality
    counterexamples.
11. Expand the synthetic harness design with product-weight equality,
    transport-stable multidirectional, raw-path-equality, outcome-derived
    nuisance, random-axis, shuffle, rank-plus-noise, product-reweighting, and
    coarsening non-naturality controls.

## Deflated / Not Evidence

This report remains a GPT/Pro claim-source report. It does not authorize:

- full panel generation;
- 16-cell aggregate claims;
- checkpoint loading;
- model inference;
- training;
- a new loss;
- observed residual, interaction, quotient-residual, transport, or holonomy
  field;
- LOSO passed;
- F3 positive;
- glass box broken.

The report says it reran the uploaded harness script. Treat that as a report
claim only. Node36's local evidence remains the canonical script and JSON:

```text
scripts/debranded_residual_transport_harness.py
docs/infra/debranded_residual_transport/synthetic_harness_v0_20260625.json
```

The report also cites external arXiv references. Those references are not used
as promoted evidence in this adoption note until node36 performs a separate
literature verification pass.

## Local Adoption

Adopt the report as a D625 Formal Note v1 development guide:

```text
next local deliverable =
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_WORKPLAN_20260625.md
```

No empirical MaoField work is authorized by this adoption. The next code work,
if any, should remain zero-GPU and synthetic unless PI explicitly approves a
different task.

## Claim Gate

Allowed:

```text
Formal Note v1 theorem/no-go work is now scoped.
```

Not allowed:

```text
MaoField residual/transport/holonomy field observed.
```
