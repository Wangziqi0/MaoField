# Node22 Vector Refresh For Report(27) And Formal v1.2 Patch — 2026-06-26

Date: 2026-06-26 CST

## Purpose

Refresh the default node36 RAG locator after adding and finalizing:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md
docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md
docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV12_PATCH_20260626.md
docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT_20260626.md
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_PATCH_20260626.md
```

RAG is only a locator. Primary files, code, JSON/JSONL, logs, verdicts, and
package hashes remain the evidence boundary.

Self-reference boundary: this record includes final post-promotion hash
backfills. It is canonical navigation, but the final hash lines themselves are
not evidence that a second self-referential pass was started after every
post-promotion edit.

After the vector promotion, node36 also ran a final lightweight inventory sweep
to remove the superseded `1250` candidate log from `maofield_file_inventory.tsv`
and record the final `1320` log. That sweep updated inventory/digest files only;
the promoted vector index remains the `1320_report27v12final` build recorded
below.

## Execution Boundary

Node36 owned scope selection, chunking, metadata writing, hashes,
verification, and promotion. Node22 was used only as a one-shot bge-m3 GPU
embedding worker.

Final node36 scratch:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260626_1320_report27v12final/
```

Final node22 temporary worker root:

```text
/home/amd/codex-node22/tmp/maofield-rag-vector-20260626_1320_report27v12final/
```

Node22 service status after build:

```text
not running port=18080
GPU use: 0%
```

## Scope And Build

Scan:

```text
scanned_files=7907
```

Scope:

```text
INCLUDE pool total=650
MaoField=546
Shape-CFD=100
truth/knowledge=4
active A=400
superseded S=250
legal hits=0
```

Build:

```text
files=400
chunks=9749
embedding endpoint=http://192.168.31.22:18080
model=bge-m3-temp
batch_size=32
embedding_seconds=100.6
rate=96.866 text/s
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=12697c08f4fd16b7cd83bd1a49e298b1eb3d058da36e3090be0f2c13cecab862

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=d858b281da1b74ea4858d67dbb83fb134ba85963906e6be7dce4461a7e23f41c
chunks=9749
```

Previous default index was backed up as:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260626_1320_report27v12final
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260626_1320_report27v12final
```

## Canonical Outputs

Updated or added under this directory:

```text
maofield_file_inventory.tsv
maofield_scan_summary.json
maofield_data_digest_20260622.md
scope_include_maofield_active_md.txt
scope_include_maofield_all_nonarchive_md.txt
canonical_scope_active_20260626_1320_report27v12final.txt
rag_build_node22_20260626_1320_report27v12final.log
NODE22_VECTOR_REFRESH_REPORT27_V12_20260626.md
```

Final lightweight inventory sweep:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260626_1348_final_inventory/scan/
scanned_files=7907
```

## Smoke Queries

Query:

```text
report27 accept_with_v1_2_required Formal v1.2 minimal patch prompt
```

Top hits included:

```text
docs/infra/debranded_residual_transport/README.md
GPT55_PRO_RESEARCH_INDEX_20260622.md
docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV12_PATCH_20260626.md
docs/infra/gpt_deep_research/README_20260622.md
```

Query:

```text
GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT FormalV12 MinimalPatch zip
```

Top hits included:

```text
docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV12_PATCH_20260626.md
MD_CATALOG.md
docs/infra/gpt_deep_research/README_20260622.md
GPT55_PRO_RESEARCH_INDEX_20260622.md
```

## Allowed Interpretation

The refreshed default RAG can now locate report (27), the v1.2 workplan, the
FormalV12 prompt, and the node142 package record.

This record's final hash backfills are not evidence that an infinite
self-referential RAG loop occurred.

This does not upgrade MaoField empirical evidence. It does not authorize full
panel work, checkpoint loading, inference, training, new loss, glass-box
language, F3/LOSO language, or observed residual/interaction/quotient/transport
/ holonomy field claims.
