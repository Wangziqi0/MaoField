# Finite Quantitative Audit-Order Instability -- Formal Note v1.6

Date: 2026-07-07 CST

Status: bounded quantitative companion to the v1.3 order-defect note and the
D706 OI zero/nonzero corollary. This is not a MaoField empirical result and
does not patch the current Zenodo V2.5 preprint.

Source decision:

```text
docs/infra/gpt_deep_research/deep_research_oi_quantitative_norm_result_report33_20260706.md
docs/infra/gpt_deep_research/OI_QUANTITATIVE_NORM_RESULT_REPORT33_ADOPTION_NOTE_20260706.md
```

Primary proof sources:

```text
FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
FORMAL_NOTE_OI_COROLLARY_COMPANION_20260706.md
```

## 0. Boundary

This note records one finite-dimensional quantitative companion:

```text
OI^{op}_{N_add}(w)
  = max_j rho_j sqrt(1-rho_j^2),
```

where `rho_j` are the canonical correlations, equivalently cosines of
principal angles, between the centered main-effect spaces `A` and `B0`.

This is the standard finite Hilbert-space two-projection commutator formula
specialized to the v1.3 `A`, `B0`, and `D_w` object. The standard projection
geometry is not claimed as new broad theory.

This note does not introduce or prove:

- MaoField empirical positive result;
- full panel, checkpoint loading, inference, training, or new loss;
- observed residual, interaction, transport, holonomy, or gluing field;
- broad new ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof by deterministic harness, JSON, or model output.

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## 1. Setting

Let `Q` and `B` be finite sets. Let `X = Q x B`, and let `w(q,b)>0` with

```text
sum_{q,b} w(q,b) = 1.
```

Use the weighted inner product:

```text
<f,g>_w = sum_{q,b} w(q,b) f(q,b) g(q,b).
```

As in v1.3, define:

```text
C  = span{1}
A  = {a(q): sum_q w_Q(q) a(q) = 0}
B0 = {b(b): sum_b w_B(b) b(b) = 0}
N_add = C direct-sum A direct-sum B0
```

Let `P_C`, `P_A`, and `P_B0` be the weighted orthogonal projections onto
`C`, `A`, and `B0`. The v1.3 order-defect operator is:

```text
D_w = R_Q_then_B - R_B_then_Q = P_B0 P_A - P_A P_B0.
```

Define the restricted audit-order instability:

```text
OI^{op}_{N_add}(w)
  = || D_w restricted to N_add ||_(N_add, ||.||_w) -> L2(w).
```

It measures the largest sequential-stripping order artifact generated from
additive nuisance inputs. It does not measure true interaction residual size.

## 2. Principal-Angle Formula

Let `rho_1,...,rho_r` be the nonzero canonical correlations between `A` and
`B0` in `L2(w)`. Equivalently, `rho_j = cos(theta_j)`, where `theta_j` are the
principal angles between `A` and `B0`.

If `A=0` or `B0=0`, set the maximum below to `0`.

### Theorem

For finite positive weights on `Q x B`,

```text
OI^{op}_{N_add}(w)
  = max_j rho_j sqrt(1-rho_j^2).
```

Equivalently,

```text
OI^{op}_{N_add}(w)
  = (1/2) max_j sin(2 theta_j).
```

Consequently,

```text
0 <= OI^{op}_{N_add}(w) <= 1/2.
```

The upper bound is the sharp bound for a pair of finite-dimensional
orthogonal projections; equality occurs on a two-projection block with
`rho_j^2 = 1/2`.

### Proof

Set:

```text
U = A
V = B0
P = P_A
Q = P_B0
```

Then:

```text
D_w = QP - PQ.
```

The operator `D_w` kills `C`, because `P_A` and `P_B0` kill constants. It also
kills `(U+V)^perp`, because both `P` and `Q` vanish there. Since `C` is
orthogonal to both `A` and `B0`, adding a constant component to an input in
`N_add` can only increase the input norm while leaving the output unchanged.
Therefore:

```text
||D_w restricted to N_add||
  = ||QP-PQ restricted to U+V||.
```

Use the standard finite-dimensional principal-angle decomposition for the pair
of subspaces `U` and `V`. Each nontrivial two-dimensional block has an
orthonormal basis `e_j,g_j`, with `e_j in U` and `g_j perpendicular to U`, such
that the corresponding unit vector in `V` is:

```text
v_j = rho_j e_j + sqrt(1-rho_j^2) g_j.
```

On the block `span{e_j,g_j}`, the projections have matrices:

```text
P = [[1, 0],
     [0, 0]]

Q = [[rho_j^2, rho_j sqrt(1-rho_j^2)],
     [rho_j sqrt(1-rho_j^2), 1-rho_j^2]].
```

Hence:

```text
QP - PQ =
[[0, -rho_j sqrt(1-rho_j^2)],
 [rho_j sqrt(1-rho_j^2), 0]].
```

The operator norm of this block is:

```text
rho_j sqrt(1-rho_j^2).
```

Common subspace blocks, orthogonal unmatched blocks, and null blocks contribute
`0`. Taking the maximum over all principal-angle blocks gives the theorem.

## 3. Recovery Of The Product-Weight Corollary

The theorem implies:

```text
OI^{op}_{N_add}(w)=0
iff every nontrivial rho_j=0
iff A orthogonal B0.
```

The only extra guard needed for this implication is that, in the present
finite positive product-index setting, `A intersection B0 = {0}`: a function
depending only on `q` and only on `b` on a fully supported `Q x B` table must
be constant, and centering then makes it zero. Thus there is no common
nonzero `rho=1` block hiding a commuting-but-nonorthogonal component.

