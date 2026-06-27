# Finite Weighted Residual Transport -- Formal Note v1.2

Date: 2026-06-27 CST

Status: Mode A minimal mathematical patch after report (28). This is not a
MaoField empirical result.

Source workplan and audit:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md
```

## 0. Boundary

This note patches Formal Note v1.1. It keeps the same evidence boundary:

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

## 1. Registered Ambient Data

Let `V` be a finite set of vertices. For each `s in V`, let
`(H_s,<.,.>_{w_s})` be a finite weighted Hilbert space, let `N_s <= H_s` be a
source-fixed nuisance subspace, and let

```text
P_s:H_s -> N_s^{perp,w_s}
```

be the weighted orthogonal residual projection.

### Definition 1. Registered Ambient Datum

A registered ambient datum is a finite Hilbert space `(E,<.,.>_E)` and linear
maps

```text
A_s:N_s^{perp,w_s} -> E
```

such that each `A_s` is an isometric embedding on the residual space:

```text
<A_s x, A_s y>_E = <x,y>_{w_s}
for all x,y in N_s^{perp,w_s}.
```

For a signal `K_s in H_s`, its registered residual is

```text
Rtilde_s(K_s) = A_s P_s K_s in E.
```

### Definition 2. Registered Diagnostics

Only after fixing a registered ambient datum may one form a residual stack,
singular spectrum, principal angle, transported norm, edge-defect norm, or
square-holonomy norm across vertices:

```text
S_reg = [Rtilde_s1 ... Rtilde_sm].
```

Without a registered ambient datum these quantities are unregistered
comparisons. They must not be called invariants.

### Definition 3. Equivalent Registration

Two registrations `(E,A_s)` and `(E',A'_s)` are equivalent if there is an
isometric isomorphism `U:E -> E'` such that

```text
U A_s = A'_s
```

on `N_s^{perp,w_s}` for every `s`.

### Proposition 1. Invariance Under Equivalent Registration

Stack singular values, Gram matrices, principal angles, and norms computed
from registered residuals are unchanged under equivalent registrations.

Proof sketch. The isometry `U` preserves all inner products among the
registered residual vectors. Singular values of a vector stack, Gram matrices,
principal angles, and norms are functions only of those inner products. Hence
they are invariant under the stated registration equivalence. This is the only
invariance language authorized by v1.2; otherwise the correct term is
registration-dependent diagnostic.

## 2. Random-Subspace Squared-Capture Null

### Proposition 2. Beta Law For Squared Capture

Let `0 < k < d`. Fix a nonzero vector `u in R^d`, and let `S` be a
Haar-uniform random `k`-plane in `R^d`. If `Pi_S` is the Euclidean orthogonal
projection onto `S`, then

```text
Z = ||Pi_S u||_2^2 / ||u||_2^2
```

has distribution

```text
Beta(k/2, (d-k)/2).
```

Proof sketch. By rotational invariance, projecting a fixed unit vector onto a
uniform random `k`-plane is equivalent to projecting a uniform random unit
vector onto the first `k` coordinates. Write that random unit vector as
`g/||g||_2` with `g_i iid N(0,1)`. Then

```text
Z = (g_1^2 + ... + g_k^2) / (g_1^2 + ... + g_d^2)
  = X / (X + Y),
```

where `X ~ chi^2_k`, `Y ~ chi^2_{d-k}`, and `X,Y` are independent. The ratio
has the stated Beta law.

Weighted version. In a finite weighted Hilbert space, first whiten the residual
space by an isometry into Euclidean coordinates, then apply the proposition.

Authorized statistic. The analytic Beta law is for squared capture `Z`, not
for the unsquared norm ratio `||Pi_S u||/||u||`. Harness v1.2 therefore uses
`random_subspace_beta_squared_capture_control`; any unsquared ratio can only be
a monotone diagnostic, not a direct Beta-calibrated gate.

## 3. Product-Weight Hoeffding Equivalence

Let `Q` and `B` be finite sets and let `X=Q x B`. Assume exact product weights

```text
w(q,b) = w_Q(q) w_B(b),
sum_q w_Q(q) = 1,
sum_b w_B(b) = 1,
w_Q,w_B > 0.
```

The weighted inner product is

```text
<f,g>_w = sum_{q,b} w_Q(q) w_B(b) f(q,b) g(q,b).
```

Define additive main-effect nuisance

```text
N_add = {c + a(q) + b(b)}.
```

For a field `K:Q x B -> R`, define

```text
mu      = E_w K,
K_Q(q) = E_w[K | q],
K_B(b) = E_w[K | b],
H(K)(q,b) = K(q,b) - K_Q(q) - K_B(b) + mu.
```

### Proposition 3. Product-Weight Hoeffding Residual

Under exact product weights,

