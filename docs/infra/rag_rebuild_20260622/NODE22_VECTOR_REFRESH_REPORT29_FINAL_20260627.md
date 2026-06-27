# Node22 Vector Refresh For Report(29) Final Metadata Pass -- 2026-06-27

Date: 2026-06-27 CST

## Purpose

Refresh the default node36 RAG locator after the final report(29) metadata
polish:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md` immediate handoff now points to the
  report(29) minor-revision audit, not the older v1.1 audit.
- `docs/infra/debranded_residual_transport/README.md` marks the report(27)
  RAG record as historical/previous.
- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_REPORT29_MINOR_REVISION_AUDIT_20260627.md`
  distinguishes the staging directory, final local zip path, canonical prompt
  path, and scratch prompt copy.

RAG is only a locator. Primary files, code, JSON/JSONL, logs, verdicts, and
package hashes remain the evidence boundary.

Self-reference boundary: this record was written after the vector promotion.
The promoted vector index locates the report(29) core materials that existed at
build time. This record, its final-hash lines, and the post-promotion pointers
to `NODE22_VECTOR_REFRESH_REPORT29_FINAL_20260627.md` are primary-file truth
for the current state, but are not guaranteed to be searchable inside
`kb_meta.jsonl` until a later refresh.

## Execution Boundary

Node36 owned scope selection, chunking, metadata writing, hashes,
verification, and promotion. Node22 was used only as a one-shot bge-m3
llama.cpp embedding worker.

Node36 scratch:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260627_1545_report29final/
```

Node22 temporary worker root:

```text
/home/amd/codex-node22/tmp/maofield-rag-vector-20260627_1545_report29final/
```

Node22 service status after build:

```text
not running port=18080
stopped pid=2231635
```

## Scope And Build

MaoField project inventory:

```text
total_files=7925
project_local_index_markdown_active=309
```

Canonical-wide scope:

```text
INCLUDE pool total=664
MaoField=560
Shape-CFD=100
truth/knowledge=4
active A=414
superseded S=250
legal hits=0
```

Build:

```text
files=414
chunks=9929
embedding endpoint=http://192.168.31.22:18080
model=bge-m3-temp
batch_size=32
embedding_seconds=102.8
rate=96.604 text/s
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=8a5fe6f7e1fb571832f33e76ac9dc813728ee98f2f95d724871e64123fc61301

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=ee5d42e4de4236f6f215b617c25287d3743ed4037ac11bf90017ea474bafc3ca
chunks=9929
```

Previous default index was backed up as:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260627_1545_report29final
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260627_1545_report29final
```

## Canonical Outputs

Updated or added under this directory:

```text
maofield_file_inventory.tsv
maofield_scan_summary.json
maofield_data_digest_20260622.md
scope_include_maofield_active_md.txt
scope_include_maofield_all_nonarchive_md.txt
canonical_scope_active_20260627_1545_report29final.txt
rag_build_node22_20260627_1545_report29final.log
NODE22_VECTOR_REFRESH_REPORT29_FINAL_20260627.md
```

## Smoke Queries

Query:

```text
report29 formal_v1_2_patch_requires_minor_revision threshold contract evaluate_test json readback final RAG
```

Top hits included:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT29_FORMALV12_MINOR_20260627.md
MD_CATALOG.md
GPT55_PRO_RESEARCH_INDEX_20260622.md
docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV12_REPORT29_MINOR_REVISION_AUDIT_20260627.md
STATE.md
docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_REPORT29_MINOR_REVISION_AUDIT_PROMPT_20260627.md
```

Query:

```text
MaoField_PRO_FoundationalResidualTransport_FormalV12_Report29_MinorRevisionAudit_20260627_1512 dc1eee e44dc
```

Top hits included:

```text
GPT55_PRO_RESEARCH_INDEX_20260622.md
MD_CATALOG.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
```

## Allowed Interpretation

The refreshed default RAG has a promoted default index with 414 active
canonical markdown files / 9929 chunks and the hashes recorded above. It can
locate the report(29) core materials and report29 minor-revision prompt/package
context that existed at build time. This post-promotion record and any later
pointer/hash text in primary files must be treated as primary-file state rather
than as already searchable RAG metadata.

This does not upgrade MaoField empirical evidence. It does not authorize full
panel work, checkpoint loading, inference, training, new loss, glass-box
language, F3/LOSO language, observed residual/interaction/quotient/transport
/ holonomy field claims, or completed-formal-system claims.
