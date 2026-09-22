# Why can equal results lead to different scientific futures

Yifan Chen · Independent researcher, Lu’an, China · ORCID 0009-0008-8344-1149

This repository contains the manuscript, exact mathematical checks, full original data for the proof-completion and coefficient-successor studies, source-mapped analysis inputs, figures, and offline reproduction entry points.

## One-command reproduction

On Linux x86_64, clone or unpack this repository and run:

```bash
./reproduce.sh
```

The default full run checks asset and raw-data SHA-256 identities, reanalyses both full raw datasets, checks the exact mathematics and source assembly, and compiles the five unchanged saved candidates in a network-disabled bubblewrap sandbox. It expects one acceptance and four rejections. The sixth request was truncated without a visible candidate and is never fabricated or compiled. No experimental model service is called.

Missing environment assets are downloaded from the fixed `nature-v8-r3` GitHub release and hash-verified before extraction. If `RELEASE_ASSETS` is already supplied beside the repository, no download is needed. `curl` is required only for the download path. Scientific analysis and sandboxed Lean compilation then run offline.

The supplied release assets contain Python 3.12.14 with locked packages and Lean 4.34.0-rc2 with pinned dependencies and the common-source build cache. The compiler recompiles each candidate; this is ordinary Lean verification, not an independent proof kernel. Host prerequisites are a Linux x86_64 glibc system, bash, tar, sha256sum, git, zstd and bubblewrap with unprivileged user namespaces. The full bundle has been tested on this configuration. Other OS/architectures are not claimed tested. Allow 30 GB free disk and about 8 GB available memory. Use `./reproduce.sh --analysis-only` to omit Lean and its large asset; this still uses the packaged Python and full raw data. Set `MAOFIELD_ASSETS=/path/to/assets` for another asset directory.

Outputs are written to a fresh `WORK/run_<UTC timestamp>` directory. Its `STATUS.json` records actual step outcomes. A nonzero exit means a failed or unavailable step, not a scientific rejection. No host or unsandboxed fallback runs Lean.

## Data and environment

`data/raw/HCLOSE.zip` and `SUCCESSOR.zip.part00/part01` contain all original payloads for the two studies, including original model reasoning, requests, candidates, compiler records and stopped/unknown states. The script joins and verifies the successor parts. `data/raw/MANIFEST.json` pins all bytes. Source-mapped reviewer inputs remain in `REPRODUCIBILITY` and are checked against a fresh export from the originals.

The same repository's prepared Release assets include `full-scientific-history.zip`, with the complete earlier-workflow archive and file-level provenance; `python-linux-x86_64.tar.gz`; and the two `lean-offline-linux-x86_64.tar.zst.part*` files. These files accompany the fixed `nature-v8-r3` Release and the linked Zenodo archives. The full-history archive is optional for reproducing the present two studies and preserves earlier failures and unrun proposals. It is never executed by the default entry point. `environment/SHA256SUMS` and `LEAN_PARTS.sha256` verify the environment. The script joins the two Lean parts and verifies the complete archive hash.

## Evidence boundary

The finite minimax witness and compact local repair are analytical statements. Successor studies are simulation/workbench records; selected traces do not establish a general history effect. The proof-completion comparison is one post-selected paired case, not six independent replications and not a full Navier–Stokes proof. Ordinary Lean replay reproduced the saved outcomes. Independent-kernel verification remains NOT_RUN. See `AUDIT` for original review findings and targeted resolutions.

## Licence and citation

Original code is Apache-2.0; original manuscript, figures and data are CC BY 4.0, to the extent of the contributor's rights. Third-party sources, model outputs and environment components retain their respective notices; see `LICENSE_STATUS.md` and `environment/THIRD_PARTY_NOTICES.md`. No blanket relicensing is intended. See `CITATION.cff`. Preprint: https://doi.org/10.5281/zenodo.22904545. Software and environments: https://doi.org/10.5281/zenodo.22904605. Full retained data: https://doi.org/10.5281/zenodo.22904604. This is a separate manuscript from the older R3.0 work; its existing DOI identifiers are not assigned to this release.
