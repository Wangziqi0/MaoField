# Order-Defect Proof Repair Candidate

Date: 2026-06-30 CST
Status: proof-repair candidate for recheck, not proof authority
Source note: `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`

## Boundary

This file is a narrow repair candidate for Proposition 2 and Proposition 3 in
the v1.3 order-defect note. It is not a new theory and not a MaoField empirical
result.

Current allowed ceiling remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

No full panel, checkpoint loading, inference, training, new loss, observed
residual field, interaction field, quotient-residual field, transport field,
holonomy field, F3, LOSO, glass-box, posted-preprint, or completed-formal-system
claim is authorized here.

The floating-point harness is deterministic regression support only; the
mathematical claims are carried by the analytic proof and exact rational
certificate, not by JSON floats.

## Setup

Let `Q` and `B` be finite sets, `X=Q x B`, and `w(q,b)>0` with
`sum_{q,b} w(q,b)=1`. Let

```text
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b)
w_Q(q) = sum_b w(q,b)
w_B(b) = sum_q w(q,b)
```

Define:

```text
C  = span{1}
A  = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

Let `P_C`, `P_A`, `P_B0`, and `P_N` be the weighted orthogonal projections onto
`C`, `A`, `B0`, and `N_add`.

Define ordered stripping operators:

```text
R_Q_then_B = (I - P_B0)(I - P_A)(I - P_C)
R_B_then_Q = (I - P_A)(I - P_B0)(I - P_C)
D_w = R_Q_then_B - R_B_then_Q
```

Because `P_A 1 = P_B0 1 = 0`,

```text
D_w = P_B0 P_A - P_A P_B0.
```

## Lemma 0: Main-Effect Intersection

```text
A cap B0 = {0}.
```

Proof. If `h in A cap B0`, then `h` is both a function of `q` alone and a
function of `b` alone. Hence `h` is constant on `Q x B`. Since `h in A`, it has
zero `w_Q`-mean; equivalently, since `h in B0`, it has zero `w_B`-mean. The
constant is therefore zero.

## Lemma 1: Product Weights Iff Main-Effect Orthogonality

For finite positive weights on `Q x B`,

```text
w(q,b) = w_Q(q) w_B(b) for all q,b
```

if and only if

```text
A is orthogonal to B0 under <.,.>_w.
```

This is Proposition 1 of the source note. The converse uses centered cell
indicators:

```text
a_q0(q) = 1_{q=q0} - w_Q(q0)
b_b0(b) = 1_{b=b0} - w_B(b0)
```

and expands:

```text
<a_q0,b_b0>_w = w(q0,b0) - w_Q(q0) w_B(b0).
```

## Repair Candidate For Proposition 2

For finite positive weights, the following are equivalent:

```text
w is product form
A is orthogonal to B0
D_w = 0
R_Q_then_B = R_B_then_Q
```

When these hold,

```text
R_Q_then_B = R_B_then_Q = I - P_N.
```

Proof. If `w` is product form, Lemma 1 gives `A orthogonal B0`. Since `C` is
orthogonal to both centered main-effect spaces, `C`, `A`, and `B0` form an
orthogonal direct sum. Therefore:

```text
P_N = P_C + P_A + P_B0
P_A P_B0 = P_B0 P_A = 0
```

The ordered stripping products reduce to `I-P_N`, and hence `D_w=0`.

Conversely, assume `D_w=0`. For any `b in B0`, `P_B0 b=b`, so

```text
0 = D_w b = P_B0 P_A b - P_A b.
```

Thus `P_A b = P_B0 P_A b`, so `P_A b` lies in `A cap B0`. By Lemma 0,

```text
P_A b = 0 for all b in B0.
```

For any `a in A` and `b in B0`, self-adjointness of the orthogonal projection
`P_A` gives:

```text
<a,b>_w = <a,P_A b>_w = 0.
```

Thus `A orthogonal B0`, and Lemma 1 implies product weights. Finally,
`R_Q_then_B = R_B_then_Q` is equivalent to `D_w=0` by definition of `D_w`.

Degenerate one-row or one-column cases are harmless: one of `A` or `B0` is zero
and every positive single-row or single-column table equals its marginal
product.

## Repair Candidate For Proposition 3

If `w` is not product form, then there exists a pure main-effect witness
`K in B0` such that:

```text
K in N_add
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K != 0
```

The nonzero wrong-order output is a sequential stripping artifact, not a true
interaction residual. This statement is existential; it does not claim that
every input differs under the two orders.

Proof. If `w` is not product form, Lemma 1 gives that `A` is not orthogonal to
`B0`. Hence there exist `a in A` and `b in B0` with `<a,b>_w != 0`. Since

```text
<a,b>_w = <a,P_A b>_w,
```

there is a `b in B0` such that `P_A b != 0`. Set `K=b`.

Because `K in B0`, it has global mean zero, so `P_C K=0`, and `P_B0 K=K`.
Therefore:

```text
R_B_then_Q K = (I-P_A)(I-P_B0)(I-P_C)K = 0.
```

Also:

```text
R_Q_then_B K
= (I-P_B0)(I-P_A)K
= -(I-P_B0)P_AK.
```

If `R_Q_then_B K=0`, then `P_AK=P_B0P_AK`, so `P_AK in B0`. But `P_AK in A`
as well, hence `P_AK in A cap B0 = {0}` by Lemma 0. This contradicts the
choice of `K` with `P_AK != 0`. Therefore `R_Q_then_B K != 0`.

Since `K in N_add`, the true additive residual is zero:

```text
(I-P_N)K = 0.
```

Thus the nonzero wrong-order output comes from sequential stripping order, not
from a true interaction residual.

## Exact Witness Anchor

The exact 2 x 2 rational witness remains the certificate-level example:

```text
w = (1/11) [[1,2],
            [3,5]]
K = (7/11, -4/11, 7/11, -4/11) in B0
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

Primary certificate files:

```text
docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
scripts/debranded_residual_transport_exact_witness_v1_4.py
```

This exact witness supports the narrow certificate claim only. It does not
upgrade the full proof stack, the harness, or MaoField Mode B.
