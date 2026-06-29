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
  previous RAG refresh record for report (27), the v1.2 prompt, and the
  FormalV12 package record; superseded as current by the report(29) refresh
  below.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md` —
  report (28), a Formal v1.2 minimal-patch design pass with classification
  `v1_2_small_patch_feasible`.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md` —
  node36 adoption note for report (28) and the local v1.2 implementation.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_2_implementation_audit_20260627.md` —
  report (29), a Formal v1.2 implementation audit with classification
  `formal_v1_2_patch_requires_minor_revision`.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_ADOPTION_NOTE_20260627.md` —
  node36 adoption note for report (29) and the local threshold-contract
  minor revision.
- `FORMAL_NOTE_V1_2_20260627.md` — implemented v1.2 formal note: registered
  ambient data, squared-capture Beta null, exact product-weight Hoeffding
  theorem, square-holonomy telescoping, and repaired single-source harness
  contract.
- `SYNTHETIC_HARNESS_V1_2_20260627.md` — v1.2 zero-GPU synthetic harness
  summary; all 12 synthetic blocks passed.
- `synthetic_harness_v1_2_20260627.json` — v1.2 harness JSON output with
  `threshold_contract_sha256=0bb99a4a711405fb65e81413cfd283d6e68d0ecd4e9c34dc027c052f332110e0`.
- `README_FOR_PRO_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md` — upload/package
  guide for the next GPT-5.5 Pro implementation audit.
- `README_FOR_PRO_FORMALV12_REPORT29_MINOR_REVISION_AUDIT_20260627.md` —
  upload/package guide for the next GPT-5.5 Pro report(29) minor-revision
  audit.
- `../DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_REPORT29_MINOR_REVISION_AUDIT_20260627.md` —
  node142 package record for the report(29) minor-revision audit prompt and
  bundle.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT29_FORMALV12_MINOR_20260627.md` —
  first report(29) RAG refresh record proving the report(29) materials,
  threshold-contract patch, report29 minor-revision prompt, and package record
  are discoverable through the node36 RAG locator.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT29_FINAL_20260627.md` —
  current final RAG refresh record after the report(29) navigation/package
  metadata polish.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_2_report29_minor_revision_audit_20260628.md` —
  report (30), a Formal v1.2 report(29) minor-revision audit with
  classification `formal_v1_2_patch_accepted_after_minor_revision`.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md` —
  node36 adoption note for report (30). It accepts only local threshold-contract
  closure and keeps Mode B at `insufficient_artifact`.
- `README_FOR_PRO_FORMALV13_THEOREM_STRENGTHENING_20260628.md` —
  upload/package guide for the next GPT-5.5 Pro Formal v1.3 theorem-strengthening
  review.
- `../gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PROMPT_20260628.md` —
  zero-context prompt for the next Mode A theorem/no-go strengthening pass.
- `../DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_FORMALV13_THEOREM_STRENGTHENING_20260628.md` —
  node19 package record for the Formal v1.3 theorem-strengthening prompt and
  bundle.
- `../rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT30_FORMALV13_20260628.md` —
  current RAG refresh record after report (30), the v1.3 prompt, and node19
  package metadata were promoted into the default node36 RAG locator.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_3_theorem_strengthening_plan_20260628.md` —
  report (31), a Formal v1.3 theorem-strengthening plan source. Node36 adopts
  only the guarded next target: product vs non-product weight boundary and
  weighted ANOVA order-defect proof audit.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md` —
  node36 adoption note for report (31), with the local verdict
  `formal_v1_3_weighted_anova_order_defect_plan_accepted_with_guards`.
- `FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` — proof-audit workplan
  for the product/non-product weight boundary, ordered residual operators, and
  sequential stripping artifact no-go.
- `README_FOR_PRO_FORMALV13_ORDER_DEFECT_PROOF_20260628.md` — upload/package
  guide for the GPT-5.5 Pro Formal v1.3 order-defect proof audit.
- `../gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` —
  zero-context prompt for the next proof-audit pass.
- `../DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_FORMALV13_ORDER_DEFECT_PROOF_20260628.md` —
  node19 package record for the Formal v1.3 order-defect proof-audit prompt
  and bundle.
