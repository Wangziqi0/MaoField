# Node22 Vector Refresh For Formal-Start Pro Package — 2026-06-25

Date: 2026-06-25 CST (`date` verified on node36 at 12:15 CST).

Purpose: refresh the default MaoField RAG index after adding the formal-start
GPT-5.5 Pro prompt and the node142 package record for the debranded finite
weighted residual transport / holonomy / operator no-go direction.

## Scope

Node36-owned scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_1212_formalpro.txt
```

Scope count:

```text
370 active canonical markdown files
```

Project scan:

```text
total_files = 7863
```

## Node22 Worker

Node22 was used only as a temporary bge-m3 HTTP embedding worker. Node36 owned
the scope, manifests, logs, verification, backup, and promotion.

Temporary worker service:

```text
endpoint = http://192.168.31.22:18080
model = bge-m3-temp
remote_root = /home/amd/codex-node22/tmp/maofield-rag-vector-20260625_1212_formalpro
```

Final node22 check:

```text
node22_bge_port_18080 = stopped
```

## Build Result

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_1212_formalpro.log
```

Runtime index:

```text
files = 370
chunks = 9362
vectors = 9362
dimension = 1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Hashes:

```text
kb.faiss      aa97f87a05ff320e062e321af1cb281c5774029444855e7fe816ac6672661de0
kb_meta.jsonl 7f237c0518294d980c27dc1d020ff145f73f27d975d7b986f0984d776eca9939
build_log     0fd693b657fa96604f7225a503d6a04dd782d7e2fd533541d758fd0a77d71fd9
scope_file    6a325e72954c94898056c3e0f9e1b34112d97e7dea53a1c7b18ddc5385ff8573
scan_summary  72a2ef98fb26bf88e30d91ad8d0a393722b0a7461e5e747f826ba51e949a3441
```

## Smoke Queries

The refreshed default RAG retrieves the new formal-start Pro package materials:

```text
query = GPT55 Pro Foundational Residual Transport Formal Note v1 theorem no-go package
top hits include:
  docs/infra/debranded_residual_transport/README_FOR_PRO_FOUNDATIONAL_20260625.md
  docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALSTART_20260625.md
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  MD_CATALOG.md
```

```text
query = MaoField formal-start 142 package zip hash foundational residual transport prompt
top hits include:
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  STATE.md
  MD_CATALOG.md
  docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALSTART_20260625.md
```

## Boundary

This refresh makes the formal-start Pro package and prompt discoverable through
default RAG. It does not create MaoField empirical evidence.

Strongest allowed local claim from the newly indexed materials:

```text
definitions_and_harness_viable_only
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
