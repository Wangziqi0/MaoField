# Order-Defect D703 Report20 Local Verification

Date: 2026-07-03 CST
Node: node36
Purpose: local evidence check before adopting report(20) as the next formal
preprint draft-gate input.

## Attachment Identity

Source attachment:

```text
/home/amd/.codex/attachments/c8b80c49-870f-4bb2-a938-9750145f25df/deep-research-report (20).md
```

Archived copy:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_english_preprint_candidate_v1_report20_20260703.md
```

SHA256:

```text
1689f07aca6e9636ebb2622489b442c8d3397fb1ab221ebf875b8e95c60974e4
```

## Report20 Boundary

Report(20) is adopted only as an English V1 internal candidate. It explicitly
says the candidate is local review only and not a release, posting, status
upgrade, paper-ready, preprint-ready, posted, or submission-authorized artifact.

## Local Exact-Witness Rerun

Command:

```bash
/home/amd/venv/bin/python scripts/debranded_residual_transport_exact_witness_v1_4.py \
  --out-dir /home/amd/codex-node36/tmp/recheck_report20_20260703/exact
```

Observed output:

```text
all_checks_passed=True
json_sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
```

The generated exact JSON contains:

```text
artifact_weighted_norm_squared = 61/177408
strongest_allowed_verdict = definitions_and_harness_viable_only
mode_b_maofield_status = insufficient_artifact
```

## Local Harness Rerun

Command:

```bash
/home/amd/venv/bin/python scripts/debranded_residual_transport_harness_v1_3.py \
  --out /home/amd/codex-node36/tmp/recheck_report20_20260703/harness/harness.json \
  --summary-md /home/amd/codex-node36/tmp/recheck_report20_20260703/harness/harness.md \
  --json-rel harness.json
```

Observed output:

```text
all_synthetic_controls_passed=True
threshold_contract_sha256=ec2a3a70dce8d19be5635b2b2a7f51caae17ee8e0a8bce2ec20ed4a55f9a82f6
strongest_allowed_verdict=definitions_and_harness_viable_only
mode_b_maofield_empirical_status=insufficient_artifact
```

## Local Verdict

Observed:

- report(20) can be archived as a source artifact;
- exact witness and deterministic harness reruns are locally consistent;
- report(20) can feed a formal preprint drafting gate under lock.

Blocked:

- report(20) does not by itself authorize public posting, submission, or
  preprint-ready status;
- a standalone draft still needs source-map, forbidden-claim, bibliography, and
  final release-gate checks.
