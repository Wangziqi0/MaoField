# Hypercube Interaction Analysis Prereg Design

Date: 2026-06-23 CST, node36.

## Boundary

This is a zero-GPU preregistration design for a future analysis script. It does
not run checkpoints, generate a full panel, train a model, create a new loss, or
establish a scientific result.

The design is motivated by GPT/PRO report (17) and the local adoption note:

- `docs/infra/gpt_deep_research/deep_research_math_ore_quotient_residual_strict_audit_20260623.md`
- `docs/infra/gpt_deep_research/MATH_ORE_QUOTIENT_RESIDUAL_ADOPTION_NOTE_20260623.md`

## Target Object

The primary future object is the strict additive interaction residual on a
finite weighted product partition.

For the current concrete carrier:

```text
X = Q_freq4 x B_tokenpos4
K_i(q,b) = cell mean logprob for checkpoint row i
A = span{constant, q4 main effects, token-position main effects}
I_i = Pi_{A_perp,w} K_i
```

Here `w` must be source-only cell weights fixed before outcome analysis.
`B_tokenpos4` is the existing outcome-independent token-position binning:

```text
position_bin = min(3, (token_pos - 1) * 4 // 63)
```

## Required Future Inputs

Before promotion beyond smoke feasibility, the analysis needs either:

- a PI-approved 50-checkpoint raw token panel with all token-level rows, or
- an aggregate generated from that raw panel that preserves enough information
  to recompute every preregistered partition and null.

Minimum raw fields:

```text
schema_id
seed
generation
source_split
audit_block_id
token_pos
flat_token_index
target_token_id
target_count_audit_blocks
slice_id
token_logprob
neg_logprob
```

Minimum aggregate fields:

```text
schema_id
repo_head
builder_script_sha256
raw_jsonl_sha256
axis_definitions
source_only_weights
cell_counts
cell_mean_logprob
cell_var_logprob
checkpoint_identity
```

## Kill Suite

The analysis is designed to kill the object unless every preregistered gate
survives.

| Gate | Statistic | Kill condition |
|---|---|---|
| Strict additive annihilation | `||Pi_{A_perp,w} K_i||_w` | interaction norm is at or below noise floor |
| Matched mean/slope | residual direction after matching global mean and q4 slope | direction or sign is unstable |
| Random equal-size partition | true token-position axis vs random equal-count axes | true axis is not better than null |
| Within-q shuffle | q-local position-label shuffle | interaction statistic does not drop |
| Bad-axis null | `audit_block_id` or other known-bad axes | bad axis creates comparable signal |
| Same-dimension subspace | true 9D interaction space vs random 9D subspaces | true subspace is not better |
| Rank/noise | singular spectrum and noise floor | `sigma2/sigma1` too low or amplitude below floor |
| Coarsen/refine | `C_rho Pi_f - Pi_c C_rho` | residual vanishes, flips, or fails naturality |
| Principal angles | seed/generation held-out subspace angles | main residual subspaces rotate arbitrarily |
| Gluing sanity | overlap mismatch for local models | obstruction is absorbed by local nuisance |

Passing these gates would not be a paper claim by itself. It would only make the
object eligible for the next design review.

## Recommended Verdict Values

Allowed verdicts:

```text
invalid_artifact
killed_by_noise_floor
killed_by_random_axis
killed_by_rank1_shadow
killed_by_coarsening
insufficient_artifact
eligible_for_next_design_review_only
```

Forbidden verdicts:

```text
interaction_field_observed
hypercube_residual_observed
residual_field_observed
LOSO_passed
F3_positive
glass_box_broken
training_authorized
new_loss_authorized
```

## Design Rule

The future script must be independent from the generator. It may consume raw
JSONL or a preregistered full-panel aggregate, but it must not load checkpoints,
run inference, train, or change the model. It must fail closed when provenance,
schema ids, raw hashes, source-only weights, or required cells are missing.

## Implementation Skeleton

The future-only gate skeleton is:

```text
scripts/q4_hypercube_interaction_prereg_analysis.py
```

It does not generate a panel or load checkpoints. With no future aggregate, its
verdict is `insufficient_artifact`. With malformed provenance, old rare/freq
rows, missing q4/token-position cells, or missing preregistered null-test result
blocks, it fails closed. Its strongest possible verdict is
`eligible_for_next_design_review_only`, never an observed-field or glass-box
claim.

D624 contract update:

```text
docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md
```

The script now requires structured `null_tests` blocks under contract version
`2026-06-24.fail_closed.v1`; block-name presence alone is insufficient. Each
block must expose machine-readable provenance, thresholds, metrics, a boolean
`pass`, and a `kill_verdict_if_fail`. The rank-shadow design-review floor is
`weighted_uncentered_sigma2_over_sigma1 >= 0.25`; the old `<0.10` threshold is
only a hard warning floor, not a pass line.
