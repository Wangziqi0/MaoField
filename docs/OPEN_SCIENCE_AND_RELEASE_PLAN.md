# Open science and reproducibility release plan

## Release objective

Permit independent reproduction of every reported processed-data check, table and figure without another model or provider call, while preserving credentials, private keys, provider-restricted content and hidden-answer integrity.

## Three-tier release

1. **Public:** manuscript, Supplement, figures, source data, processed results, frozen contracts, figure/statistics code, validators, failure summaries, SHA-256 manifests and environment locks.
2. **Reviewer-only:** de-identified raw trajectories, post-unblinding assignments, provider records where terms permit, scorer/validator receipts, full engineering lineage and restricted hidden-test evidence through a persistent controlled-access archive.
3. **Private / never release:** API keys, DPAPI or decryption private keys, personal credentials, editorial correspondence, provider content lacking redistribution permission and hidden answers whose publication would invalidate reuse.

Controlled access follows `docs/CONTROLLED_ACCESS_POLICY.md`; complete requests receive a response within 14 business days.

## Primary reproduction path

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r environment/requirements.txt
bash scripts/reproduce_offline.sh
```

Expected: zero model calls and zero provider calls; manifest verification; frozen statistical checks; regeneration of Figures 1–5 and Extended Data Figures 1–8.

## Provider-dependent advanced path

This path is not needed to reproduce the paper. It requires exact provider/model availability, dated API behaviour, author-controlled credentials and any hardware/runtime prerequisites. The GLM branch registered 18,156 attempts with zero retries. Provider behaviour, pricing and hosted-model versions may not be fully reproducible. Provider-derived records are released only where redistribution rights permit.

## Current identifier state

- Repository: <https://github.com/Wangziqi0/MaoField> (private staging)
- GitHub Release: not created
- Zenodo software DOI: not created
- Zenodo data DOI: not created
- Preprint identifier: not created
- Journal submission identifier: not created

The future software and source-data Zenodo deposits will be separate. Real identifiers will be inserted only after creation and readback; placeholders are not published.

