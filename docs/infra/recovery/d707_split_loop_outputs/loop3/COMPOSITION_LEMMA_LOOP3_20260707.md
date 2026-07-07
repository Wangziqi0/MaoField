# Composition Lemma - Loop 3 - 2026-07-07

Status: `FINITE_LINEAR_ALGEBRA_LEMMA_FOR_PRO_REVIEW`

This file proves the typed composition identity needed before Loop 4. It is local finite linear algebra under the definitions in `FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`. Pro A review remains required before promotion into any formal note body.

## Setup

Let

```text
alpha:c_0 -> c_1
beta: c_1 -> c_2
```

be composable declared paths. Here `alpha` and `beta` may themselves be multi-edge paths, as long as the endpoint of `alpha` is the startpoint of `beta`.

By Loop 3 definitions:

```text
U_alpha:H_{c_0}->H_{c_1}
T_alpha:O_{c_0}->O_{c_1}
Delta_alpha = T_alpha Phi_{c_0} - Phi_{c_1} U_alpha : H_{c_0}->O_{c_1}
```

and

```text
U_beta:H_{c_1}->H_{c_2}
T_beta:O_{c_1}->O_{c_2}
Delta_beta = T_beta Phi_{c_1} - Phi_{c_2} U_beta : H_{c_1}->O_{c_2}.
```

The composed path `beta circ alpha` means first `alpha`, then `beta`. Therefore:

```text
U_{beta circ alpha}=U_beta U_alpha:H_{c_0}->H_{c_2}
T_{beta circ alpha}=T_beta T_alpha:O_{c_0}->O_{c_2}.
```

## Lemma

For composable paths `alpha:c_0->c_1` and `beta:c_1->c_2`,

```text
Delta_{beta circ alpha} = T_beta Delta_alpha + Delta_beta U_alpha.
```

## Type Check

The left-hand side is:

```text
Delta_{beta circ alpha}:H_{c_0}->O_{c_2}.
```

The first right-hand term is typed because:

```text
Delta_alpha:H_{c_0}->O_{c_1}
T_beta:O_{c_1}->O_{c_2}
T_beta Delta_alpha:H_{c_0}->O_{c_2}.
```

The second right-hand term is typed because:

```text
U_alpha:H_{c_0}->H_{c_1}
Delta_beta:H_{c_1}->O_{c_2}
Delta_beta U_alpha:H_{c_0}->O_{c_2}.
```

Thus every term in the claimed identity is a linear map `H_{c_0}->O_{c_2}`.

## Proof

Starting from the definition of path defect for the composed path:

```text
Delta_{beta circ alpha}
  = T_{beta circ alpha} Phi_{c_0}
    - Phi_{c_2} U_{beta circ alpha}
```

Use the path-composition definitions:

```text
Delta_{beta circ alpha}
  = T_beta T_alpha Phi_{c_0}
    - Phi_{c_2} U_beta U_alpha.
```

Add and subtract the middle typed term `T_beta Phi_{c_1} U_alpha`:

```text
Delta_{beta circ alpha}
  = T_beta T_alpha Phi_{c_0}
    - T_beta Phi_{c_1} U_alpha
    + T_beta Phi_{c_1} U_alpha
    - Phi_{c_2} U_beta U_alpha.
```

Group the first two terms and the last two terms:

```text
Delta_{beta circ alpha}
  = T_beta (T_alpha Phi_{c_0} - Phi_{c_1} U_alpha)
    + (T_beta Phi_{c_1} - Phi_{c_2} U_beta) U_alpha.
```

Recognize the two defects:

```text
Delta_{beta circ alpha}
  = T_beta Delta_alpha + Delta_beta U_alpha.
```

This proves the identity as a finite-dimensional linear-map equality.

## Empty Path Check

For the empty path `id_c`:

```text
Delta_{id_c}=0:H_c->O_c.
```

If `alpha=id_{c_0}`, then `beta circ alpha=beta`, `U_alpha=I_{H_{c_0}}`, and:

```text
T_beta Delta_alpha + Delta_beta U_alpha
  = T_beta 0 + Delta_beta I_{H_{c_0}}
  = Delta_beta.
```

If `beta=id_{c_1}`, then `beta circ alpha=alpha`, `T_beta=I_{O_{c_1}}`, `Delta_beta=0`, and:

```text
T_beta Delta_alpha + Delta_beta U_alpha
  = I_{O_{c_1}} Delta_alpha + 0 U_alpha
  = Delta_alpha.
```

Thus the composition lemma is consistent with the empty-path identities.

## Loop 4 Use

Loop 4 may apply this lemma to powers of a cycle `gamma` to obtain the recurrence for iterated cycle defects. Loop 4 must still check domains, codomains, restriction norms, and any extra invariance or growth hypotheses separately.
