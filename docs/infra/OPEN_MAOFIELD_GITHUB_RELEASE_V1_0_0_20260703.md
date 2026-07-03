# Open-MaoField GitHub Release v1.0.0

Date verified: 2026-07-03 16:53:58 CST on node36.

## Release Created

- Repository: `https://github.com/Wangziqi0/Open-MaoField`
- Release: `v1.0.0`
- Release URL: `https://github.com/Wangziqi0/Open-MaoField/releases/tag/v1.0.0`
- Published at: `2026-07-03T08:52:41Z`
- Target commit: `a7192065ee1e1ffce23785f906970a308a134ffa`
- Draft: `false`
- Prerelease: `false`

Local verification:

```text
gh release view v1.0.0 --repo Wangziqi0/Open-MaoField
git fetch --tags origin
git rev-parse v1.0.0
```

The fetched tag resolves to:

```text
a7192065ee1e1ffce23785f906970a308a134ffa
```

## Zenodo Status

PI reported that the Zenodo GitHub integration for `Wangziqi0/Open-MaoField`
was enabled before node36 created the release.

Current DOI state from node36:

```text
Zenodo release DOI: PENDING_NOT_CONFIRMED_BY_NODE36
Zenodo preprint DOI: NO
```

Zenodo search/API did not return a precise `Open-MaoField` DOI during the
immediate post-release check. This is not a failure; Zenodo ingestion can lag.
Do not cite any DOI until it is visible on the Zenodo record.

## Release Body Boundary

The release body says this is a public sanitized release of the finite
projection-order-defect line and preserves the boundary:

- no MaoField empirical positive result;
- no full-panel execution;
- no checkpoint inference;
- no model training;
- no new optimization loss;
- no deployed-model residual/interaction/transport/holonomy observation;
- no completed broad theory;
- no claim that JSON floats or deterministic harness prove the theorem;
- duplicate risk remains `MEDIUM`.

## Next Step

1. Wait for Zenodo to finish GitHub release archiving.
2. Copy the generated repository/software release DOI back to node36.
3. Create a separate Zenodo `Publication -> Preprint` upload for the PDF if the
   target is a formal Zenodo preprint rather than only a software/repository
   release.
4. Reserve the preprint DOI before publishing if the DOI should appear in the
   PDF front matter.
5. After the DOI exists, patch public repo metadata and canonical status.
