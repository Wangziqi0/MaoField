# Node22 Vector Refresh -- Order-Defect Metadata/Label Patch V6

Date: 2026-06-30 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh indexes the D630 report(10) metadata/label patch state after:

- archiving report(10);
- adding report(10) adoption note;
- adding report(9) label erratum;
- adding V6 metadata/label taskbook;
- adding V6 zero-context Pro prompt;
- adding V6 package record;
- updating `STATE.md` and `MD_CATALOG.md`.

RAG remains a locator only. Primary files, exact rational certificate, scripts,
JSON, logs, verdicts, and local adoption notes remain the evidence sources.

## Final Sidecar Policy

Exact live RAG hashes for the final V6 refresh are intentionally stored in
sidecar text files, not embedded verbatim in this indexed Markdown file. This
avoids a self-hash loop: if an indexed Markdown file contains the digest of an
index that contains that Markdown file, the digest changes when the Markdown is
edited.

Final V6 sidecars:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1640_metadatalabel_v6_finalrecord.txt
docs/infra/rag_rebuild_20260622/scope_hash_20260630_1640_metadatalabel_v6_finalrecord.txt
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1640_metadatalabel_v6_finalrecord.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1640_metadatalabel_v6_finalrecord.txt
docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1640_metadatalabel_v6_finalrecord.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1640_metadatalabel_v6_finalrecord.log
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1640_metadatalabel_v6_finalrecord.txt
```

Final smoke files:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_metadatalabel_v6_package_record_20260630_1640.txt
docs/infra/rag_rebuild_20260622/rag_smoke_metadatalabel_v6_prompt_20260630_1640.txt
docs/infra/rag_rebuild_20260622/rag_smoke_metadatalabel_v6_erratum_20260630_1640.txt
docs/infra/rag_rebuild_20260622/rag_smoke_metadatalabel_v6_state_modeb_20260630_1640.txt
```

Expected smoke result: package and prompt queries locate the V6 package record
and V6 prompt; the erratum query locates the report(9) label erratum; the
state/Mode-B query keeps `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK`,
`LOCKED_NO_PAPER_BODY`, and `insufficient_artifact` visible. Direct files remain
evidence; RAG remains locator only.
