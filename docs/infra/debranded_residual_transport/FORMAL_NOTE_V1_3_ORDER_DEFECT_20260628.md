# Finite Weighted Residual Transport -- Formal Note v1.3

Date: 2026-06-28 CST

Status: Mode A finite-dimensional order-defect proof note after report (32).
This is not a MaoField empirical result.

Source workplan and audit:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_3_order_defect_proof_audit_20260628.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_AUDIT_ADOPTION_NOTE_20260628.md
```

## 0. Boundary

This note strengthens the v1.2 product-weight Hoeffding boundary. It keeps the
same evidence boundary:

- no full MaoField panel has run;
- no 16-cell full-panel aggregate exists;
- no residual, interaction, quotient-residual, transport, or holonomy field has
  been observed in MaoField data;
- no LOSO, F3, glass-box, checkpoint-loading, model-inference, training, or
  new-loss claim is authorized;
- every example below is finite, synthetic, and zero-GPU.

Allowed ceiling:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status:

```text
insufficient_artifact
```

## 1. Finite Weighted ANOVA Setup

Let `Q` and `B` be finite sets, let `X=Q x B`, and let `w(q,b)>0` with

```text
sum_{q,b} w(q,b) = 1.
```

The weighted inner product is

```text
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b).
```

Define marginals:

```text
w_Q(q) = sum_b w(q,b)
w_B(b) = sum_q w(q,b)
```

Strict positivity implies `w_Q(q)>0` and `w_B(b)>0`.

Define subspaces inside `R^{Q x B}`:

```text
C  = span{1}
A  = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

The direct sum above is an algebraic direct sum. In general it is not an
orthogonal direct sum: `C` is orthogonal to `A` and `B0`, but `A` and `B0` are
orthogonal exactly in the product-weight case proved below.

Let `P_C`, `P_A`, `P_B0`, and `P_N` be weighted orthogonal projections onto
`C`, `A`, `B0`, and `N_add`. In general,

```text
P_N != P_C + P_A + P_B0
```

unless the decomposition is orthogonal.

For any field `f`, write

```text
mu_f = sum_{q,b} w(q,b) f(q,b)
E_w[f|q] = sum_b w(q,b) f(q,b) / w_Q(q)
E_w[f|b] = sum_q w(q,b) f(q,b) / w_B(b)
```

Then:

```text
P_C f = mu_f
P_A f = E_w[f|q] - mu_f
P_B0 f = E_w[f|b] - mu_f
```

where the last two expressions are viewed as q-only and b-only functions.

## 2. Product Weight Iff Main-Effect Orthogonality

### Proposition 1

For finite positive weights on `Q x B`, the following are equivalent:

```text
w(q,b) = w_Q(q) w_B(b) for all q,b
A is orthogonal to B0 under <.,.>_w
```

### Proof

Assume first that `w(q,b)=w_Q(q)w_B(b)`. For any `a in A` and `b in B0`,

```text
<a,b>_w
= sum_{q,b} w_Q(q)w_B(b)a(q)b(b)
= (sum_q w_Q(q)a(q)) (sum_b w_B(b)b(b))
= 0.
```

Thus `A` is orthogonal to `B0`.

Conversely, assume `A` is orthogonal to `B0`. Fix `q0 in Q` and `b0 in B` and
define centered indicators:

```text
a_q0(q) = 1_{q=q0} - w_Q(q0)
b_b0(b) = 1_{b=b0} - w_B(b0)
```

These satisfy `a_q0 in A` and `b_b0 in B0`. Orthogonality gives

```text
0 = <a_q0,b_b0>_w.
```

Expanding:

```text
<a_q0,b_b0>_w = w(q0,b0) - w_Q(q0) w_B(b0).
```

Hence `w(q0,b0)=w_Q(q0)w_B(b0)` for every cell, so `w` is product form.

The degenerate one-row or one-column cases are harmless: one of `A` or `B0`
is zero and any positive single-row or single-column probability table equals
its marginal product.

## 3. Sequential Stripping Order Defect

