# Preprint, repository, archive and NMI release sequence

## Recommended same-day sequence

1. Freeze the final manuscript, repository and release manifests; record SHA-256 values.
2. Create the public GitHub release and a persistent reviewer-only archive; test all links. Do not publish secrets or restricted provider/hidden-answer material.
3. Mint the Zenodo software/data archive from the exact GitHub release after licences are author-confirmed.
4. Do not submit to arXiv in this release; publish the canonical Zenodo preprint using the final preprint text. Primary category: `cs.AI`; suggested secondary categories: `cs.LG`, `cs.MA`. Final classification is subject to arXiv moderation and author endorsement.
5. Submit to Nature Machine Intelligence through the online system and disclose the actual preprint identifier, DOI and licence in the submission fields and cover letter.
6. Cross-link the GitHub release and four Zenodo records; the Zenodo preprint is canonical. Update the preprint record with the journal DOI if published.

## Version wording

```text
Version 1. Preprint; not peer reviewed.
Journal submission status: RESOLVED_IN_R3.0_RELEASE.
This version reports the frozen Phase 23 and GLM terminal analyses and an explicitly labelled post-hoc identification audit. No endpoint, threshold, model, world or confirmatory result was changed by the audit.
```

## Accurate significance summary

AI-agent evaluations often infer retained history from current answers, retrieval scores or structural reports. MaoField asks two different questions: whether a current state is sufficient for future intervention responses, and whether the evaluator can identify that sufficiency. A preregistered causal study produced an exact null-like extreme and a near-saturated dissociation-like extreme, each recurring in held-out worlds, while independent calibration showed that neither identified its apparent conclusion. A disjoint provider replication passed ordinary behavioural controls but still established neither history inheritance, a bounded null nor valid structural dissociation. The result is a claim-specific identification boundary: reproducible statistical extremity cannot substitute for an evaluator shown to separate the future response laws relevant to the claim.


## R3.0 published identifiers

- Canonical preprint: https://doi.org/10.5281/zenodo.22209245 (CC BY 4.0; 31 August 2026)
- Software: https://doi.org/10.5281/zenodo.22209301 and https://github.com/Wangziqi0/MaoField/releases/tag/R3.0 (Apache-2.0)
- Source data: https://doi.org/10.5281/zenodo.22209309 (CC BY 4.0)
- Reviewer evidence metadata: https://doi.org/10.5281/zenodo.22209316 (files restricted; no redistribution)
- arXiv: NOT_SUBMITTED_BY_PI_DECISION
