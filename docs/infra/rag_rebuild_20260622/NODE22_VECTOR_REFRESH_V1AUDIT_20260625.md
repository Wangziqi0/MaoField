# Node22 Vector Refresh For Formal Note v1 Audit — 2026-06-25

Date: 2026-06-25 CST (`date` verified on node36 at 15:15 CST).

Purpose: refresh the default MaoField RAG index after archiving the GPT-5.5 Pro
Formal Note v1 audit and adding the node36 adoption note plus v1 workplan for
the debranded finite weighted residual transport / holonomy / operator no-go
direction.

## Scope

Node36-owned scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_1512_v1auditclean.txt
```

Scope count:

```text
374 active canonical markdown files
```

Project scan:

```text
total_files = 7868
```

## Node22 Worker

Node22 was used only as a temporary bge-m3 HTTP embedding worker. Node36 owned
the scope, manifests, logs, verification, backup, and promotion.

Temporary worker service:

```text
endpoint = http://192.168.31.22:18080
model = bge-m3-temp
remote_root = /home/amd/codex-node22/tmp/maofield-rag-vector-20260625_1512_v1auditclean
```

Final node22 check:

```text
node22_bge_port_18080 = stopped
```

## Build Result

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_1512_v1auditclean.log
```

Runtime index:

```text
files = 374
chunks = 9438
vectors = 9438
dimension = 1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Hashes:

```text
kb.faiss      a5a3e61694e9a7a1a28305dfb8efb674978b93b5da4d8cad508e7d6c819d91af
kb_meta.jsonl fc5af9e173b9fe3faf7e156d470f37c7936bbec0db847144581638af4ab3b33b
build_log     ede3a76b7f016c2dc4c0e202e9fc75b760a564d7556d21f3a2b08c5ff55ed01b
scope_file    f118f08a297e670b6a7cbc7d01eb63924a211f374c359a8d775ea7a6dc91dd2f
scan_summary  abad8af238579cec6fc8155cb40f2c76d97854e283f570260949c6052b548c38
```

The earlier `1457_v1audit` candidate was superseded after stripping trailing
whitespace from the raw Pro report and updating its adoption-note sha256. The
current default RAG is the post-clean `1512_v1auditclean` build above.

## Smoke Queries

The refreshed default RAG retrieves the new Formal Note v1 audit materials:

```text
query = Formal Note v1 workplan keep math project kill empirical positive story
top hits include:
  GPT55_PRO_RESEARCH_INDEX_20260622.md
  STATE.md
  MD_CATALOG.md
  docs/infra/debranded_residual_transport/README.md
  docs/infra/gpt_deep_research/FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_ADOPTION_NOTE_20260625.md
```

```text
query = edge commutation square holonomy rank shadow gluing absorption product reweighting separation v1
top hits include:
  docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_WORKPLAN_20260625.md
  docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V0_20260625.md
  docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md
```

## Boundary

This refresh makes the Formal Note v1 audit, adoption note, and workplan
discoverable through default RAG. It does not create MaoField empirical
evidence.

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
