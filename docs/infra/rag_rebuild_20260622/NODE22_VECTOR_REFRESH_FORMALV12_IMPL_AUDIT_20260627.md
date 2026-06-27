# Node22 Vector Refresh For Formal v1.2 Implementation Audit -- 2026-06-27

Date: 2026-06-27 CST

## Purpose

Refresh the default node36 RAG locator after adding and finalizing the Formal
v1.2 implementation-audit materials:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
scripts/debranded_residual_transport_harness_v1_2.py
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md
docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json
docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md
docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md
```

RAG is only a locator. Primary files, code, JSON/JSONL, logs, verdicts, and
package hashes remain the evidence boundary.

Self-reference boundary: this record was written after the vector promotion.
Therefore the promoted vector index locates the v1.2 implementation and package
record, but this record itself will be fully indexed only in a later refresh.

Final inventory sweep boundary: after writing this record and the associated
README/status updates, node36 reran the MaoField project inventory only. That
final sweep found `total_files=7918` and `index_markdown_active=303` inside
MaoField. The promoted vector index was not rebuilt a second time. The `407`
active documents below are the broader canonical RAG build scope: MaoField
active project markdown plus Shape-CFD and truth/knowledge support documents.

## Execution Boundary

Node36 owned scope selection, chunking, metadata writing, hashes,
verification, and promotion. Node22 was used only as a one-shot bge-m3 GPU
embedding worker.

Node36 scratch:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260627_1315_v12impl/
```

Node22 temporary worker root:

```text
/home/amd/codex-node22/tmp/maofield-rag-vector-20260627_1315_v12impl/
```

Node22 service status after build:

```text
not running port=18080
GPU use: 0%
```

## Scope And Build

Scan:

```text
scanned_files=7916
```

Scope:

```text
INCLUDE pool total=657
MaoField=553
Shape-CFD=100
truth/knowledge=4
active A=407
superseded S=250
legal hits=0
```

Build:

```text
files=407
chunks=9843
embedding endpoint=http://192.168.31.22:18080
model=bge-m3-temp
batch_size=32
embedding_seconds=102.1
rate=96.400 text/s
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=c9aa97afed0b25119f930821a0a21390fadc8e7dd463374b2b2da39e11c6da73

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=e25f9fa3dbfd67ddcbba50e0547b81e8fbfdcea3e93df89d4751444f4b8aa701
chunks=9843
```

Previous default index was backed up as:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260627_1315_v12impl
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260627_1315_v12impl
```

## Canonical Outputs

Updated or added under this directory:

```text
maofield_file_inventory.tsv
maofield_scan_summary.json
maofield_data_digest_20260622.md
scope_include_maofield_active_md.txt
scope_include_maofield_all_nonarchive_md.txt
canonical_scope_active_20260627_1315_v12impl.txt
rag_build_node22_20260627_1315_v12impl.log
NODE22_VECTOR_REFRESH_FORMALV12_IMPL_AUDIT_20260627.md
```

## Smoke Queries

Query:

```text
report28 v1_2_small_patch_feasible Formal v1.2 implementation harness threshold contract
```

Top hits included:

```text
STATE.md
MD_CATALOG.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md
GPT55_PRO_RESEARCH_INDEX_20260622.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md
```

Query:

```text
FormalV12 ImplementationAudit zip ddb74fa1620324f59a4a5384eccf29c8089216a5a5a6af38dff7d465ceecbbf2 prompt 58be0c35904789a41ba94a3bef6445c23a66527c7bb5d2bef484306d227008b4
```

Top hits included:

```text
docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md
MD_CATALOG.md
GPT55_PRO_RESEARCH_INDEX_20260622.md
```

## Allowed Interpretation

The refreshed default RAG can now locate report (28), the Formal v1.2 note,
the v1.2 harness summary and JSON, the implementation-audit prompt, and the
node142 package record.

This does not upgrade MaoField empirical evidence. It does not authorize full
panel work, checkpoint loading, inference, training, new loss, glass-box
language, F3/LOSO language, observed residual/interaction/quotient/transport
/ holonomy field claims, or completed-formal-system claims.
