# Q4 Residual Field Strict Math Audit Adoption Note

Date: 2026-06-23 CST, node36.

## Source

Archived GPT/PRO report:

`docs/infra/gpt_deep_research/deep_research_q4_residual_field_strict_math_audit_20260623.md`

The report audits an uploaded / packaged repository snapshot around commit
`57fc6b1`. Treat it as a claim-source and mathematical critique, not as
runtime evidence for the current `main`.

## Local Adoption

Adopted:

- The true q4 object is not the scalar mean mode `D`, not the primary projection
  scalar `P`, and not any old rare/freq F3 aggregate.
- The object to audit is the weighted slope-orthogonal residual field:

  ```text
  r_i = u_i - <v, u_i>_w v
  ```

  plus the stricter fold-local scalar-slope residual that removes only
  `alpha(D, generation, generation^2) * v` using non-held-out seeds.
- The q4 analysis must include rank/noise-floor pressure, fold-local leakage
  control, matched-mean stability, and a random mean-null projection
  multiplicity guard.
- Existing strong wording remains blocked: `LOSO passed`, `F3 positive`,
  `mean-null vector field survives`, `glass box broken`, `training authorized`,
  and `new loss authorized`.

Deflated / superseded by current local code:

- The report says the full-panel generator mode and separate q4 fold-local
  analysis path were missing in the audited package. That was true for the
  audited snapshot, but current `main` after `d4eaed0` has:
  - `--full-panel-dry-run`
  - a PI approval-token guard before `--full-panel`
  - explicit 5 seed x 10 generation checkpoint inventory
  - `scripts/q4_full_panel_foldlocal_analysis.py`
- This does not approve the full panel. It only means the old engineering
  blocker has been reduced to a guarded implementation gate.

## Local Changes Made From This Report

- `scripts/q4_full_panel_foldlocal_analysis.py` now explicitly records:
  - projection geometry for `r_i = u_i - <v,u_i>_w v`
  - fold-local scalar-slope residuals
  - rank/noise checks on the residual field rather than generic `U` only
  - a random mean-null projection multiplicity guard
- `scripts/math_turn_loso_audit.py` is marked legacy-only and now rejects q4
  panel aggregate inputs, instructing callers to use the q4 fold-local script.

## Current Decision

The D623 decision remains unchanged:

```text
real q4 full panel: not run
training: not authorized
new loss: not authorized
strong mathematical claim: blocked
strongest local status: implementation-gated, ready only for PI decision on whether to generate the 50-checkpoint q4 panel
```

If PI later approves the 50-checkpoint panel, the next step is to run the
guarded full-panel generator, then run `scripts/q4_full_panel_foldlocal_analysis.py`
on the produced aggregate and submit the resulting JSON/markdown verdict to
strict review.
