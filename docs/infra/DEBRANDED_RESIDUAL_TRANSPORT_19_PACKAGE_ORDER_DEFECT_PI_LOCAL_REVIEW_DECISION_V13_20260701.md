# Node19 Package Record -- Order-Defect PI Local Review Decision V13

Date: 2026-07-01 CST
Authority: node36
Destination: node19 desktop

## Purpose

This is the light zero-context package for the next GPT-5.5 Pro task after
report(17).

Report(17) returned:

```text
RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
```

Node36 adopts this only as:

```text
PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
```

The V13 bundle asks Pro to help node36 and the human PI confirm a locked local
review decision and preserve the boundary checklist. It must not produce an
English draft or authorize an English rewrite by itself.

## Current Files On Node19 Desktop

```text
C:\Users\amd\Desktop\MaoField_PRO_OrderDefect_PILocalReviewDecision_V13_FINAL_20260701_2028.zip
C:\Users\amd\Desktop\GPT55_PRO_ORDER_DEFECT_PI_LOCAL_REVIEW_DECISION_V13_PROMPT_20260701.md
```

## Source Files On Node36 Scratch

```text
/home/amd/codex-node36/tmp/orderdefect_pi_local_review_decision_v13_20260701_2028/out/MaoField_PRO_OrderDefect_PILocalReviewDecision_V13_FINAL_20260701_2028.zip
/home/amd/codex-node36/tmp/orderdefect_pi_local_review_decision_v13_20260701_2028/out/GPT55_PRO_ORDER_DEFECT_PI_LOCAL_REVIEW_DECISION_V13_PROMPT_20260701.md
/home/amd/codex-node36/tmp/orderdefect_pi_local_review_decision_v13_20260701_2028/out/SHA256SUMS.external.txt
/home/amd/codex-node36/tmp/orderdefect_pi_local_review_decision_v13_20260701_2028/out/unzip_test.txt
/home/amd/codex-node36/tmp/orderdefect_pi_local_review_decision_v13_20260701_2028/out/internal_sha256_check.txt
/home/amd/codex-node36/tmp/orderdefect_pi_local_review_decision_v13_20260701_2028/out/zip_filelist.txt
```

## Hash Policy

The zip cannot contain its own final sha256 without changing that sha256. The
V13 bundle therefore uses a two-level identity policy:

- package-content identity inside the zip:
  `SHA256SUMS.txt` and `PACKAGE_FILE_MANIFEST.sha256`;
- zip-container identity outside the zip:
  node36 scratch `SHA256SUMS.external.txt` and node19 readback.

Exact zip hashes belong to external command output and node19 readback, not to
zip-internal status files.

## Included Categories

The final zip contains:

- `prompt/GPT55_PRO_ORDER_DEFECT_PI_LOCAL_REVIEW_DECISION_V13_PROMPT_20260701.md`;
- `PACKAGE_README.md`, `PACKAGE_FILE_LIST.txt`, `PACKAGE_FILE_MANIFEST.sha256`,
  and internal `SHA256SUMS.txt`;
- `from_repo/STATE.md`, `MD_CATALOG.md`, project `AGENTS.md`, `CLAUDE.md`, and
  `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- report(17), its adoption note, the V13 taskbook, V13 prompt, and this V13
  package record;
- report(16), its adoption note, the report(15) path hygiene note, the V12
  taskbook, V12 prompt, and V12 package record;
- report(15), its adoption note, the V11 taskbook, V11 prompt, and V11 package
  record;
- report(14), report(13), report(12), report(11), report(10), report(9),
  report(8), and adoption-note provenance;
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
PREPARE_PI_LOCAL_REVIEW_DECISION_V13
PI_LOCAL_REVIEW_ONLY_KEEP_LOCK
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

This package may request a PI local-review recommendation and a boundary
checklist only. It does not authorize paper-ready claims, preprint-ready claims,
posting, submission, English draft generation, completed formal-system wording,
full panel, checkpoint inference, training, new loss, observed
residual/interaction/transport/holonomy field, glass-box, F3, LOSO, or MaoField
empirical positive claims.
