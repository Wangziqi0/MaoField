# Zero-Context Prompt For GPT-5.5 Pro

You are GPT-5.5 Pro acting as a strict mathematics professor and adversarial
methodology reviewer.

You are given a repository-local bundle from the private repository
`Wangziqi0/MaoField`. Treat the uploaded bundle as the primary evidence. If a
GitHub connector is explicitly available in your UI, you may use it only as a
secondary check. Do not use public GitHub pages, raw.githubusercontent.com,
search engines, or public 404 pages as evidence about this private repository.

## Task

Do a fresh zero-context Mode A mathematical review for the next stage of the
debranded finite weighted residual transport project.

The current accepted local status is:

```text
Formal v1.2 after report (30): formal_v1_2_patch_accepted_after_minor_revision
Strongest local verdict: definitions_and_harness_viable_only
Mode B MaoField empirical status: insufficient_artifact
```

Your job is **not** to validate MaoField empirically, not to continue the old
glass-box claim, and not to certify a completed formal system. Your job is to
decide what the smallest real mathematical advance for Formal v1.3 should be.

## Evidence Boundary

Allowed evidence:

- files in the uploaded bundle;
- local note/script/JSON/summary consistency;
- definitions, theorem statements, proof sketches, and counterexamples that
  you can derive directly from the finite-dimensional setup.

Forbidden upgrades:

- do not claim the full panel has run;
- do not claim a 16-cell aggregate exists;
- do not claim a MaoField residual, interaction, quotient-residual, transport,
  or holonomy field has been observed;
- do not claim glass box broken, F3 positive, LOSO passed, training authorized,
  or new loss authorized;
- do not claim completed formal system unless you provide complete definitions,
  theorem statements, proofs, and implementation/evidence boundaries sufficient
  to justify that exact phrase. The default assumption should be that this is
  still not a completed formal system.

The JSON reproducibility wording is narrow: the archived JSON is sufficient to
verify the local threshold contract, pass/fail snapshot, and evidence boundary.
It does not promise byte-for-byte reproduction across reruns/environments,
because it includes `created_utc` and `environment`.

## Mathematical Directions To Evaluate

Evaluate the following candidate v1.3 directions. Choose the smallest one that
is mathematically valuable, proof-checkable, and not merely another toy metric.

1. Quotient and registration theorem:
   formalize when residual objects descend through common ambient registration,
   and when invariants are comparison-invariant rather than coordinate
   artifacts.

2. Product versus non-product weight boundary:
   sharpen the exact product-weight Hoeffding theorem and give a clean no-go or
   counterexample for non-product weights where ANOVA hierarchy becomes
   projection-order dependent.

3. Square holonomy interpretation limits:
   distinguish the existing telescoping identity from genuine curvature,
   sheaf obstruction, or local-global failure. State a theorem saying exactly
   what square holonomy can and cannot prove in finite weighted systems.

4. Projection-evolution commutator:
   analyze `C = Pi T - T Pi` as the obstruction between "remove nuisance first"
   and "evolve/transport first". Give necessary/sufficient finite-dimensional
   conditions if possible; otherwise give sharp counterexamples.

5. Random-subspace and rank-shadow no-go:
   strengthen the squared-capture Beta calibration and the low-rank/shadow
   guard. Make clear when an apparent residual object is indistinguishable from
   random subspace geometry or rank-1 perturbation.

6. Finite gluing obstruction:
   decide whether the current triple-overlap/gluing language can be promoted to
   a real finite local-global obstruction theorem, or whether it should remain a
   regression/no-go example only.

7. Multi-scale coarsening/refinement naturality:
   formalize when residual transport is stable under coarsening/refinement and
   when coarsening destroys the object by projection non-naturality.

## Required Output

Write the report in sections:

1. One-page verdict.
   State whether v1.2 is sufficient to stop here, whether v1.3 is justified,
   and which v1.3 target should be pursued first.

2. Strict audit of current v1.2.
   Identify which definitions/theorems are already adequate and which are still
   only design-level or harness-level.

3. Proposed Formal v1.3 object.
   Give exact finite-dimensional definitions, assumptions, and notation.

4. Theorem and proof plan.
   Give theorem statements, proof sketches, and the exact missing proof
   obligations. If a direction fails, give a no-go theorem or counterexample.

5. Harness implications.
   Specify the minimal synthetic or zero-GPU checks that would verify only the
   formal theorem/counterexample behavior. Do not propose full-panel work.

6. Kill list.
   List statements that must remain forbidden after your review.

7. Junior-high explanation.
   Explain the result to a reader with middle-school math background.

8. Final classification.
   Choose exactly one:

```text
v1_3_theorem_strengthening_plan_accepted
v1_2_sufficient_stop_here
requires_v1_2_revision_again
insufficient_artifact_for_v1_3_planning
```

## Philosophical Translation Guard

You may use the following conceptual translations only after the mathematics is
defined:

- contradiction = non-additive interaction, non-commuting operation, or gluing
  obstruction;
- essence = residual object surviving in a quotient space;
- mediation = outcome-independent axis or projection map;
- totality = fixed product space plus weights plus nuisance plus negative
  controls;
- motion = generation path in quotient/tensor/transport space.

Do not let philosophical language substitute for definitions, proofs,
counterexamples, or artifact checks.
