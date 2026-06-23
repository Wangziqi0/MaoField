# MaoField q4 Implementation Gate Update

Date: 2026-06-23 CST, node36.

## Scope

This update implements the next engineering gate requested after the strict q4
audits. It does not run the 50-checkpoint full panel, train a model, create a
new loss, or license any glass-box wording.

## Code Changes

- `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py`
  now has a `--full-panel-dry-run` mode that enumerates the locked 5 seed x 10
  generation checkpoint plan and records that no checkpoint was loaded.
- The same generator has a guarded `--full-panel` mode. It fails before data
  preparation unless `--full-panel-approval-token PI_APPROVED_Q4_FULL_PANEL` is
  supplied by the PI.
- `scripts/q4_full_panel_foldlocal_analysis.py` is a separate analysis path for
  a future q4 full-panel aggregate. It rejects old rare/freq aggregate rows and
  reports only four possible verdicts: `invalid_artifact`, `killed`,
  `insufficient_artifact`, or `eligible_for_next_design_review_only`.

## Report(9) Residual-Field Tightening

After `deep_research_q4_residual_field_strict_math_audit_20260623.md`, the
separate q4 analysis path was tightened to audit the explicit object:

```text
r_i = u_i - <v, u_i>_w v
```

The script now records projection geometry, fold-local scalar-slope residuals,
rank/noise pressure on the residual field, and a random mean-null projection
multiplicity guard. The legacy `scripts/math_turn_loso_audit.py` now rejects q4
panel aggregate inputs and points callers to the q4 fold-local script.

## Report(11) Hypercube Zero-GPU Feasibility

After `deep_research_q4_hypercube_extension_strict_math_audit_20260623.md`, the
hypercube extension was limited to formal preregistration / zero-GPU feasibility
only. Local additions:

- `scripts/build_hypercube_schema_20260623.py`
- `scripts/q4_hypercube_zero_gpu_audit.py`
- `hypercube_schema_q4_tokenpos4_20260623.json`
- `Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.{json,md}`

The minimal candidate is `Q_freq4 x B_tokenpos4`, derived from locked q4 slices
and the existing `token_pos` field. Existing smoke raw rows have 16/16 non-empty
cells with min cell count 324, but the audit verdict is only
`formal_prereg_only`. This is not a full panel and does not support a scientific
claim.

## Report(13) Current-Repo Hypercube Audit

After `deep_research_q4_hypercube_current_repo_strict_audit_20260623.md`, the
same boundary remains in force. Report (13) confirms against current repository
state that `Q_freq4 x B_tokenpos4` is a formal preregistration coordinate
system, not an observed hypercube residual field.

No code change is authorized by report (13). Its suggested hypercube fold-local
analysis path is a future-only design target and would require a separate
artifact kind, PI-approved full-panel generation, strict additive nuisance
controls, matched-slope gates, generation-block leave-out, coarsening/refinement
checks, and random same-dimension subspace guards.

## Report(15) Interaction-Field Smoke Direction

After `deep_research_future_math_objects_interaction_field_audit_20260623.md`,
the best future mathematical object is recorded as a weighted product-partition
interaction field over `Q_freq4 x B_tokenpos4`:

```text
I_i = Pi_{A_perp,w} K_i
```

where `A` removes constant cell mean, q4 frequency main effects, and
token-position main effects.

Local zero-GPU reproduction was added in
`scripts/q4_hypercube_interaction_smoke_audit.py`, with canonical outputs:

- `Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.json`
- `Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md`

The verdict is only `smoke_conjecture_only`. The calculation reproduces the
small report(15) smoke hint, but it is not a full-panel artifact, not a
scientific result, and not authorization for training, a new loss, or hypercube
full-panel generation.

## Local Verification

Verification ran only under node36 scratch:

`/home/amd/codex-node36/tmp/q4_gate_impl_20260623/`

Commands passed:

- Python compile check for both scripts.
- CLI help checks for both scripts.
- q4 full-panel dry run with expected schema hash and expected repo head.
- `--full-panel` without approval token rejected before checkpoint inference.
- Analysis self-test completed on synthetic q4-shaped input.
- Old `highorder_result.json` rare/freq aggregate was rejected as
  `invalid_artifact`.
- Legacy LOSO script accepted old rare/freq aggregate input and rejected
  q4-shaped input.
- `git diff --check` passed.

The dry run wrote:

`/home/amd/codex-node36/tmp/q4_gate_impl_20260623/out/q4_full_panel_dry_run_20260623_v2_plan.json`

Key dry-run facts:

- `checkpoint_count = 50`
- all expected `model.safetensors` files exist
- `full_panel_generated = false`
- `no_checkpoint_loaded = true`
- `training_authorized = false`

## Claim Boundary

This is an implementation gate, not a scientific result. It does not imply:

- LOSO passed
- F3 positive
- mean-null vector field survives
- glass box broken
- training is authorized
- a new loss is authorized

The next scientific step remains gated: generate a real q4 full-panel aggregate
only after explicit PI approval, then run the separate fold-local q4 analysis
and submit the produced aggregate and verdict to strict review.
