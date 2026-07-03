# Node22 Vector Refresh -- Open-MaoField DOI Backfill

Date: 2026-07-03 CST
Authority: node36
Worker: node22 one-shot GPU embedding service
Project: MaoField
Tag: `20260703_1708_open_maofield_doi_backfill`

## Purpose

Refresh the canonical MaoField RAG index after Zenodo record
`https://zenodo.org/records/21157578` was verified and the DOI was backfilled
into the public `Open-MaoField` repository and canonical status files.

RAG remains a locator only. It is not proof, arXiv/journal-submission authority,
peer-review authority, or evidence for MaoField empirical claims.

## Sidecars

Exact active-file count, chunk count, scope hash, build log, candidate hashes,
promoted hashes, smoke outputs, and node22 start/stop records are kept in
sidecars named with this tag:

```text
20260703_1708_open_maofield_doi_backfill
```

## Smoke Targets

Smoke queries must locate:

- `docs/infra/OPEN_MAOFIELD_ZENODO_DOI_BACKFILL_20260703.md`;
- `STATE.md` with Zenodo repository/software DOI `10.5281/zenodo.21157578`;
- concept DOI `10.5281/zenodo.21157577`;
- the no-Zenodo-preprint/no-peer-review boundary;
- Mode B `insufficient_artifact`;
- duplicate risk `MEDIUM`.

## Boundary

This refresh must not be treated as evidence that a separate Zenodo preprint has
been published, an arXiv/journal submission has occurred, peer review has
occurred, a full panel has run, training/inference occurred, or any MaoField
residual, interaction, transport, holonomy, glass-box, F3, or LOSO result has
been observed.
