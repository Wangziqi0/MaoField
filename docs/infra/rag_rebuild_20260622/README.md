# MaoField RAG Rebuild — 2026-06-22

This directory contains project-side outputs for rebuilding MaoField coverage in
the canonical RAG index.

## Files

- `maofield_file_inventory.tsv` — recursive inventory of MaoField files.
- `maofield_scan_summary.json` — compact scan summary.
- `maofield_data_digest_20260622.md` — markdown digest for RAG indexing.
- `scope_include_maofield_active_md.txt` — active MaoField markdown only.
- `scope_include_maofield_all_nonarchive_md.txt` — non-archive MaoField
  markdown, including superseded entries; not for default RAG.
- `canonical_scope_active_20260622_230118.txt` — global active canonical scope
  used for the D622 post-q4 node22-vector rebuild.
- `canonical_scope_active_20260623_091046.txt` — global active canonical scope
  used for the D623 report(7) node22-vector refresh.
- `NODE22_VECTOR_REBUILD_20260622.md` — rebuild record, index hashes, backup
  paths, and verification boundary for the temporary node22 GPU vector worker.
- `NODE22_VECTOR_REFRESH_REPORT7_20260623.md` — D623 refresh record proving
  report(7) and its adoption note are discoverable through default RAG.

## Policy

Default RAG should index active markdown and this digest. Raw JSON/JSONL/log
files and checkpoints are evidence targets, not embedding targets.

D622 post-q4: default `/media/amd/raid1/rag/index` was refreshed from a
node36-controlled rebuild that used node22 only for temporary bge-m3 vector
generation. See `NODE22_VECTOR_REBUILD_20260622.md`.

D623 report(7): default `/media/amd/raid1/rag/index` was refreshed again after
archiving the q4 object strict math audit and adoption note. See
`NODE22_VECTOR_REFRESH_REPORT7_20260623.md`.

Rebuild entry point:

```bash
/media/amd/raid1/canonical/projects/MaoField/scripts/rag_rebuild_maofield_36.sh
```

Optional node22 handoff/probe:

```bash
/media/amd/raid1/canonical/projects/MaoField/scripts/rag_rebuild_node22_runner.sh
```
