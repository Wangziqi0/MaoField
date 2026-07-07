# Formal Note: Typed Chart and Path Definitions - Loop 3 - 2026-07-07

Status: `LOOP3_DEFINITION_PATCH`

Scope: definition hygiene for the finite chart/path defect object only. This note does not start experiments, does not assert empirical positives, does not solve a black-box mechanism, and does not expand the theory beyond the local finite-dimensional definitions requested for Loop 3.

Source gate: Loop 0 status line is `READY_FOR_LOOP3`; Loop 0 state lock, claim ledger, forbidden-claims checklist, and source-anchor table were consumed before writing this file.

Review gate: the definitions and the composition lemma are finite linear algebra, but final mathematical promotion remains for Pro A / Main Pro review after Loop 4.

## Claim Boundary

- `Identity is not naming; identity is path closure under declared material relations` is `PROGRAMME_FRAMING` only.
- v1.6 remains finite two-way-table two-projection commutator geometry only.
- The black-box evaluation audit remains a method schema / empirical hypothesis, not a mechanism solution.
- No observed transport, holonomy, gluing, residual, or collapse field is asserted here.
- No NMI-ready, paper-ready, empirical-positive, proof-by-JSON, dynamic-collapse, broad ANOVA, sheaf, contextuality, dependent-input, or general projection-theory claim is made here.

## 1. Ambient Finite Chart System

Let `G=(C,E)` be a finite directed chart graph. A chart label is denoted by `c in C`. An edge is denoted by `e:c->c'`. Multiple declared edges between the same endpoints are allowed if they represent different declared material relations; the edge label is then part of the data.

All vector spaces are over `R`.

For every chart `c`, choose one of the following conventions and keep it explicit:

1. finite-dimensional real Hilbert spaces, with norms induced by their inner products; or
2. finite-dimensional real normed vector spaces, with norms declared as part of the chart data.

The Loop 3 definitions use only finite-dimensional linear maps and the declared norms. Hilbert structure is needed only when a later local result explicitly invokes inner products or orthogonal projections.

No canonical identification, common norm, isometry, invertibility, or transport between distinct charts is assumed unless it is explicitly declared as additional data.

## 2. Chart Data

For each chart `c`, the chart consists of:

- `H_c`: the raw/input chart space, a finite-dimensional real Hilbert space or finite-dimensional real normed vector space.
- `O_c`: the object/output chart space, a finite-dimensional real Hilbert space or finite-dimensional real normed vector space.
- `||.||_{H_c}`: the declared domain norm on `H_c`.
- `||.||_{O_c}`: the declared codomain norm on `O_c`.
- `Phi_c:H_c->O_c`: a linear chart operator.

Domain and codomain convention:

```text
Phi_c in Lin(H_c,O_c)
```

Because the spaces are finite-dimensional, every declared linear map is bounded with respect to the declared norms.

## 3. Edge Data

For each declared directed edge `e:c->c'`, define:

- `U_e = U_{c->c'}:H_c->H_{c'}` as the raw transport.
- `T_e = T_{c->c'}:O_c->O_{c'}` as the object transport.

Linearity and type convention:

```text
U_{c->c'} in Lin(H_c,H_{c'})
T_{c->c'} in Lin(O_c,O_{c'})
```

No edge is assumed invertible, norm-preserving, or canonical. The identity claim across an edge is licensed only when the declared intertwining relation holds:

```text
T_{c->c'} Phi_c = Phi_{c'} U_{c->c'}.
```

The edge defect is the typed linear map:

```text
Delta_{c->c'} = T_{c->c'} Phi_c - Phi_{c'} U_{c->c'} : H_c -> O_{c'}.
```

## 4. Path Data

Let `alpha` be a composable directed path

```text
alpha: c_0 -> c_1 -> ... -> c_k
```

with declared edges `e_i:c_{i-1}->c_i` for `i=1,...,k`.

The raw transport along `alpha` is:

