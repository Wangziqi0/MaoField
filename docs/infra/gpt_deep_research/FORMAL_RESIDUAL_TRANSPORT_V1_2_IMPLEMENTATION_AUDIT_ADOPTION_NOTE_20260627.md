# Formal Residual Transport v1.2 Implementation Audit Adoption Note

Date: 2026-06-27 CST

## Source

Archived report:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_implementation_audit_20260627.md
```

This was the GPT-5.5 Pro zero-context audit of the Formal v1.2
implementation-audit bundle prepared after report (28).

## Classification

Node36 adopts report (29) as a Mode A implementation-audit claim-source:

```text
formal_v1_2_patch_requires_minor_revision
```

The report accepted the mathematical core of the v1.2 patch:

- registered ambient before invariant language;
- squared-capture random-subspace Beta statistic;
- exact product-weight Hoeffding theorem and non-product boundary;
- square-holonomy telescoping with correct operator order.

It identified one implementation-level minor revision in the threshold contract
meta-audit:

1. `threshold_contract_single_source_control` had assigned its own `pass`
   instead of routing through `evaluate_test()`.
2. `json_threshold_contract_sha256` was a runtime mirror, not a hash read back
   from a written JSON artifact.

## Local Action Taken

Node36 made the smallest local patch:

- `scripts/debranded_residual_transport_harness_v1_2.py`
  - adds an `evaluate_test()` branch for `threshold_contract_single_source_control`;
  - makes the meta-block metrics-only before evaluation;
  - marks all evaluated blocks with `evaluated_by="evaluate_test"`;
  - performs a two-phase JSON write/readback so the final meta-block records
    `json_threshold_contract_source=readback_from_written_json_threshold_contract`.
- `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md`
  - updates the threshold contract description to match the repaired harness.
- `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md`
  and `synthetic_harness_v1_2_20260627.json`
  - regenerated from node36 SSD scratch after the minor revision.

Validation scratch:

```text
/home/amd/codex-node36/tmp/maofield-formal-v12-minor-20260627_1505/
```

Post-revision harness facts:

```text
all_synthetic_controls_passed=true
threshold_contract_sha256=0bb99a4a711405fb65e81413cfd283d6e68d0ecd4e9c34dc027c052f332110e0
threshold_contract_single_source_control.pass=true
threshold_contract_single_source_control.evaluated_by=evaluate_test
threshold_contract_single_source_control.json_threshold_contract_source=readback_from_written_json_threshold_contract
threshold_contract_single_source_control.per_test_threshold_mismatches=[]
```

## Allowed Interpretation

This closes the report (29) minor revision at the level of local
finite-dimensional synthetic harness consistency.

Strongest local verdict remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## Still Forbidden

This adoption note does not authorize:

- completed formal system;
- full panel;
- 16-cell full-panel aggregate;
- checkpoint loading;
- model inference;
- training;
- new loss;
- observed MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- glass-box-broken language;
- F3-positive or LOSO-passed language.

The next Pro task should be a narrow zero-context audit of the repaired v1.2
threshold-contract minor revision, not a new broad design pass and not a
MaoField empirical validation.
