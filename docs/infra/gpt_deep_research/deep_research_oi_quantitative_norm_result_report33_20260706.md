# OI Quantitative Norm Result Report33

Date verified: 2026-07-06 22:30:01 CST on node36.

Source attachment:

```text
/home/amd/.codex/attachments/3f9f8ab0-09b9-43ca-bc9b-6dc4f8b31a78/pasted-text.txt
```

Source sha256:

```text
b100f3791e52dc49557acb4d3bc8450c408496c1b59c3e68082108a023294501
```

This is a normalized, RAG-oriented archive of the Pro response. It is a
claim-source report, not a node36 proof implementation.

## Verdict

Pro selected:

```text
PROVE_QUANTITATIVE_OI_NORM_RESULT
```

The proposed next bounded step is a quantitative refinement of the already
implemented OI corollary companion:

```text
OI^{op}_{N_add}(w) = ||D_w restricted to N_add||
```

Instead of only proving the zero/nonzero criterion, Pro proposes an exact
finite-dimensional norm formula in terms of principal angles, equivalently
canonical correlations, between the two centered main-effect subspaces `A` and
`B0` in `L^2(w)`.

## Proposed Theorem Shape

Let `Q` and `B` be finite sets, let `w(q,b)>0` be a probability weight on
`X=Q x B`, and let `C`, `A`, `B0`, `N_add`, `P_A`, `P_B0`, and

```text
D_w = P_B0 P_A - P_A P_B0
```

be as in the v1.3 finite order-defect note and the D706 OI companion.

Let `rho_1,...,rho_r in [0,1)` be the canonical correlations between `A` and
`B0`, equivalently the singular values of `P_A restricted to B0` with the
inherited `L^2(w)` inner product. If `theta_j` are the corresponding principal
angles, `rho_j = cos(theta_j)`.

Pro proposes:

```text
OI^{op}_{N_add}(w)
  = max_j rho_j * sqrt(1 - rho_j^2)
  = (1/2) max_j sin(2 theta_j)
```

with value `0` if `A=0` or `B0=0`.

Consequences proposed by Pro:

```text
0 <= OI^{op}_{N_add}(w) <= 1/2
```

and the upper bound is sharp in the finite two-projection problem when some
canonical correlation equals `1/sqrt(2)`.

## Relation To Product Weights

The implemented zero/nonzero corollary is recovered formally as:

```text
OI^{op}_{N_add}(w)=0
  iff every rho_j=0
  iff A is orthogonal to B0
  iff w(q,b)=w_Q(q)w_B(b).
```

This keeps the result inside the existing v1.3 spine: product weights iff
centered main-effect orthogonality, and the OI companion vanishes iff product
weights.

## Dependence Tensor Form

Pro proposes the centered dependence tensor:

```text
E_w(q,b) = w(q,b) - w_Q(q) w_B(b)
```

and normalized dependence matrix:

```text
Z_w(q,b) = E_w(q,b) / sqrt(w_Q(q) w_B(b)).
```

The proposed statement is that the nonzero singular values of `Z_w` are exactly
the canonical correlations `rho_j` between `A` and `B0`. Therefore:

```text
OI^{op}_{N_add}(w)
  = max_{rho in Sing(Z_w)} rho * sqrt(1 - rho^2).
```

Important limitation from the report: outside near-product or rank-one regimes,
the OI value is not determined by the scalar spectral norm `||Z_w||_2` alone,
because `rho * sqrt(1-rho^2)` increases on `[0,1/sqrt(2)]` and decreases on
`[1/sqrt(2),1]`. The singular spectrum matters.

## Near-Product Bound

Let:

```text
epsilon = ||Z_w||_2 = max_j rho_j.
```

Pro proposes the general bound:

```text
OI^{op}_{N_add}(w) <= min(epsilon, 1/2).
```

If `epsilon <= 1/sqrt(2)`, then:

```text
OI^{op}_{N_add}(w) = epsilon * sqrt(1 - epsilon^2).
```

For small `epsilon`, this is `epsilon + O(epsilon^3)` with the inequality
`epsilon * sqrt(1 - epsilon^2) <= epsilon`.

If marginals are bounded below by

```text
m_Q = min_q w_Q(q),    m_B = min_b w_B(b),
```

then Pro notes the safe raw-tensor estimate:

```text
OI^{op}_{N_add}(w) <= ||Z_w||_2 <= ||Z_w||_F <= ||E_w||_F / sqrt(m_Q m_B).
```

