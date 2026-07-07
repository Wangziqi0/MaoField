# Finite Chart/Path/Cycle Defect Calculus Under Declared Transports

Internal v0 local draft, D707, 2026-07-07.

This note implements the report38 verdict `DRAFT_INTERNAL_V0_NOW` under the
report37 boundary `REVISE_BEFORE_FORMAL_NOTE`. It is a narrow finite-dimensional
linear-algebra note. It is not a public-ready paper, not an empirical MaoField
result, not a black-box mechanism claim, and not a broad theory.

## 1. Scope And Non-Claims

This note only treats declared finite chart data:

- a finite directed graph of charts;
- finite-dimensional real normed vector spaces assigned to charts;
- declared linear chart maps;
- declared linear edge transports;
- path defects, cycle defects, iterated cycle defects, and finite-horizon norm
  estimates.

It does not claim:

- MaoField empirical positive result;
- observed residual, interaction, transport, holonomy, gluing, or collapse field;
- black-box mechanism solved;
- dynamic-collapse theory;
- NMI-ready, paper-ready, public-ready, or submission-ready status;
- broad ANOVA, dependent-input, projection, sheaf, contextuality, or path-closure
  theory;
- proof by RAG, prompt, handoff, manifest, JSON, harness, or model output.

Mode B remains `insufficient_artifact`. Duplicate risk remains `MEDIUM`.

## 2. Declared Finite Chart Data

Let `G=(C,E)` be a finite directed graph. For each chart `c in C`, let
`H_c` and `O_c` be finite-dimensional real normed vector spaces, and let

```text
Phi_c : H_c -> O_c
```

be a linear map.

For each directed edge `e:c->c'`, let

```text
U_e : H_c -> H_c'
T_e : O_c -> O_c'
```

be declared linear transports. No empirical or canonical-transformation claim is
made by calling these maps transports; they are part of the declared finite
object.

For a path

```text
alpha = (c_0 --e_1--> c_1 --e_2--> ... --e_k--> c_k),
```

define the ordered composites

```text
U_alpha = U_e_k ... U_e_1 : H_c0 -> H_ck
T_alpha = T_e_k ... T_e_1 : O_c0 -> O_ck.
```

For the empty path `id_c`, set

```text
U_id_c = I_Hc,
T_id_c = I_Oc.
```

The path defect is the linear map

```text
Delta_alpha = T_alpha Phi_c0 - Phi_ck U_alpha : H_c0 -> O_ck.
```

For the empty path, `Delta_id_c=0`.

For any subset `S subset H_c0`, define the restricted sup-ratio

```text
||Delta_alpha|_S||
  = sup { ||Delta_alpha x|| / ||x|| : x in S, x != 0 }.
```

If `S` contains no nonzero vector, this value is defined to be `0`. When `S` is
only a subset and not a linear subspace, this is only a restricted sup-ratio; do
not silently invoke linear-operator norm theorems on `S`.

## 3. Lemma: Path-Defect Composition

Let `alpha:c_0->c_1` and `beta:c_1->c_2` be composable paths. Write
`beta circ alpha` for first following `alpha`, then following `beta`. Then

```text
Delta_{beta circ alpha} = T_beta Delta_alpha + Delta_beta U_alpha.
```

### Proof

By definition of path composition,

```text
Delta_{beta circ alpha}
  = T_beta T_alpha Phi_c0 - Phi_c2 U_beta U_alpha.
```

Add and subtract the middle term `T_beta Phi_c1 U_alpha`:

```text
Delta_{beta circ alpha}
  = T_beta (T_alpha Phi_c0 - Phi_c1 U_alpha)
    + (T_beta Phi_c1 - Phi_c2 U_beta) U_alpha
  = T_beta Delta_alpha + Delta_beta U_alpha.
```

Every term has type `H_c0 -> O_c2`. Empty-path cases are consistent with
`Delta_id_c=0`.

## 4. Cycle Defects And Iterated Defects

Let `gamma:c_0->...->c_0` be a finite directed cycle based at `c_0`. Define

```text
Delta_gamma = T_gamma Phi_c0 - Phi_c0 U_gamma : H_c0 -> O_c0.
```

For `n>=1`, define the `n`-fold iterated cycle defect

```text
Delta_{gamma,n}
  = T_gamma^n Phi_c0 - Phi_c0 U_gamma^n : H_c0 -> O_c0.
```

