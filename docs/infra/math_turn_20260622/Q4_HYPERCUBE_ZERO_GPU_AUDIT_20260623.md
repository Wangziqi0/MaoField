# MaoField q4 Hypercube Zero-GPU Audit

- Final verdict: `formal_prereg_only`
- Schema: `/media/amd/raid1/canonical/projects/MaoField/docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json`
- Raw glob: `/media/amd/raid1/canonical/wip/maofield_panel_primary_20260622/raw/smoke_seed*_generation*_token_panel.jsonl`
- Raw files: `3`

## Boundary

This audit reads existing smoke raw JSONL rows only. It does not load
checkpoints, run inference, train, generate a full panel, or authorize a
new loss. Its strongest possible conclusion is formal preregistration
feasibility.

## Verdict Reasons

- q4 x token_pos4 cells are non-empty in existing smoke raw rows
- this is not a full panel and does not support a scientific claim

## Occupancy

### `smoke_seed1_generation0_token_panel.jsonl`

- Status: `parsed`
- Seed/generation: `1` / `0`
- q4 x token_pos4 min cell count: `324`
- q4 x token_pos4 max cell count: `690`
- audit_block_id primary-axis decision: `rejected_sparse_high_dimensional_axis`

```text
[[363, 324, 360, 327], [629, 690, 656, 606], [550, 511, 499, 460], [506, 523, 533, 527]]
```
### `smoke_seed2_generation5_token_panel.jsonl`

- Status: `parsed`
- Seed/generation: `2` / `5`
- q4 x token_pos4 min cell count: `324`
- q4 x token_pos4 max cell count: `690`
- audit_block_id primary-axis decision: `rejected_sparse_high_dimensional_axis`

```text
[[363, 324, 360, 327], [629, 690, 656, 606], [550, 511, 499, 460], [506, 523, 533, 527]]
```
### `smoke_seed42_generation9_token_panel.jsonl`

- Status: `parsed`
- Seed/generation: `42` / `9`
- q4 x token_pos4 min cell count: `324`
- q4 x token_pos4 max cell count: `690`
- audit_block_id primary-axis decision: `rejected_sparse_high_dimensional_axis`

```text
[[363, 324, 360, 327], [629, 690, 656, 606], [550, 511, 499, 460], [506, 523, 533, 527]]
```

## Blocked Claims

- `LOSO passed`
- `F3 positive`
- `mean-null vector field survives`
- `residual field observed`
- `glass box broken`
- `training authorized`
- `new loss authorized`
- `full panel approved`
