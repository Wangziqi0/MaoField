# Debranded Residual Transport Direction

Date: 2026-06-25 CST

This directory is the formal start of the debranded mathematics direction inside
the MaoField repository.

It is intentionally separated from the MaoField empirical line:

- MaoField remains a negative-centered empirical pilot and measurement-audit
  case.
- This directory studies finite weighted residual transport / holonomy /
  operator no-go objects.
- Passing local toy harnesses does not observe a MaoField residual field.
- No full panel, checkpoint loading, training, or new loss is authorized here.

## Current Entry Points

- `FORMAL_NOTE_V0_20260625.md` — first finite-dimensional definition note.
- `SYNTHETIC_HARNESS_V0_20260625.md` — seven-block zero-GPU harness
  specification and first run summary.
- `synthetic_harness_v0_20260625.json` — first run JSON output.
- `FORMAL_NOTE_V1_WORKPLAN_20260625.md` — node36 workplan for the next
  operator/no-go formal note, based on the GPT-5.5 Pro v1 audit.
- `FORMAL_NOTE_V1_20260625.md` — proof-style v1 note: finite weighted Hilbert
  systems, source-fixed nuisance, edge/path no-go lemmas, random/rank/gluing
  guards, and a non-product-weight counterexample.
- `SYNTHETIC_HARNESS_V1_20260625.md` — v1 zero-GPU synthetic harness summary:
  product-weight equality, product-reweighting separation, outcome-derived
  nuisance invalidation, transport-stable multidirectional control, square
  no-go controls, rank/random-axis controls, and gluing absorption.
- `synthetic_harness_v1_20260625.json` — v1 harness JSON output.
- `FORMAL_NOTE_V1_1_WORKPLAN_20260625.md` — node36 patch plan after the
  strict Pro audit of v1: quotient descent, projection-evolution commutator,
  holonomy decomposition, analytic/random nulls, rank perturbation, and
  triple-overlap gluing.

## Current Verdict

Strongest allowed local verdict:

```text
definitions_and_harness_viable_only
```

This means the definitions are executable on toy finite systems and have
positive/negative controls. It does not mean that MaoField contains an observed
residual, interaction, transport, or holonomy field.

## Current Next Step

Patch toward Formal Note v1.1 under the same zero-GPU/synthetic boundary. The
strict audit says v1 is a serious draft, not a completed formal system. Do not
turn the v1 note or synthetic harness into an empirical claim.
