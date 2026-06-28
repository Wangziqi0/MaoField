# Formal Residual Transport v1.3 Order-Defect Proof-Audit Adoption Note

Date: 2026-06-28 CST
Scope: node36 adoption of report (32), archived as
`deep_research_formal_residual_transport_v1_3_order_defect_proof_audit_20260628.md`.

Report attachment sha256:

```text
a41cb203f5ac66138898822bad5fa84f8be4ecdebbb57620dd45c9e751df2d97
```

## Adopted Classification

```text
formal_v1_3_order_defect_proof_audit_accepted_with_minor_arithmetic_correction_and_claim_guards
```

Node36 adopts report (32) as a Mode A finite-dimensional proof audit source
for the weighted ANOVA order-defect target selected by report (31). The
report's internal classification was:

```text
v1_3_order_defect_proof_plan_accepted
```

The node36 adoption is narrower and evidence-gated: it accepts the T1/T2/T3
finite-dimensional proof direction and the three-block deterministic
zero-GPU harness target, while recording a minor arithmetic correction in one
optional symmetric witness.

## What This Accepts

The accepted v1.3 mathematical content is:

1. For finite positive weights on `Q x B`, product form is equivalent to
   weighted orthogonality of the zero-mean q-only subspace `A` and zero-mean
   b-only subspace `B0`.
2. The ordered residual-stripping operators
   `R_Q_then_B=(I-P_B0)(I-P_A)(I-P_C)` and
   `R_B_then_Q=(I-P_A)(I-P_B0)(I-P_C)` are equal iff the weight is product
   form.
3. If the weight is not product form, then there exists a pure main-effect
   witness whose true orthogonal additive residual is zero but whose
   wrong-order sequential stripping residual is nonzero.
4. The nonzero wrong-order output is a `sequential stripping artifact` or
   `interaction-like artifact`, not a true interaction residual and not a
   product-measure Hoeffding interaction.

This supports writing a local v1.3 proof note and a deterministic zero-GPU
synthetic harness. It does not complete the broader formal system.

## Arithmetic Correction

Report (32)'s main `B0` witness is correct. For

```text
w=(1,2,3,5)/11
K=(7/11,-4/11,7/11,-4/11) in B0
```

the verified coordinates are:

```text
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

Report (32)'s optional symmetric `A` witness coordinates had an 11x scaling
slip. For

```text
K'=(8/11,8/11,-3/11,-3/11) in A
```

the corrected coordinates are:

```text
R_Q_then_B K' = 0
R_B_then_Q K' = (1/42, -1/84, 5/224, -3/224)
```

This correction does not affect T1, T2, or the main T3 witness.

## Local Follow-Through

Node36 implements the accepted proof-audit target here:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
scripts/debranded_residual_transport_harness_v1_3.py
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
```

The v1.3 harness has no random draws and no MaoField data reads. It checks:

```text
product_weight_order_independence_control
centered_indicator_product_iff_control
nonproduct_pure_main_effect_no_go_control
threshold_contract_single_source_control
```

## Evidence Boundary

Report (32), the local proof note, and the v1.3 synthetic harness are Mode A
finite-dimensional mathematics artifacts. They do not add MaoField data, load
checkpoints, run inference, run a full panel, or authorize training/new loss
work.

Strongest allowed local status remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## Still Forbidden

This adoption does not authorize any of the following claims:

- completed formal system;
- theorem stack complete;
- Formal v1.3 completed as a whole system;
- empirical MaoField upgrade;
- full panel has run;
- 16-cell full-panel aggregate exists;
- checkpoint loading, inference, training, or new loss is authorized;
- observed MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- glass box broken;
- LOSO passed;
- F3 positive;
- all non-product-weight inputs show order dependence.

The correct T2 quantifier is existential: non-product weights imply the two
ordered operators are unequal, so some witness signal shows order dependence.
Constants and true `N_add^perp` residuals can still agree under both orders.

## Next Allowed Step

The next useful GPT-5.5 Pro task is a strict audit of the local v1.3 proof note
and deterministic harness:

- verify definitions and projection notation;
- check T1, T2, and T3 line by line;
- verify exact rational witness coordinates, including the corrected symmetric
  witness;
- audit the v1.3 script, JSON, and summary;
- return PASS/WARN/FAIL for definitions, T1, T2, T3, harness, and claim
  boundary.

No full-panel, checkpoint, training, or MaoField empirical work is implied.