By v1.3 Proposition 1,

```text
A orthogonal B0
iff w(q,b)=w_Q(q)w_B(b) for all q,b.
```

Therefore the D706 zero/nonzero companion is recovered:

```text
OI^{op}_{N_add}(w)=0
iff w is product form.
```

This is a quantitative refinement of that corollary, not a new empirical
claim.

## 4. Normalized Dependence Tensor

Define:

```text
E_w(q,b) = w(q,b) - w_Q(q)w_B(b)
Z_w(q,b) = E_w(q,b) / sqrt(w_Q(q)w_B(b)).
```

Then the nonzero singular values of `Z_w` are exactly the canonical
correlations between `A` and `B0`.

### Proof

For `a in A` and `b in B0`,

```text
<a,b>_w
  = sum_{q,b} w(q,b) a(q)b(b).
```

Since `a` and `b` are centered under `w_Q` and `w_B`,

```text
sum_{q,b} w_Q(q)w_B(b)a(q)b(b) = 0.
```

Therefore:

```text
<a,b>_w
  = sum_{q,b} (w(q,b)-w_Q(q)w_B(b)) a(q)b(b).
```

Under the isometries:

```text
a(q) -> sqrt(w_Q(q)) a(q)
b(b) -> sqrt(w_B(b)) b(b),
```

the cross bilinear form is represented by the matrix `Z_w`. Also:

```text
Z_w sqrt(w_B) = 0
sqrt(w_Q)^T Z_w = 0,
```

because `E_w` has zero row and column marginal sums. Hence the nonzero singular
values of the full matrix `Z_w` are precisely the singular values of the
cross-Gram map between the centered spaces. These singular values are the
canonical correlations `rho_j`.

Thus:

```text
OI^{op}_{N_add}(w)
  = max_{rho in Sing(Z_w)} rho sqrt(1-rho^2),
```

where zero singular values contribute zero.

## 5. Near-Product Bound

Let:

```text
epsilon = ||Z_w||_2 = max_j rho_j.
```

Then always:

```text
OI^{op}_{N_add}(w) <= min(epsilon, 1/2).
```

If:

```text
epsilon <= 1/sqrt(2),
```

then the function `rho sqrt(1-rho^2)` is increasing on the whole observed
spectrum, so:

```text
OI^{op}_{N_add}(w) = epsilon sqrt(1-epsilon^2).
```

For small `epsilon`, this is the first-order perturbative estimate:

```text
OI^{op}_{N_add}(w) = epsilon + O(epsilon^3),
```

with the one-sided guard:

```text
epsilon sqrt(1-epsilon^2) <= epsilon.
```

If:

```text
m_Q = min_q w_Q(q)
m_B = min_b w_B(b),
```

then the raw tensor estimate:

```text
OI^{op}_{N_add}(w)
  <= ||Z_w||_2
  <= ||Z_w||_F
  <= ||E_w||_F / sqrt(m_Q m_B)
```

is immediate.

Important limitation: outside the near-product range, `OI^{op}_{N_add}` is not
determined by the single scalar `||Z_w||_2` alone. The full singular spectrum
matters, because `rho sqrt(1-rho^2)` decreases after `rho=1/sqrt(2)`.

## 6. Exact 2 x 2 Formula

For:

```text
w = [[a, b],
     [c, d]],
```

with `a,b,c,d>0` and `a+b+c+d=1`, define:

```text
r1 = a+b
r2 = c+d
s1 = a+c
s2 = b+d
tau = ad-bc.
```

The normalized dependence matrix has rank one, and its only nonzero canonical
correlation satisfies:

```text
rho^2 = (ad-bc)^2 / ((a+b)(c+d)(a+c)(b+d)).
```

Therefore:

```text
(OI^{op}_{N_add}(w))^2
  = rho^2 (1-rho^2)
```

or explicitly:

```text
(OI^{op}_{N_add}(w))^2
  = ((ad-bc)^2 / ((a+b)(c+d)(a+c)(b+d)))
    * (1 - ((ad-bc)^2 / ((a+b)(c+d)(a+c)(b+d)))).
```

For the v1.3 witness:

```text
w = (1/11) [[1,2],
            [3,5]],
```

the exact values are:

```text
tau = -1/121
rho^2 = 1/672
(OI^{op}_{N_add}(w))^2 = 671/451584.
```

These are exact operator-norm values. They are not the same normalization as
the v1.4 fixed-witness artifact:

```text
||R_Q_then_B K||_w^2 = 61/177408.
```

For this table:

```text
(671/451584) / (61/177408) = 121/28.
```

The old v1.4 number is the output norm of one unnormalized witness. The v1.6
number is the squared operator norm after input normalization. Mixing them is
a claim error.

## 7. Exact Support Artifact

The exact-support script is:

```text
scripts/debranded_residual_transport_exact_oi_quantitative_v1_6.py
```

It generates:

```text
EXACT_OI_QUANTITATIVE_V1_6_20260707.md
exact_oi_quantitative_v1_6_20260707.json
```

These artifacts check the `2 x 2` arithmetic using `fractions.Fraction`. They
are support artifacts only. They do not replace the analytic proof above.

## 8. Forbidden Upgrades

Do not use this quantitative companion to claim:

- MaoField empirical positive results;
- full panel, checkpoint loading, inference, training, or new loss;
- observed residual, interaction, transport, holonomy, or gluing field;
- F3 positive, LOSO passed, or glass-box success;
- broad new ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof by deterministic harness, JSON, or model output;
- paper-ready, peer-reviewed, arXiv-submitted, or journal-submitted status.
