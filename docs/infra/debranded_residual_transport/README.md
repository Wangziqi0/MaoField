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
  RAG refresh record proving the v1.1 patch materials are discoverable through
  the node36 RAG locator.
- `README_FOR_PRO_FORMALV11_AUDIT_20260625.md` — upload/package guide for the
  GPT-5.5 Pro Formal v1.1 strict proof/harness audit.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_FORMALV11_PRO_20260625.md` —
  pre-final RAG refresh record proving the Formal v1.1 Pro audit prompt,
  package README, and node142 package record were discoverable through the
  node36 RAG locator before the final `2315` rebuild.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_FORMALV11_FINAL_20260625.md` —
  current final RAG refresh record for the `2315` node142 package and updated
  standalone prompt hash.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md` —
  strict GPT-5.5 Pro audit of Formal v1.1, with final classification
  `accept_with_v1_2_required`.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md` —
  node36 adoption note for report (27).
- `FORMAL_NOTE_V1_2_WORKPLAN_20260626.md` — minimal v1.2 patch plan:
  common ambient registration, squared-capture random null closure,
  product-weight theorem proof, holonomy telescoping, and single-source
  threshold contract.
- `README_FOR_PRO_FORMALV12_PATCH_20260626.md` — upload/package guide for the
  GPT-5.5 Pro Formal v1.2 minimal patch pass.
- `../DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_PATCH_20260626.md` —
  node142 package record for the Formal v1.2 minimal-patch prompt and bundle.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT27_V12_20260626.md` —
  current default RAG refresh record for report (27), the v1.2 prompt, and the
  FormalV12 package record.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md` —
  report (28), a Formal v1.2 minimal-patch design pass with classification
  `v1_2_small_patch_feasible`.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md` —
  node36 adoption note for report (28) and the local v1.2 implementation.
- `FORMAL_NOTE_V1_2_20260627.md` — implemented v1.2 formal note: registered
  ambient data, squared-capture Beta null, exact product-weight Hoeffding
  theorem, square-holonomy telescoping, and single-source harness contract.
- `SYNTHETIC_HARNESS_V1_2_20260627.md` — v1.2 zero-GPU synthetic harness
  summary; all 12 synthetic blocks passed.
- `synthetic_harness_v1_2_20260627.json` — v1.2 harness JSON output with
  `threshold_contract_sha256=0bb99a4a711405fb65e81413cfd283d6e68d0ecd4e9c34dc027c052f332110e0`.
- `README_FOR_PRO_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md` — upload/package
  guide for the next GPT-5.5 Pro implementation audit.

## Current Verdict

Strongest allowed local verdict:

```text
definitions_and_harness_viable_only
```

This means the definitions are executable on toy finite systems and have
positive/negative controls. It does not mean that MaoField contains an observed
residual, interaction, transport, or holonomy field.

## Current Next Step

Use the Formal v1.2 implementation-audit package as the next strict target. It
asks GPT-5.5 Pro to audit whether the local v1.2 note, script, JSON, and
summary actually close report (28)'s small-patch obligations. Do not turn the
v1.2 note, implementation package, or synthetic harness into an empirical
claim.
