# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Preprint Final Gate

Use the uploaded zip as the primary evidence bundle for local repository facts.
Do not use public GitHub, raw GitHub URLs, search-engine snippets, or model
memory as evidence for local files. If a local file is absent from the bundle,
say so. You may use external scholarly search only for bibliography and
duplicate-risk checking, and you must cite stable records such as DOI, arXiv,
publisher pages, MathSciNet, zbMATH, or Crossref. Treat chat-internal citation
handles as non-evidence.

Repository/project context inside the bundle: MaoField is only the storage
container for a debranded Mode A finite-dimensional mathematics line. This task
is not MaoField empirical validation.

## Mission

Act as a strict mathematics professor, proof auditor, and academic-compliance
reviewer. This is a final-gate check after the v1.4 audit returned:

```text
preprint_requires_minor_bibliography_or_wording_fixes
posting_decision=revise_first
```

The v1.4 audit already passed the math core:

```text
exact_fraction_certificate=PASS
exact_projection_matrix_dump=PASS
T1_T2_T3_unchanged_after_edits=PASS
evidence_boundary=PASS
```

Your job is not to generate a new roadmap. Your job is to decide whether the
v1.5 local fixes close the remaining WARN items enough to move to a short-note
draft gate.

## Primary Files To Inspect

```text
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/debranded_residual_transport/README.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_ADOPTION_NOTE_20260629.md
```

## Required Top-Level Classification

Return exactly one:

```text
short_note_draft_gate_passed_after_copyediting
short_note_requires_minor_wording_or_bibliography_fixes
short_note_requires_major_mathematical_revision
short_note_requires_major_related_work_revision
short_note_should_not_be_posted_yet
reject_as_duplicate_or_overclaim
```

Then provide PASS/WARN/FAIL for:

```text
v1_4_WARN_items_closed
formal_bibliography_floor
Lamboni_2026_inclusion
projection_theory_boundary
harness_regression_only_boundary_markdown
harness_regression_only_boundary_json
harness_regression_only_boundary_script
project_internal_wording_removed
novelty_wording_narrow_enough
exact_math_still_unchanged
preprint_placeholder_ready_for_short_note_drafting
evidence_boundary
non_specialist_explanation
```

## Specific Checks

Verify that the bibliography/positioning file contains a durable floor for:

```text
Hooker 2007, DOI 10.1198/106186007x237892
Chastaing, Gamboa, Prieur 2012, DOI 10.1214/12-ejs749
Chastaing, Gamboa, Prieur 2014/2015, DOI 10.1080/00949655.2014.960415
Owen and Prieur 2017, DOI 10.1137/16m1097717
Iooss and Prieur 2019, DOI 10.1615/int.j.uncertaintyquantification.2019028372
Il Idrissi et al. 2025, DOI 10.1016/j.jmva.2025.105444
Lamboni 2026, DOI 10.1137/24m1712680
Bottcher and Spitkovsky 2010, DOI 10.1016/j.laa.2009.11.002
Corach and Maestripieri, arXiv:1011.5237
Halmos 1969, DOI 10.1090/S0002-9947-1969-0251519-5
```

Verify that the final novelty sentence is no broader than:

```text
a compact finite weighted projection-order artifact note with an exact 2 x 2 witness
```

Verify that the harness boundary is present in the preprint placeholder,
README, harness markdown, harness JSON, and harness script:

```text
The floating-point harness is deterministic regression support only; the
mathematical claims are carried by the analytic proof and exact rational
certificate, not by JSON floats.
```

Return FAIL if any current file treats JSON floats as exact proof.

Confirm that the exact math has not been weakened or broadened:

- finite positive weighted two-way table only;
- product-weight iff main-effect orthogonality;
- order-independence iff product weights;
- non-product implies an existential pure-main-effect witness, not universal
  order dependence for every input;
- nonzero wrong-order output is a sequential stripping artifact, not a true
  interaction residual;
- exact 2 x 2 rational witness remains the certificate-level example.

## Evidence Boundary

Forbidden upgrades:

- MaoField empirical positive result;
- full panel has run;
- 16-cell aggregate exists;
- checkpoint loading, inference, training, or new loss is authorized;
- MaoField residual / interaction / quotient-residual / transport / holonomy
  field has been observed;
- glass box broken;
- F3 positive or LOSO passed;
- completed formal system;
- broad new ANOVA theory;
- broad new dependent-input decomposition theory;
- broad new noncommuting projection theory;
- holonomy / gluing / sheaf / curvature claims.

Allowed local ceiling:

```text
definitions_and_harness_viable_only
```

Mode B MaoField status:

```text
insufficient_artifact
```

## Output Requirements

Be severe. If this is still not ready for a short-note draft gate, say exactly
what remains and give corrected wording. If it is ready only after copyediting,
say so. Do not write the paper; audit the gate.
