# Open-MaoField Zenodo DOI Backfill

Date verified: 2026-07-03 17:07:29 CST on node36.

## Zenodo Record

- Zenodo record URL: `https://zenodo.org/records/21157578`
- API record URL: `https://zenodo.org/api/records/21157578`
- Repository/software release DOI: `10.5281/zenodo.21157578`
- Concept DOI: `10.5281/zenodo.21157577`
- DOI URL: `https://doi.org/10.5281/zenodo.21157578`
- Resource type from Zenodo API: `Software`
- Version from Zenodo API: `1.0.0`
- Title from Zenodo API:
  `Open-MaoField: Finite Projection Order Defects in Residual Metric Audits`
- Creator from Zenodo API: `Chen, Yifan`
- Publication date from Zenodo API: `2026-07-03`
- License from Zenodo API: `apache2.0`

This is the GitHub-Zenodo archived repository/software release DOI. It is not a
separate Zenodo `Publication -> Preprint` DOI.

## Public Repository Backfill

Public repository:

```text
https://github.com/Wangziqi0/Open-MaoField
```

Post-release DOI metadata commit:

```text
7aba164 docs: record Zenodo DOI for v1.0.0
```

Files updated:

- `README.md`
- `CITATION.cff`
- `MANIFEST.sha256`
- `docs/release_notes_v1.0.0.md`
- `docs/zenodo_release_checklist_v1.0.0.md`

GitHub Release `v1.0.0` body was edited to display:

```text
Zenodo repository/software release DOI: https://doi.org/10.5281/zenodo.21157578
Zenodo concept DOI: https://doi.org/10.5281/zenodo.21157577
```

The release target remains:

```text
a7192065ee1e1ffce23785f906970a308a134ffa
```

No new GitHub release was created for the DOI backfill, to avoid creating an
unnecessary second release DOI.

## Verification

Public repo checks:

- `CITATION.cff` parsed as YAML.
- `doi == 10.5281/zenodo.21157578`.
- `version == 1.0.0`.
- `sha256sum -c MANIFEST.sha256` passed.
- `git diff --check` passed.
- Public main readback points to commit `7aba1649c1a08a728694f6be82dcefecae781353`.

## Boundary

- This is now a citable repository/software release DOI.
- It is not a peer-reviewed publication.
- It is not an arXiv/journal submission.
- It is not a separate Zenodo preprint DOI.
- It does not change Mode B MaoField empirical status.
- Mode B remains `insufficient_artifact`.
- Duplicate risk remains `MEDIUM`.
- No MaoField empirical positive result, full-panel execution, checkpoint
  inference, model training, new loss, observed deployed-model field,
  glass-box claim, F3/LOSO pass, completed broad theory, or harness/JSON-as-proof
  claim is authorized.

## Next Step For Formal Preprint

If PI wants a formal Zenodo preprint, create a separate Zenodo upload:

```text
Resource type: Publication
Publication type: Preprint
Main file: paper/preprint.pdf
```

Reserve that preprint DOI before publication if the DOI should appear inside the
PDF. After reserve DOI, node36 should patch TeX/PDF and metadata, then PI can
publish the Zenodo preprint record.
