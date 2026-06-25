# Node22 Vector Refresh For Formal v1.1 Patch -- 2026-06-25

## Scope

This refresh updates the default MaoField RAG index after the local Formal
Residual Transport v1.1 patch landed.

- Verified time: 2026-06-25 CST, node36.
- Node36 scratch root:
  `/home/amd/codex-node36/tmp/maofield-rag-20260625_2218_v11patch/`
- Node22 temporary worker root:
  `/home/amd/codex-node22/tmp/maofield-rag-vector-20260625_2218_v11patch/`
- Temporary node22 service: llama.cpp embedding server, alias `bge-m3-temp`,
  endpoint `http://192.168.31.22:18080`.
- Node22 service state after refresh: stopped.
- Active canonical scope:
  `docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_2218_v11patch.txt`

The active canonical scope contains 387 files. The MaoField recursive scan saw
7890 files total, including 553 markdown files, with 282 MaoField markdown
files marked `index_markdown_active` and 2142 structured/text data files kept
as digest-only evidence targets.

## Build Result

Node36 controlled scope, chunking, FAISS writing, metadata writing,
verification, and promotion. Node22 only served temporary embeddings.

```text
[1/4] files=387
[2/4] chunks=9614 chunk_seconds=13.2
[3/4] remote_embed endpoint=http://192.168.31.22:18080 model=bge-m3-temp batch=32 batches=301
[4/4] wrote index
      faiss=/home/amd/codex-node36/tmp/maofield-rag-20260625_2218_v11patch/index/kb.faiss bytes=39378989 vectors=9614 dim=1024
      meta=/home/amd/codex-node36/tmp/maofield-rag-20260625_2218_v11patch/index/kb_meta.jsonl bytes=11795374
[stat] files=387 chunks=9614 embed_seconds=99.1 rate=97.039text/s
```

## Node22 Stop Readback

After promotion, node36 re-read the node22 temporary service state using
`ssh -F /dev/null` at 2026-06-25 22:38:48 CST:

```text
not running port=18080 log=/home/amd/codex-node22/tmp/maofield-rag-vector-20260625_2218_v11patch/bge-m3-llama-18080.log
GPU[0] : GPU use (%): 0
GPU[1] : GPU use (%): 0
```

## Hashes

Promoted default RAG index:

```text
a7bcd313a53adabd4e6ccef715cf09024c66bd39c20d3489f1eceb6a82359457  /media/amd/raid1/rag/index/kb.faiss
9ccf1498210b2bfd7184bad730d0c283e96475aa1b6ae9fc3d3f30d064fa39f6  /media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
2fd6f4e4627a8a2285e933deab715766dae7f801aec8dab273d499f7f489ec84  /media/amd/raid1/rag/index/kb.faiss.bak_pre_20260625_2218_v11patch
72b35756d2b31083ae475746207c8ab8f266bab3fcd4e5b0ea03f2db3554997e  /media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260625_2218_v11patch
```

Promoted audit artifacts:

```text
cb748db02d959550aad90899d3150406b3a8bdecf2fa51515112061b981a8409  docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_2218_v11patch.txt
72e51d58ca010b1de86f5ba2cc4c311fc7d5678e53316dd2ead30e2ca24222f4  docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_2218_v11patch.log
8dedcf337fafaf829b5fca006a54cb5c3684784be1e2cf336a010df7886d336d  docs/infra/rag_rebuild_20260622/maofield_file_inventory.tsv
84ecf825b64f93b759e7b2971b2edb130e7968bd425cdbd344440ce77fcd4900  docs/infra/rag_rebuild_20260622/maofield_scan_summary.json
a0683ab1b53f796b53461bc95aeceb05560bbfd3746503ed7ea5d05230f60208  docs/infra/rag_rebuild_20260622/maofield_data_digest_20260622.md
```

## Smoke Queries

The refreshed default RAG retrieves the v1.1 package and its guardrails:

```text
query = SYNTHETIC_HARNESS_V1_1 threshold contract environment metadata
top hits include:
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md
  docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  STATE.md

query = Finite Weighted Residual Transport Formal Note v1.1 harness contract
top hits include:
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md
  docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_strict_audit_20260625.md
```

A broader theme query for quotient descent and projection-evolution commutator
still preferentially retrieves the v1 strict-audit/adoption/workplan documents
before the formal note body. Treat that as navigation behavior, not a claim
failure: primary evidence remains the v1.1 files themselves.

## Evidence Boundary

This refresh only proves that the default RAG can locate the newly promoted
v1.1 formal/harness materials. It does not prove any MaoField empirical claim.
It does not run full panel, load checkpoints, perform inference, train a model,
authorize a new loss, or observe a real residual/transport/holonomy field.

Strongest allowed status after this refresh remains:

```text
definitions_and_harness_viable_only
```