```text
U_alpha = U_{e_k} ... U_{e_1}
        = U_{c_{k-1}->c_k} ... U_{c_0->c_1}
        : H_{c_0} -> H_{c_k}.
```

The object transport along `alpha` is:

```text
T_alpha = T_{e_k} ... T_{e_1}
        = T_{c_{k-1}->c_k} ... T_{c_0->c_1}
        : O_{c_0} -> O_{c_k}.
```

Operators are composed right to left: the map next to the input acts first.

For the empty path `id_c` at chart `c`, define:

```text
U_{id_c} = I_{H_c}:H_c->H_c
T_{id_c} = I_{O_c}:O_c->O_c.
```

For composable paths `alpha:c_0->c_1` and `beta:c_1->c_2`, the composed path `beta circ alpha` means "first `alpha`, then `beta`", with:

```text
U_{beta circ alpha} = U_beta U_alpha : H_{c_0} -> H_{c_2}
T_{beta circ alpha} = T_beta T_alpha : O_{c_0} -> O_{c_2}.
```

## 5. Path Defect

For any composable path

```text
alpha: c_0 -> c_1 -> ... -> c_k,
```

define the path defect:

```text
Delta_alpha = T_alpha Phi_{c_0} - Phi_{c_k} U_alpha : H_{c_0} -> O_{c_k}.
```

The endpoint types are:

```text
T_alpha Phi_{c_0}: H_{c_0} -> O_{c_k}
Phi_{c_k} U_alpha: H_{c_0} -> O_{c_k}
Delta_alpha:       H_{c_0} -> O_{c_k}.
```

For the empty path:

```text
Delta_{id_c} = I_{O_c} Phi_c - Phi_c I_{H_c} = 0 : H_c -> O_c.
```

Path closure along `alpha` means `Delta_alpha=0`. Failure of path closure is measured by `Delta_alpha`, but this file does not assert that any empirical MaoField data exhibits such a failure.

## 6. Restriction and Norm Convention

Let `S subset H_{c_0}`. The restricted defect is the restricted map:

```text
Delta_alpha|_S : S -> O_{c_k}.
```

The norm used for this restriction is always the declared domain norm from `H_{c_0}` and declared codomain norm from `O_{c_k}`:

```text
||Delta_alpha|_S||
  = sup { ||Delta_alpha x||_{O_{c_k}} / ||x||_{H_{c_0}} : x in S, x != 0 }.
```

Convention: if `S` contains no nonzero vector, set `||Delta_alpha|_S||=0`.

If `S` is a linear subspace, this is the usual operator norm of the restricted linear map on `S` with the inherited norm. If `S` is only a subset, this is a restricted sup-ratio over `S`; no linear-domain theorem should be invoked for arbitrary `S` without adding the needed hypothesis.

No assumption is made that `S` is invariant under any `U_gamma`. In particular, do not assume `U_gamma(S) subset S`, `U_gamma^j(S) subset S`, or any comparable control unless it is explicitly stated as an additional hypothesis.

## 7. Composition Lemma Interface

For composable paths `alpha:c_0->c_1` and `beta:c_1->c_2`, the finite linear-algebra composition lemma is:

```text
Delta_{beta circ alpha} = T_beta Delta_alpha + Delta_beta U_alpha.
```

Type check:

```text
Delta_alpha: H_{c_0} -> O_{c_1}
T_beta Delta_alpha: H_{c_0} -> O_{c_2}
U_alpha: H_{c_0} -> H_{c_1}
Delta_beta U_alpha: H_{c_0} -> O_{c_2}
Delta_{beta circ alpha}: H_{c_0} -> O_{c_2}.
```

A detailed proof is recorded in `COMPOSITION_LEMMA_LOOP3_20260707.md`. Pro A review is requested before theorem-body promotion.

## 8. Loop 4 Handoff Boundary

Loop 4 may use these definitions to treat a cycle `gamma:c_0->...->c_0` as a special path and define cycle defects and finite-horizon iterates. Loop 4 should not import empirical claims, black-box mechanism claims, dynamic-collapse claims, or readiness claims.
