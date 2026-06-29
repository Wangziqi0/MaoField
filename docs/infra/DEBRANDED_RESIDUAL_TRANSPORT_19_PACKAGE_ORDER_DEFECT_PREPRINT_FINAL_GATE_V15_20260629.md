# Node19 Package Record -- Order-Defect Preprint Final Gate v1.5

Date: 2026-06-29 CST
Machine authority: node36
Destination: node19 desktop

## Purpose

Prepare a zero-context GPT-5.5 Pro package for the v1.5 final-gate audit after
the v1.4 exact/bibliography report returned:

```text
preprint_requires_minor_bibliography_or_wording_fixes
posting_decision=revise_first
```

This package asks Pro to decide whether the remaining WARN items are closed:

- formal bibliography and novelty positioning;
- Lamboni 2026 and projection-theory boundary;
- harness markdown/JSON/script disclaimer;
- project-internal wording removal;
- short-note draft gate.

This is Mode A finite-dimensional mathematics only. It is not MaoField
empirical validation.

## Node36 Staging

Scratch staging directory:

```text
/home/amd/codex-node36/tmp/maofield-pro-orderdefect-finalgate-v15-20260629_1420final
```

Local zip:

```text
/home/amd/codex-node36/tmp/MaoField_PRO_OrderDefect_PreprintFinalGate_V15_20260629_1420final.zip
```

Standalone prompt source:

```text
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PREPRINT_FINAL_GATE_PROMPT_20260629.md
```

## Verification

`unzip -t` on node36:

```text
No errors detected in compressed data
```

Package manifest:

```text
20 files in FILELIST.txt
20 entries in MANIFEST.sha256
21 regular files in zip, because MANIFEST.sha256 is generated after FILELIST.txt
```

Node36 hashes:

```text
zip sha256=7b5b7b7fa25806892598db3aa1f6fe02e9901dff29cdc24b1e1642d6a4a59707
prompt sha256=20cf4707d16262e2743391d4d2c2ebaa85ef068ae7796391f3cc2162093b9fd7
state_snapshot sha256=ef83e1a6f4c6aaf7a75227a7ec648a4f3ad7b8ca82a639c99d29bdb7a1f259ac
md_catalog_snapshot sha256=f62ef5c278c6e0e75c1bae239a77bf2e7477cb12764f59070dadf8be01a1e16c
preprint_placeholder sha256=428753cbcfd4b839c9dbf700989c281c099100990f5dda7e171a3ff344729628
bibliography_positioning sha256=e994d35f78692f2a207af2be41da1ad73c087349d01102aa6c88e3cea699b434
synthetic_harness_md sha256=63cdb841bd8489486527911aa2ee9ea32e47f9db5213faf38d013bb2915b5f57
synthetic_harness_json sha256=8bc68a6a660b90c00d0e9ce387eb213a7108e9e221704d53565c96e9a9c73cd4
v1_4_adoption_note sha256=2ec3a098240f6909e2b76b8e2479fdd35046be86d515b9b1dd45510cba9ca292
v1_4_pro_report sha256=2dd42dbd323e21e54b730e90d38e58402f521077a8d0f89de1f8b2a5f6acbccc
```

Node19 desktop artifacts:

```text
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_PreprintFinalGate_V15_20260629_1420final.zip
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_PreprintFinalGate_V15_20260629_1420final.zip.sha256
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_PREPRINT_FINAL_GATE_PROMPT_20260629.md
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_PREPRINT_FINAL_GATE_PROMPT_20260629.md.sha256
```

Node19 PowerShell `Get-FileHash -Algorithm SHA256` matched:

```text
zip sha256=7B5B7B7FA25806892598DB3AA1F6FE02E9901DFF29CDC24B1E1642D6A4A59707
prompt sha256=20CF4707D16262E2743391D4D2C2EBAA85EF068AE7796391F3CC2162093B9FD7
```

## Included Core Files

The zip includes:

- `FILELIST.txt`;
- `MANIFEST.sha256`;
- `prompt/GPT55_PRO_ORDER_DEFECT_PREPRINT_FINAL_GATE_PROMPT_20260629.md`;
- `from_repo/STATE.md`;
- `from_repo/MD_CATALOG.md`;
- `from_repo/docs/infra/debranded_residual_transport/README.md`;
- `from_repo/docs/infra/debranded_residual_transport/README_FOR_PRO_ORDER_DEFECT_PREPRINT_FINAL_GATE_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`;
- `from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`;
- `from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`;
- `from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`;
- `from_repo/docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PREPRINT_FINAL_GATE_PROMPT_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_ADOPTION_NOTE_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_preprint_rigor_audit_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PREPRINT_RIGOR_AUDIT_ADOPTION_NOTE_20260629.md`;
- `from_repo/scripts/debranded_residual_transport_harness_v1_3.py`;
- `from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py`.

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

- MaoField empirical positive result;
- full panel has run;
- checkpoint inference, training, or new loss is authorized;
- MaoField residual / interaction / quotient-residual / transport / holonomy
  field has been observed;
- glass box broken;
- F3 positive or LOSO passed;
- completed formal system;
- broad new ANOVA theory;
- broad new dependent-input decomposition theory;
- broad new noncommuting projection theory;
- holonomy / gluing / sheaf / curvature claims.

## Self-Reference Boundary

The zip package cannot self-certify its final zip hash. The authoritative
final package hash is the external hash pair verified by node36 `sha256sum`
and node19 PowerShell `Get-FileHash`, recorded above.
