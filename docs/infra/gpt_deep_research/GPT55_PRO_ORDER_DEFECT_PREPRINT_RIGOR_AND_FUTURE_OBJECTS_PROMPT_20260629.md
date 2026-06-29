# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Preprint Rigor, Deduplication, And Future Objects

Use the uploaded zip as the primary evidence bundle. Do not use public GitHub,
raw GitHub URLs, search-engine snippets, or model memory as evidence for local
repo facts. If a file is absent from the uploaded bundle, say so. You may use
external scholarly search only for related-work / duplicate-work assessment,
and you must cite exact papers or say `not verified`.

Repository/project context inside the bundle: MaoField is only the storage
container for a debranded Mode A finite-dimensional mathematics line. This task
is not MaoField empirical validation.

## Mission

Act as a strict mathematics professor, proof auditor, and academic-compliance
reviewer. Your job is to decide whether the current order-defect note can be
turned into a short academically honest preprint placeholder, and to identify
future mathematical objects that could be developed without reviving MaoField
empirical claims.

Primary goals:

1. Perform a line-by-line correctness and rigor audit of the finite weighted
   order-defect derivations.
2. Audit the deterministic harness and JSON against the formal claims.
3. Check whether the proposed preprint framing is duplicate work, overbroad, or
   academically unsafe.
4. Propose future mathematical object directions that are narrow, falsifiable,
   and compliant with the evidence boundary.
5. Give drafting instructions for a 4-6 page short note, including exact
   wording to keep, wording to remove, and related-work positioning.

If the proof or harness audit fails, do not perform broad future-object
brainstorming. Limit future-object output to repair directions required to make
the current order-defect object mathematically sound.

## Primary Files To Inspect

```text
from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_3_order_defect_proof_audit_20260628.md
from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_AUDIT_ADOPTION_NOTE_20260628.md
from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_3_theorem_strengthening_plan_20260628.md
from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
from_repo/docs/infra/debranded_residual_transport/README.md
from_repo/STATE.md
from_repo/MD_CATALOG.md
```

## Required Top-Level Classification

Return exactly one:

```text
preprint_placeholder_mathematically_safe_after_minor_polish
preprint_placeholder_requires_mathematical_revision
preprint_placeholder_requires_related_work_reframing
preprint_placeholder_should_not_be_posted_yet
reject_as_duplicate_or_overclaim
```

Then provide PASS/WARN/FAIL for:

```text
finite_weighted_setup
projection_notation_and_subspaces
T1_product_weight_iff_orthogonality
T2_order_defect_iff_product
T3_nonproduct_pure_main_effect_artifact_no_go
exact_2x2_rational_witness
harness_script_summary_json_consistency
preprint_claim_boundary
related_work_and_duplicate_risk
future_object_roadmap
non_specialist_explanation
```

## Mathematical Claims To Verify

Finite setup:

```text
Q, B finite
X = Q x B
w(q,b) > 0
sum_{q,b} w(q,b) = 1
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b)
w_Q(q) = sum_b w(q,b)
w_B(b) = sum_q w(q,b)
C = span{1}
A = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

Audit that `N_add` is an algebraic direct sum in general, not an orthogonal
direct sum unless product form is established. Audit that `P_N` is the weighted
orthogonal projection onto the whole additive subspace and that the note never
uses `P_N=P_C+P_A+P_B0` outside the product-weight case.

T1:

```text
w(q,b) = w_Q(q) w_B(b) for all q,b
iff
A orthogonal B0 under <.,.>_w
```

Audit the centered-indicator proof and all degenerate one-row/one-column
cases.

T2:

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q
D_w = (P_B0 P_A - P_A P_B0)(I - P_C)
```

Audit whether the simplification to `P_B0 P_A - P_A P_B0` is legitimate on the
whole space, and whether `D_w=0 iff w` is product form is fully proved. Enforce
the quantifier guard: if `D_w != 0`, the conclusion is existential, not
universal over all inputs.

T3:

If `w` is non-product, audit the proof that there exists a pure main-effect
witness `K in A` or `K in B0` such that:

```text
(I-P_N)K = 0
one ordered residual is zero
the opposite ordered residual is nonzero
```

The nonzero output must be described as a sequential stripping artifact or
interaction-like artifact, not a true interaction residual.

## Exact 2x2 Coordinate Audit

Main witness:

