# MaoField q4 Hypercube Interaction Smoke Audit

- Final verdict: `smoke_conjecture_only`
- Schema: `/media/amd/raid1/canonical/projects/MaoField/docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json`
- Raw files: `3`

## Boundary

This audit reads existing smoke raw JSONL rows only. It does not load
checkpoints, run inference, train, generate a full panel, authorize a new
loss, or establish a scientific result.

## Interaction Object

For each smoke checkpoint, this audit forms a 4 x 4 cell-mean logprob
matrix over `Q_freq4 x B_tokenpos4`, then subtracts the weighted additive
subspace spanned by a constant term, q4 frequency main effects, and
token-position main effects. The residual is a smoke-only interaction
field candidate.

## Per-File Summary

### `smoke_seed1_generation0_token_panel.jsonl`

- Seed/generation: `1` / `0`
- Mean-null norm: `1.54346036175`
- Interaction residual norm: `0.154697177312`
- Interaction / mean-null ratio: `0.100228`

### `smoke_seed2_generation5_token_panel.jsonl`

- Seed/generation: `2` / `5`
- Mean-null norm: `1.7217832238`
- Interaction residual norm: `0.192098159622`
- Interaction / mean-null ratio: `0.111569`

### `smoke_seed42_generation9_token_panel.jsonl`

- Seed/generation: `42` / `9`
- Mean-null norm: `1.64914623863`
- Interaction residual norm: `0.179455359478`
- Interaction / mean-null ratio: `0.108817`

## Cross-Smoke Shape

- `smoke_seed1_generation0_token_panel.jsonl` vs `smoke_seed2_generation5_token_panel.jsonl`: `0.948185`
- `smoke_seed1_generation0_token_panel.jsonl` vs `smoke_seed42_generation9_token_panel.jsonl`: `0.947159`
- `smoke_seed2_generation5_token_panel.jsonl` vs `smoke_seed42_generation9_token_panel.jsonl`: `0.969198`

- Weighted uncentered singular values: `[0.3006574328979052, 0.0397940554598102, 0.032537468204918006]`
- Weighted uncentered sigma2/sigma1: `0.13235679915261944`
- Weighted row-centered sigma2/sigma1: `0.677982315704983`
- Unweighted uncentered sigma2/sigma1: `0.1465017784812324`

## Verdict

The interaction pattern is reproducible as a small smoke-derived
calculation, but this is not a full panel and cannot support a
scientific or philosophical claim. The low uncentered sigma2/sigma1
also warns that the three-smoke pattern is close to one dominant shape.

Missing controls before promotion: random equal-size token-position
partition controls, within-q token-position shuffle controls, bad-axis
controls, cell variance/noise modeling, held-out seed tests, and
generation-block leave-out tests.

## Blocked Claims

- `LOSO passed`
- `F3 positive`
- `mean-null vector field survives`
- `residual field observed`
- `hypercube residual observed`
- `glass box broken`
- `training authorized`
- `new loss authorized`
- `full panel approved`
