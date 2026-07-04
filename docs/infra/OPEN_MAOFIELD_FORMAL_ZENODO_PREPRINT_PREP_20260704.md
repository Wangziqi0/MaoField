# Open-MaoField Formal Zenodo Preprint Prep

Date verified: 2026-07-04 11:10:50 CST.

Canonical repo HEAD at preflight: `d2b91c5 docs(release): record Open-MaoField Zenodo DOI`.

Public repo preflight source:

```text
/home/amd/codex-node36/tmp/open_maofield_public_seed_20260703/repo
HEAD: 7aba164 docs: record Zenodo DOI for v1.0.0
```

## Verdict

```text
READY_TO_RESERVE_FORMAL_PREPRINT_DOI
```

This is not yet `PUBLISHED_FORMAL_PREPRINT`.

The existing Zenodo DOI `10.5281/zenodo.21157578` is a repository/software release DOI. For a formal preprint, create a new Zenodo upload with resource type `Publication -> Preprint`.

## Preflight Checks

- `date`: verified `2026-07-04 11:10:50 CST (+0800)`.
- Canonical `STATE.md`: read before this preparation.
- RAG query: `Open-MaoField formal preprint Zenodo DOI v1.0 exact witness forbidden claim boundary`.
- Public manifest: `sha256sum -c MANIFEST.sha256` PASS.
- PDF check: `paper/preprint.pdf` is 8 pages, not encrypted, no JavaScript.
- Exact witness rerun in SSD scratch:
  - output JSON hash: `0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6`;
  - `all_checks_passed=True`;
  - generated JSON matches tracked public JSON byte-for-byte.
- Harness rerun in SSD scratch:
  - controls pass;
  - regenerated JSON differs from tracked public JSON only by `created_utc`;
  - tracked public harness JSON remains manifest-verified.
- Forbidden-claim scan over public README, paper, docs, certificate and harness found only boundary-context occurrences. No positive MaoField empirical claim was detected in the public release surface.
- Bibliography metadata was checked against Crossref for the core DOI floor. Lamboni DOI metadata currently resolves as SIAM/ASA JUQ 14(2), 691-710, published online/date `2026-06-30`; Böttcher spelling resolves as `A. Böttcher` in Crossref.
- arXiv metadata was checked through the arXiv API for the listed LLM-evaluation and projection references. One initial timeout for `2206.04615` succeeded on retry.

## Formal Preprint Boundary

Allowed:

- A bounded finite-dimensional mathematical preprint about projection order defects in finite positive weighted two-way tables.
- An exact rational 2 x 2 witness and analytic proof as the mathematical evidence.
- The Open-MaoField repository/software DOI as a related reproducibility artifact.

Forbidden:

- MaoField empirical positive result.
- Full-panel execution.
- Checkpoint inference or model training.
- New optimization loss.
- Observed residual, interaction, transport, or holonomy field in deployed models.
- F3 positive or LOSO passed.
- Glass-box broken.
- Broad new ANOVA, dependent-input decomposition, projection-product, or interpretability theory.
- JSON floats or deterministic harness outputs as proof.
- Peer review, arXiv submission, or journal submission unless those events actually occur.

## Recommended Release Sequence

1. Create a new Zenodo upload.
2. Choose `Publication -> Preprint`.
3. Fill the form using `OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_FORM_VALUES_20260704.md`.
4. Upload `paper/preprint.pdf` as the primary manuscript.
5. Add `paper/preprint.tex` as source if desired.
6. Add the repository/software DOI `10.5281/zenodo.21157578` as a related identifier, not as the preprint DOI.
7. Click `Reserve DOI` first.
8. If DOI-in-PDF polish is required, stop after reserve and send the reserved preprint DOI back to node36 for TeX/PDF metadata update. Node36 currently has no local LaTeX compiler in PATH, so PDF recompilation must be done on a machine with a LaTeX toolchain or by an external compile service.
9. If DOI-in-PDF polish is not required, publish after final human preview.

## Current Hard Stop

Do not call the current Zenodo software DOI a formal preprint DOI. The formal preprint becomes live only after the separate Zenodo `Publication -> Preprint` upload is published.

