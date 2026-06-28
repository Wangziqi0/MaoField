# GPT-5.5 Pro Zero-Context Prompt: Formal v1.3 Order-Defect Proof Note And Harness Audit

Use the uploaded zip as the primary evidence bundle. Do not use public GitHub,
public web browsing, raw GitHub URLs, search engine results, or model memory as
evidence. If a file is absent from the uploaded bundle, say so.

Repository/project context inside the bundle: MaoField is only the storage
container for this debranded Mode A finite-dimensional mathematics line. This
task is not MaoField empirical validation.

## Task

You are acting as a strict mathematics professor and proof/harness auditor.
Audit the local Formal v1.3 order-defect implementation after report (32).

Primary files to inspect:

```text
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_3_order_defect_proof_audit_20260628.md
from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_AUDIT_ADOPTION_NOTE_20260628.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
from_repo/scripts/debranded_residual_transport_harness_v1_2.py
from_repo/STATE.md
```

## Required Verdict

Return exactly one top-level classification:

```text
formal_v1_3_order_defect_note_and_harness_pass
formal_v1_3_order_defect_note_requires_minor_revision
formal_v1_3_order_defect_theorem_statement_requires_revision
formal_v1_3_order_defect_harness_requires_revision
reject_as_overclaim_or_empirical_upgrade
```

Then give separate PASS/WARN/FAIL verdicts for:

```text
definitions_and_projection_notation
T1_product_weight_iff_main_effect_orthogonality
T2_order_defect_iff_product
T3_nonproduct_pure_main_effect_no_go
exact_rational_witness_coordinates
harness_script_and_json
claim_boundary
```

## Mathematical Claims To Audit

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

Audit that `N_add` is treated as an algebraic direct sum in general, not as an
orthogonal direct sum unless product-form has been proved.

Audit that `P_C`, `P_A`, `P_B0` are weighted orthogonal projections onto the
individual subspaces, while `P_N` is the weighted orthogonal projection onto
the whole `N_add`. In general the note must not use:

```text
P_N = P_C + P_A + P_B0
```

unless product-form is already established.

T1:

```text
w(q,b) = w_Q(q) w_B(b) for all q,b
iff
A orthogonal B0 under <.,.>_w
```

Audit the centered-indicator proof:

```text
a_q0(q) = 1_{q=q0} - w_Q(q0)
b_b0(b) = 1_{b=b0} - w_B(b0)
<a_q0,b_b0>_w = w(q0,b0) - w_Q(q0) w_B(b0)
```

T2:

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q
```

Audit the operator identity:

```text
D_w = (P_B0 P_A - P_A P_B0)(I - P_C)
```

and whether the simplification to the commutator is legitimate as an operator
on the whole space.

Audit:

```text
D_w = 0 iff w is product form
R_Q_then_B = R_B_then_Q iff w is product form
```

Important quantifier guard: if `D_w != 0`, the correct conclusion is that
there exists a witness input with order dependence. Do not say every input
differs.

T3:

If `w` is non-product, audit the proof that there exists a pure main-effect
witness `K in A` or `K in B0` such that:

```text
(I-P_N)K = 0
one ordered residual is zero
the opposite ordered residual is nonzero
```

The nonzero output must be called `sequential stripping artifact` or
`interaction-like artifact`, not true interaction residual.

## Exact Coordinate Audit

The main witness should be:

```text
w = (1/11) [[1,2],
            [3,5]]
K = (7/11, -4/11, 7/11, -4/11) in B0
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

The optional symmetric A witness should use the corrected coordinates:

```text
K' = (8/11, 8/11, -3/11, -3/11) in A
R_Q_then_B K' = 0
R_B_then_Q K' = (1/42, -1/84, 5/224, -3/224)
```

Report (32) had an 11x scaling slip in this optional symmetric witness. Check
whether the local proof note, script, summary, and JSON all use the corrected
coordinates and whether any similar scaling mistakes remain.

## Harness Audit

Audit that the v1.3 harness:

- has no MaoField data reads;
- has no checkpoint loading, inference, training, or full-panel execution;
- has no random draws;
- uses the central evaluator `evaluate_test`;
- serializes a single threshold contract into JSON;
- verifies JSON-side threshold hash by readback;
- has exactly these theorem-control blocks:

```text
product_weight_order_independence_control
centered_indicator_product_iff_control
nonproduct_pure_main_effect_no_go_control
threshold_contract_single_source_control
```

Do not accept a harness if it only checks floating values while losing the
exact rational witness meaning. If you find a numerical tolerance problem,
state the exact failing quantity and a minimal repair.

## Evidence Boundary

The strongest local MaoField status allowed by the bundle is:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

Forbidden upgrades:

- full panel has run;
- 16-cell aggregate exists;
- checkpoint loading/inference/training/new loss is authorized;
- MaoField residual, interaction, quotient-residual, transport, or holonomy
  field has been observed;
- glass box broken;
- LOSO passed;
- F3 positive;
- completed formal system;
- theorem stack complete;
- Formal v1.3 completed as a whole system;
- non-product wrong-order artifact is a true product-measure Hoeffding
  interaction.

Philosophy, MaoField history, and conceptual language may motivate why the
object matters, but cannot substitute for proof, script, JSON, or source-file
evidence.

## Output Format

1. One-page verdict.
2. PASS/WARN/FAIL table for the seven audit components listed above.
3. Exact list of any mathematical errors, if any.
4. Exact list of any script/JSON/harness errors, if any.
5. Exact minimal patch instructions if revision is required.
6. Short explanation for a non-specialist with roughly middle-school math
   background.
