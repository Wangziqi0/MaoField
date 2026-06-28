# Node19 Package Record — Formal v1.3 Order-Defect Proof Audit

Date: 2026-06-28 CST
Machine authority: node36
Destination: node19 desktop

## Purpose

Prepare a zero-context GPT-5.5 Pro package for a proof-level audit of the
Formal v1.3 weighted ANOVA order-defect theorem target selected by report
(31).

This package is for Mode A finite-dimensional mathematics only. It is not a
MaoField empirical validation package.

## Node36 Staging

Scratch staging directory:

```text
/home/amd/codex-node36/tmp/maofield-pro-formalv13-orderdefect-report31-20260628_1758fixed
```

Local zip:

```text
/home/amd/codex-node36/tmp/MaoField_PRO_FoundationalResidualTransport_FormalV13_OrderDefectProof_Report31_20260628_1758fixed.zip
```

Standalone prompt source:

```text
docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md
```

## Verification

`unzip -t` on node36:

```text
No errors detected in compressed data
```

Node36 hashes:

```text
zip sha256=3780b31e6f420c7dbf07d9378849f348c3ee151680c20e14aa84ee3ba4a6f7bb
prompt sha256=2450a5ef34e1730d4fe178a28fd6f72b9f7afe451d093f5342f1fc812795ffde
manifest sha256=3b5fb3f18de4fa56e3a86017db16632462a63f25bb12eb5ac4ff4ca851ffd921
```

Node19 desktop artifacts:

```text
C:\Users\amd\Desktop\MaoField_PRO_FoundationalResidualTransport_FormalV13_OrderDefectProof_Report31_20260628_1758fixed.zip
C:\Users\amd\Desktop\GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md
```

Node19 `Get-FileHash -Algorithm SHA256` matched:

```text
zip sha256=3780B31E6F420C7DBF07D9378849F348C3EE151680C20E14AA84EE3BA4A6F7BB
prompt sha256=2450A5EF34E1730D4FE178A28FD6F72B9F7AFE451D093F5342F1FC812795FFDE
```

## Self-Reference Boundary

A zip package cannot self-certify its final zip hash when it contains status
files or manifests captured during package construction. Treat files inside the
zip as a contextual snapshot. The authoritative final package hash is the
external pair verified by node36 `sha256sum` and node19 `Get-FileHash`,
recorded in this canonical package record after the final copy.

If an internal package snapshot contains older status text, that is not
evidence of a transfer failure by itself. Resolve conflicts using this
canonical package record plus the node19 desktop `Get-FileHash` result.

Use only the `1758fixed` package for the next Pro pass. Earlier `1555`,
`1734final`, and transient `1751fixed` packages are superseded: `1734final`
still had a stale top-level README pointer to the intermediate
`NODE22_VECTOR_REFRESH_REPORT31_ORDERDEFECT_20260628.md` record, while
`1758fixed` points to `NODE22_VECTOR_REFRESH_REPORT31_FINAL_20260628.md` and
treats `ORDERDEFECT` only as superseded provenance.

## Included Core Files

The zip includes:

- `00-README_FOR_19_AND_PRO.md`;
- `00-CURRENT_STATUS_FOR_PRO.md`;
- `prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md`;
- current repository status and navigation files as a contextual snapshot;
- report (31) archive and adoption note;
- Formal v1.3 order-defect workplan;
- report (30) archive/adoption note as provenance;
- Formal v1.2 note, synthetic harness summary, JSON, and script;
- node36/RAG/project rule files with source-prefixed names;
- file list and per-file SHA256 manifest.

## Evidence Boundary

Allowed strongest local verdict:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

Forbidden upgrades:

- full panel has run;
- checkpoint inference, training, or new loss is authorized;
- MaoField residual / interaction / quotient-residual / transport / holonomy
  field has been observed;
- glass box broken;
- F3 positive or LOSO passed;
- Formal v1.3 completed;
- completed formal system.
