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

## Policy

Default RAG should index active markdown and this digest. Raw JSON/JSONL/log
files and checkpoints are evidence targets, not embedding targets.

Rebuild entry point:

```bash
/media/amd/raid1/canonical/projects/MaoField/scripts/rag_rebuild_maofield_36.sh
```

Optional node22 handoff/probe:

```bash
/media/amd/raid1/canonical/projects/MaoField/scripts/rag_rebuild_node22_runner.sh
```
