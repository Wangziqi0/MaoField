# Node19 Package Record -- Order-Defect Paper Draft v1.6

Date: 2026-06-29 CST
Machine authority: node36
Destination: node19 desktop

## Purpose

Prepare a zero-context GPT-5.5 Pro package for the v1.6 order-defect paper
draft pass.  This package follows the v1.5 final-gate report:

```text
short_note_requires_minor_wording_or_bibliography_fixes
```

The package is gate-conditioned.  Pro must first verify v1.6 wording and
evidence gates.  Only if those gates pass may it draft a 4-6 page short note.

This is Mode A finite-dimensional mathematics only. It is not MaoField
empirical validation.

## Node36 Staging

Scratch staging directory:

```text
/home/amd/codex-node36/tmp/maofield-pro-orderdefect-paperdraft-v16-20260629_1610final
```

Local zip:

```text
/home/amd/codex-node36/tmp/maofield-pro-orderdefect-paperdraft-v16-20260629_1610final/MaoField_PRO_OrderDefect_PaperDraft_V16_20260629_1610final.zip
```

Standalone prompt source:

```text
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md
```

## Verification

`unzip -t` on node36:

```text
No errors detected in compressed data
```

Package manifest:

```text
36 files in FILELIST.txt
36 entries in MANIFEST.sha256
37 regular files in package tree, because MANIFEST.sha256 is generated after FILELIST.txt
```

Node36 hashes:

```text
zip sha256=1bb3981f7ac06e6a5daf8db2b936e4ecf592dcea84d9d788d340337fc594b91c
prompt sha256=67f5b5f3f608dbccba951f28c23c5948fff29ba2d127fb5ec9af8620e9c8a68f
state_snapshot sha256=c212295b5e029d18630534cc38a421e99b0f55e5c851d15b5df2344fb904930d
md_catalog_snapshot sha256=087b14fc7b88cb7f7a9b68fc15c086a416104e5d731465943c77c278e0a286a9
wording_lock sha256=04565a27643b2c44fe5ef477de01868db5db7fed5f571fc2676d052b4c04aa20
rag_index sha256=8ea8eaadaa4b015f239bf7821665db84daecc9928c9d533a6e29da968d861510
rag_meta sha256=5c9a5015c534778a36ddf6a805b01527915b25f408146871a943e3c6e5e71ed0
rag_scope sha256=5ca9b31e1e09928dd4655d036e79130b583bfdeea9a5b66b4bb246e080a023a8
```

Node19 desktop artifacts:

```text
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_PaperDraft_V16_20260629_1610final.zip
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_PaperDraft_V16_20260629_1610final.zip.sha256
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md.sha256
```

Node19 PowerShell `Get-FileHash -Algorithm SHA256` matched:

```text
zip sha256=1BB3981F7AC06E6A5DAF8DB2B936E4ECF592DCEA84D9D788D340337FC594B91C
prompt sha256=67F5B5F3F608DBCCBA951F28C23C5948FFF29BA2D127FB5EC9AF8620E9C8A68F
```

## Included Core Files

The zip includes:

- `FILELIST.txt`;
- `MANIFEST.sha256`;
- `prompt/GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md`;
- `from_repo/canonical_AGENTS.md`;
- `from_repo/AGENTS.md`;
- `from_repo/STATE.md`;
- `from_repo/MD_CATALOG.md`;
- `from_repo/docs/infra/debranded_residual_transport/README.md`;
- `from_repo/docs/infra/debranded_residual_transport/README_FOR_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`;
- `from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`;
- `from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`;
- `from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`;
- `from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`;
- `from_repo/docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_5_final_gate_audit_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_ADOPTION_NOTE_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_preprint_rigor_audit_20260629.md`;
- `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PREPRINT_RIGOR_AUDIT_ADOPTION_NOTE_20260629.md`;
- `from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PAPERDRAFT_V16_20260629.md`;
- `from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PAPERDRAFT_V16_FINAL_20260629.md`;
- `from_repo/docs/infra/rag_rebuild_20260622/promoted_hashes_20260629_1540_v16paper.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/promoted_hashes_20260629_1601_v16final.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/rag_smoke_v16_wording_lock_20260629_1540_v16paper.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/rag_smoke_v16_paper_prompt_20260629_1540_v16paper.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/rag_smoke_v15_final_gate_20260629_1540_v16paper.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/rag_smoke_v16_final_state_20260629_1601_v16final.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/rag_smoke_v16_paper_prompt_20260629_1601_v16final.txt`;
- `from_repo/docs/infra/rag_rebuild_20260622/rag_smoke_v16_node19_package_20260629_1601_v16final.txt`;
- `from_repo/scripts/debranded_residual_transport_harness_v1_3.py`;
- `from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py`;
- `from_repo/scripts/rag_build_index_node22_http.py`.

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
- 16-cell aggregate exists;
- checkpoint loading, inference, training, or new loss is authorized;
- MaoField residual / interaction / quotient-residual / transport / holonomy
  field has been observed;
- glass box broken;
- F3 positive or LOSO passed;
- completed formal system;
- broad new ANOVA theory;
- broad new dependent-input decomposition theory;
- broad new noncommuting projection theory;
- holonomy / gluing / sheaf / curvature claims;
- JSON floats or the deterministic harness prove the theorem.

## Self-Reference Boundary

The zip package cannot self-certify its final zip hash.  The authoritative
final package hash is the external hash pair verified by node36 `sha256sum`
and node19 PowerShell `Get-FileHash`, recorded above.  This package record was
written after the zip was created, so it is not inside the zip.
