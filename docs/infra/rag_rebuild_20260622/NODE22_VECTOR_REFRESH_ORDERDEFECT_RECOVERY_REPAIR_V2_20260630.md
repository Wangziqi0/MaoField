# Node22 Vector Refresh -- Order-Defect Recovery Repair v2

Date: 2026-06-30 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh indexes the D630 recovery-repair state after archiving the latest
Pro recovery gate audit, adopting it as a gate-only audit, adding the D630
taskbook, adding the v2 zero-context Pro prompt, updating `STATE.md` and
`MD_CATALOG.md`, and creating the node19 light package record.

Primary indexed context before the build includes:

- `STATE.md`;
- `MD_CATALOG.md`;
- `docs/infra/recovery/ORDER_DEFECT_D630_TASKBOOK_NEXT_PRO_20260630.md`;
- `docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md`;
- `docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`;
- `docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`;
- `docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`;
- `docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md`;
- `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_gate_audit_20260630.md`;
- `docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_GATE_AUDIT_ADOPTION_NOTE_20260630.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_RECOVERY_REPAIR_V2_PROMPT_20260630.md`;
- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_RECOVERY_REPAIR_V2_20260630.md`.

## Method

Node36 owns scope, chunking, metadata, FAISS writing, hash verification,
promotion, and smoke queries.  Node22 only runs the temporary bge-m3 embedding
HTTP worker.

Post-build hashes, logs, smoke query files, and node22 stop status are recorded
below after the build.

## Initial Promoted Index Before Final Package Hash Update

```text
scanned MaoField files: 8077
active canonical markdown files: 476
chunks: 10757
kb.faiss sha256=1b22107162a1f45faf97410e6c50b5ccb4a39898e5f396d31a6373d8403c9a48
kb_meta.jsonl sha256=6b01e0e7efa45bce5538446aa4e106098b06df2e8188ebc2e14a5ae56223b377
canonical scope sha256=dc3be6001279b0342d8a584a6dd4a669481ea4aab057c713fb0607d2590abf65
```

Candidate build stats:

```text
files=476
chunks=10757
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=94.126 text/s
```

Initial artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260630_1030_recoveryrepair_v2
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260630_1030_recoveryrepair_v2
```

Final node22 worker status:

```text
not running port=18080
GPU use after stop: 0%
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1030_recoveryrepair_v2.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260630_1030_recoveryrepair_v2.log
docs/infra/rag_rebuild_20260622/scope_select_20260630_1030_recoveryrepair_v2.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1030_recoveryrepair_v2.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1030_recoveryrepair_v2.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1030_recoveryrepair_v2.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1030_recoveryrepair_v2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_recovery_v2_20260630_1030.txt
docs/infra/rag_rebuild_20260622/rag_smoke_v2_prompt_20260630_1030.txt
docs/infra/rag_rebuild_20260622/rag_smoke_exact_prompt_filename_20260630_1030.txt
docs/infra/rag_rebuild_20260622/rag_smoke_prompt_verdicts_20260630_1030.txt
docs/infra/rag_rebuild_20260622/rag_smoke_math_rescue_20260630_1030.txt
docs/infra/rag_rebuild_20260622/rag_smoke_package_v2_20260630_1030.txt
docs/infra/rag_rebuild_20260622/maofield_file_inventory.tsv
docs/infra/rag_rebuild_20260622/maofield_scan_summary.json
docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md
```

## Smoke Checks

Smoke query:

```text
Order Defect recovery repair v2 emergency lock STOP_AND_FIX_GATES
```

returned top hits including:

- `docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md`;
- `docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_GATE_AUDIT_ADOPTION_NOTE_20260630.md`;
- `MD_CATALOG.md`;
- `STATE.md`;
- `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_gate_audit_20260630.md`;
- `docs/infra/debranded_residual_transport/README.md`.

Smoke query:

```text
KEEP_LOCK_AND_FIX LIFT_LOCK_ONLY_IF_USER_CONFIRMS_AND_SNAPSHOT_CLEAN DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT
```

returned top hits including:

- `docs/infra/recovery/ORDER_DEFECT_D630_TASKBOOK_NEXT_PRO_20260630.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_RECOVERY_REPAIR_V2_PROMPT_20260630.md`;
- `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_gate_audit_20260630.md`;
- `docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md`;
- `docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_GATE_AUDIT_ADOPTION_NOTE_20260630.md`.

Smoke query:

```text
MATH_PROOF_RESCUE_AUDIT_20260629 exact rational witness 61/177408
```

returned top hits including:

- `docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`;
- `docs/infra/gpt_deep_research/deep_research_order_defect_recovery_gate_audit_20260630.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_PROMPT_20260629.md`.

Smoke query:

```text
MaoField Order Defect RecoveryRepair V2 zip 442c46ee 252K
```

returned top hits including:

- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_RECOVERY_REPAIR_V2_20260630.md`;
- `docs/infra/recovery/GPT55_PRO_ORDERDEFECT_RECOVERY_HANDOFF_PROMPT_20260629.md`.

RAG remains a locator only.  These hits do not prove mathematical claims or
empirical MaoField claims; primary files, exact certificates, scripts, JSON,
logs, and verdicts remain the evidence sources.

## Final Rerun After Package Hash Update

After replacing the intermediate `1025` package with the `1030final` package in
`STATE.md`, `MD_CATALOG.md`, and the package record, node36 performed one final
node22-vector refresh so the runtime RAG index contains the final package hash.

Final authoritative promoted index:

```text
scanned MaoField files: 8088
active canonical markdown files: 476
chunks: 10763
kb.faiss sha256=3a51e0cb05e2a5930688dc30ebb3ef782ddb8eaf36d16d100b0895bb5439d17a
kb_meta.jsonl sha256=cb70618265fe7e8cc11ff807f894e3482da4768fed651178d4fb4a231566b75f
canonical scope sha256=dc3be6001279b0342d8a584a6dd4a669481ea4aab057c713fb0607d2590abf65
embedding rate=94.219 text/s
```

Final logs:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1035_recoveryrepair_v2_final.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260630_1035_recoveryrepair_v2_final.log
docs/infra/rag_rebuild_20260622/scope_select_20260630_1035_recoveryrepair_v2_final.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1035_recoveryrepair_v2_final.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1035_recoveryrepair_v2_final.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1035_recoveryrepair_v2_final.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1035_recoveryrepair_v2_final.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final_package_hash_20260630_1035.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final_prompt_verdicts_20260630_1035.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final_lock_adoption_20260630_1035.txt
```

Final node22 worker status:

```text
not running port=18080
GPU use after stop: 0%
```

Final smoke checks confirm the index can locate:

- the final package hash `0f43a152...` and `1030final` package record;
- the D630 taskbook verdict options;
- the D630 v2 prompt output format;
- the D630 recovery audit adoption note;
- the emergency-lock boundary in `STATE.md` and recovery handoff files.

## Final2 Rerun After Prompt Hash Drift Correction

After the independent audit found that a later whitespace cleanup changed the
canonical v2 prompt hash from `5346722e...` to `8ab9cad8...`, node36 rebuilt the
light package as `1043final2`, updated `STATE.md`, `MD_CATALOG.md`, and the
package record, copied the corrected package and prompt to node19, and then ran
one final node22-vector refresh.

Final2 node19 package:

```text
MaoField_PRO_OrderDefect_RecoveryRepair_V2_20260630_1043final2.zip
sha256=eeb288e239345c06f60f14d0800c1ead94e570915729e1176d1b9b2f4c936303
size=248K
files=62
prompt_sha256=8ab9cad85b33324907f2b9af12b44acb3db2fbe69aff33b37b21691e93880d2f
```

Final2 authoritative promoted index:

```text
scanned MaoField files: 8088
active canonical markdown files: 476
chunks: 10767
kb.faiss sha256=c2802dcb71a1959030f754a37dfe891c5926e815e0e540e2896594f4c3c6650c
kb_meta.jsonl sha256=0afec8f7b558bb660a7657c1ebc103f902225046ec38177b68a01bda61ab53d3
canonical scope sha256=dc3be6001279b0342d8a584a6dd4a669481ea4aab057c713fb0607d2590abf65
embedding rate=94.252 text/s
```

Final2 logs:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1048_recoveryrepair_v2_final2.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260630_1048_recoveryrepair_v2_final2.log
docs/infra/rag_rebuild_20260622/scope_select_20260630_1048_recoveryrepair_v2_final2.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1048_recoveryrepair_v2_final2.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1048_recoveryrepair_v2_final2.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1048_recoveryrepair_v2_final2.txt
docs/infra/rag_rebuild_20260622/node22_stop_20260630_1048_recoveryrepair_v2_final2.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1048_recoveryrepair_v2_final2.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1048_recoveryrepair_v2_final2.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final2_package_hash_20260630_1048.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final2_prompt_hash_20260630_1048.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final2_verdict_options_20260630_1048.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final2_emergency_lock_20260630_1048.txt
docs/infra/rag_rebuild_20260622/rag_smoke_final2_package_record_exact_20260630_1048.txt
```

Final2 node22 worker status:

```text
not running port=18080
GPU use after second stop check: 0%
```

Final2 smoke checks confirm the index can locate:

- final2 package record and `1043final2` package path;
- final2 package hash `eeb288e239...`;
- final2 prompt hash `8ab9cad85...`;
- D630 taskbook verdict options
  `KEEP_LOCK_AND_FIX` /
  `LIFT_LOCK_ONLY_IF_USER_CONFIRMS_AND_SNAPSHOT_CLEAN` /
  `DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT`;
- external-model emergency-lock wording in `STATE.md`, recovery handoff, and
  adoption notes.

RAG remains a locator only.  These hits do not prove mathematical claims or
empirical MaoField claims; primary files, exact certificates, scripts, JSON,
logs, and verdicts remain the evidence sources.
