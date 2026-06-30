# Order-Defect Report 9 Local Verification

Date: 2026-06-30 CST
Authority: node36
Scratch root: `/home/amd/codex-node36/tmp/orderdefect_report9_localdraft_20260630_1448`

## Scope

This file records local checks after Pro report (9). It is not a new proof and
not a MaoField empirical result.

## Source Report

```text
docs/infra/gpt_deep_research/deep_research_order_defect_proof_repair_recheck_report9_20260630.md
sha256=be486334cb1d9765cc4bf64f9c34ba43d664b84ae7c64685841d06a2428dc979
```

Accepted local verdict:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
```

## Exact Witness Rerun

Command run under the project root, with outputs written to SSD scratch:

```text
/home/amd/venv/bin/python scripts/debranded_residual_transport_exact_witness_v1_4.py --out-dir /home/amd/codex-node36/tmp/orderdefect_report9_localdraft_20260630_1448/exact_witness_rerun
```

Observed output:

```text
all_checks_passed=True
json_sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
```

The exact content includes:

```text
main_b0_artifact_norm_sq_exact: pass
||R_Q_then_B K||_w^2 = 61/177408
```

Whole-file hash drift is expected across environments because the script writes
runtime/platform metadata. The mathematical certificate content is the relevant
check.

## Deterministic Harness Rerun

Command run under the project root, with outputs written to SSD scratch:

```text
/home/amd/venv/bin/python scripts/debranded_residual_transport_harness_v1_3.py --out /home/amd/codex-node36/tmp/orderdefect_report9_localdraft_20260630_1448/harness_rerun/synthetic_harness_v1_3_20260628.json --summary-md /home/amd/codex-node36/tmp/orderdefect_report9_localdraft_20260630_1448/harness_rerun/SYNTHETIC_HARNESS_V1_3_20260628.md
```

Observed hashes:

```text
14009bc085958579f0eb453588ad91cd069c47acfd4e56177af0031e6b4b7b73  synthetic_harness_v1_3_20260628.json
361e55f4ae813f1e23f9a1dc6f54584cfa5a648e3c925ef31b678e26e7d8fcec  SYNTHETIC_HARNESS_V1_3_20260628.md
```

Observed control:

```text
all_synthetic_controls_passed: true
threshold_contract_sha256: ec2a3a70dce8d19be5635b2b2a7f51caae17ee8e0a8bce2ec20ed4a55f9a82f6
```

Canonical sentence present in both Markdown and JSON:

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

The harness remains `HARNESS_ONLY`; it does not prove the theorem.

## Current Boundary

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall paper status: LOCKED_NO_PAPER_BODY
Mode B MaoField empirical status: insufficient_artifact
```
