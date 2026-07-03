# V2.5 Final Synthesis Comparison And Adoption

Date verified on node36: 2026-07-03 15:41-16:00 CST

## Input Package

User-provided attachment:

```text
/home/amd/.codex/attachments/721b7855-21b3-4007-b3c3-ee4e665f7bed/MaoField_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.zip
```

Input zip SHA256:

```text
06b9e9c15956741843ba377e89a8b1f94c67bc15e94f4a39bbf7ee8cd8ecd204
```

The package SHA256SUMS file verified successfully for:

```text
848d6a37bd9310578f8efb4991d60f6892528c029fde976aa08133f2640bef59  MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex
83b21463351d578e2a22b4785c9fe97e34e9ab4006e77d153895860933ddddde  MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.pdf
10d52534216fe6a83101dda1284c4b82b7f25c37c7087cba59ec40c6ba5535c9  V2_5_FINAL_SYNTHESIS_RELEASE_GATE_NOTE_20260703.md
0bb23498cf3c230f2bacd0744bc09ae136cb065691d0c025cc11d1e056c97853  V2_5_SOURCE_MAP_AND_CHANGELOG_20260703.md
97759a9e576d7dfb6852acd42a10648dc513751cefb565aee12c2fc5830f46ab  render_contact_sheet.png
```

## Difference From V2.4

V2.5 keeps the V2.4 title and author metadata:

```text
Finite Projection Order Defects in Residual Metric Audits:
A Mathematical Starting Point for Black-Box Evaluation

Yifan Chen
```

Main changes relative to the canonical V2.4 under-lock source:

- visible `PROGRAMMATIC_PREPRINT_DRAFT_CANDIDATE_UNDER_LOCK` block is removed;
- paper-facing `Scope and claim boundary` paragraph is used instead;
- `draft` wording is mostly changed to `manuscript`;
- V2.5 includes a compiled 8-page PDF and render contact sheet;
- bibliography is simplified in places compared with V2.4, especially selected
  arXiv version suffixes and the Il Idrissi author list;
- V2.5 reintroduces `measurement field` / `weighted evaluation field` wording.

## Adoption Decision

Adopt V2.5 as the current final-synthesis manuscript package because it has a
compiled PDF, preserves the finite theorem and exact witness, keeps the
Mode B boundary, keeps `MEDIUM duplicate risk`, and removes the most visibly
internal under-lock governance block from the paper text.

Canonical note: after package verification, the promoted source-map/changelog
markdown was wording-normalized in three places (`accepted proof chain`,
`accepted commutator proof`, `accepted title`) to avoid publication-status
ambiguity. The TeX, PDF, release-gate note, and contact sheet remain byte-identical
to the verified package files.

Do not treat V2.5 as peer reviewed, submitted, accepted, Zenodo-archived, or
as a GitHub Release. Public upload to `Open-MaoField` is a repository commit
only unless the PI separately creates a release or DOI.

## Risk Notes

The phrase `measurement field` / `weighted evaluation field` is accepted as
paper-facing language in this package, but it must not be used to claim an
observed residual, interaction, transport or holonomy field in MaoField data.

Bibliography remains `MEDIUM duplicate risk`. Before journal/arXiv/DOI use,
run another authoritative metadata pass.

## Local Verification

PDF metadata on node36:

```text
Producer: pdfTeX-1.40.26
Pages: 8
File size: 243837 bytes
PDF version: 1.7
```

PDF text was extracted with `pdftotext` for claim scanning. The rendered contact
sheet was inspected on node36; no obvious clipping, overlap, black-square glyph
failure, or equation truncation was seen.

Forbidden-claim scan found no positive matches outside boundary/negative
contexts for paper-ready, preprint-ready, public-postable, posted, submitted,
accepted, submission-authorized, broad new theory, completed formal system,
MaoField empirical positive result, full panel, checkpoint inference, training,
new loss, observed MaoField residual/interaction/transport/holonomy field,
glass-box success, F3 positive, LOSO passed, JSON-float proof or harness proof.

## Durable Artifacts Promoted To Canonical

```text
docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex
docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.pdf
docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_RENDER_CONTACT_SHEET_20260703.png
docs/infra/recovery/V2_5_FINAL_SYNTHESIS_RELEASE_GATE_NOTE_20260703.md
docs/infra/recovery/V2_5_SOURCE_MAP_AND_CHANGELOG_20260703.md
```

## Public Repository Update

`Open-MaoField` will be updated with the V2.5 TeX/PDF/contact sheet and source
map while retaining the public claim-boundary and duplicate-risk notes. No
GitHub Release or Zenodo DOI is created by this adoption step.
