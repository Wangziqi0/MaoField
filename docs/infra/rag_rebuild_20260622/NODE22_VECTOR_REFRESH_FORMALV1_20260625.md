# Node22 Vector Refresh For Formal Note v1 Draft — 2026-06-25

Date: 2026-06-25 CST (`date` verified on node36 at 17:42 CST).

Purpose: refresh the default MaoField RAG index after drafting
`FORMAL_NOTE_V1_20260625.md` and updating the canonical project indexes for the
debranded finite weighted residual transport / holonomy / operator no-go
direction.

## Scope

Node36-owned scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_1735_formalv1.txt
```

Scope count:

```text
376 active canonical markdown files
```

Project scan:

```text
total_files = 7872
index_markdown_active = 271
```

## Node22 Worker

Node22 was used only as a temporary bge-m3 HTTP embedding worker. Node36 owned
the scope, manifests, logs, verification, backup, and promotion.

Temporary worker service:

```text
endpoint = http://192.168.31.22:18080
model = bge-m3-temp
remote_root = /home/amd/codex-node22/tmp/maofield-rag-vector-20260625_1735_formalv1
```

Final node22 check:

```text
node22_bge_port_18080 = stopped
```

## Build Result

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_1735_formalv1.log
```

Runtime index:

```text
files = 376
chunks = 9464
vectors = 9464
dimension = 1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Hashes:

```text
kb.faiss      dd83502728b903cba949a3e0bcea7ec0666bc55ee36b4b2953912777d7fde51d
kb_meta.jsonl 6d7bc59b9dc666182af0e6d00ad8018e53ca943aa6de423af9873c9ec122602d
build_log     90a5e06e6089dbee8b8951336ef9f27461e1163e3f6fb2fe61dbcd903557fad8
scope_file    d8ea038047e6bcbe642a934bd439a90f2a033c58897bf69f44599e5fb9353ab2
scan_summary  a280d96ca9d6575ce212b47e2092753eb9216df59dae1a353b4c1e80a97d53b4
inventory     7a845d33cf013c49dbd6b65fa4d5bf39444a53d29cc8d7ff1977a3bd252b8997
data_digest   82e3a586340560cda11bcfc476aaf1bf8b935cfc17fd7d176d8e37b57ac313c6
```

## Smoke Queries

The refreshed default RAG retrieves Formal Note v1 materials:

```text
query = Formal Note v1 source-fixed nuisance edge commutation square holonomy no-go non-product weight counterexample
top hits include:
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_ADOPTION_NOTE_20260625.md
  DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md
```

```text
query = P_N K argmin quotient representative outcome-derived nuisance vacuity weighted projection lemma
top hits include:
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_WORKPLAN_20260625.md
  FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_ADOPTION_NOTE_20260625.md
```

## Boundary

This refresh makes Formal Note v1 discoverable through default RAG. It does not
create MaoField empirical evidence.

Strongest allowed local claim:

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
