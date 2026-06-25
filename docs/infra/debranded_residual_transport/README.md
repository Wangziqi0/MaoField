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

## Current Verdict

Strongest allowed local verdict:

```text
definitions_and_harness_viable_only
```

This means the definitions are executable on toy finite systems and have
positive/negative controls. It does not mean that MaoField contains an observed
residual, interaction, transport, or holonomy field.

## Current Next Step

Review Formal Note v1 and design the v1 synthetic harness additions. Do not
turn the v1 note into an empirical claim.
