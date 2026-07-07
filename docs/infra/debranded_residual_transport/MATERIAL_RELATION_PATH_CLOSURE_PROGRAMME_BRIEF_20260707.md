# Material-Relation Path Closure For Finite Metric Objects

Date: 2026-07-07 CST

Status:

```text
PROGRAMME_LEVEL_SYNTHESIS_AND_NEXT_PROOF_TASK_SOURCE
```

This brief incorporates Report34 as a bounded research-direction synthesis.
It does not modify the current Zenodo V2.5 preprint and does not promote any
MaoField empirical claim.

Source:

```text
docs/infra/gpt_deep_research/deep_research_material_relation_path_closure_report34_20260707.md
docs/infra/gpt_deep_research/MATERIAL_RELATION_PATH_CLOSURE_REPORT34_ADOPTION_NOTE_20260707.md
```

## 1. Core Sentence

```text
Identity is not naming; identity is path closure under material relations.
```

Chinese working form:

```text
同一性不是命名，而是物质关系中的路径闭合。
```

This sentence is a programme-level framing. It is not itself a theorem.

## 2. Four-Layer Spine

The current research subject should be organized as four layers:

| Layer | Name | Question | Current Carrier |
|---|---|---|---|
| 1 | finite order-defect spine | do two stripping paths identify the same object? | `D_w=R_{Q->B}-R_{B->Q}` |
| 2 | quantitative OI geometry | how large is the finite order artifact? | `OI^{op}_{N_add}(w)=||D_w|_{N_add}||` |
| 3 | finite cycle identity defect | does a charted object close around a finite loop? | `Delta_gamma=T_gamma Phi-Phi U_gamma` |
| 4 | black-box metric-object audit | can black-box evaluation outputs be legally compared as the same metric object? | declared chart, transport, and defect certificate |

The first two layers are currently supported by bounded exact notes. The third
and fourth layers are next-task definitions, not established broad theories.

## 3. Current Exact Spine

The current exact finite spine is:

```text
X = Q x B
w(q,b)>0
L2(w) = R^{Q x B}
C = span{1}
A = centered q-main effects
B0 = centered b-main effects
N_add = C direct-sum A direct-sum B0
```

Ordered stripping maps:

```text
R_{Q->B} = (I-P_B0)(I-P_A)(I-P_C)
R_{B->Q} = (I-P_A)(I-P_B0)(I-P_C)
```

Order-defect operator:

```text
D_w = R_{Q->B} - R_{B->Q}
    = P_B0 P_A - P_A P_B0
```

The v1.3 and D706 companion claims remain bounded:

```text
OI^{op}_{N_add}(w)=0 iff w(q,b)=w_Q(q)w_B(b)
```

The D707 v1.6 quantitative companion is:

```text
OI^{op}_{N_add}(w)
  = max_j rho_j sqrt(1-rho_j^2),
```

where `rho_j` are principal-angle / canonical-correlation invariants between
`A` and `B0`, equivalently nonzero singular values of
`Z_w=(w-w_Q otimes w_B)/sqrt(w_Q w_B)`.

## 4. Programme Translation

Safe translation:

```text
material relation
  -> declared chart operation
  -> finite path closure / failure
  -> identity licensed / not licensed
```

In this translation:

| Concept | Finite Object | Safe Reading |
|---|---|---|
| material relation | `w(q,b)` or declared chart data | concrete relation structure, not a name |
| mediation | `w-w_Q otimes w_B`, `U`, `T` | finite coupling or declared transport |
| practice path | ordered stripping or chart path | actual operation sequence |
| identity condition | commutation / intertwining / closure | conditional identity license |
| non-identity certificate | `D_w`, `Delta`, `Delta_gamma` | exact finite obstruction |

Philosophy guides the object choice and wording discipline. It does not
replace proof.

## 5. Finite Chart Defect Candidate

For a finite chart `c`, let:

```text
H_c = raw audit table space
O_c = processed metric-object space
Phi_c: H_c -> O_c
```

For two charts `c,c'`, declared raw and object transports are:

```text
U_{c->c'}: H_c -> H_{c'}
T_{c->c'}: O_c -> O_{c'}
```

The finite identity license is the intertwining condition:

```text
T_{c->c'} Phi_c = Phi_{c'} U_{c->c'}.
```

The edge defect is:

```text
Delta_{c->c'} = T_{c->c'} Phi_c - Phi_{c'} U_{c->c'}.
```

If `Delta_{c->c'} K != 0`, then same-named metric outputs are not licensed as
the same metric object on witness `K`.

This is a candidate finite definition to be audited by Pro.

## 6. Cycle Identity Defect Candidate

For a closed finite path:

```text
gamma: c_0 -> c_1 -> ... -> c_k = c_0
```

with composed transports `U_gamma` and `T_gamma`, define:

```text
Delta_gamma = T_gamma Phi_{c_0} - Phi_{c_0} U_gamma.
```

For a finite audit subspace `S subset H_{c_0}`:

```text
CID_gamma(S) = || Delta_gamma |_S ||.
```

For repeated loop execution:

```text
Delta_{gamma,n} = T_gamma^n Phi_{c_0} - Phi_{c_0} U_gamma^n
CIC_N(gamma,S) = max_{1<=n<=N} || Delta_{gamma,n} |_S ||.
```

Finite telescoping identity to verify:

```text
Delta_{gamma,n}
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j.
```

If the one-loop defect is zero, all iterates close. If it is nonzero, finite
iteration defect can be bounded under explicit norm assumptions. This is a
bounded finite-linear-algebra task, not a broad dynamic-collapse theory.

## 7. Black-Box Metric-Object Audit

For a black-box model `M`, a declared evaluation chart produces:

```text
K_c(M) in H_c
O_c(M) = Phi_c K_c(M)
```

The programme does not claim to open the model mechanism. It first asks whether
the external metric object is identical across charts:

```text
T_{c->c'} Phi_c K_c(M)
  = Phi_{c'} U_{c->c'} K_c(M).
```

If this fails, then the cross-chart ability identity claim is not licensed.

Safe claim:

```text
MaoField provides a finite metric-object identity audit programme for black-box
evaluation outputs.
```

Unsafe claim:

```text
MaoField solves all AI black-box mechanisms.
```

## 8. Boundaries

This brief does not authorize:

- MaoField empirical positive result;
- full panel, checkpoint loading, inference, training, or new loss;
- observed residual, interaction, transport, holonomy, gluing, or collapse
  field;
- broad ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof by deterministic harness, JSON, or model output;
- current Zenodo V2.5 preprint patching.

Mode B remains:

```text
insufficient_artifact
```
