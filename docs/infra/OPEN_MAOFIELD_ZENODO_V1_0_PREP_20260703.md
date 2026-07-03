# Open-MaoField Zenodo / v1.0.0 Preparation

Date verified: 2026-07-03 16:30:27 CST on node36.

## Public Repository State

- Repository: `https://github.com/Wangziqi0/Open-MaoField`
- Branch: `main`
- Public commit prepared for Zenodo/v1.0.0 metadata:
  `a7192065ee1e1ffce23785f906970a308a134ffa`
- Commit message: `docs: prepare v1.0.0 zenodo release metadata`

## Added / Updated Public Files

- `.zenodo.json`
- `CITATION.cff`
- `README.md`
- `MANIFEST.sha256`
- `docs/release_notes_v1.0.0.md`
- `docs/zenodo_release_checklist_v1.0.0.md`

## Verification

Public repo checks run on node36:

- `jq . .zenodo.json` passed.
- `CITATION.cff` parsed as YAML and `version == 1.0.0`.
- `sha256sum -c MANIFEST.sha256` passed.
- `git diff --check` passed before commit.
- Exact rational witness rerun passed:
  `all_checks_passed=True`,
  JSON sha256 `0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6`.
- Deterministic harness rerun passed:
  `all_synthetic_controls_passed=True`.
- Public risk-term scan returned only boundary/negative-context matches.

Scratch verification directory:

```text
/home/amd/codex-node36/tmp/open_maofield_v1_0_verify_20260703/
```

## Zenodo Rules Verified From Official Docs

Zenodo official help says:

- A repository must be enabled from Zenodo's GitHub settings before new
  releases are automatically ingested and archived.
- `.zenodo.json` can provide Zenodo-specific metadata.
- If both `.zenodo.json` and `CITATION.cff` exist, Zenodo uses
  `.zenodo.json` and ignores `CITATION.cff` for GitHub release archiving.
- After a repository is enabled, creating a GitHub release lets Zenodo process
  and archive it; the DOI exists only after Zenodo finishes processing.

Sources:

- `https://help.zenodo.org/docs/github/enable-repository/`
- `https://help.zenodo.org/docs/github/describe-software/zenodo-json/`
- `https://help.zenodo.org/docs/github/archive-software/github-upload/`

## Current Release Boundary

Prepared but not yet done:

- Zenodo repository integration: `NOT_CONFIRMED_BY_NODE36`
- GitHub Release `v1.0.0`: `NOT_CREATED`
- Zenodo DOI: `NO`
- arXiv / journal submission: `NO`
- peer review: `NO`

Do not cite a DOI until Zenodo displays one.

## Claim Boundary

This v1.0.0 preparation does not change the scientific ceiling:

- Mode B MaoField empirical status remains `insufficient_artifact`.
- Duplicate risk remains `MEDIUM`.
- No MaoField empirical positive result is claimed.
- No full panel, checkpoint inference, training, new loss, F3/LOSO pass,
  glass-box break, observed residual/interaction/transport/holonomy field,
  completed broad theory, or harness/JSON-as-proof claim is authorized.

## Next Step

Human owner should enable `Wangziqi0/Open-MaoField` in Zenodo first. Only after
that should node36 create the GitHub Release `v1.0.0`, so Zenodo can archive the
release and mint the DOI.
