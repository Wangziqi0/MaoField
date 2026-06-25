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
- `FORMAL_NOTE_V1_1_20260625.md` — proof-style v1.1 patch note: quotient
  descent, `[P,T]` commutator criterion, square-holonomy decomposition,
  transported-invariant ambient-space requirement, random-subspace analytic
  null, rank perturbation, finite gluing complex, and product-weight
  equivalence boundary.
- `SYNTHETIC_HARNESS_V1_1_20260625.md` — v1.1 zero-GPU synthetic harness
  summary: bad-edge defect, projection-evolution commutator, harder
  random-subspace heldout, shuffle null distribution, triple-overlap gluing,
  threshold contract, and environment metadata.
- `synthetic_harness_v1_1_20260625.json` — v1.1 harness JSON output.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_V11PATCH_20260625.md` —
  default RAG refresh record proving the v1.1 patch materials are discoverable
  through the node36 RAG locator.

## Current Verdict

Strongest allowed local verdict:

```text
definitions_and_harness_viable_only
```

This means the definitions are executable on toy finite systems and have
positive/negative controls. It does not mean that MaoField contains an observed
residual, interaction, transport, or holonomy field.

## Current Next Step

Use v1.1 as the next strict audit target. It patches the v1 gaps identified by
report (26), and the default RAG now indexes the v1.1 patch materials, but this
remains zero-GPU synthetic/formal work. Do not turn the v1.1 note or synthetic
harness into an empirical claim.
