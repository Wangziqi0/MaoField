# Node19 Package Record -- Order-Defect Metadata/Label Patch V6

Date: 2026-06-30 CST
Authority: node36
Destination: node19 desktop

## Purpose

This is the light zero-context package for the next GPT-5.5 Pro advisory audit
after report(10).

It repairs metadata and label blockers only:

- include the V5 package record Markdown in the bundle;
- include this V6 package record Markdown in the bundle;
- include internal `SHA256SUMS.txt`;
- include the report(9) label erratum;
- preserve the external zip-container hash policy.

It must not be used to draft a paper body, lift the external-model emergency
lock, promote proof authority, promote bibliography authority, or upgrade
MaoField Mode B.

## Current Files On Node19 Desktop

```text
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_MetadataLabelPatch_V6_FINAL_20260630_1640.zip
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_METADATA_LABEL_PATCH_V6_PROMPT_20260630.md
```

## Source Files On Node36 Scratch

```text
/home/amd/codex-node36/tmp/orderdefect_metadata_label_patch_v6_20260630_1640/out/MaoField_PRO_OrderDefect_MetadataLabelPatch_V6_FINAL_20260630_1640.zip
/home/amd/codex-node36/tmp/orderdefect_metadata_label_patch_v6_20260630_1640/out/GPT55_PRO_ORDER_DEFECT_METADATA_LABEL_PATCH_V6_PROMPT_20260630.md
/home/amd/codex-node36/tmp/orderdefect_metadata_label_patch_v6_20260630_1640/out/SHA256SUMS.external.txt
/home/amd/codex-node36/tmp/orderdefect_metadata_label_patch_v6_20260630_1640/out/unzip_test.txt
/home/amd/codex-node36/tmp/orderdefect_metadata_label_patch_v6_20260630_1640/out/zip_filelist.txt
```

## Hash Policy

The zip cannot contain its own final sha256 without changing that sha256. The
V6 bundle therefore uses a two-level identity policy:

- package-content identity inside the zip:
  `SHA256SUMS.txt` and `PACKAGE_FILE_MANIFEST.sha256`;
- zip-container identity outside the zip:
  node36 scratch `SHA256SUMS.external.txt` and node19 readback.

This Markdown intentionally does not embed the final zip sha256. Exact zip
hashes belong to external command output and node19 readback, not to
zip-internal status files.

## Included Categories

The final zip contains:

- `prompt/GPT55_PRO_ORDER_DEFECT_METADATA_LABEL_PATCH_V6_PROMPT_20260630.md`;
- `PACKAGE_README.md`, `PACKAGE_FILE_LIST.txt`, `PACKAGE_FILE_MANIFEST.sha256`,
  and internal `SHA256SUMS.txt`;
- `from_repo/STATE.md`, `MD_CATALOG.md`, project `AGENTS.md`, `CLAUDE.md`, and
  `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- report(10), report(10) adoption note, V6 taskbook, and report(9) label
  erratum;
- report(9), report(9) adoption note, local-draft taskbook, and local
  exact/harness verification record;
- V5 package record and this V6 package record;
- V4 package record as provenance;
- exact witness Markdown/JSON/script;
- deterministic harness Markdown/JSON/script;
- bibliography, wording-lock, recovery rescue audits, and forbidden-claim scan;
- V6 RAG refresh record with final sidecar policy.

Excluded:

- checkpoints, model weights, raw experiment datasets, old recovery zips, and
  large raw grep logs.

## Boundary

Current local state:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
KEEP_LOCK_AND_FIX
```

Current live labels:

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

This package does not authorize full panel, checkpoint inference, training, new
loss, observed residual/interaction/transport/holonomy field, glass-box, F3,
LOSO, posted preprint, paper-ready status, or completed formal system.
