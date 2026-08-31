# MaoField: scientific history, current equivalence and future intervention

This repository is the public MaoField R3.0 software and reproducibility release for the Article **"Opposed statistical extremes reveal an identification boundary in causal tests of AI scientific agents."** The canonical preprint is https://doi.org/10.5281/zenodo.22209245.

`main` is the sole authoritative R3.0/NMI reproducibility branch. All other branches are retained only as historical records and are not release, citation or reproduction authorities; no historical branch is merged into this release. Historical commit metadata, including existing Claude `Co-Authored-By` trailers, is preserved verbatim.

Early repository development used Anthropic Claude. Final Phase 23 analysis, manuscript drafting and release engineering used ChatGPT Pro/Web Pro and OpenAI Codex. Yifan Chen is the sole human author and assumes full responsibility for the scientific judgement, statistics, claims, text and released artifacts. See `docs/AI_ASSISTANCE_DISCLOSURE.md`.

## The scientific object

MaoField does not treat history as a fact list, token trace or present conclusion. Its minimum scientific-history carrier is a practice-grounded relation:

```text
rejected route R
↔ decisive practice P
↔ external evidence E
↔ scope S
↔ reopening condition K
```

The study asks whether histories that are equal under a **prespecified evaluator-visible current-content map** nevertheless generate different future responses in fresh, clean successors.

## Identification chain

```text
P0 practice-grounded history
→ RPESK carrier
→ C_flat current-content coarse-graining
→ future response law Ψ_h(i)
→ system-side defect D_I(C)
→ clean-successor randomized experiment
→ Direct P1/P5
→ independent A_SIB and M_R channels
→ P2/P3/P4
→ evaluator kernel K_i
→ evaluator-visible defect D_I^K(C)
→ claim-specific separation and claim ceiling
```

Measurement is the epistemic bridge from observed statistics to system-side facts; it is not the entire theory of scientific history. See `docs/EXECUTABLE_CLAIM_GRAPH.md` and `provenance/executable_claim_graph.json`.

## Three contributions

1. **Formal identification principle.** Evaluator-visible current equivalence does not establish future intervention equivalence without claim-relevant separation.
2. **Empirical phenomenon.** Phase 23 produced exact treatment invariance and a near-saturated channel gap, each recurring in held-out worlds, while frozen calibration placed both in the same non-identification class. Replication stabilized the statistics, not their scientific meaning.
3. **Reusable causal architecture.** Five randomized history arms, four future cells, common worlds and scorers, independent clean successors, sealed replication, typed failures and a non-compensatory result tree provide a reusable test of practice-grounded scientific history.

A disjoint GLM provider branch passed ordinary behavioural controls but established neither a complete history-inheritance signature, a bounded null nor valid structural dissociation. It shows that an evaluator can be operationally competent yet scientifically non-separating for another claim family.

The repository does **not** claim universal HFI, a proved action–structure dissociation, a Transformer defect, a universal benchmark collapse or actual future-response divergence.

## Offline reproduction

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r environment/requirements.txt
bash scripts/reproduce_offline.sh
```

This path uses frozen processed results and source-data tables. It makes **zero model or provider calls** and rebuilds the public statistical checks and figures. The generated receipt verifies the executable claim chain from released inputs to display items and final proposition states.

## Evidence tiers

- **Public release tier:** this repository's source, processed source data, display figures, manifests and no-provider offline workflow.
- **Reviewer-only tier:** auditable raw endpoint ledgers, assignments, permitted provider records and execution lineage under controlled access; these files are not stored in this repository.
- **Permanently private tier:** credentials, private/decryption keys, provider-restricted content and reusable hidden-answer material.

Controlled-access requests are governed by `docs/CONTROLLED_ACCESS_POLICY.md` and are answered within 14 business days. No unrestricted hidden answers or secrets are supplied.

## Release and submission identifiers

- GitHub Release: <https://github.com/Wangziqi0/MaoField/releases/tag/R3.0>
- Zenodo software DOI: <https://doi.org/10.5281/zenodo.22209301>
- Zenodo source-data DOI: <https://doi.org/10.5281/zenodo.22209309>
- Canonical Zenodo preprint DOI: <https://doi.org/10.5281/zenodo.22209245> (CC BY 4.0; 31 August 2026)
- Journal submission identifier: NMI initial submission not yet submitted

## Licences

- Code: Apache License 2.0.
- Original data, documentation, manuscript text and figures: Creative Commons Attribution 4.0 International.
- Restricted provider records and hidden-answer material are excluded and receive no public licence.

See `LICENSE`, `LICENSES/`, `QUICKSTART.md`, `REPRODUCIBILITY.md`, `docs/RELEASE_MATRIX.md` and `docs/PREPRINT_AND_SUBMISSION_SEQUENCE.md`.
