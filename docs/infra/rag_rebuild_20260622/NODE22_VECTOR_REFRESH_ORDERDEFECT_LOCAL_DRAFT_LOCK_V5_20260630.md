# Node22 Vector Refresh -- Order-Defect Local-Draft Lock V5

Date: 2026-06-30 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh indexes the D630 report(9) local-draft-locked state after:

- archiving Pro report(9);
- adding the report(9) adoption note;
- adding the local-draft locked taskbook;
- adding the local exact/harness verification record;
- adding the V5 zero-context Pro audit prompt;
- updating `STATE.md` and `MD_CATALOG.md`.

RAG remains a locator only. Primary files, exact rational certificate, scripts,
JSON, logs, verdicts, and local adoption notes remain the evidence sources.

## Method

Node36 owned scope selection, chunking, metadata, FAISS writing, hash
verification, promotion, and smoke queries. Node22 only ran a temporary
`llama.cpp` bge-m3 HTTP embedding worker.

```text
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
node22 temporary root=/home/amd/codex-node22/tmp/maofield-rag-vector-20260630_1456_localdraft_v5
node36 scratch=/home/amd/codex-node36/tmp/orderdefect_localdraft_lock_v5_20260630_1456/rag
```

Two setup issues were encountered and resolved before promotion:

- first start exposed the integrated GPU and hit a `gfx1036` rocBLAS/Tensile
  error;
- restart with only GPU0 exposed then failed on physical batch size 512 for a
  523-token chunk;
- final restart used `ROCR_VISIBLE_DEVICES=0 HIP_VISIBLE_DEVICES=0` and
  `-b 1024 -ub 1024`, matching the previously successful V4 configuration.

No failed candidate was promoted.

## Promoted Index

```text
active canonical markdown files: 492
chunks: 11029
kb.faiss sha256=96aa744f1da2edb6c03fb5476542cb21dd6789c7ae06c569545e5daca631b4d7
kb_meta.jsonl sha256=73bcd20a856e6c4839745bc7324d0a93e55f5f7acd79856efcb686ceae94b31d
canonical scope sha256=83548d25b744facd76b0c3ba50ca622544c17d105c5404c687de83fd2043e11b
embedding rate=92.771 text/s
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/backups/pre_localdraft_v5_20260630_1456/kb.faiss.bak
/media/amd/raid1/rag/index/backups/pre_localdraft_v5_20260630_1456/kb_meta.jsonl.bak
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1456_localdraft_v5.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260630_1456_localdraft_v5.log
docs/infra/rag_rebuild_20260622/scope_select_20260630_1456_localdraft_v5.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1456_localdraft_v5.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1456_localdraft_v5.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1456_localdraft_v5.txt
docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1456_localdraft_v5.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1456_localdraft_v5.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1456_localdraft_v5.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_report9_20260630_1456.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_prompt_package_20260630_1456.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_modeb_20260630_1456.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_state_20260630_1456.txt
```

## Node22 Stop Status

Second status check:

```text
not running port=18080
GPU[0] use: 0%
GPU[1] use: 0%
```

## Smoke Checks

Smoke query:

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK report9 Proposition 2 Proposition 3 COMPLETE_LOCAL_DRAFT
```

returned top hits:

- `docs/infra/recovery/ORDER_DEFECT_D630_LOCAL_DRAFT_LOCKED_TASKBOOK_20260630.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_LOCAL_DRAFT_LOCK_AUDIT_V5_PROMPT_20260630.md`;
- `docs/infra/gpt_deep_research/deep_research_order_defect_proof_repair_recheck_report9_20260630.md`;
- `docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md`;
- V4 proof-repair provenance files and the report(9) adoption note.

Smoke query:

```text
GPT55_PRO_ORDER_DEFECT_LOCAL_DRAFT_LOCK_AUDIT_V5_PROMPT package identity V4 package record
```

returned top hits:

- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_LOCAL_DRAFT_LOCK_AUDIT_V5_PROMPT_20260630.md`;
- `MD_CATALOG.md`.

Smoke query:

```text
Mode B insufficient_artifact no full panel no training no observed residual field
```

returned boundary hits that preserve Mode B as `insufficient_artifact`; exact
current boundary remains `STATE.md` plus the adoption notes and taskbooks.

