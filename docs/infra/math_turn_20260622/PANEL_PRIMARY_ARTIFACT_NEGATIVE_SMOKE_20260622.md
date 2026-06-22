# MaoField q4 Panel Negative Smoke Record

> Generated on node36 at 2026-06-22T21:43:22.
> This is an invalid-artifact smoke record, not a full panel result.

## Boundary

- No checkpoint was loaded.
- No training, backward pass, optimizer step, text generation, or new loss was run.
- These tests only verify that bad schema/provenance inputs fail.

## Result

- Overall status: **pass**
- Generator: `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py`
- Schema: `docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json`

## Cases

| case | expected failure | status | matched text |
|---|---|---|---|
| expected_schema_hash_mismatch | yes | pass | `schema_sha256 mismatch` |
| expected_builder_hash_mismatch | yes | pass | `builder_script_sha256 mismatch` |
| wrong_source_split | yes | pass | `schema source_split must be train` |
| source_hash_mismatch | yes | pass | `input_ids_sha256 mismatch` |
| q4_bin_size_mismatch | yes | pass | `q4 bin sizes mismatch` |

## Wording Guard

- Status: **pass**
- Hits: `0`

## Claim Boundary

This record does not approve full panel generation. It only closes
the first fail-fast negative-smoke requirement from report (6).