```text
w = (1/11) [[1,2],
            [3,5]]
K = (7/11, -4/11, 7/11, -4/11) in B0
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

Optional symmetric A witness:

```text
K' = (8/11, 8/11, -3/11, -3/11) in A
R_Q_then_B K' = 0
R_B_then_Q K' = (1/42, -1/84, 5/224, -3/224)
```

Report (32) had an 11x scaling slip in the optional symmetric witness. Verify
that the local note, script, summary, JSON, and preprint placeholder use the
corrected coordinates and that no similar arithmetic slip remains.

## Harness Audit

Audit that the v1.3 harness:

- has no MaoField data reads;
- has no checkpoint loading, inference, training, full-panel execution, or new
  loss work;
- has no random draws;
- uses a central evaluator rather than hard-coded pass text;
- serializes a single threshold contract into JSON;
- verifies JSON-side threshold hash by readback;
- preserves exact rational witness meaning, not only approximate floats.

If the harness is insufficient as proof support, specify whether the fix is:

```text
symbolic_fraction_check
exact_projection_matrix_dump
additional_random_nonproduct_regression
do_not_use_harness_as_proof
```

## Related-Work And Duplicate-Work Audit

Do not claim broad novelty over dependent-input ANOVA, Sobol indices, Shapley
effects, correlated-input sensitivity analysis, or general noncommuting
projection theory.

At minimum, check and position against:

```text
Chastaing, Gamboa, Prieur (2012), Generalized Hoeffding-Sobol decomposition for dependent variables
Chastaing, Gamboa, Prieur (2015), Generalized Sobol sensitivity indices for dependent variables: numerical methods
Owen, Prieur (2017), On Shapley Value for Measuring Importance of Dependent Inputs
Iooss, Prieur (2019), Shapley effects for sensitivity analysis with correlated inputs
Il Idrissi, Bousquet, Gamboa, Iooss, Loubes (2025), Hoeffding decomposition of functions of random dependent variables
noncommuting orthogonal projections / alternating projections literature,
including von Neumann alternating projections, products of orthogonal
projections, and projection commutator/order-dependence results
```

Your duplicate-work question is narrow:

```text
Is there already a standard named theorem or paper that exactly covers the
finite diagnostic-field order artifact: non-product cell weights plus ordered
main-effect stripping can make a pure main effect produce a false
interaction-like residual, with a minimal finite witness and diagnostic
harness?
```

Answer one of:

```text
no_exact_duplicate_found_but_close_prior_work
likely_duplicate_of_existing_named_result
insufficient_literature_access_to_judge
```

If close prior work exists, give exact citations and say how the note should
reframe itself. The safe novelty framing is likely:

```text
not a new ANOVA theory; a compact diagnostic artifact note for finite weighted
empirical pipelines.
```

## Future Mathematical Objects To Evaluate

Propose future directions only if they remain Mode A mathematics and do not
upgrade MaoField empirical status. For each object, give:

```text
name
definition sketch
what theorem/no-go it could support
what prior work it risks duplicating
minimum zero-GPU harness
kill criterion
preprint suitability: now / later / not worth it
```

Candidate objects to consider:

1. General multi-axis finite weighted order defects for chains of nuisance
   projections.
2. Commutator norm and witness extraction for arbitrary nuisance subspaces.
3. Source-fixed quotient residuals `R = P_{N^\perp,w}K` with nuisance registry.
4. Scale-lattice residual transport with edge defect and square-holonomy
   telescoping, but only if it avoids overclaiming sheaf obstruction theory.
5. Exact product-weight Hoeffding boundary versus non-product weighted
   projection residuals.
6. Random-axis / random-subspace negative controls for finite diagnostic
   fields.
7. Gluing / local-to-global obstruction only as a finite consistency complex,
   not as philosophical metaphor.
8. Drafting a sequence of short notes: order defect first, then transport
   only if the first note survives strict review.

## Evidence Boundary And Forbidden Claims

Strongest local verdict allowed by this bundle:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status:

```text
insufficient_artifact
```

Forbidden:

- MaoField empirical positive result;
- observed MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- full panel run;
- 16-cell aggregate;
- checkpoint loading, inference, training, or new loss authorization;
- glass box broken;
- LOSO passed;
- F3 positive;
- completed formal system;
- theorem stack complete;
- philosophy as proof;
- "first dialectical materialism", "first reflexive AI", or "paradigm shift".

## Required Output Format

1. One-page verdict.
2. PASS/WARN/FAIL table for the audit components.
3. Mathematical error list with exact fixes, or `none found`.
4. Harness/script/JSON error list with exact fixes, or `none found`.
5. Duplicate-work / related-work assessment with citations.
6. Preprint posting decision: post narrow placeholder now / revise first /
   do not post.
7. Future object roadmap ranked by academic safety and mathematical value.
8. Drafting plan for a 4-6 page note, including section titles.
9. Exact wording to keep, exact wording to delete, and exact wording to add.
10. A short explanation for a non-specialist with roughly middle-school math
    background.