For a subset `S subset H_c0`, one may record the finite quantities

```text
CID_gamma(S) = ||Delta_gamma|_S||
CIC_N(gamma,S) = max_{1<=n<=N} ||Delta_{gamma,n}|_S||.
```

These are finite-object bookkeeping quantities only. They are not observed
collapse, not a black-box mechanism, and not an empirical field.

## 5. Proposition: Finite Cycle Telescoping

For every `n>=1`,

```text
Delta_{gamma,n}
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j.
```

In particular, if `Delta_gamma=0`, then `Delta_{gamma,n}=0` for every finite
`n>=1`.

### Proof

Apply the path-defect composition lemma to `alpha=gamma^n` and `beta=gamma`.
This gives the recurrence

```text
Delta_{gamma,n+1}
  = T_gamma Delta_{gamma,n} + Delta_gamma U_gamma^n.
```

For `n=1`, the proposed formula is the identity

```text
Delta_{gamma,1} = Delta_gamma.
```

Assume the formula holds for `n`. Then

```text
Delta_{gamma,n+1}
  = T_gamma (sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j)
    + Delta_gamma U_gamma^n
  = sum_{j=0}^{n} T_gamma^{n-j} Delta_gamma U_gamma^j.
```

This is the claimed formula with `n+1` in place of `n`. The final statement
follows immediately by substituting `Delta_gamma=0`.

## 6. Proposition: Finite-Horizon Global Norm Bound

Assume

```text
||T_gamma|| <= a,
||U_gamma|| <= b
```

for `a,b>=0`, using the operator norms induced by the declared norms on
`H_c0` and `O_c0`. Then for any subset `S subset H_c0` and any `n>=1`,

```text
||Delta_{gamma,n}|_S||
  <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||.
```

Consequently,

```text
CIC_N(gamma,S)
  <= max_{1<=n<=N} sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||.
```

### Proof

If `S` contains no nonzero vector, the left side is `0` by convention. Otherwise
take any nonzero `x in S`. By the telescoping identity,

```text
Delta_{gamma,n} x
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j x.
```

Using the triangle inequality and submultiplicativity,

```text
||Delta_{gamma,n} x||
  <= sum_{j=0}^{n-1}
       ||T_gamma^{n-1-j}|| ||Delta_gamma|| ||U_gamma^j x||
  <= sum_{j=0}^{n-1}
       a^{n-1-j} b^j ||Delta_gamma|| ||x||.
```

Divide by `||x||` and take the supremum over nonzero `x in S`.

## 7. Restricted-Norm Caveat

The safe proposition above uses the global norm `||Delta_gamma||`. For an
arbitrary subset `S`, do not replace it by `||Delta_gamma|_S||`.

A refined restricted bound requires additional image-control assumptions. For
example, if `S` is a linear subspace, `U_gamma(S) subset S`, and
`||U_gamma|_S|| <= b_S`, then

```text
||Delta_{gamma,n}|_S||
  <= sum_{j=0}^{n-1} a^{n-1-j} b_S^j ||Delta_gamma|_S||.
```

More generally, one must control the sets `U_gamma^j(S)` and the corresponding
restricted sup-ratios. Without such hypotheses, the global bound is the correct
bounded statement.

## 8. Positioning

This note intentionally presents a finite bookkeeping calculus for declared
intertwining defects. It may be close to standard commutator, intertwining, and
path-defect algebra. The present local value is organizational and boundary
disciplining: it collects the Loop3/Loop4 finite identities into one typed note
and keeps programme-level language out of the theorem body.

It does not claim novelty beyond this bounded local formulation.

## 9. Boundary Checklist

Allowed:

- internal v0 local draft;
- finite chart/path/cycle definitions;
- composition identity;
- cycle telescoping identity;
- finite-horizon global norm bound;
- restricted-norm caveat with image-control or invariance.

Forbidden:

- MaoField empirical-positive result;
- full panel, checkpoint loading, inference, training, or new loss claim;
- observed residual, interaction, transport, holonomy, gluing, or collapse field;
- black-box mechanism solved;
- dynamic-collapse theory;
- broad new ANOVA, dependent-input, projection, sheaf, contextuality, or
  path-closure theory;
- NMI-ready, public-ready, paper-ready, or submission-ready claim;
- proof-by-RAG, prompt, handoff, manifest, JSON, harness, or model output.

