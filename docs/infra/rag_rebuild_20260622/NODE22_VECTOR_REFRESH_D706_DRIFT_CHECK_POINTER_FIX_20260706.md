# Node22 Vector Refresh -- D706 Drift Check Pointer Fix

Date verified on node36: 2026-07-06 12:40:01 CST

Status:

```text
PROMOTED_AND_NODE22_STOPPED_POINTER_FIX
```

This refresh follows a drift check. The mathematical direction did not drift,
but `MD_CATALOG.md` had one stale pointer to the removed intermediate D706 RAG
record. The catalog pointer was corrected, then the canonical RAG index was
rebuilt so retrieval no longer advertises the missing intermediate record.

RAG remains a locator only. This refresh does not authorize new mathematical or
empirical claims.

## Tag

```text
20260706_1240_drift_check_pointer_fix
```

## Scope

```text
scanned_files=8711
active_md_files=523
all_nonarchive_md_files=772
active_scope_sha256=56444a7eb6e49b8c1d371d7d29af1897bfe66fb73bd3761adc3af4515e0fccd9
all_nonarchive_scope_sha256=418f6fdfd1ee8ec6538c4096d94133b08d5efcac6e9065f9840d9d389b4fee34
```

Canonical sidecars:

```text
docs/infra/rag_rebuild_20260622/rag_scan_20260706_1240_drift_check_pointer_fix.log
docs/infra/rag_rebuild_20260622/scope_include_maofield_active_md_20260706_1240_drift_check_pointer_fix.txt
docs/infra/rag_rebuild_20260622/scope_include_maofield_all_nonarchive_md_20260706_1240_drift_check_pointer_fix.txt
docs/infra/rag_rebuild_20260622/scope_counts_20260706_1240_drift_check_pointer_fix.txt
docs/infra/rag_rebuild_20260622/scope_sha256_20260706_1240_drift_check_pointer_fix.txt
```

## Build And Promotion

```text
files=523
chunks=9814
dim=1024
candidate_kb.faiss_sha256=d9df156e40e3344068ebbc8bcd46f5f18979b4bdf59eccab1c4ed496e62afb23
candidate_kb_meta.jsonl_sha256=fc60e835b2fcce65ba41aef037e0e3e40ada5b6686fcfff3c3764462751cee3e
faiss_ntotal=9814
meta_lines=9814
VERIFY_PASS
```

Promoted hashes:

```text
d9df156e40e3344068ebbc8bcd46f5f18979b4bdf59eccab1c4ed496e62afb23  /media/amd/raid1/rag/index/kb.faiss
fc60e835b2fcce65ba41aef037e0e3e40ada5b6686fcfff3c3764462751cee3e  /media/amd/raid1/rag/index/kb_meta.jsonl
9814 /media/amd/raid1/rag/index/kb_meta.jsonl
```

Backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_node22_20260706_1240_drift_check_pointer_fix
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_node22_20260706_1240_drift_check_pointer_fix
```

## Node22 Stop

```text
stopped pid=3528258
not running port=18080
```

Canonical logs:

```text
docs/infra/rag_rebuild_20260622/node22_start_20260706_1240_drift_check_pointer_fix.log
docs/infra/rag_rebuild_20260622/node22_stop_20260706_1240_drift_check_pointer_fix.log
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260706_1240_drift_check_pointer_fix.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260706_1240_drift_check_pointer_fix.log
```

## Smoke

Smoke log:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_20260706_1240_drift_check_pointer_fix.log
```

Queries checked:

```text
D706 Pro decision brief primary mathematical decision GQ-FCR current status no broad theory
NODE22_VECTOR_REFRESH_D706_PRO_DECISION_PACKAGE_FINAL current RAG authoritative
NODE22_VECTOR_REFRESH_D706_MATH_LANDING_EXTERNAL_SCAN_FINAL stale path should not exist
GQ-FCR Delta squared m_plus m_minus exact rational
```

Smoke verdict:

```text
PASS_LOCATOR
```

The stale intermediate record path no longer appears as a RAG hit for the stale
path query. The current D706 Pro decision package record, state, catalog, and
GQ-FCR draft remain discoverable.

## Drift Verdict

```text
NO_MATHEMATICAL_DIRECTION_DRIFT
```

The only issue found was documentation/index hygiene: one catalog pointer and a
RAG index built before the pointer cleanup. The mathematical boundaries remain:

- finite order-defect certificate is the landed public mathematical result;
- GQ-FCR is a Pro-gated draft candidate, not yet an implemented certificate;
- Pro has the primary mathematical decision role for this round;
- no broad sheaf, consistency-radius, contextuality, ANOVA, or projection
  theory claim is authorized;
- Mode B MaoField empirical status remains `insufficient_artifact`.
