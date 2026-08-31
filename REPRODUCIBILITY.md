# Reproducibility

## Tier 1 — public offline reproduction (primary)

Reproduce the public processed-data checks, tables and figures without a model/API call.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r environment/requirements.txt
bash scripts/reproduce_offline.sh
```

Expected counters: model calls 0; provider calls 0. The command verifies the release manifest, checks frozen key quantities and regenerates Figures 1–5 and Extended Data Figures 1–8.

## Tier 2 — reviewer-only raw replay

The reviewer-only tier supports replay from raw trajectories to endpoints and from endpoints to statistics using immutable evidence. It may include Phase 23/GLM trajectories, post-unblinding assignments, scorer A/B source and receipts, validators, permitted provider records and engineering fail-stop lineage. It is not stored in this repository and is governed by `docs/CONTROLLED_ACCESS_POLICY.md`.

Requests must identify the requester, affiliation or verifiable research identity, purpose, requested materials and security plan. The author will respond within 14 business days. Approved access is purpose-limited, non-transferable and subject to provider rights, hidden-answer protection and the data-use conditions stated in the policy.

## Tier 3 — provider-dependent full rerun

Not required to reproduce the reported paper. It requires author-controlled credentials, exact provider/model identifiers, dated API behaviour and any local hardware/runtime dependencies. GLM registered 18,156 attempts with zero retries. Phase 23 used six independent conditions. Hosted-model behaviour may not be exactly reproducible. Credentials and restricted payloads are never distributed.

No release tier may contain API keys, DPAPI/private decryption material, personal credentials, unauthorized provider content or unrestricted hidden answers.

