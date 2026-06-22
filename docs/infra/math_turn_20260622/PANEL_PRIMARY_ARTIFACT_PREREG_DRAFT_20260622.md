# MaoField Math-Turn Panel Primary Artifact Prereg Draft

> Draft prereg for review. Not locked. Do not run checkpoint inference from
> this file. Checkpoint inference requires a separate locked runbook/schema.
> 2026-06-22 17:08 CST: execution superseded by
> `PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md`; keep this file as review trail.

## Purpose

The current aggregate high-order artifact is insufficient. This draft defines a
candidate primary artifact that can test whether a preregistered slice-level
mean-null observable is killed, remains insufficient, or only becomes eligible
for later next-step design.

## Non-Negotiable Boundaries

- No GPU training.
- No new loss implementation.
- No claim that `LOSO passed`, `mean-null vector field survives`, `F3 is
  positive`, or `glass box broken`.
- Existing report(3)/(4) are claim-source only.
- STATE claim updates wait until the new primary JSON/MD verdict exists. A
  coordination-only STATE note may be added without upgrading claims.

## Data Source

- Checkpoint root:
  `experiments/exp018_cat/data/checkpoints_armb/alpha0.0`
- Included seeds:
  `{1,2,3,4,42}`
- Included generations:
  `0..9`
- Model paths:
  `no_preserve_seed{seed}/generation_{generation}`
- Fixed audit block source, matching `highorder_ppl_run.py`:
  first 128 blocks from `tokenize_and_block(load_wikitext2()["train"], tok, 64)`.

Do not call this validation/test data unless a later locked prereg changes the
split and reruns all comparisons. The word "evaluation" in this draft means
"held fixed for this audit", not Wikitext validation/test.

## Slice Schema Candidates

The first locked run should use one primary schema and one sensitivity schema.
Both are defined only from target-token counts/frequencies on the fixed audit
blocks, before reading generation outcomes. These are data-sequence statistics,
not generation-0 model statistics. The locked run must record the slice-schema
file hash before any panel outcome is computed.

Primary schema:

```text
schema_id = freq_q4_audit_targets
J = 4
slice_id = target_frequency_audit_blocks quantile bin, using deterministic quantile edges
```

Sensitivity schema:

```text
schema_id = freq_q8_audit_targets
J = 8
slice_id = target_frequency_audit_blocks quantile bin, using deterministic quantile edges
```

The old rare/freq top-bottom-20 masks are comparison-only. They do not certify
`J>=4`.

This is an exploration-aware prospective lock, not a clean confirmatory prereg.
`q4` is the only primary schema candidate. `q8`, old rare/freq masks, and any
additional projection are sensitivity-only and cannot trigger the strongest
verdict by themselves.

Before any panel outcome is computed, a schema JSON must be hash-locked with
block indices, tokenizer identity, target token ids/counts, quantile algorithm,
tie policy, edge inclusivity, empty-bin policy, and threshold policy. The panel
generator must load that schema. If the schema is missing, bins collide, or a
bin is empty, the generator must abort rather than invent fallback bins.

## Required Panel Fields

Panel rows should be token-level or compressed token-level rows. If storage is
too large, a compressed representation must still preserve enough information
to recompute all registered slice aggregates.

```text
artifact_version
schema_id
seed
generation
checkpoint_path
source_split
audit_block_source
audit_block_id
token_pos
flat_token_index
target_token_id
target_count_audit_blocks
target_frequency_audit_blocks
slice_id
token_logprob
```

## Required Aggregate Fields

For each `(schema_id, seed, generation, slice_id)`:

```text
n_tokens
mean_logprob
weight
```

For each `(schema_id, seed, generation)`:

```text
D = sum_j weight_j * mean_logprob_j
u_j = mean_logprob_j - D
```

This uses logprob slice means as the first diagnostic carrier. A later KL
carrier may be added only after this diagnostic gate is reviewed.

## Gates

All gates must write machine-readable JSON.

1. LOSO nuisance gate:
   - nuisance basis includes at least mean logprob and generation controls used
     by `scripts/math_turn_loso_audit.py`.
   - report per-projection CV-R2 and delta-R2.
   - fit nuisance residualization and projection rules inside each held-out
     fold; held-out seed outcomes must not tune thresholds, projections, or
     pairings.
   - report as a within-regime seed-held-out diagnostic only. The 50
     seed-generation rows are not 50 independent samples.
2. Matched-mean gate:
   - use tolerances `0.02` and `0.04` unless reviewers change them before lock.
   - report pair count, sign fraction, z score, and stability decision.
   - pair selection must be locked or fold-local before seeing the held-out
     seed outcome.
3. Rank/residual gate:
   - build the centered projected slice matrix from `u_j`.
   - report singular values and `sigma2/sigma1`.
   - fail if effectively rank-1 or if residual is below the noise floor.
   - threshold values and the noise-floor source must be locked before this
     draft becomes an executable runbook. Candidate sources are seed bootstrap,
     within-generation variance, or negative-control synthetic panels.
4. Data-source gate:
   - manifest must contain `source_split=train`, block range/hash, tokenizer
     hash, script commit/hash, and schema hash.
   - any verdict/report that mislabels the blocks as Wikitext validation/test or
     uses `eval_split` is `invalid_artifact`.
5. Multiplicity gate:
   - the primary schema, primary projection, and primary verdict rule must be
     listed before the run.
   - q8, old top-bottom-20 masks, and extra projections are sensitivity-only.
6. Cluster/replication gate:
   - report per-seed trajectory effects, leave-one-seed verdict, and
     per-generation paired summaries.
   - no result from this run counts as independent external replication.

## Verdict Vocabulary

- `invalid_artifact`: manifest/source/schema fields are mislabeled, missing, or
  inconsistent with the locked runbook.
- `killed`: registered slice projections collapse into nuisance/mean/factor
  shadow or fail LOSO.
- `insufficient_artifact`: artifact exists but gates are mixed, underpowered,
  or missing a required component.
- `eligible_for_next_design_review_only`: the primary q4 projection passes
  LOSO, matched-mean, rank/residual, data-source, multiplicity,
  cluster/replication, nuisance-leakage, and wording gates without unregistered
  slice or threshold changes.

The strongest vocabulary item above still does not authorize broad claims,
training, loss implementation, `F3 positive`, `mean-null vector field
survives`, or `glass box broken`. It only opens a separate next-design review.

## Review Queue

Before implementation:

- Code explorer must confirm exact patch points in `highorder_ppl_run.py`.
- Claim gate must confirm wording does not leak into positive claims.
- Antithesis must attack binning, pseudo-replication, nuisance leakage, and
  impossible-gate drift.