Smoke query:

```text
STATE D630 report9 LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK Mode B insufficient_artifact
```

returned the local-draft taskbook, V5 prompt, report(9) verification record,
and `STATE.md` among the top eight hits. Direct `STATE.md` reading remains the
volatile-status authority; RAG is only a locator.

## V5 Package-Record Sync

After the first V5 refresh, the V5 node19 package record itself was created.
This follow-up sync preserves the previous broad canonical default scope and
adds the new V5 package record plus this RAG record, so the shared default RAG
does not shrink to MaoField-only scope.

```text
timestamp=20260630_1520_localdraft_v5_pkgrecord
file_list=docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1520_localdraft_v5_pkgrecord.txt
active markdown files=494
chunks=11046
kb.faiss sha256=6a9426213314bbeed8386f4f1acec2366032191328858d4489e499d8e5dee197
kb_meta.jsonl sha256=ae04769ac2122996a38abe6a2e401068bfb4656e3ad053be0dc3ec89968522e4
scope sha256=f6b240950e37133477c2936dc1f24ece85727156b9d4d1ec9b711a8690496147
embedding rate=93.559 text/s
```

Candidate and promotion evidence:

```text
docs/infra/rag_rebuild_20260622/rag_scan_20260630_1520_localdraft_v5_pkgrecord.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1520_localdraft_v5_pkgrecord.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1520_localdraft_v5_pkgrecord.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1520_localdraft_v5_pkgrecord.txt
docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1520_localdraft_v5_pkgrecord.txt
docs/infra/rag_rebuild_20260622/scope_hash_20260630_1520_localdraft_v5_pkgrecord.txt
```

Node22 was stopped after the build. The second status check reports:

```text
not running port=18080
GPU[0] use: 0%
GPU[1] use: 0%
```

Smoke files:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_pkgrecord_package_20260630_1520.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_pkgrecord_prompt_20260630_1520.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_pkgrecord_prompt_direct_20260630_1520.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_pkgrecord_state_20260630_1520.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_pkgrecord_modeb_20260630_1520.txt
```

Key smoke results:

- The exact V5 zip hash query returns
  `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_LOCAL_DRAFT_LOCK_V5_20260630.md`
  as rank 1.
- The direct uploaded-zip-only / no-public-GitHub prompt query returns
  `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_LOCAL_DRAFT_LOCK_AUDIT_V5_PROMPT_20260630.md`
  as rank 1.
- The state and Mode B boundary queries keep `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK`
  and `insufficient_artifact` visible. Direct `STATE.md` reading remains the
  status authority; RAG is only a locator.

## Superseded Repack Caveat And Finalrecord Policy

After the 1520 RAG sync, node36 made interim V5 repacks (`1528`, then `1535`).
Those are superseded provenance. The final package identity is carried by the
external node19 package record, not by zip-internal status files.

The final RAG sync for the current V5 package uses:

```text
timestamp=20260630_1550_localdraft_v5_finalrecord
file_list=docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1550_localdraft_v5_finalrecord.txt
candidate_hashes=docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1550_localdraft_v5_finalrecord.txt
promoted_hashes=docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1550_localdraft_v5_finalrecord.txt
backup_hashes=docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1550_localdraft_v5_finalrecord.txt
build_log=docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1550_localdraft_v5_finalrecord.log
```

Exact final live RAG hashes are intentionally stored in the sidecar
`promoted_hashes_20260630_1550_localdraft_v5_finalrecord.txt`, not embedded
verbatim in this indexed Markdown file. This avoids the same self-hash loop as
zip packages: if an indexed Markdown file contains the digest of an index that
contains that Markdown file, the digest changes when the file is edited.

Final smoke files:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_finalrecord_package_20260630_1550.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_finalrecord_prompt_20260630_1550.txt
docs/infra/rag_rebuild_20260622/rag_smoke_localdraft_v5_finalrecord_state_modeb_20260630_1550.txt
```

Expected smoke result: the package query returns
`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_LOCAL_DRAFT_LOCK_V5_20260630.md`
with the final `1550` package hash; the prompt query keeps the uploaded-zip-only
guard visible; the state/Mode-B query keeps `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK`
and `insufficient_artifact` visible. Direct files remain evidence; RAG remains
locator only.
