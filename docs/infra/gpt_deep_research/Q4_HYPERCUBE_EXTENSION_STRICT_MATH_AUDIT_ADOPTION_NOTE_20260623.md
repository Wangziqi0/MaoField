# Q4 Hypercube Extension Strict Math Audit Adoption Note

Date: 2026-06-23 CST, node36.

## Source

Archived GPT/PRO report:

`docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md`

The report audits an uploaded / packaged repository snapshot that did not
include the later D623 implementation-gate and report(9) residual-field code.
Treat it as a claim-source and mathematical critique, not as runtime evidence
for the current `main`.

## Local Adoption

Adopted:

- The q4 hypercube idea is not an observed phenomenon. It is only a possible
  formal preregistration extension of the q4 residual-field audit.
- A hypercube object must be a finite product cell vector with source-only
  weights, outcome-independent axes, and a nuisance subspace fixed before
  looking at outcomes.
- The minimal local candidate is `Q_freq4 x B_tokenpos4`, where `Q_freq4` is
  the locked q4 frequency slice and `B_tokenpos4` is a coarse token-position
  axis derived from `token_pos`.
- The mandatory nuisance space removes:
  - the constant cell mean mode,
  - the locked q4 frequency slope lifted across the new axis,
  - all pure token-position main effects.
- Hypercube residuals do not solve non-identification by default. They increase
  coordinate freedom and require sparse-cell, coarsening/refinement, random
  subspace, matched-mean/matched-slope, rank/noise, and fold-local guards.

Deflated / superseded by current local code:

- The report says the full-panel mode and `scripts/q4_full_panel_foldlocal_analysis.py`
  were missing. That was true for its audited package, but current `main` after
  `d4eaed0` / `e47bc88` has a full-panel dry-run, PI approval-token guard, and
  q4 residual-field analysis script.
- This does not approve the full panel. It only corrects stale engineering
  status in the report.

## Local Changes Made From This Report

- `scripts/build_hypercube_schema_20260623.py` defines the zero-GPU
  `q4_tokenpos4_hypercube_20260623` preregistration schema without changing the
  locked q4 primary schema.
- `scripts/q4_hypercube_zero_gpu_audit.py` reads existing smoke raw JSONL rows
  only and can output at most `formal_prereg_only`.
- `docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json`
  records source-only cell occupancy and mandatory nuisance dimensions.
- `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.{json,md}`
  records the zero-GPU feasibility audit over existing smoke raw rows.

## Current Decision

The D623 decision remains unchanged:

```text
real q4 full panel: not run
q4 hypercube full panel: not proposed as executable work
training: not authorized
new loss: not authorized
strong mathematical claim: blocked
strongest hypercube status: formal preregistration feasibility only
```

Do not claim `residual field observed`, `LOSO passed`, `F3 positive`,
`mean-null vector field survives`, `glass box broken`, `training authorized`,
`new loss authorized`, or `full panel approved`.
