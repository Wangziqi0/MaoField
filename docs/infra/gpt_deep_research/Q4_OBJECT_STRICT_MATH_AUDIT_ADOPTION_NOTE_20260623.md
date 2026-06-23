# Q4 Object Strict Math Audit Adoption Note

Date: 2026-06-23 CST
Local authority: node36 canonical MaoField state
External claim-source: `deep_research_q4_object_strict_math_audit_20260623.md`

## Scope

This note records the node36 interpretation of GPT/PRO report (7), a strict
mathematical audit of the q4 object package. Treat the report as a claim-source
and implementation-review guide, not as experiment evidence.

The report was generated from the 2026-06-23 bridge package built at git
`57fc6b1 docs(rag): record post-q4 node22 vector rebuild`.

## Adopt

- Reject the current implemented q4 artifact as a mathematical-advance
  candidate.
- Preserve the narrower future object definition: a fold-local q4 mean-null
  residual audit object, not the current scalar projection by itself.
- Continue treating current artifacts as schema/provenance/smoke alignment
  only:
  - q4 schema/runbook locked;
  - manifest-only smoke exists;
  - one-checkpoint smoke exists;
  - negative fail-fast smoke exists;
  - three-point multi-checkpoint smoke exists;
  - no full 50-checkpoint panel exists.
- Keep the strongest current scientific claim at `insufficient_artifact` /
  weak F3 lead only. This does not authorize training, a new loss, or a glass-box
  claim.

## Deflate

- The report's formal definition is useful as an implementation target, but it
  is not yet an observed object in MaoField.
- The primary scalar q4 projection `P` is only a one-dimensional diagnostic
  carrier. It cannot by itself identify a non-scalar residual structure in the
  q4 mean-null subspace.
- Existing `math_turn_loso_audit.py` remains an audit of old rare/freq aggregate
  rows, not a q4 full-panel analysis path.
- Report path and line references point into the uploaded bridge package. For
  promoted claims, re-check canonical files directly under this repository.

## Reject / Block

Do not claim:

- `LOSO passed`;
- `F3 positive`;
- `mean-null vector field survives`;
- `glass box broken`;
- full q4 panel approval;
- training authorization;
- new loss authorization.

Do not promote q8 to primary. The q8 attempt remains sensitivity-only because
the locked edge policy produced an empty bin.

## Required Next Engineering Work

Before any full-panel run is considered, implement and review:

1. Full-panel generator mode in
   `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py`.
   It must explicitly enumerate all 5 seeds x 10 generations, fail on missing
   checkpoints, write raw rows outside git, write small aggregate/manifests, and
   stay mutually exclusive with smoke modes.
2. Unified provenance fields for all generated artifacts, including builder
   script hash, generator script hash, schema hash, source hashes, artifact
   generation commit, and dirty-state note. Do not hand-edit old manifests to
   backfill provenance; regenerate under a clean audited command if needed.
3. A separate fold-local q4 analysis script, for example
   `scripts/q4_full_panel_foldlocal_analysis.py`. It must not reuse old
   rare/freq aggregate rows as primary evidence.
4. Kill-tests required before any positive wording:
   - fold-local nuisance-only residualization;
   - fold-local matched-mean pairing at both locked tolerances;
   - mean-only synthetic negative control;
   - rank-1 synthetic negative control;
   - rank/noise-floor gate;
   - multiplicity gate enforcing q4 primary only.

All code execution that may write caches/logs/intermediate files on node36
should use `/home/amd/codex-node36/tmp/<task>/` and promote only reviewed durable
artifacts back into canonical.

## Current Decision

Report (7) strengthens the existing block rather than relaxing it:

```text
q4 schema/smoke layer: implemented enough for implementation review
full q4 mathematical object: not implemented
full 50-checkpoint panel: not approved
training/new loss/glass-box claim: blocked
next action: implement generator mode + separate fold-local analysis path, then review
```
