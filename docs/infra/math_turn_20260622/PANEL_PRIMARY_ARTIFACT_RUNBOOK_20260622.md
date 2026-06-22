# MaoField Math-Turn Panel Primary Artifact Runbook

> Status: locked primary q4 schema, no panel artifact generated yet.
> Generated on node36 at 2026-06-22 17:08 CST.

## Boundary

This runbook locks the data source, primary slice schema, and audit gates for
the next raw-logprob/checkpoint panel artifact. It does not report a panel
result and does not change the current project verdict:

```text
current aggregate verdict = insufficient_artifact
current math turn status   = blocked-until-gated
```

No GPU training, optimizer step, backward pass, EMA update, new loss
implementation, or model-generated text is authorized by this runbook.

## Locked Files

Schema builder:

```text
scripts/build_panel_schema_20260622.py
sha256 = ad71fdb55258b4a1b26bfcf28aa9893fba52a358bbd6b1a03670579677932969
```

Locked schema JSON:

```text
docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json
sha256 = 25027448058bab6e79aa27f5c96446ccdfed85a01855a0d6d60db244c84d64d7
```

Rebuild command:

```bash
HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false \
  /home/amd/venv/bin/python scripts/build_panel_schema_20260622.py
```

The rebuild must reproduce the schema hashes below before any checkpoint
inference output is accepted.

## Data Source

The fixed audit blocks are the first 128 blocked sequences from Wikitext-2
raw-v1 train split, matching the existing high-order audit source.

```text
dataset_id                  = wikitext
dataset_config              = wikitext-2-raw-v1
source_split                = train
tokenizer_id                = facebook/opt-125m
block_size                  = 64
audit_block_indices         = 0..127
n_audit_blocks              = 128
n_next_token_positions      = 8064
n_unique_target_tokens      = 2225
input_ids_sha256            = 36ab5539fd93af5f83ca972204f463b2a4a26fd7782a6aca6c3aa60149ca6a04
target_ids_sha256           = 3b9ba1a5782857a11ce71b3c3ff8814ed7fbcd5e047da0e66a803f2bc2db8b7b
target_counts_sha256        = 9ccda56cbf334b807276352645e96b1910b03e7e01e3b8f3f00904b5f58ef221
```

Any artifact or report that calls this Wikitext validation/test data, or uses
`eval_split` instead of `source_split=train`, is `invalid_artifact`.

## Primary Schema

Primary schema:

```text
schema_id                   = freq_q4_audit_targets_20260622
role                        = primary
frequency_reference          = target_count_audit_blocks
quantile_library             = numpy.quantile
quantile_method              = nearest
assignment_policy            = np.searchsorted(edges, frequency, side='right')
edge_inclusivity             = right side by searchsorted side='right'
empty_bin_policy             = abort
edges                        = [2, 10, 73]
bin_sizes                    = [1374, 2581, 2020, 2089]
empty_bins                   = []
min_frequency                = 1
max_frequency                = 428
```

Primary projection is the q4 ordered frequency-slope projection. For each row,
let `k_j = mean_logprob(slice_j)`, `w_j = n_j / sum_j n_j`, and
`D = sum_j w_j k_j`. Define `u_j = k_j - D`. The only primary scalar projection
is:

```text
v_raw = [-1.5, -0.5, 0.5, 1.5]
v     = weighted_center_and_unit_normalize(v_raw, weights=w)
P     = sum_j w_j * v_j * u_j
```

No other projection can trigger the strongest verdict.

## Sensitivity Schema

The attempted q8 schema is not locked:

```text
schema_id   = freq_q8_audit_targets_20260622
role        = sensitivity_only
status      = not_locked_empty_bin
edges       = [1, 2, 5, 10, 39, 73, 238]
bin_sizes   = [0, 1374, 1531, 1050, 1077, 943, 1062, 1027]
empty_bins  = [0]
```

Because the preregistered edge policy creates an empty bin, q8 cannot be used
for the primary verdict and must not be repaired after seeing this fact. A later
q8-like sensitivity design requires a separate prospective schema.

## Checkpoint Panel Scope

Allowed checkpoint scope for the first panel:

```text
checkpoint_root = experiments/exp018_cat/data/checkpoints_armb/alpha0.0
model_paths     = no_preserve_seed{seed}/generation_{generation}
seeds           = [1, 2, 3, 4, 42]
generations     = 0..9
device          = cpu
dtype           = float32
```

The 50 seed-generation rows are not 50 independent samples. They are
within-regime seed trajectories from one checkpoint root and one base-reset
regime.

