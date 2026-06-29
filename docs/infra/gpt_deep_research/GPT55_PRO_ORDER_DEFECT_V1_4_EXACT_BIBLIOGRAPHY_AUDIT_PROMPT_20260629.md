# GPT-5.5 Pro Zero-Context Prompt: Order-Defect v1.4 Exact Appendix And Bibliography Audit

Use the uploaded zip as the primary evidence bundle. Do not use public GitHub,
raw GitHub URLs, search-engine snippets, or model memory as evidence for local
repo facts. If a local file is absent from the bundle, say so. You may use
external scholarly search only for bibliography / duplicate-risk assessment,
and you must provide durable citations: DOI, arXiv, publisher page, MathSciNet,
zbMATH, or another stable bibliographic record. Treat chat-internal citation
handles as non-evidence.

Repository/project context inside the bundle: MaoField is only the storage
container for a debranded Mode A finite-dimensional mathematics line. This task
is not MaoField empirical validation.

## Mission

Act as a strict mathematics professor, proof auditor, and academic-compliance
reviewer. This is a narrow second-pass audit after the previous classification:

```text
preprint_placeholder_requires_related_work_reframing
revise_first
```

Your job is to decide whether the new v1.4 exact rational appendix/certificate,
harness-boundary edits, and related-work reframing are sufficient to move the
order-defect placeholder toward a short, narrow preprint note.

Do not generate a broad roadmap. Do not revive MaoField empirical claims. Do
not discuss holonomy, gluing, sheaf, curvature, or empirical residual fields
except to say they are out of scope or blocked.

## Primary Files To Inspect

```text
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_preprint_rigor_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PREPRINT_RIGOR_AUDIT_ADOPTION_NOTE_20260629.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/debranded_residual_transport/README.md
from_repo/STATE.md
from_repo/MD_CATALOG.md
```

## Required Top-Level Classification

Return exactly one:

```text
preprint_ready_as_short_note_after_copyediting
preprint_requires_minor_bibliography_or_wording_fixes
preprint_requires_major_mathematical_revision
preprint_requires_major_related_work_revision
preprint_should_not_be_posted_yet
reject_as_duplicate_or_overclaim
```

Then provide PASS/WARN/FAIL for:

```text
exact_fraction_certificate
exact_projection_matrix_dump
T1_T2_T3_unchanged_after_edits
harness_regression_only_boundary
related_work_durable_citations
duplicate_risk
novelty_wording
preprint_readiness
evidence_boundary
non_specialist_explanation
```

## Exact Mathematics To Verify

Use exact rational arithmetic, not decimal approximations, to verify the v1.4
certificate. Recompute or audit:

```text
w = (1/11) [[1,2],
            [3,5]]
K_B = (7/11, -4/11, 7/11, -4/11) in B0
K_A = (8/11, 8/11, -3/11, -3/11) in A
R_Q_then_B K_B = (1/32, 5/168, -1/96, -1/84)
R_B_then_Q K_B = 0
||R_Q_then_B K_B||_w^2 = 61/177408
R_Q_then_B K_A = 0
R_B_then_Q K_A = (1/42, -1/84, 5/224, -3/224)
D_w = P_B0 P_A - P_A P_B0
```

Check whether the exact matrices in `exact_witness_v1_4_20260629.json` are
consistent with these identities. If a matrix entry is wrong, return FAIL and
give the corrected fraction.

## Proof-Text Audit

Confirm that the edits did not alter the core proof claims:

- finite positive weighted setup;
- algebraic direct sum versus orthogonal direct sum boundary;
- `P_N != P_C + P_A + P_B0` outside product weights;
- T1 product weight iff `A orthogonal B0`;
- T2 order defect iff product weights;
- T3 non-product pure-main-effect witness exists;
- nonzero wrong-order output is a sequential stripping artifact, not a true
  interaction residual;
- non-product implies existential witness only, not all inputs differ.

## Harness Boundary Audit

The v1.3 harness uses floating point regression checks. Audit whether every
current text says this clearly:

```text
The harness is deterministic regression support only.
The analytic proof and exact rational certificate carry the mathematical claim.
The harness is not a proof artifact.
```

Return FAIL if any text still treats JSON floats as exact proof.

## Bibliography And Duplicate-Risk Audit

Audit the bibliography with durable records. At minimum verify and position
against:

```text
Hooker 2007, Generalized Functional ANOVA Diagnostics for High-Dimensional Functions of Dependent Variables, DOI 10.1198/106186007x237892
Chastaing, Gamboa, Prieur 2012, Generalized Hoeffding-Sobol decomposition for dependent variables, DOI 10.1214/12-EJS749
Chastaing, Gamboa, Prieur 2014/2015 numerical methods, DOI 10.1080/00949655.2014.960415
Owen and Prieur 2017, DOI 10.1137/16m1097717
Iooss and Prieur 2019, DOI 10.1615/int.j.uncertaintyquantification.2019028372
Il Idrissi et al. 2025, DOI 10.1016/j.jmva.2025.105444
Bottcher and Spitkovsky 2010, A gentle guide to the basics of two projections theory, DOI 10.1016/j.laa.2009.11.002
Corach and Maestripieri, Products of orthogonal projections and polar decompositions, arXiv:1011.5237
Halmos two-subspace theory: verify exact record before recommending citation
```

For each record, say:

```text
verified / not_verified
how close it is
whether it forces wording changes
```

The safe novelty wording is:

```text
not a new ANOVA theory;
not a new dependent-input decomposition theory;
not a new noncommuting projection theory;
a compact finite weighted projection-order artifact note with an exact 2x2 witness.
```

Return `reject_as_duplicate_or_overclaim` if you find an exact duplicate.

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
- broad new noncommuting projection theory;
- holonomy / gluing / sheaf / curvature claims.

Allowed local ceiling remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## Required Output

Give:

1. top-level classification;
2. PASS/WARN/FAIL table;
3. exact arithmetic audit notes;
4. bibliography / duplicate-risk audit with durable records;
5. exact wording to keep/remove/change before posting;
6. final posting decision: post now / revise first / do not post;
7. a concise non-specialist explanation.
