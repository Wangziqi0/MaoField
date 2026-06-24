# MaoField q4 x tokenpos4 Null-Tests Contract

Date: 2026-06-24 CST

## Boundary

This file defines the future-only zero-GPU `null_tests` contract used by:

```text
scripts/q4_hypercube_interaction_prereg_analysis.py
```

It is not an experiment result. It does not authorize full-panel generation,
checkpoint loading, model inference, training, a new loss, or any positive
MaoField claim.

Current MaoField evidence status remains:

```text
stable non-scalar residual object: insufficient_artifact
existing interaction smoke: smoke_conjecture_only
```

## Purpose

The checker consumes only a future provenance-checked aggregate:

```text
artifact_kind = maofield_q4_tokenpos4_interaction_full_panel_aggregate
aggregate_schema_id = q4_tokenpos4_interaction_full_panel_20260623
```

The `null_tests` blocks are fail-closed anti-packaging gates. They prevent an
old q4/F3 smoke artifact, a rank-1 scalar shadow, a random axis, a coarsening
artifact, or a local nuisance mismatch from being renamed into a quotient
residual field.

Even when every block passes, the strongest possible verdict remains:

```text
eligible_for_next_design_review_only
```

That verdict is not evidence of an observed residual field.

## Top-Level Contract

A future aggregate must include:

```text
null_tests_contract_version = 2026-06-24.fail_closed.v1
null_tests = object
```

The checker currently requires these eight result blocks:

```text
matched_mean_slope
random_equal_size_partition
within_q_position_shuffle
bad_axis_audit_block_id
same_dimension_random_subspace
coarsen_refine_naturality
principal_angle_stability
gluing_sanity
```

Noise-floor and rank-shadow gates are computed by the checker from the
aggregate rows before external `null_tests` can promote the artifact to design
review. The rank-shadow design-review floor is:

```text
weighted_uncentered_sigma2_over_sigma1 >= 0.25
```

The old `< 0.10` threshold remains only as a hard rank-1 warning floor; it is
not a pass line.

## Common Block Fields

Each block must contain machine-readable fields:

```text
test_id
contract_version
computed_from
schema_id
weights_source
parameters
metrics
thresholds
stat_name
primary_value
null_distribution_summary
empirical_p_or_quantile
pass
kill_verdict_if_fail
reasons
notes
required_fields
failure_behavior
no_checkpoint_loaded_by_checker
no_model_inference_by_checker
no_training
no_new_loss
```

`pass` must be a JSON boolean. A string such as `"true"`, a placeholder, or a
missing value is insufficient. `notes` can explain a result but cannot override
`pass: false`.

Each block must also declare:

```text
weights_source.outcome_independent = true
computed_from.raw_jsonl_sha256 = raw_jsonl_sha256
schema_id = q4_tokenpos4_interaction_full_panel_20260623
contract_version = 2026-06-24.fail_closed.v1
```

## Kill Mapping

If a required block is missing or malformed:

```text
insufficient_artifact
```

If a block claims outcome-derived weights, mismatched raw provenance, checkpoint
loading, model inference, training, or a new loss:

```text
invalid_artifact
```

If a block is structurally valid but has `pass: false`, the checker uses the
block's `kill_verdict_if_fail.final_verdict`:

```text
matched_mean_slope                  -> killed_by_rank1_shadow
random_equal_size_partition          -> killed_by_random_axis
within_q_position_shuffle            -> killed_by_random_axis
bad_axis_audit_block_id              -> killed_by_random_axis
same_dimension_random_subspace       -> killed_by_random_axis
coarsen_refine_naturality            -> killed_by_coarsening
principal_angle_stability            -> insufficient_artifact
gluing_sanity                        -> killed_by_coarsening
```

The checker gives priority to hard failure verdicts before any design-review
eligibility.

## Plain Explanation

Think of `K_t` as a 4 by 4 table of numbers. The checker first subtracts the
ordinary background: overall mean, q4 main effect, and token-position main
effect. The leftover is the candidate interaction.

The null tests ask simple questions:

- Is the leftover bigger than noise?
- Is it more than one fixed template getting brighter or dimmer?
- Does it remain after matching mean and q4 slope?
- Does the real token-position axis beat random axes?
- Does the signal disappear when position labels are shuffled?
- Does a known bad axis produce the same signal?
- Does the true 9D interaction space beat random 9D spaces?
- Does the object behave consistently under coarsening/refinement?
- Are held-out seed/generation subspaces stable?
- Is local mismatch really non-gluable, or can nuisance absorb it?

If the answer is weak, missing, malformed, or random-axis-like, the object is
killed or remains insufficient. This is a design gate, not a discovery.
