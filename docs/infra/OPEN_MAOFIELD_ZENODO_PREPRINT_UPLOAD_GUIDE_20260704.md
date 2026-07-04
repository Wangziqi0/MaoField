# Open-MaoField Zenodo Formal Preprint Upload Guide

Date verified: 2026-07-04 16:48:36 CST.

Superseded status note, added 2026-07-04 18:24 CST:

```text
This upload guide is superseded by the published formal Zenodo preprint record
docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md.
The live formal preprint DOI is 10.5281/zenodo.21190475.
```

Use this guide for a new Zenodo upload. Do not edit the existing GitHub-Zenodo
software record for this step.

## Upload Decision

```text
Target: formal Zenodo preprint
Current state: READY_TO_RESERVE_FORMAL_PREPRINT_DOI
Already published: repository/software DOI 10.5281/zenodo.21157578
Not yet published: separate formal preprint DOI
```

## Files On Node19 Desktop

```text
C:\Users\amd\Desktop\Open-MaoField_Formal_Zenodo_Preprint_READY_TO_RESERVE_DOI_20260704_1110.zip
C:\Users\amd\Desktop\OPEN_MAOFIELD_ZENODO_PREPRINT_UPLOAD_GUIDE_20260704.md
C:\Users\amd\Desktop\OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_FORM_VALUES_20260704.md
C:\Users\amd\Desktop\OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PREP_20260704.md
```

Zip SHA256:

```text
83d1ab698c37e8c5756cd467e6de7125cda6d9a8c863be2d221a451d45875144
```

## Zenodo Steps

1. Sign in to Zenodo.
2. Create a new upload.
3. Choose upload/resource type:

```text
Publication
```

4. Choose publication type:

```text
Preprint
```

5. Upload the primary manuscript from inside the zip:

```text
Open-MaoField_Formal_Zenodo_Preprint_READY_TO_RESERVE_DOI_20260704/paper/preprint.pdf
```

6. Optional supporting files from inside the zip:

```text
paper/preprint.tex
README.md
CITATION.cff
docs/claim_boundary_note.md
docs/duplicate_risk_note.md
certificate/exact_witness_certificate.py
certificate/exact_witness_v1_4_20260629.json
harness/deterministic_harness.py
harness/synthetic_harness_v1_3_20260628.json
MANIFEST.sha256
```

7. Fill metadata with `OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_FORM_VALUES_20260704.md`.
8. Add the repository/software release DOI as a related identifier:

```text
10.5281/zenodo.21157578
```

Suggested relation from the preprint record:

```text
Is supplemented by
```

9. Click `Reserve DOI` first.
10. If you want the reserved DOI inside the PDF/TeX, stop after reserve and send
    the reserved DOI to node36 for a DOI-backfill compile step.
11. If metadata-only DOI is acceptable, preview the record carefully, then publish.

## Metadata Values

Title:

```text
Finite Projection Order Defects in Residual Metric Audits: A Mathematical Starting Point for Black-Box Evaluation
```

Creator:

```text
Yifan Chen
```

Publication date if published today:

```text
2026-07-04
```

Version:

```text
1.0.0-preprint
```

Language:

```text
English
```

Description:

```text
This preprint studies a finite-dimensional projection-order defect in residual metric audits. In a positive weighted two-way table, product weights are equivalent to orthogonality of the centered row and column main-effect spaces and to order-independence of two declared sequential stripping maps. Under non-product weights, an exact rational 2 x 2 witness shows that a wrong sequential stripping order can create a nonzero procedural output for a pure-main-effect object whose true additive residual is zero. The result is intentionally bounded: it is a finite mathematical note and a starting point for black-box evaluation methodology, not a broad new ANOVA theory, not an empirical MaoField positive result, and not a claim that language-model residual, interaction, transport, or holonomy fields have been observed. The accompanying Open-MaoField repository release provides the exact certificate, deterministic regression harness, source files, and claim-boundary notes.
```

Keywords:

```text
projection order defects
weighted two-way tables
finite-dimensional Hilbert spaces
residual metric audits
black-box evaluation
functional ANOVA
dependent inputs
orthogonal projections
exact rational certificate
MaoField
```

Recommended manuscript license:

```text
Creative Commons Attribution 4.0 International (CC BY 4.0)
```

Repository/code license remains:

```text
Apache License 2.0
```

## Must Not Claim

- Do not call `10.5281/zenodo.21157578` the preprint DOI.
- Do not claim peer review.
- Do not claim arXiv or journal submission.
- Do not claim MaoField empirical positive evidence.
- Do not claim full-panel execution, checkpoint inference, model training, or
  a new optimization loss.
- Do not claim observed residual, interaction, transport, or holonomy fields in
  deployed models.
- Do not claim broad new ANOVA, dependent-input, projection, model-collapse, or
  interpretability theory.
- Do not claim the deterministic harness or JSON floats prove the theorem.

## After Publication

Send the new formal preprint DOI and Zenodo record URL back to node36. Then
node36 should backfill:

- `STATE.md`;
- public `Open-MaoField` README/CITATION/release notes if needed;
- canonical release records;
- RAG index;
- git commit and push.
