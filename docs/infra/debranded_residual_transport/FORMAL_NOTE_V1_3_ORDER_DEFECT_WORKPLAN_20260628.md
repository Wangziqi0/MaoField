# Formal Note v1.3 Order-Defect Workplan

Date: 2026-06-28 CST
Status: workplan only
Input report: `../gpt_deep_research/deep_research_formal_residual_transport_v1_3_theorem_strengthening_plan_20260628.md`

## Boundary

This is a Mode A finite-dimensional mathematics workplan. It is not a
MaoField empirical result and it does not authorize checkpoint loading,
inference, training, full-panel work, or a new loss.

Current strongest local status remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## Target

Formal v1.3 should first strengthen the product versus non-product weight
boundary in the v1.2 product-weight Hoeffding proposition.

Working name:

```text
weighted_anova_order_defect_product_weight_boundary
```

## Finite Setup

Let `Q` and `B` be finite sets and let `X = Q x B`.
Let `w(q,b) > 0` with `sum_{q,b} w(q,b) = 1`.

Define the weighted inner product:

```text
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b).
```

Define marginals:

```text
w_Q(q) = sum_b w(q,b)
w_B(b) = sum_q w(q,b)
```

Define subspaces inside `R^{Q x B}`:

```text
C = span{1}
A = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

Use `B0` for the b-only subspace in implementation notes to avoid clashing
with the set name `B`.

Let `P_C`, `P_A`, `P_B0`, and `P_N` be weighted orthogonal projections onto
these subspaces.

## Proposed Theorems To Audit

### T1. Product Weight Iff Main-Effect Orthogonality

For finite positive weights, the following are equivalent:

```text
w(q,b) = w_Q(q) w_B(b) for all q,b
A is orthogonal to B0 under <.,.>_w
```

Suggested proof obligation: use centered indicators

```text
a_q0(q) = 1_{q=q0} - w_Q(q0)
b_b0(b) = 1_{b=b0} - w_B(b0)
```

and verify:

```text
<a_q0, b_b0>_w = w(q0,b0) - w_Q(q0) w_B(b0)
```

### T2. Sequential Stripping Order-Defect Criterion

Define ordered residual operators:

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q
```

Because `P_A 1 = P_B0 1 = 0`, the intended simplification is:

```text
R_Q_then_B - R_B_then_Q = (P_B0 P_A - P_A P_B0)(I - P_C)
D_w = P_B0 P_A - P_A P_B0
```

Proposed criterion:

```text
D_w = 0 iff w is product-form.
```

Audit requirement: check whether this iff holds exactly as stated, or whether
additional conditions are required. Repair the statement if needed.
If `D_w != 0`, the correct claim is that the two ordered stripping operators
are not equal and therefore some witness signal shows order dependence. Do not
claim that every input signal shows an order-dependent residual.

### T3. Non-Product Pure-Main-Effect Fake Residual No-Go

If `w` is not product-form, there should exist a pure main effect `K in B0`
or `K in A` such that:

```text
(I - P_N) K = 0
one ordered stripping residual is zero
the opposite ordered stripping residual is nonzero
```

Audit requirement: verify the proof and give a minimal witness. The current
candidate witness is the v1.2 `product_reweighting_separation` 2 x 2
non-product weight example with raw weights `(1,2,3,5)`.
Use `sequential stripping artifact` or `interaction-like artifact` for the
wrong-order residual. Do not call it a true interaction residual.

## Minimal Harness Targets

If the theorem statements survive audit, Formal v1.3 implementation should add
only zero-GPU synthetic controls:

1. `product_weight_order_independence_control`
   - product weights;
   - `||D_w||` near zero;
   - `R_Q_then_B`, `R_B_then_Q`, and `I-P_N` agree on basis/random test vectors.

2. `centered_indicator_product_iff_control`
   - verify centered-indicator identity for every cell;
   - verify product/non-product classification from the identity.

3. `nonproduct_pure_main_effect_no_go_control`
   - use the 2 x 2 non-product witness;
   - verify true additive residual is zero;
   - verify one sequential order creates a nonzero fake residual.

No MaoField data, checkpoints, full panel, or training belongs in this harness.

## Kill List

Do not write any of the following:

- Formal v1.3 is complete;
- completed formal system;
- theorem stack complete;
- MaoField residual/interaction/transport/holonomy field observed;
- product-measure Hoeffding interaction under non-product weights;
- full panel, F3 positive, LOSO passed, glass box broken;
- training or new loss authorized.