```text
P_{N_add}^{perp,w} K = H(K).
```

Proof sketch. Decompose `N_add` into the orthogonal direct sum of constants,
zero-mean `q`-only functions, and zero-mean `b`-only functions. Product weights
make the last two pieces orthogonal because

```text
<a(q),b(b)>_w
= (sum_q w_Q(q)a(q)) (sum_b w_B(b)b(b)) = 0
```

whenever both terms have weighted mean zero. The projections of `K` onto these
three subspaces are `mu`, `K_Q-mu`, and `K_B-mu`. Subtracting them gives
`H(K)`.

Boundary. If observed weights are not exact product weights, the above
orthogonality need not hold. The authorized name is then non-product weighted
projection residual, not product-measure Hoeffding interaction. The existing
`product_reweighting_separation` regression remains the boundary example.

## 4. Path Defect And Square Holonomy Telescoping

Let a finite path be

```text
p: s_0 -> s_1 -> ... -> s_m
```

with maps `C_i:H_{s_{i-1}} -> H_{s_i}` and projections `P_i` at `s_i`.
Define, for `J subset {1,...,m-1}`,

```text
M_p(J) =
P_m C_m Q_{m-1} C_{m-1} ... Q_1 C_1 P_0,

Q_i = P_i if i in J, otherwise I.
```

The raw endpoint-projected transport is `M_p(empty)`. The fully projected path
transport is

```text
Chat_p = M_p({1,...,m-1}).
```

The path projection defect is

```text
Delta_p = Chat_p - M_p(empty).
```

### Proposition 4. Per-Edge Telescoping Formula

For `m >= 1`,

```text
Delta_p =
sum_{i=1}^{m-1} (M_p({1,...,i}) - M_p({1,...,i-1})).
```

Equivalently, each summand inserts one additional internal projection. For
`m=1` the sum is empty and `Delta_p=0`.

Proof. This is a finite telescoping sum. The length-2 case is

```text
P_2 C_2 P_1 C_1 P_0 - P_2 C_2 C_1 P_0
= P_2 C_2 (P_1 - I) C_1 P_0.
```

The length-3 case is

```text
P_3 C_3 P_2 C_2 P_1 C_1 P_0 - P_3 C_3 C_2 C_1 P_0
= P_3 C_3 C_2 (P_1-I) C_1 P_0
 + P_3 C_3 (P_2-I) C_2 P_1 C_1 P_0.
```

The general case repeats the same insertion.

For two paths `p,q:s -> t`, square holonomy is

```text
Omega_{p,q} = Chat_p - Chat_q
            = P_t(C_p-C_q)P_s + Delta_p - Delta_q.
```

Thus nonzero projected square holonomy is exactly raw endpoint path mismatch
plus transported internal projection leakage. This is a finite path identity;
it is not by itself a sheaf obstruction theory or a curvature theorem.

## 5. Harness v1.2 Contract

Harness v1.2 implements this note through a versioned synthetic script:

```text
scripts/debranded_residual_transport_harness_v1_2.py
```

The v1.2 contract rule is:

1. `build_threshold_contract()` is the single source of thresholds.
2. Block functions compute metrics only.
3. `evaluate_test()` assigns pass/fail from the single contract.
4. JSON serializes the same contract and its hash.
5. `threshold_contract_single_source_control` verifies per-test threshold
   equality and contract hash equality.

The v1.2 blocks are:

```text
exact_product_weight_equality_control
product_reweighting_separation
quotient_descent_control
common_ambient_registration_control
projection_evolution_commutator_obstruction
raw_path_equality_square_control
coarsening_non_naturality_trap
rank1_perturbation_bound_control
random_subspace_beta_squared_capture_control
square_holonomy_telescoping_control
triple_overlap_gluing_cocycle
threshold_contract_single_source_control
```

Passing these blocks supports only formal design review on synthetic finite
examples. It does not provide MaoField empirical evidence.

## 6. Downgraded And Forbidden Statements

The following remain forbidden after v1.2:

- common ambient invariant theory is complete;
- random-subspace nulls are absolute structure detectors;
- product-weight Hoeffding language applies to non-product weights;
- square holonomy telescoping equals sheaf obstruction theory;
- `sigma2/sigma1 >= 0.25` is a universal mathematical constant;
- full panel has run;
- 16-cell full-panel aggregate exists;
- MaoField residual, interaction, quotient-residual, transport, or holonomy
  field has been observed;
- glass box is broken;
- LOSO or F3 is positive;
- checkpoint loading, inference, training, or new loss is authorized.

## 7. Local Verdict

```text
v1_2_small_patch_feasible
```

This verdict means the finite-dimensional definitions and synthetic harness
are now tighter than v1.1. It does not mean the formal system is complete, and
it does not change Mode B MaoField empirical status.
