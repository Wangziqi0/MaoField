# Node19 Package Record -- Order-Defect Boundary-Locked Draft Review V11

Date: 2026-07-01 CST
Authority: node36
Destination: node19 desktop

## Purpose

This is the light zero-context package for the next GPT-5.5 Pro task after
report(15).

Revision note: independent read-only audit found that the first `1325` package
still carried a stale `MD_CATALOG.md` pointer saying the current Pro prompt was
D701 report(13) V9. Node36 fixed that pointer and repacked this V11 bundle as
`V11_FIX_20260701_1352`. The original `1325` zip is superseded provenance.

Report(15) returned:

```text
BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE
```

Node36 adopts this only as:

```text
RECEIVE_LOCAL_DRAFT_CANDIDATE_UNDER_LOCK_PREPARE_V11_REVIEW
```

The V11 bundle asks Pro to review report(15)'s local draft candidate under the
emergency lock. It may recommend acceptance for node36/PI local review,
patching, or stopping. It must not be used to lift the emergency lock, claim
paper-ready status, claim preprint-ready status, submit or post anything,
promote Pro into proof authority, promote bibliography authority, or upgrade
MaoField Mode B.

## Current Files On Node19 Desktop

```text
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_BoundaryLockedDraftReview_V11_FIX_20260701_1352.zip
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_PROMPT_20260701.md
```

## Source Files On Node36 Scratch

```text
/home/amd/codex-node36/tmp/orderdefect_boundary_locked_draft_review_v11_fix_20260701_1352/out/MaoField_PRO_OrderDefect_BoundaryLockedDraftReview_V11_FIX_20260701_1352.zip
/home/amd/codex-node36/tmp/orderdefect_boundary_locked_draft_review_v11_fix_20260701_1352/out/GPT55_PRO_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_PROMPT_20260701.md
/home/amd/codex-node36/tmp/orderdefect_boundary_locked_draft_review_v11_fix_20260701_1352/out/SHA256SUMS.external.txt
/home/amd/codex-node36/tmp/orderdefect_boundary_locked_draft_review_v11_fix_20260701_1352/out/unzip_test.txt
/home/amd/codex-node36/tmp/orderdefect_boundary_locked_draft_review_v11_fix_20260701_1352/out/internal_sha256_check.txt
/home/amd/codex-node36/tmp/orderdefect_boundary_locked_draft_review_v11_fix_20260701_1352/out/zip_filelist.txt
```

## Hash Policy

The zip cannot contain its own final sha256 without changing that sha256. The
V11 bundle therefore uses a two-level identity policy:

- package-content identity inside the zip:
  `SHA256SUMS.txt` and `PACKAGE_FILE_MANIFEST.sha256`;
- zip-container identity outside the zip:
  node36 scratch `SHA256SUMS.external.txt` and node19 readback.

This Markdown intentionally does not embed the final zip sha256. Exact zip
hashes belong to external command output and node19 readback, not to
zip-internal status files.

## Included Categories

The final zip contains:

- `prompt/GPT55_PRO_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_REVIEW_V11_PROMPT_20260701.md`;
- `PACKAGE_README.md`, `PACKAGE_FILE_LIST.txt`, `PACKAGE_FILE_MANIFEST.sha256`,
  and internal `SHA256SUMS.txt`;
- `from_repo/STATE.md`, `MD_CATALOG.md`, project `AGENTS.md`, `CLAUDE.md`, and
  `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- report(15), its adoption note, the V11 taskbook, V11 prompt, and this V11
  package record;
- report(14), its adoption note, the V10 taskbook, V10 prompt, and V10 package
  record;
- report(13), report(12), report(11), report(10), report(9), report(8), and
  adoption-note provenance;
- exact witness Markdown/JSON/script;
- deterministic harness Markdown/JSON/script;
- formal note v1.3 and proof-repair candidate;
- bibliography, wording-lock, recovery rescue audits, and forbidden-claim scan;
- current and provenance RAG refresh records needed to explain locator status.

Excluded:

- checkpoints, model weights, raw experiment datasets, old recovery zips,
  training/inference payloads, and any public paper-ready artifact.

## Boundary

Current local state:

```text
RECEIVE_LOCAL_DRAFT_CANDIDATE_UNDER_LOCK_PREPARE_V11_REVIEW
BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY
EMERGENCY_LOCK_STILL_ACTIVE
```

Current live labels:

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall status: BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY
Mode B MaoField empirical status: insufficient_artifact
```

This package may request review or patching of the local draft candidate under
lock. It does not authorize paper-ready claims, preprint-ready claims, posting,
submission, completed formal-system wording, full panel, checkpoint inference,
training, new loss, observed residual/interaction/transport/holonomy field,
glass-box, F3, LOSO, or MaoField empirical positive claims.
