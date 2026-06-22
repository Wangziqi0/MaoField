# MaoField Math-Turn Panel Primary Artifact Coordination

> Node36 coordination file, 2026-06-22 16:46 CST.
> Purpose: make the current multi-agent task durable even if session context is
> compacted. This is a coordination/spec file, not a result verdict.
> 2026-06-22 17:08 CST update: execution moved to
> `PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` and
> `panel_schema_freq_q4_audit_targets_20260622.json`.

## Status Check

- Canonical repo: `/media/amd/raid1/canonical/projects/MaoField`
- Current HEAD at dispatch: `47a9119 docs(gpt): archive math-turn framework audit`
- Dirty state at dispatch: existing untracked `.codex/` and `AGENTS.md` only.
- Current STATE verdict: math turn remains `blocked-until-gated`.
- Current aggregate gate verdict: `insufficient_artifact`.
- Forbidden upgrades: `LOSO passed`, `mean-null vector field survives`,
  `glass box broken`, `F3 positive`, or any new training authorization.

## Objective

Produce a prereg/runbook for a candidate primary artifact, pending review and
successful artifact generation:

```text
raw-logprob/checkpoint mode
+ fixed preregistered slices
+ slice-level panel JSON/JSONL
+ machine-readable LOSO / matched-mean / rank-residual verdict fields
```

No GPU training is authorized. No new loss is authorized.

## Known Local Anchors

- Existing aggregate audit:
  `docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md`
- Existing aggregate result:
  `experiments/exp020_metric_stress_test/highorder_ppl_20260618/highorder_result.json`
- Current aggregate audit script:
  `scripts/math_turn_loso_audit.py`
- Logprob source script:
  `experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py`
- Checkpoint root used by `highorder_ppl_run.py`:
  `experiments/exp018_cat/data/checkpoints_armb/alpha0.0`
- Main seed/gen grid available from local inventory:
  seeds `{1,2,3,4,42}`, generations `0..9`.
- RAG stale risk: the 2026-06-22 13:44 RAG index does not include
  report(3), report(4), the adoption note, or math-turn gate files. Direct
  reads are required for all D622 math-turn material.
- Current high-order script uses the first 128 64-token blocks from
  `raw["train"]` via `load_wikitext2()` and `tokenize_and_block(...)`; do not
  call these validation/test blocks unless a new script changes the source.
- Current raw logprobs are not persisted. `highorder_ppl_run.py` keeps
  `LP[(seed, gen)]` in memory and writes only aggregate rows.
- Preliminary local inventory reports 51 alpha-0 generation directories: the
  intended 50 for seeds `{1,2,3,4,42}` times generations `0..9`, plus
  `seed0/generation_0`; this must be verified by the generator/runbook log
  before promotion.

## Six-Agent Dispatch

Because the tool has a live-agent concurrency limit, dispatch was staged.

### Dispatched Roles

1. `state_auditor`: verify STATE/MD_CATALOG/math-turn consistency and blocked claims.
2. `rag_librarian`: locate relevant files and RAG stale risks.
3. `explorer-checkpoints`: inventory checkpoints, fixed train/audit blocks, and existing artifacts.
4. `explorer-code`: inspect highorder scripts and patch points for panel generation.
5. `claim_gate`: review proposed schema/prereg for claim leakage.
6. `antithesis_reviewer`: attack the plan for binning, pseudo-replication,
   nuisance leakage, and impossible-gate drift.

## Agent Claims / Coordination Notes So Far

- `state_auditor`: status OK for prereg/runbook work only; STATE must not be
  updated with a survival or positive claim before a new JSON/MD verdict exists.
- `rag_librarian`: RAG is stale for report(3)/(4) and math-turn files; use
  direct reads. No raw logprob artifact exists yet. Existing high-order result
  is aggregate only.
- `explorer-checkpoints`: alpha-0 panel generation appears feasible with CPU
  inference, but no raw per-token logprob or `J>=4` panel artifact exists.
