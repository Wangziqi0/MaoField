# Wording Lock v1.6 -- Harness Boundary

Date: 2026-06-29 CST
Classification: core/wip wording lock
Source audit: `../gpt_deep_research/deep_research_order_defect_v1_5_final_gate_audit_20260629.md`

## Canonical Sentence

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

## Scope

This v1.6 lock closes the narrow wording WARN from the v1.5 final-gate audit.
It does not add a new theorem, does not change the exact rational witness, and
does not upgrade any MaoField empirical status.

The sentence must appear verbatim in:

- `README.md`;
- `PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`;
- `SYNTHETIC_HARNESS_V1_3_20260628.md`;
- `synthetic_harness_v1_3_20260628.json`;
- `../../../scripts/debranded_residual_transport_harness_v1_3.py`.

## Claim Ceiling

Allowed:

```text
definitions_and_harness_viable_only
```

Blocked:

```text
full_panel_has_run
sixteen_cell_full_panel_aggregate_exists
residual_field_observed
interaction_field_observed
quotient_residual_field_observed
transport_field_observed
holonomy_field_observed
glass_box_broken
LOSO_passed
F3_positive
training_authorized
new_loss_authorized
completed_formal_system
formal_v1_3_completed
```
