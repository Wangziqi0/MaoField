# Node22 Vector Refresh -- Formal Zenodo Preprint Prep

Date: 2026-07-04 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260704_1120_formal_zenodo_preprint_prep`

## Purpose

Refresh the canonical MaoField RAG index after formal Zenodo `Publication ->
Preprint` preparation docs were added for Open-MaoField.

RAG remains a locator only. It is not proof, DOI-publication authority,
arXiv/journal-submission authority, peer-review authority, or evidence for
MaoField empirical claims.

## Scope And Promotion

Sidecars for this refresh use the tag:

```text
20260704_1120_formal_zenodo_preprint_prep
```

Key results:

```text
active files: 586
chunks: 11945
kb.faiss sha256: 27b7312d2a799fdb0c125c70d3bfb6894919b37eefed08fd77c545c0a3761c57
kb_meta.jsonl sha256: f20a77d47162b380ebe9b17c13b3ac6bb1463cbc074fd35b355f2567c9c3e97f
node22 port 18080 after build: not running
```

## Smoke Targets

Smoke queries locate:

- `docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PREP_20260704.md`;
- `docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_FORM_VALUES_20260704.md`;
- `STATE.md` with `READY_TO_RESERVE_FORMAL_PREPRINT_DOI`;
- the boundary that the existing DOI `10.5281/zenodo.21157578` is a
  repository/software DOI, not a formal preprint DOI;
- Mode B `insufficient_artifact`;
- duplicate risk `MEDIUM`.

## Boundary

This refresh must not be treated as evidence that a formal Zenodo preprint has
already been published, an arXiv/journal submission has occurred, peer review
has occurred, a full panel has run, training/inference occurred, or any
MaoField residual, interaction, transport, holonomy, glass-box, F3, or LOSO
result has been observed.

