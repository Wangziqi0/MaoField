# Node22 Vector Refresh For Formal v1 Package — 2026-06-25

Date: 2026-06-25 CST (`date` verified on node36 at 18:16 CST).

Purpose: refresh the default MaoField RAG index after adding the Formal v1
synthetic harness, the zero-context Formal v1 GPT-5.5 Pro prompt, and the
node142 FormalV1 package record.

## Scope

Node36-owned scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_1811_formalv1package.txt
```

Scope count:

```text
380 active canonical markdown files
```

Project scan:

```text
total_files = 7879
```

## Node22 Worker

Node22 was used only as a temporary bge-m3 HTTP embedding worker. Node36 owned
the scope, manifests, logs, verification, backup, and promotion.

Temporary worker service:

```text
endpoint = http://192.168.31.22:18080
model = bge-m3-temp
remote_root = /home/amd/codex-node22/tmp/maofield-rag-vector-20260625_1811_formalv1package
```

Final node22 check:

```text
node22_bge_port_18080 = stopped
node22_gpu_use_after_stop = 0%
```

## Build Result

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_1811_formalv1package.log
```

Runtime index:

```text
files = 380
chunks = 9501
vectors = 9501
dimension = 1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Hashes:

```text
kb.faiss      bad6c71370986a7fd59a4f78a6f0205571152a2f863a90a915a42e4d9dbd143c
kb_meta.jsonl e2a941b28953522b47d0f130533454443023d9bcb7c4376efeb340268fb07e24
build_log     7f93ba83b8e864031d70d201869843f43f715129d591ddd8e0823767de7d7cc8
scope_file    67d5a684429af575bce81c64aed39a77c5a6475b2fa4b8c19c68c9cf6721adfe
scan_summary  c850236c733eab7c0e1d86e98852753c92db18d0f5f8c4cbedca0d2bc1daa0af
inventory     f10e9554b950d9fdef18f6509628f1f5bd4f43ec037f6fbb755dda598b544ccf
data_digest   3745888e3e175ebe55a001dadbb8f3894ec9f514aa256c86d4e0a072e8614666
```

Previous default index was backed up as:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260625_1811_formalv1package
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260625_1811_formalv1package
```

## Smoke Queries

The refreshed default RAG retrieves Formal v1 harness materials:

```text
query = Formal v1 synthetic harness product reweighting separation outcome-derived nuisance invalidation
top hits include:
  docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_20260625.md
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md
```

The refreshed default RAG retrieves Formal v1 package/prompt context:

```text
query = GPT55 Pro Formal v1 package prompt debranded residual transport
top hits include:
  docs/README.md
  docs/infra/debranded_residual_transport/README_FOR_PRO_FOUNDATIONAL_20260625.md
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  docs/infra/gpt_deep_research/README_20260622.md
```

## Boundary

This refresh makes the Formal v1 harness and FormalV1 Pro package discoverable
through default RAG. It does not create MaoField empirical evidence.

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