- `../gpt_deep_research/deep_research_formal_residual_transport_v1_3_order_defect_proof_audit_20260628.md` —
  report (32), a Formal v1.3 order-defect proof audit with internal
  classification `v1_3_order_defect_proof_plan_accepted`.
- `../gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_AUDIT_ADOPTION_NOTE_20260628.md` —
  node36 adoption note for report (32), with the local verdict
  `formal_v1_3_order_defect_proof_audit_accepted_with_minor_arithmetic_correction_and_claim_guards`.
- `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` — local proof note for the
  product/non-product weight boundary, ordered residual operators, and
  sequential stripping artifact no-go.
- `SYNTHETIC_HARNESS_V1_3_20260628.md` — deterministic v1.3 zero-GPU theorem
  controls; all four blocks passed.
- `synthetic_harness_v1_3_20260628.json` — v1.3 harness JSON output with
  `threshold_contract_sha256=ec2a3a70dce8d19be5635b2b2a7f51caae17ee8e0a8bce2ec20ed4a55f9a82f6`.
- `PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` — local preprint placeholder
  for the narrow order-defect note, including duplicate-work boundaries and
  related-work cautions. This is not an external submission.
- `README_FOR_PRO_ORDER_DEFECT_PREPRINT_RIGOR_20260629.md` — upload/package
  guide for a GPT-5.5 Pro proof-rigor, related-work, future-object, and
  preprint-safe drafting audit.
- `../DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PREPRINT_RIGOR_20260629.md` —
  node19 package record for the 2026-06-29 preprint-rigor/future-objects
  prompt and zip.
- `../gpt_deep_research/deep_research_order_defect_preprint_rigor_audit_20260629.md` —
  strict Pro audit of the order-defect preprint placeholder, with
  classification `preprint_placeholder_requires_related_work_reframing`.
- `../gpt_deep_research/ORDER_DEFECT_PREPRINT_RIGOR_AUDIT_ADOPTION_NOTE_20260629.md` —
  node36 adoption note for the preprint-rigor audit, with local verdict
  `revise_first_before_preprint_package`.
- `EXACT_WITNESS_V1_4_20260629.md` — exact rational certificate for the 2x2
  witness using fraction arithmetic; all exact checks passed.
- `exact_witness_v1_4_20260629.json` — machine-readable exact certificate
  output.
- `../../../scripts/debranded_residual_transport_exact_witness_v1_4.py` —
  script that generated the exact certificate under SSD scratch before
  promotion to canonical.
- `README_FOR_PRO_ORDER_DEFECT_V1_4_EXACT_BIBLIO_AUDIT_20260629.md` —
  upload/package guide for the next GPT-5.5 Pro exact-symbolic and
  bibliography audit.
- `../gpt_deep_research/GPT55_PRO_ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_PROMPT_20260629.md` —
  zero-context prompt for the next exact appendix / bibliography / duplicate
  risk pass.
- `../DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_V14_EXACT_BIBLIO_AUDIT_20260629.md` —
  node19 package record for the v1.4 exact/bibliography audit package.
- `README_FOR_PRO_FORMALV13_ORDER_DEFECT_IMPLEMENTATION_AUDIT_20260628.md` —
  upload/package guide for the next GPT-5.5 Pro proof-note and harness audit.
- `../gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_IMPLEMENTATION_AUDIT_PROMPT_20260628.md` —
  zero-context prompt for auditing the local v1.3 note, script, summary, and
  JSON.

## Current Verdict

Strongest allowed local verdict:

```text
definitions_and_harness_viable_only
```

This means the definitions are executable on toy finite systems and have
positive/negative controls. It does not mean that MaoField contains an observed
residual, interaction, transport, or holonomy field.

## Current Next Step

Use the v1.4 exact-symbolic / bibliography package as the next strict target.
It should ask GPT-5.5 Pro to audit the exact rational certificate, confirm that
harness wording is regression-support-only, and verify durable related-work
records before any preprint-readiness claim. Do not request more roadmap
generation in that pass. Do not turn the v1.2/v1.3/v1.4 notes, reports,
prompts, packages, exact certificate, or synthetic harnesses into an empirical
MaoField claim or a completed formal-system claim.
