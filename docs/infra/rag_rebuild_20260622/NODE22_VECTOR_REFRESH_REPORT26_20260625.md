# Node22 Vector Refresh For Report 26 / v1.1 Workplan — 2026-06-25

Date: 2026-06-25 CST (`date` verified on node36 at 21:51 CST).

Purpose: refresh the default MaoField RAG index after adding the Formal v1
strict audit report, node36 adoption note, v1.1 workplan, and updated
navigation/status files.

## Scope

Node36-owned scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_2151_report26.txt
```

Scope count:

```text
384 active canonical markdown files
```

Project scan:

```text
total_files = 7884
```

## Node22 Worker

Node22 was used only as a temporary bge-m3 HTTP embedding worker. Node36 owned
scope generation, file scanning, chunking, build logs, hash verification,
backup, and promotion.

Temporary worker service:

```text
endpoint = http://192.168.31.22:18080
model = bge-m3-temp
remote_root = /home/amd/codex-node22/tmp/maofield-rag-vector-20260625_2151_report26
```

Note: node36's default SSH config was blocked by a local bad-permission config
file, so this refresh used `ssh -F /dev/null` for node22 commands. This did not
modify SSH configuration.

Final node22 check:

```text
node22_bge_port_18080 = stopped
node22_gpu_use_after_stop = 0%
```

## Build Result

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_2151_report26.log
```

Runtime index:

```text
files = 384
chunks = 9574
vectors = 9574
dimension = 1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Hashes:

```text
kb.faiss      2fd6f4e4627a8a2285e933deab715766dae7f801aec8dab273d499f7f489ec84
kb_meta.jsonl 72b35756d2b31083ae475746207c8ab8f266bab3fcd4e5b0ea03f2db3554997e
build_log     c6f5793d87fde35acad65fdba00d0b1307881bcadf406ee3e0d7d941721b490b
scope_file    0ceca206d88d691b74d4e81af5d034aebb336b60698b28a6ee3280e705e813ba
scan_summary  9b0e57bdf7cec415dda5de0564e948451169effd9f3e8ff13ff071d3d64afa5a
inventory     f5362bd758fbcd8ca436cf1eb5991e32016b9da9fc877f87fbfea218f9eefb71
data_digest   f61cac644c29753f9b24c8711591ca7eff99ea907d2fb36c905a30f79fc0019e
```

Previous default index was backed up as:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260625_2151_report26
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260625_2151_report26
```

## Smoke Queries

The refreshed default RAG retrieves report (26) / v1.1 patch-plan material:

```text
query = report 26 Formal v1 strict audit commutator obstruction v1.1 patch plan
top hits include:
  docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md
  MD_CATALOG.md
  docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_strict_audit_20260625.md
  docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md
  STATE.md
```

The refreshed default RAG also retrieves the v1.1 workplan directly:

```text
query = Formal Note v1.1 Workplan finite gluing complex exit gate formal_v1_1_blocked_or_incomplete
top hits include:
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_WORKPLAN_20260625.md
  docs/infra/debranded_residual_transport/README.md
  STATE.md
```

## Boundary

This refresh makes report (26), its adoption note, and the v1.1 workplan
discoverable through default RAG. It does not create MaoField empirical
evidence.

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
