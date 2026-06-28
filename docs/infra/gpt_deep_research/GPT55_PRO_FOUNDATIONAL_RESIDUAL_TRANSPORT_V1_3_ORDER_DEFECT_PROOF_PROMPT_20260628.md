# Zero-Context Prompt For GPT-5.5 Pro

You are GPT-5.5 Pro acting as a strict mathematics professor and adversarial
methodology reviewer.

You are given a repository-local bundle from the private repository
`Wangziqi0/MaoField`. Treat the uploaded bundle as the primary evidence. If a
GitHub connector is explicitly available in your UI, you may use it only as a
secondary check. Do not use public GitHub pages, raw.githubusercontent.com,
search engines, or public 404 pages as evidence about this private repository.

## Task

Do a fresh zero-context Mode A proof audit for Formal v1.3 of the debranded
finite weighted residual transport project.

The previous Pro report classified the next target as:

```text
v1_3_theorem_strengthening_plan_accepted
```

Node36 adopted only the target:

```text
formal_v1_3_weighted_anova_order_defect_plan_accepted_with_guards
```

Your job is to decide whether the proposed v1.3 order-defect theorem package is
mathematically correct, repair it if needed, and specify the exact minimal
zero-GPU harness checks. Your job is not to validate MaoField empirically, not
to continue the old glass-box claim, and not to certify a completed formal
system.

## Read First

Read these files in order:

1. `00-README_FOR_19_AND_PRO.md`
2. `00-CURRENT_STATUS_FOR_PRO.md`
3. `prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md`
4. `from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_3_theorem_strengthening_plan_20260628.md`
5. `from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md`
6. `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md`
7. `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md`
8. `from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md`
9. `from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json`
10. `from_repo/scripts/debranded_residual_transport_harness_v1_2.py`

Use older v1.1/v1.2 audit files only as provenance.

## Evidence Boundary

Allowed evidence:

- files in the uploaded bundle;
- local note/script/JSON/summary consistency;
- finite-dimensional definitions, theorem statements, proofs, and
  counterexamples derived directly from the setup.

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

## Proposed Object To Audit

Let `Q` and `B` be finite sets, `X = Q x B`, and let `w(q,b) > 0` with total
mass one. Define:

```text
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b)
w_Q(q) = sum_b w(q,b)
w_B(b) = sum_q w(q,b)
C = span{1}
A = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

Let `P_C`, `P_A`, `P_B0`, and `P_N` be weighted orthogonal projections.

Define ordered residual operators:

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q
```

The workplan claims the intended simplification:

```text
R_Q_then_B - R_B_then_Q = (P_B0 P_A - P_A P_B0)(I - P_C)
D_w = P_B0 P_A - P_A P_B0
```

## Theorem Claims To Verify Or Repair

Audit these proposed statements strictly.

### T1. Product Weight Iff Main-Effect Orthogonality

For finite positive weights, the following should be equivalent:

```text
w(q,b) = w_Q(q) w_B(b) for all q,b
A is orthogonal to B0 under <.,.>_w
```

Suggested proof uses centered indicators:

```text
a_q0(q) = 1_{q=q0} - w_Q(q0)
b_b0(b) = 1_{b=b0} - w_B(b0)
<a_q0,b_b0>_w = w(q0,b0) - w_Q(q0) w_B(b0)
```

Check this proof for correctness, edge cases, and notation pitfalls.

### T2. Sequential Stripping Order-Defect Criterion

The workplan asks whether:

```text
D_w = 0 iff w is product-form
R_Q_then_B = R_B_then_Q iff w is product-form
```

Check whether this iff is true as stated. If false, give the sharp corrected
statement and a counterexample.
If the operators differ, distinguish "there exists a witness input" from
"every input differs".

### T3. Non-Product Pure-Main-Effect Fake Residual No-Go

The workplan asks whether non-product `w` implies existence of a pure main
effect `K in A` or `K in B0` such that:

```text
(I - P_N) K = 0
one ordered stripping residual is zero
the opposite ordered stripping residual is nonzero
```

Check the proof and give a minimal 2 x 2 witness if correct. The existing v1.2
non-product example uses raw weights `(1,2,3,5)`.
Use the phrase `sequential stripping artifact` or `interaction-like artifact`
for the wrong-order residual unless you prove a stronger interpretation.

## Required Output

Write the report in sections:

1. One-page verdict.
2. Definitions and notation audit.
3. T1 proof audit.
4. T2 proof audit.
5. T3 proof audit and minimal witness.
6. Minimal harness implications, with exact pass/fail quantities.
7. Kill list of statements that must remain forbidden.
8. Junior-high explanation.
9. Final classification, choosing exactly one:

```text
v1_3_order_defect_proof_plan_accepted
requires_v1_3_definition_revision
requires_v1_2_boundary_reopen
reject_order_defect_choose_different_v13_target
insufficient_artifact_for_order_defect_review
```

Do not propose full-panel work. Do not propose training. Do not propose a new
loss. Do not turn this into a MaoField empirical validation task.
