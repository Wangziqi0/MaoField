# Order-Defect D630 Metadata/Label Patch V6 Taskbook

Date: 2026-06-30 CST
Authority: node36
Source audit: report(10)

## Goal

Repair the remaining V5 metadata/label blockers without changing the math
claim boundary.

Current verdict remains:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
KEEP_LOCK_AND_FIX
```

## Scope

This V6 patch is allowed to change only:

- package identity documentation;
- bundle content selection;
- report(9) label erratum / live-label references;
- `STATE.md` / `MD_CATALOG.md` navigation;
- RAG locator refresh records.

It must not:

- draft a paper body;
- lift the external-model emergency lock;
- promote proof or bibliography authority;
- claim Mode B positive evidence;
- run full panel, checkpoint inference, training, or new loss;
- claim observed residual / interaction / transport / holonomy fields.

## Required Fixes

1. Include the current V5 package record Markdown in the next zip:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_LOCAL_DRAFT_LOCK_V5_20260630.md
```

2. Include the V6 package record Markdown in the next zip, but do not embed the
   final zip container hash in that Markdown. The final zip hash remains
   external through node36 scratch and node19 readback to avoid self-hash loops.

3. Include package-internal `SHA256SUMS.txt` and
   `PACKAGE_FILE_MANIFEST.sha256`. These describe package contents, not the zip
   container itself.

4. Include the report(9) label erratum:

```text
docs/infra/gpt_deep_research/ORDER_DEFECT_REPORT9_LABEL_ERRATUM_20260630.md
```

5. Keep RAG as locator only. Exact live RAG hashes must remain in sidecar text
   files, not inside indexed status/catalog Markdown.

## Correct Live Labels

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

## Exit Criteria

V6 can be sent to GPT-5.5 Pro only after:

- package includes V5 package record;
- package includes V6 package record;
- package includes internal `SHA256SUMS.txt`;
- package includes report(9) label erratum;
- package unzip test passes;
- forbidden payload scan finds no checkpoint/model/raw-full-panel payload;
- node19 readback matches node36 package hash;
- RAG final smoke locates V6 package record, V6 prompt, label erratum, and
  current `LOCKED_NO_PAPER_BODY` boundary;
- independent audit returns no blocker.

