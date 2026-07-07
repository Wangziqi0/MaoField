# Cycle Norm Bounds - Loop 4 - 2026-07-07

Status: `FINITE_HORIZON_NORM_BOUNDS_FOR_PRO_REVIEW`

This file records basic norm bounds for the Loop 4 cycle-iteration defect. The bounds are finite-dimensional operator-norm estimates under declared chart norms. They are not empirical MaoField findings and not dynamic-collapse theory.

## Setup

Let `gamma:c_0->...->c_0` be a declared finite cycle. The base-chart maps are:

```text
U_gamma:H_{c_0}->H_{c_0}
T_gamma:O_{c_0}->O_{c_0}
Delta_gamma:H_{c_0}->O_{c_0}.
```

For `n>=1`:

```text
Delta_{gamma,n}
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j.
```

All norms below are induced by the declared base-chart norms from Loop 3.

## Basic Global Bound

Assume:

```text
||T_gamma|| <= a
||U_gamma|| <= b
```

for constants `a,b>=0`. Then for any `S subset H_{c_0}` and any `n>=1`:

```text
||Delta_{gamma,n}|_S||
  <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||.
```

Here `||Delta_gamma||` is the global operator norm from `H_{c_0}` to `O_{c_0}`.

## Proof

For `x in S`, `x != 0`, use the telescoping identity:

```text
Delta_{gamma,n}x
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j x.
```

By the triangle inequality and submultiplicativity:

```text
||Delta_{gamma,n}x||_{O_{c_0}}
  <= sum_{j=0}^{n-1}
       ||T_gamma^{n-1-j}||
       ||Delta_gamma||
       ||U_gamma^j x||_{H_{c_0}}
```

and:

```text
||T_gamma^{n-1-j}|| <= a^{n-1-j}
||U_gamma^j x||_{H_{c_0}} <= b^j ||x||_{H_{c_0}}.
```

Therefore:

```text
||Delta_{gamma,n}x||_{O_{c_0}} / ||x||_{H_{c_0}}
  <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||.
```

Taking the supremum over nonzero `x in S` gives the displayed restricted bound. If `S` contains no nonzero vector, the Loop 3 convention gives `||Delta_{gamma,n}|_S||=0`, so the bound also holds.

## Finite-Horizon Bound For `CIC_N`

For `N>=1`:

```text
CIC_N(gamma,S)
  = max_{1<=n<=N} ||Delta_{gamma,n}|_S||.
```

Under the same hypotheses:

```text
CIC_N(gamma,S)
  <= max_{1<=n<=N}
       sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||.
```

This is a finite maximum over declared bounds. It does not assert asymptotic convergence, divergence, collapse, or empirical behavior.

## Restricted-Defect Refinement

Replacing the global norm `||Delta_gamma||` by `||Delta_gamma|_S||` requires an extra hypothesis. The reason is that the telescoping summand applies `Delta_gamma` to:

```text
U_gamma^j x,
```

not necessarily to a vector still lying in `S`.

A valid sufficient hypothesis is:

```text
U_gamma^j(S) subset S for every 0<=j<=n-1.
```

Together with `||U_gamma||<=b`, this gives:

```text
||Delta_{gamma,n}|_S||
  <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma|_S||.
```

More generally, without invariance of `S`, one may use image-set control. Let:

```text
S_j = U_gamma^j(S).
```

If the restricted sup-ratios `||Delta_gamma|_{S_j}||` and restricted growth factors `||U_gamma^j|_S||` are controlled, then:

```text
||Delta_{gamma,n}|_S||
  <= sum_{j=0}^{n-1}
       a^{n-1-j}
       ||Delta_gamma|_{S_j}||
       ||U_gamma^j|_S||.
```

The invariant-set bound is the special case where `S_j subset S` and `||U_gamma^j|_S||<=b^j`.

## Boundary

These are only finite operator-norm estimates for declared cycle-defect propagation. They are not observed model collapse, not dynamic-collapse theory, not black-box mechanism interpretation, and not an empirical positive result.
