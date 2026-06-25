# Node22 Vector Refresh For Report(25) — 2026-06-25

Date: 2026-06-25 CST (`date` verified on node36 at 10:44 CST).

Purpose: refresh the default MaoField RAG index after archiving report(25),
its adoption note, and the first formal-note outline for the debranded finite
weighted residual transport / holonomy / operator no-go direction.

## Scope

Node36-owned scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_1044_report25.txt
```

Scope count:

```text
362 active canonical markdown files
```

Project scan:

```text
total_files = 7851
markdown = 528
index_markdown_active = 257
digest_only_data = 2131
git_head_at_scan = 31837ab
```

## Node22 Worker

Node22 was used only as a temporary bge-m3 HTTP embedding worker. Node36 owned
the scope, manifests, logs, verification, backup, and promotion.

Temporary worker service:

```text
endpoint = http://192.168.31.22:18080
model = bge-m3-temp
```

Final node22 check:

```text
node22_bge_port_18080 = stopped
```

## Build Result

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_1044_report25.log
```

Runtime index:

```text
files = 362
chunks = 9301
vectors = 9301
dimension = 1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Hashes:

```text
kb.faiss      546a3fd518feb311ede88dbe9d3d08d148fdb2fa8ac584f356d9aa4897b80cb2
kb_meta.jsonl f9436c5e204a8b56140f66835eb50f45c2e5ba8f1ce63897580314bce0782544
build_log     a48e588be71e12586e98d7681a1b86693f8327d8841ee612fb6117c512b59b0a
scope_file    ad6894fba14e6f6edba3cd7184de7c6bb2362d1b81e38755a9b308a44dd83845
scan_summary  2f577aafabd00ad6b5322f5fc16d6fca87a9492927ba0526774abc4c17aa3bee
```

## Boundary

This refresh makes the D625 strict-audit materials discoverable through
default RAG. It does not create MaoField empirical evidence.

Strongest allowed local claim from the newly indexed materials:

```text
formal_note_agenda_adopted
```

Still forbidden:

- full-panel result observed;
- 16-cell aggregate exists;
- residual / interaction / quotient-residual field observed;
- residual transport or holonomy field observed;
- LOSO passed;
- F3 positive;
- glass box broken;
- training or new loss authorized.

RAG locates these files; primary files, code, JSON/JSONL, logs, and verdicts
remain the only claim evidence.