## Output Discipline

Raw token-level JSONL is expected to be large and should not be committed to
git. Use canonical wip storage for raw panel rows, for example:

```text
/media/amd/raid1/canonical/wip/maofield_panel_primary_20260622/raw/
```

Small manifests, aggregate JSON, verdict JSON, and markdown summaries may be
committed under:

```text
experiments/exp020_metric_stress_test/panel_primary_20260622/
```

Every generated manifest must include:

```text
repo_head
dirty_state_note
schema_path
schema_sha256
builder_script_sha256
source_split=train
input_ids_sha256
target_ids_sha256
target_counts_sha256
checkpoint_root
seeds
generations
device
dtype
no_training=true
no_new_loss=true
```

## Gates

All gates must write machine-readable JSON.

### 1. Data-Source Gate

Fail as `invalid_artifact` if any source hash mismatches, if `source_split` is
not `train`, if the schema is missing, or if report wording mislabels the fixed
train blocks as Wikitext validation/test.

### 2. Schema-Freeze Gate

The panel generator must load the schema JSON above. It must not change
quantile method, tie policy, edge inclusivity, empty-bin policy, or bins. If the
primary q4 schema is not reproduced exactly, the run aborts.

### 3. Reproduction Gate

Before new panel claims, aggregate values recomputed from the panel must
reproduce the existing high-order row fields within `1e-5` absolute tolerance
where the old fields are available:

```text
mean_lp
F1_var
F1_tail
F3_slice_rare
F3_slice_freq
F3_slice_gap
```

### 4. LOSO Gate

Use leave-one-seed-out CV on the primary scalar `P`.

```text
model_a = poly5(D)
model_b = poly5(D) + generation + generation^2
weak_delta_threshold = 0.02
permutation_p_one_sided_threshold = 0.10
```

This is only a within-regime seed-held-out diagnostic, not independent
replication.

### 5. Matched-Mean Gate

Use the primary scalar `P` and mean mode `D`.

```text
tolerances = [0.02, 0.04]
stable_fraction_threshold = 0.70
z_threshold = 2.58
```

Pairing must be locked or fitted fold-locally before seeing held-out seed
outcomes. Both tolerances must be reported; the strongest verdict requires both
to pass.

### 6. Nuisance-Leakage Gate

Residualization, matched-mean pairing, and projection fitting must be fold-local
inside each held-out seed. Report correlations of primary `P` and each `u_j`
with:

```text
D
generation
generation^2
```

Mean-only synthetic controls and rank-1 synthetic controls must not pass the
full gate stack.

### 7. Rank/Noise-Floor Gate

Build the centered q4 `u_j` matrix after the data-source and reproduction gates.
Report singular values and `sigma2/sigma1`.

Locked thresholds:

```text
sigma2_over_sigma1_min = 0.25
residual_amplitude_floor = 2 * max(noise_floor_seed_bootstrap_p90,
                                   noise_floor_rank1_control_p90)
bootstrap_replicates = 2000
bootstrap_rng_seed = 0
```

Fail if the projected slice matrix is effectively rank-1 or if residual
amplitude is below the locked noise floor.

### 8. Multiplicity Gate

Only `freq_q4_audit_targets_20260622` and the primary q4 slope projection can
trigger the strongest verdict. q8, old top-bottom-20 masks, alternative
projections, and post-hoc slices are sensitivity-only.

### 9. Cluster/Replication Gate

Report per-seed trajectory effects, leave-one-seed verdicts, and per-generation
paired summaries. Do not describe this panel as independent external
replication.

### 10. Wording Gate

Allowed verdict vocabulary:

```text
invalid_artifact
killed
insufficient_artifact
eligible_for_next_design_review_only
```

Forbidden wording in verdict summaries:

```text
LOSO passed
F3 positive
mean-null vector field survives
glass box broken
training authorized
new loss authorized
```

## Strongest Possible Outcome

Even if all gates pass, the strongest allowed statement is:

```text
The q4 fixed-train-block logprob panel is eligible for next design review only.
```

It does not authorize training, a new loss, `F3 positive`, `mean-null vector
field survives`, or `glass box broken`.

## Next Implementation Step

Implement a new panel generator, not a mutation of the locked aggregate script:

```text
experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py
```

The first implementation should support:

```text
--schema docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json
--manifest-only
--one-checkpoint-smoke
--device cpu
--dtype float32
```

Do not run the full 50-checkpoint panel until manifest-only and one-checkpoint
smoke outputs pass the data-source and schema-freeze gates.
