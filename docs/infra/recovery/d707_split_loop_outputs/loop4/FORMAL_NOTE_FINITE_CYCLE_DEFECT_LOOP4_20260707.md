# Formal Note: Finite Cycle Defect - Loop 4 - 2026-07-07

Status: `LOOP4_FINITE_CYCLE_DEFECT_DEFINITION`

Scope: finite cycle-defect definitions and finite-horizon iteration under the typed chart/path definitions from Loop 3. This note does not start experiments, does not write a real black-box audit, does not assert empirical positives, and does not introduce dynamic-collapse theory.

Source gate: Loop 0 status line is `READY_FOR_LOOP3`; Loop 3 status line is `READY_FOR_LOOP4`. Loop 0 claim-hygiene artifacts and Loop 3 typed-definition artifacts were consumed before writing this file.

Review gate: the definitions below are finite linear algebra under declared chart data. Promotion into a formal note body remains for Pro A / Main Pro review.

## Claim Boundary

- `Identity is not naming; identity is path closure under declared material relations` remains `PROGRAMME_FRAMING` only.
- Cycle-iteration defect is finite path-defect propagation under declared transports.
- No observed transport, holonomy, gluing, residual, or collapse field is asserted here.
- No black-box mechanism interpretation, empirical MaoField positive result, NMI-ready status, proof-by-JSON, broad ANOVA, sheaf, contextuality, dependent-input, or general projection-theory claim is made here.

## 1. Loop 3 Data Used

Use the Loop 3 finite chart graph `G=(C,E)`. For each chart `c`, the typed data are:

```text
H_c, O_c, ||.||_{H_c}, ||.||_{O_c}, Phi_c:H_c->O_c.
```

For each declared edge `e:c->c'`, the typed transports are:

```text
U_e:H_c->H_{c'}
T_e:O_c->O_{c'}.
```

For a path `alpha:c_0->...->c_k`, Loop 3 defines:

```text
U_alpha:H_{c_0}->H_{c_k}
T_alpha:O_{c_0}->O_{c_k}
Delta_alpha = T_alpha Phi_{c_0} - Phi_{c_k} U_alpha : H_{c_0}->O_{c_k}.
```

No invertibility, isometry, canonical identification, or invariance of a subset `S` is assumed unless explicitly declared.

## 2. Cycle and Cycle Transports

Let `gamma` be a finite directed cycle based at `c_0`:

```text
gamma: c_0 -> c_1 -> ... -> c_m = c_0.
```

With declared edges `e_i:c_{i-1}->c_i`, define the raw cycle transport:

```text
U_gamma = U_{e_m} ... U_{e_1}:H_{c_0}->H_{c_0}.
```

Define the object cycle transport:

```text
T_gamma = T_{e_m} ... T_{e_1}:O_{c_0}->O_{c_0}.
```

Thus `U_gamma` and `T_gamma` are endomorphisms of the base chart spaces, but they are not assumed to be identities, invertible, norm-preserving, or canonical.

## 3. One-Cycle Defect

The finite cycle defect is the Loop 3 path defect for the cycle `gamma`:

```text
Delta_gamma = T_gamma Phi_{c_0} - Phi_{c_0} U_gamma : H_{c_0}->O_{c_0}.
```

Cycle closure at one traversal means:

```text
Delta_gamma = 0.
```

This is a declared-transport statement only. It is not an observation about MaoField data and not a claim about model collapse.

## 4. Restricted Cycle Identity Defect

For `S subset H_{c_0}`, define:

```text
CID_gamma(S) = ||Delta_gamma|_S||.
```

The norm is the Loop 3 restricted sup-ratio using the declared base-chart norms:

```text
||Delta_gamma|_S||
  = sup { ||Delta_gamma x||_{O_{c_0}} / ||x||_{H_{c_0}} : x in S, x != 0 }.
```

If `S` contains no nonzero vector, set `CID_gamma(S)=0`.

If `S` is a linear subspace, this is the usual operator norm of the restricted linear map. If `S` is only a subset, this is only a restricted sup-ratio over `S`; no linear-domain theorem is invoked without an added subspace hypothesis.

## 5. Iterated Cycle Defect

For `n>=1`, let `gamma^n` denote the path obtained by traversing `gamma` exactly `n` times, beginning and ending at `c_0`. By Loop 3 path-composition conventions:

```text
U_{gamma^n}=U_gamma^n:H_{c_0}->H_{c_0}
T_{gamma^n}=T_gamma^n:O_{c_0}->O_{c_0}.
```

Define the `n`-cycle iterated defect:

```text
Delta_{gamma,n}
  = T_gamma^n Phi_{c_0} - Phi_{c_0} U_gamma^n
  : H_{c_0}->O_{c_0}.
```

Equivalently:

```text
Delta_{gamma,n}=Delta_{gamma^n}.
```

For `n=1`, this reduces to:

```text
Delta_{gamma,1}=Delta_gamma.
```

## 6. Finite-Horizon Cycle Iteration Constant

For `N>=1` and `S subset H_{c_0}`, define:

```text
CIC_N(gamma,S)
  = max_{1<=n<=N} ||Delta_{gamma,n}|_S||.
```

This is a finite-horizon quantity. It records the largest restricted iterated defect among the first `N` traversals of a declared finite cycle. It does not assert asymptotic behavior, observed collapse, empirical positivity, or a black-box mechanism.

## 7. Type Check

The types in the cycle and iterated definitions are:

```text
Phi_{c_0}:H_{c_0}->O_{c_0}
U_gamma^n:H_{c_0}->H_{c_0}
T_gamma^n:O_{c_0}->O_{c_0}
T_gamma^n Phi_{c_0}:H_{c_0}->O_{c_0}
Phi_{c_0} U_gamma^n:H_{c_0}->O_{c_0}
Delta_{gamma,n}:H_{c_0}->O_{c_0}.
```

Thus every displayed difference is a typed linear map `H_{c_0}->O_{c_0}`.

## 8. Loop 4 Handoff

The companion files `TELESCOPING_PROOF_LOOP4_20260707.md` and `CYCLE_NORM_BOUNDS_LOOP4_20260707.md` prove the finite telescoping identity and record basic finite-horizon bounds. The boundary file `BOUNDARY_GUARDS_LOOP4_20260707.md` records the forbidden-claim guards.
