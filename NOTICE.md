# NOTICE — MaoField v0.1.1

## Copyright

© 2026 Yifan Chen (Chen Yifan). All rights not explicitly granted by the licenses below are reserved.

## Licenses

MaoField is a dual-licensed project:

| Artifact class | License | SPDX |
|---|---|---|
| Research manuscript (`paper/arxiv_v1_full.md`, PDF outputs, figures) | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |
| Experimental data (stationary-state field snapshots `states_*.bin`, observables JSON, analysis outputs) | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |
| Source code (Rust engines, Python analysis scripts) | MIT License | `MIT` |
| Review records (`REVIEW_*.md`), verdicts, task specifications | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |

Full license texts:
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/legalcode
- MIT: https://opensource.org/license/mit/

## Third-party credits

### Upstream datasets
- **BEIR benchmark suite** (Thakur et al., 2021 — NeurIPS Datasets Track). NFCorpus, SciFact, FiQA, ArguAna, TREC-COVID subsets used in arXiv v1 §4.2. Each BEIR dataset carries its own license; refer to the BEIR repository for terms.

### Upstream models
- **BGE-M3 embedding model** (Chen et al., 2024 — BAAI). Used as the base semantic encoder producing the 1024-dimensional source fields `S₀` in arXiv v1 §4.6 and Phase B Experiment 1 (`experiments/exp017_dialectics/results/phase_b_exp1/`). BGE-M3 is distributed under MIT license; see https://huggingface.co/BAAI/bge-m3.
- **BGE-reranker-v2-m3** (Chen et al., 2024 — BAAI). Used as the SOTA baseline in arXiv v1 §4.2 Block I. Same licensing as BGE-M3.

### Software dependencies
- `rayon` (crates.io) — MIT / Apache 2.0 dual license.
- `serde`, `serde_json` (crates.io) — MIT / Apache 2.0 dual license.
- `numpy`, `scipy` (PyPI) — BSD-3-Clause.
- `pandoc`, `pdflatex`, `lualatex` — GPL family (used as external build tools, not redistributed).

## Review protocol attribution

The spawn-agent review pipeline institutionalized throughout this project was developed jointly during 2026-04-13–15 by the principal investigator (Yifan Chen) and two research-assistant agent instances (referred to internally as "Win" and "Linux"). The protocol and the 27+ review records it produced during arXiv v1 preparation and the Phase B Experiment 1 campaign are part of the methodological contribution of the v0.1.1 release; they are released under CC BY 4.0.

## Archival

All release artifacts are mirrored on Zenodo under concept DOI [`10.5281/zenodo.19550341`](https://doi.org/10.5281/zenodo.19550341). Specific version DOIs are issued per release; the v0.1.1 version DOI will be assigned upon Zenodo publication.

## Contact

For licensing questions, corrections, or reuse inquiries: Yifan Chen, [ORCID 0009-0008-8344-1149](https://orcid.org/0009-0008-8344-1149).
