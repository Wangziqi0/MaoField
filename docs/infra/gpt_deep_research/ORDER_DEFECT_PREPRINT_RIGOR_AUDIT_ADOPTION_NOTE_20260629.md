# Order-Defect Preprint Rigor Audit Adoption Note

Date: 2026-06-29 CST
Machine authority: node36
Source report:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_preprint_rigor_audit_20260629.md
attachment_sha256=d2693abc4aea8623540a4c3cb7038f1a3c8cc59b16a5cf4a4e56b9f809bc5ce0
```

## Local Adoption Verdict

```text
revise_first_before_preprint_package
```

The report's top-level classification was:

```text
preprint_placeholder_requires_related_work_reframing
```

Node36 adopts the narrow mathematical part only:

- T1/T2/T3 are locally consistent with the finite positive-weight setup in
  `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`.
- The main 2x2 witness coordinates and norm square remain correct.
- The optional symmetric witness remains corrected relative to report (32).
- The harness is clean deterministic regression support, not a proof artifact.

Node36 does not adopt any external-bibliography claim as final until durable
records are verified. Chat-internal citation handles in the source report are
not accepted as bibliography.

## Required Fixes Before External Preprint

1. Add an exact rational witness certificate for the 2x2 example.
2. Dump exact projection / commutator matrices for `P_C`, `P_A`, `P_B0`,
   `P_N`, and `D_w`.
3. Make every harness mention explicitly regression-support-only.
4. Replace broad or project-internal terms such as "diagnostic field" with
   "finite weighted two-way array/table" in outward-facing text.
5. Verify durable related-work records for Hooker-style weighted functional
   ANOVA diagnostics, dependent-input Hoeffding/Sobol/Shapley work, and
   noncommuting two-projection / projection-commutator literature.
6. Keep holonomy, gluing, sheaf, curvature, empirical residual field, and
   MaoField-positive language out of the next package except as blocked or
   explicitly out of scope.

## Local Fixes Applied

This adoption pass adds:

```text
scripts/debranded_residual_transport_exact_witness_v1_4.py
docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
```

The exact certificate uses `fractions.Fraction`, has no random draws, and
verifies:

- zero true additive residual for the main `B0` witness;
- zero opposite-order residual for the main `B0` witness;
- exact artifact vector `(1/32, 5/168, -1/96, -1/84)`;
- exact norm square `61/177408`;
- zero true additive residual for the symmetric `A` witness;
- exact symmetric artifact vector `(1/42, -1/84, 5/224, -3/224)`;
- exact equality between the order-defect operator and the projection
  commutator in the 2x2 case;
- nonzero order defect.

## Evidence Boundary

Allowed ceiling remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField status remains:

```text
insufficient_artifact
```

Forbidden upgrades:

- MaoField empirical positive result;
- full panel completion or 16-cell aggregate;
- observed residual, interaction, quotient-residual, transport, or holonomy
  field;
- F3 positive, LOSO passed, glass-box broken;
- checkpoint loading, inference, training, or new loss authorization;
- completed formal system;
- broad new ANOVA theory;
- broad new noncommuting projection theory.

## Next Pro Task

Send a revised package to GPT-5.5 Pro for a narrow second-pass audit:

- exact-symbolic appendix / certificate;
- proof text unchangedness after wording edits;
- harness boundary wording;
- durable bibliography and duplicate-risk check;
- final preprint-readiness gate.

Do not ask for more roadmap generation in this pass.