Define ordered stripping operators:

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q
```

Because `P_A 1 = P_B0 1 = 0`,

```text
D_w = (P_B0 P_A - P_A P_B0)(I - P_C)
```

as an operator on all of `R^{Q x B}`. Since
`(P_B0 P_A - P_A P_B0)P_C=0`, this is equivalently

```text
D_w = P_B0 P_A - P_A P_B0.
```

### Proposition 2

For finite positive weights:

```text
D_w = 0 iff w is product form
R_Q_then_B = R_B_then_Q iff w is product form
```

When `w` is product form, both ordered stripping operators equal the true
orthogonal additive residual projector:

```text
R_Q_then_B = R_B_then_Q = I - P_N.
```

### Proof

If `w` is product form, Proposition 1 gives `A orthogonal B0`. Thus
`P_A` vanishes on `B0`, `P_B0` vanishes on `A`, and

```text
P_B0 P_A = P_A P_B0 = 0.
```

So `D_w=0`. The decomposition `C orthogonal A orthogonal B0` is then an
orthogonal direct sum, hence `P_N=P_C+P_A+P_B0`, and the ordered products reduce
to `I-P_N`.

Conversely assume `D_w=0`. Take any `b in B0`. Since `P_B0 b=b`,

```text
0 = D_w b = P_B0 P_A b - P_A b.
```

Thus `P_A b = P_B0 P_A b`, so `P_A b` lies in both `A` and `B0`. The algebraic
intersection `A cap B0` is zero: any function depending only on `q` and only
on `b` is constant, and zero mean forces that constant to be zero. Therefore

```text
P_A b = 0 for all b in B0.
```

For any `a in A` and `b in B0`,

```text
<a,b>_w = <a,P_A b>_w = 0.
```

So `A` is orthogonal to `B0`, and Proposition 1 implies `w` is product form.
The equivalence with `R_Q_then_B=R_B_then_Q` is the definition of `D_w`.

### Quantifier Guard

If `D_w != 0`, the correct conclusion is existential:

```text
there exists a witness signal f with R_Q_then_B f != R_B_then_Q f.
```

It is false to claim that every input differs. Constants lie in the kernel of
both ordered residual maps, and true `N_add^perp` residuals are fixed by both
orders.

## 4. Non-Product Pure-Main-Effect No-Go

### Proposition 3

If `w` is not product form, then there exists a pure main-effect witness
`K in A` or `K in B0` such that:

```text
(I - P_N)K = 0
one ordered stripping residual is zero
the opposite ordered stripping residual is nonzero
```

The nonzero wrong-order output is a sequential stripping artifact, not a true
interaction residual.

### Proof

If `w` is not product form, Proposition 1 says `A` is not orthogonal to `B0`.
Hence there exists `b in B0` with `P_A b != 0`; otherwise `P_A` would vanish
on all of `B0`, forcing `A orthogonal B0`.

Set `K=b`. Since `K in N_add`,

```text
(I - P_N)K = 0.
```

Also

```text
R_B_then_Q K = (I-P_A)(I-P_B0)(I-P_C)K = 0
```

because `K in B0` and `P_C K=0`. Meanwhile

```text
R_Q_then_B K = (I-P_B0)(I-P_A)K = -(I-P_B0)P_A K.
```

If this were zero, `P_A K` would lie in `B0`; but `P_A K` already lies in `A`,
so `P_A K in A cap B0 = {0}`, contradicting the choice of `K`. Thus the
opposite ordered residual is nonzero.

## 5. Minimal 2 x 2 Witness

Use the non-product weight

```text
w = (1/11) [[1,2],
            [3,5]]
```

in row-major order `(q1,b1),(q1,b2),(q2,b1),(q2,b2)`.
Its marginals are:

```text
w_Q = (3/11, 8/11)
w_B = (4/11, 7/11)
```

and

```text
w - w_Q tensor w_B = (1/121) [[-1, 1],
                              [ 1,-1]].
```

Take the pure b-only zero-mean witness

```text
K = (7/11, -4/11, 7/11, -4/11) in B0.
```

Then:

```text
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

This is the main v1.3 no-go witness.

The optional symmetric q-only witness is:

```text
K' = (8/11, 8/11, -3/11, -3/11) in A
R_Q_then_B K' = 0
R_B_then_Q K' = (1/42, -1/84, 5/224, -3/224)
```

Report (32) printed this optional symmetric vector with an 11x scaling slip.
The corrected vector above is the one implemented in the v1.3 harness.

## 6. Harness

The deterministic zero-GPU harness is:

```text
scripts/debranded_residual_transport_harness_v1_3.py
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
```

It contains exactly four blocks:

```text
product_weight_order_independence_control
centered_indicator_product_iff_control
nonproduct_pure_main_effect_no_go_control
threshold_contract_single_source_control
```

All pass/fail decisions are assigned by `evaluate_test()` against a serialized
top-level threshold contract. There are no random draws and no MaoField data
reads.

## 7. Authorized Interpretation

The v1.3 theorem controls support local formal design/proof review only. They
show that the product/non-product weight boundary and sequential-stripping
order-defect no-go are internally checkable on finite synthetic examples.

They do not show that MaoField contains an observed residual, interaction,
transport, or holonomy field. They do not authorize full-panel work,
checkpoint loading, inference, training, new loss, F3/LOSO, glass-box, or
completed-formal-system language.