## Proposed 2x2 Formula

For a positive `2 x 2` probability table:

```text
w = [[a, b],
     [c, d]],
```

write:

```text
r1 = a+b,  r2 = c+d,
s1 = a+c,  s2 = b+d,
tau = ad-bc.
```

The proposed rank-one formula is:

```text
rho = |ad-bc| / sqrt((a+b)(c+d)(a+c)(b+d)).
```

Therefore:

```text
OI^{op}_{N_add}(w)
  = rho * sqrt(1-rho^2)
```

or equivalently:

```text
(OI^{op}_{N_add}(w))^2
  = ((ad-bc)^2 / ((a+b)(c+d)(a+c)(b+d)))
    * (1 - ((ad-bc)^2 / ((a+b)(c+d)(a+c)(b+d)))).
```

For the v1.3 table:

```text
w = (1/11) * [[1,2],
              [3,5]],
```

Pro computes:

```text
tau = -1/121
rho^2 = 1/672
(OI^{op}_{N_add}(w))^2 = 671/451584.
```

Node36 arithmetic check confirms these three rational values. However, this
number is not the same quantity as the old v1.4 pure-main-effect artifact norm
`61/177408`; the latter is an output norm for a particular witness rather than
the operator norm after input normalization. Node36 computed:

```text
(671/451584) / (61/177408) = 121/28.
```

Any future formal note must keep those normalizations separate.

## Proof Dependencies Proposed By Pro

Pro says the proof should use only:

1. The v1.3 finite weighted two-way-table setup.
2. The v1.3 identity `D_w = P_B0 P_A - P_A P_B0`.
3. The finite-dimensional principal-angle decomposition for two subspaces of a
   Hilbert space.
4. Proposition 1 only to translate `A` orthogonal to `B0` back into product
   weights.

Pro says Proposition 3 is not needed for the quantitative formula itself, but
remains useful for the existential-witness explanation behind the already
accepted zero/nonzero corollary.

## Proof Sketch Proposed By Pro

Set:

```text
U = A,   V = B0,   P = P_A,   Q = P_B0.
```

Then:

```text
D_w = QP - PQ.
```

The constant subspace `C` is killed by `D_w`, and `D_w` vanishes on
`(U+V)^\perp`, so the norm reduces to `U+V`.

On a principal-angle block, choose orthonormal vectors `e_j in U` and
`g_j perpendicular to U` such that:

```text
v_j = rho_j e_j + sqrt(1-rho_j^2) g_j
```

spans the corresponding direction in `V`. On the block
`span{e_j,g_j}`, the projections have matrices:

```text
P = [[1,0],
     [0,0]]

Q = [[rho_j^2, rho_j sqrt(1-rho_j^2)],
     [rho_j sqrt(1-rho_j^2), 1-rho_j^2]].
```

Thus:

```text
QP - PQ =
[[0, -rho_j sqrt(1-rho_j^2)],
 [rho_j sqrt(1-rho_j^2), 0]].
```

The operator norm of this skew-symmetric block is:

```text
rho_j sqrt(1-rho_j^2).
```

Taking the maximum over principal-angle blocks gives the proposed formula.

For the dependence tensor, Pro uses the centered-main-effect identity:

```text
<a,b>_w = sum_{q,b} (w(q,b)-w_Q(q)w_B(b)) a(q)b(b),
```

and the isometries:

```text
a(q) -> sqrt(w_Q(q)) a(q),
b(b) -> sqrt(w_B(b)) b(b),
```

to represent the cross bilinear form by `Z_w`. This identifies the singular
values of `Z_w` with the canonical correlations.

## Boundary

This report supports only a finite operator-geometry refinement of the accepted
OI companion. It does not prove:

- MaoField empirical positive result;
- full panel, training, inference, checkpoint loading, new loss, F3 positive,
  LOSO passed, or glass-box success;
- observed residual, interaction, transport, holonomy, or gluing field;
- broad ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof by JSON floats or deterministic harness.

The prior-art risk is manageable only if any future note states plainly that
the principal-angle / two-projection commutator formula is standard finite
Hilbert-space geometry. The local contribution would be the narrow
specialization to the v1.3 `A`, `B0`, and `D_w` object, plus the exact `2 x 2`
and near-product corollaries if locally proof-checked.

Mode B remains:

```text
insufficient_artifact
```

Duplicate risk remains:

```text
MEDIUM
```
