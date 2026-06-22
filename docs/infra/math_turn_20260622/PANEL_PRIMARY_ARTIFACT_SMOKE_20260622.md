# MaoField q4 Panel Generator Smoke Record

> Generated on node36 at 2026-06-22 17:36 CST.
> This is a generator smoke record, not a full panel verdict.

## Boundary

The smoke run validates that the q4 locked-schema generator can:

- reload the fixed Wikitext-2 train audit blocks;
- verify schema/source hashes;
- load exactly one alpha0 checkpoint on CPU fp32;
- write one-checkpoint q4 aggregates and raw token rows;
- reproduce the existing high-order aggregate row for seed1/gen0.

It does not generate the 50-checkpoint panel and does not change the current
project verdict:

```text
current aggregate verdict = insufficient_artifact
current math turn status   = blocked-until-gated
```

No training, optimizer step, backward pass, EMA update, new loss, or text
generation was run.

## Inputs

```text
schema = docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json
schema_sha256 = 25027448058bab6e79aa27f5c96446ccdfed85a01855a0d6d60db244c84d64d7
generator = experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py
checkpoint = experiments/exp018_cat/data/checkpoints_armb/alpha0.0/no_preserve_seed1/generation_0
source_split = train
device = cpu
dtype = float32
```

## Commands

```bash
HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false \
  /home/amd/venv/bin/python \
  experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py \
  --manifest-only

HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false \
  /home/amd/venv/bin/python \
  experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py \
  --one-checkpoint-smoke --seed 1 --generation 0
```

## Outputs

Committed small artifacts:

```text
experiments/exp020_metric_stress_test/panel_primary_20260622/manifest_only_20260622.json
experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed1_gen0_manifest.json
experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed1_gen0_aggregate.json
```

Raw token rows are outside git:

```text
/media/amd/raid1/canonical/wip/maofield_panel_primary_20260622/raw/smoke_seed1_generation0_token_panel.jsonl
sha256 = 90e5104f714306f7e1eaa7c14b26aa8333f4c42ad0e684521e757efa992d5dbe
n_rows = 8064
```

## Gate Results

Manifest-only:

```text
data_source_gate = pass
schema_freeze_gate = pass
full_panel_generated = false
training_authorized = false
```

One-checkpoint smoke:

```text
data_source_gate = pass
schema_freeze_gate = pass
one_checkpoint_smoke = pass
old_aggregate_reproduction = pass
full_panel_generated = false
training_authorized = false
elapsed_s = 2.271
```

Existing aggregate row reproduction for seed1/gen0:

```text
mean_lp          abs_diff = 0.0
F1_var          abs_diff = 0.0
F1_tail         abs_diff = 0.0
F3_slice_rare   abs_diff = 0.0
F3_slice_freq   abs_diff = 0.0
F3_slice_gap    abs_diff = 0.0
```

## q4 Smoke Aggregate

```text
n_tokens = 8064
global_mean_lp = -3.1623525619506836
global_ppl = 23.626112493679635
primary_projection_P = 1.4694237198551585
```

Slice rows:

| slice_id | n_tokens | mean_logprob |
|---:|---:|---:|
| 0 | 1374 | -5.237409591674805 |
| 1 | 2581 | -4.247951030731201 |
| 2 | 2020 | -2.304041862487793 |
| 3 | 2089 | -1.2862061262130737 |

## Claim Boundary

This smoke pass only shows that the generator is aligned with the locked q4
schema and the old aggregate computation for one checkpoint. It does not
authorize:

```text
LOSO passed
F3 positive
mean-null vector field survives
glass box broken
training authorized
new loss authorized
```

## Post-Review Decision

PRO report (6), archived after this smoke record, does not approve a full
50-checkpoint q4 panel generation yet. The next allowed work is provenance
cleanup, fail-fast negative smokes, multi-checkpoint smoke coverage, and a
separate fold-local q4 analysis path before PI/PRO revisits the launch decision.
