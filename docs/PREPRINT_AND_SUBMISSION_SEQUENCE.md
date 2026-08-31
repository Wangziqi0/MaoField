# Preprint, repository, archive and NMI release sequence

## Recommended same-day sequence

1. Freeze the final manuscript, repository and release manifests; record SHA-256 values.
2. Create the public GitHub release and a persistent reviewer-only archive; test all links. Do not publish secrets or restricted provider/hidden-answer material.
3. Mint the Zenodo software/data archive from the exact GitHub release after licences are author-confirmed.
4. Submit the arXiv preprint using the final preprint text. Primary category: `cs.AI`; suggested secondary categories: `cs.LG`, `cs.MA`. Final classification is subject to arXiv moderation and author endorsement.
5. Submit to Nature Machine Intelligence through the online system and disclose the actual preprint identifier, DOI and licence in the submission fields and cover letter.
6. Cross-link the real GitHub release, Zenodo DOI and arXiv record. Update the preprint record with the journal DOI if published.

## Version wording

```text
Version 1. Preprint; not peer reviewed.
Journal submission status: AUTHOR_INPUT_NEEDED.
This version reports the frozen Phase 23 and GLM terminal analyses and an explicitly labelled post-hoc identification audit. No endpoint, threshold, model, world or confirmatory result was changed by the audit.
```

## Accurate significance summary

AI-agent evaluations often infer retained history from current answers, retrieval scores or structural reports. MaoField asks two different questions: whether a current state is sufficient for future intervention responses, and whether the evaluator can identify that sufficiency. A preregistered causal study produced an exact null-like extreme and a near-saturated dissociation-like extreme, each recurring in held-out worlds, while independent calibration showed that neither identified its apparent conclusion. A disjoint provider replication passed ordinary behavioural controls but still established neither history inheritance, a bounded null nor valid structural dissociation. The result is a claim-specific identification boundary: reproducible statistical extremity cannot substitute for an evaluator shown to separate the future response laws relevant to the claim.