- `explorer-code`: prefer a new raw panel generator over editing the locked
  aggregate script; generator must load a locked slice schema and reproduce the
  old aggregate rows as a drift guard.
- `claim_gate`: downgraded wording from result-like claims to prereg/runbook
  language; bare `survive` is not an allowed project claim.
- `antithesis_reviewer`: prereg draft is acceptable only as a draft. It is not
  a locked runbook until train/eval naming, schema freezing, multiplicity,
  cluster/replication, nuisance leakage, rank/noise-floor, and wording gates
  are specified.
- `main-thread`: locked q4 schema/runbook created. q8 sensitivity candidate is
  not locked because the preregistered edge policy creates an empty bin.

## Main-Thread Responsibilities

- Keep edits in canonical node36 only.
- Do not touch `.codex/` or untracked local `AGENTS.md`.
- Maintain a strict distinction between:
  - observed local code/JSON/checkpoints;
  - derived script outputs;
  - proposed math framework;
  - blocked claims.
- Integrate agent results into a small prereg/schema/runbook before any script
  that loads checkpoints is run.

## Draft Panel Schema

Minimum row-level fields:

```text
artifact_version
run_id
seed
generation
checkpoint_path
source_split
audit_block_source
audit_block_id
example_id
token_pos
target_token_id
target_token_text_optional
target_count_audit_blocks
target_frequency_audit_blocks
slice_schema_id
slice_id
token_logprob
mean_lp_context_optional
source_file
```

Minimum aggregate fields:

```text
slice_schema_id
seed
generation
slice_id
n_tokens
mean_logprob
k_value
weight
mean_mode_D
u_value
```

## Draft Slice Schema

Preliminary candidate only, not locked:

- Source: fixed Wikitext train blocks currently used by
  `highorder_ppl_run.py` via `raw["train"]`; call them evaluation blocks only
  in the sense of being held fixed for this audit, not Wikitext
  validation/test.
- Frequency reference: target-token counts on the fixed audit blocks. This is a
  data-sequence statistic, not a generation-0 model statistic.
- First schema candidate: 4 quantile bins over
  `target_frequency_audit_blocks`.
- Alternative sensitivity schema: 8 quantile bins over
  `target_frequency_audit_blocks`.
- `q4` is the only primary schema candidate. `q8` is sensitivity-only and
  cannot trigger the strongest verdict by itself.
- Keep rare/freq top-bottom 20% only as a comparison with the old aggregate
  artifact, not as certification of `J>=4`.

## Draft Gates

- LOSO nuisance gate: compare nuisance-only model against nuisance+generation
  or nuisance+projected-slice model, holding out seeds. This is only a
  within-regime seed-held-out diagnostic, not independent replication.
- Matched-mean gate: require stable sign under preregistered tolerances before
  claiming non-mean structure.
- Rank/residual gate: reject if projected slice matrix is effectively rank-1
  or below noise floor.
- Schema-freeze gate: freeze schema JSON before panel outcomes, including block
  indices, tokenizer identity, token counts, quantile algorithm, tie policy,
  edge inclusivity, empty-bin policy, and hash. Missing or colliding schema
  aborts rather than changing bins.
- Multiplicity gate: predeclare the primary schema/projection/verdict rule; q8
  and old top-bottom masks are sensitivity-only.
- Cluster/replication gate: 50 seed-generation rows are not 50 independent
  samples. Report seed-trajectory effects and per-generation summaries.
- Nuisance leakage gate: residualization, matched-mean pairing, and projection
  fitting must be fold-local.
- Rank/noise-floor gate: thresholds and noise-floor source must be locked before
  the runbook becomes executable.
- Verdict vocabulary: `invalid_artifact`, `killed`, `insufficient_artifact`,
  `eligible_for_next_design_review_only`.

## Immediate Next Work

1. Implement a checkpoint/logprob panel generator with manifest-only and
   one-checkpoint-smoke modes.
2. Do not run the full 50-checkpoint panel until the generator passes the
   data-source and schema-freeze gates in the locked runbook.
