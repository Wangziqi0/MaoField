# Math Proof Rescue Audit 2026-06-29

Generated: `2026-06-29 21:28:29 CST +0800`

This audit summarizes current local proof state. It is not a new theorem and not a paper draft.

## Current Mathematical Object

- finite set `X = Q x B`;
- positive weights `w(q,b)>0`, normalized to probability weights;
- weighted Hilbert space with `<f,g>_w = sum w f g`;
- constant subspace `C`;
- centered row/main-effect space `A`;
- centered column/main-effect space `B0`;
- additive nuisance `N_add = C + A + B0`.

Primary setup lines: `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:43`, `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:64`.

## Theorem Statements And Status

| theorem/object | current file | proof status | dependency | script/harness relation |
| --- | --- | --- | --- | --- |
| product-weight iff A perpendicular B0 | docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md | COMPLETE_LOCAL_DRAFT | finite sums; centered indicators | harness has regression control; exact script not primary |
| order-independence iff product weights | docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md | PLAUSIBLE_LOCAL_DRAFT | commutator D_w and Proposition 1 | v1.3 harness controls product/nonproduct cases |
| pure-main-effect non-product artifact | docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md | PLAUSIBLE_LOCAL_DRAFT | nonorthogonality gives existential witness | exact 2x2 certificate verifies one witness |
| exact 2 x 2 rational witness | docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md | CERTIFICATE | fractions.Fraction script | exact script output is certificate-level example |

## Specific Risk Checks

- Existential vs universal: guarded at `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:237`.
- Wrong-order residual vs true interaction residual: guarded at `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`.
- `P_N` residual vs sequential stripping output: exact witness states `(I-P_N)K = 0` while wrong-order output is nonzero; see `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:318`.
- Noncommuting projection overclaim: bibliography file explicitly says not new projection theory at `docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:29`.
- Holonomy/curvature/sheaf/gluing: old exploratory words exist in prior audit trail; they are not part of current order-defect claim.

## Exact 2 x 2 Rational Witness

```text
w = (1/11) [[1,2],
            [3,5]]
K = ['7/11', '-4/11', '7/11', '-4/11']
(I-P_N)K = ['0', '0', '0', '0']
R_B_then_Q K = ['0', '0', '0', '0']
R_Q_then_B K = ['1/32', '5/168', '-1/96', '-1/84']
||R_Q_then_B K||_w^2 = 61/177408
```

Script path: `scripts/debranded_residual_transport_exact_witness_v1_4.py`.
JSON path: `docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`.

Canonical exact JSON sha256: `0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6`.
Scratch rerun exact JSON sha256: `0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6`.
Exact rerun identical to canonical: `true`.

Canonical harness JSON sha256: `283378e1d5f515d57be1ec6348c068b4b1b33af49439086ef8cce53b364a65fc`.
Scratch harness rerun JSON sha256: `bab7f5baa31a4d5c0981e8681c5acf1cbd936cc198ee4c0183f59b084ceb928c`.
Harness rerun note: hash may differ because `created_utc` is runtime-specific; all synthetic controls passed in rerun if JSON field `all_synthetic_controls_passed` is true.

## Proof Responsibility Boundary

The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
