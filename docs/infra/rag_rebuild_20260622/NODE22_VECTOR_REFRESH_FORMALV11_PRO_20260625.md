# Node22 Vector Refresh -- Formal v1.1 Pro Audit Package

Date: 2026-06-25 CST

Superseded by:

```text
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_FORMALV11_FINAL_20260625.md
```

Reason: the standalone prompt and 142 package were rebuilt as the final `2315`
package after this refresh, so this record is retained as the pre-final
FormalV11-Pro refresh record.

## Verdict

Default MaoField RAG was refreshed after adding the Formal v1.1 strict-audit
GPT-5.5 Pro prompt, package README, and node142 package record.

This refresh proves that the package/prompt/status records are discoverable
through the node36 RAG locator. It does not promote any MaoField empirical
claim.

Strongest allowed local verdict remains:

```text
definitions_and_harness_viable_only
```

Mode B empirical status remains:

```text
insufficient_artifact
```

## Inputs

- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Git source HEAD before refresh: `7f528ca docs(math): land formal residual transport v1.1`
- Scan time: 2026-06-25 23:03 CST
- Scanned files: 7895
- Active canonical scope: 391 files
- Candidate chunks: 9646
- Embedding model: temporary node22 `bge-m3-temp`
- Embedding endpoint: `http://192.168.31.22:18080`
- Build batch size: 32

Primary newly indexed package artifacts:

- `docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md`
- `docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV11_AUDIT_20260625.md`
- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV11_AUDIT_20260625.md`

Supporting current-state artifacts:

- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_strict_audit_20260625.md`
- `docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md`
- `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md`
- `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md`

## Build Log

```text
[1/4] files=391
[2/4] chunks=9646 chunk_seconds=12.8
[3/4] remote_embed endpoint=http://192.168.31.22:18080 model=bge-m3-temp batch=32 batches=302
[4/4] wrote index
      faiss=/home/amd/codex-node36/tmp/maofield-rag-20260625_2248_formalv11pro/index/kb.faiss bytes=39510061 vectors=9646 dim=1024
      meta=/home/amd/codex-node36/tmp/maofield-rag-20260625_2248_formalv11pro/index/kb_meta.jsonl bytes=11838158
[stat] files=391 chunks=9646 embed_seconds=99.4 rate=97.078text/s
```

Full copied build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_2248_formalv11pro.log
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_2248_formalv11pro.txt
```

## Hashes

Promoted default RAG index:

```text
kb.faiss=63e1bc9713e53c5677f7e1ddbe53a1df2bf69cd7e61e070c27c7f8572a23f5c2
kb_meta.jsonl=3d5b0c8051fea10e079b67a02be0e4d98337af6e5f8ccaa2bbd4132cc9ed7d79
```

Previous default RAG backup:

```text
/media/amd/raid1/rag/index/backups/pre_formalv11pro_20260625_2248/kb.faiss.bak
sha256=a7bcd313a53adabd4e6ccef715cf09024c66bd39c20d3489f1eceb6a82359457

/media/amd/raid1/rag/index/backups/pre_formalv11pro_20260625_2248/kb_meta.jsonl.bak
sha256=9ccf1498210b2bfd7184bad730d0c283e96475aa1b6ae9fc3d3f30d064fa39f6
```

Node142 package material:

```text
MaoField_PRO_FoundationalResidualTransport_FormalV11_Audit_20260625_2242.zip
sha256=1a79d2f5f668838fc86157fd938a160b8c4e511d083b5fed80ee73b1858463f6

GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md
sha256=0ea8a9e0ed97f4b0573c77a0af6b37e79911ecd562063eaf6deade15a210494c
```

## Node22 Worker Boundary

Node36 owned scope, scan, build command, hashes, backup, promotion, and smoke
verification. Node22 was used only as a temporary vector worker.

After promotion, the node22 service reported:

```text
not running port=18080
GPU[0] : GPU use (%): 1
GPU[1] : GPU use (%): 0
```

## Smoke Queries

Command:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "Formal v1.1 strict audit Pro package prompt report26 proof harness" --top-k 8 --project MaoField
```

Top hits included:

1. `docs/infra/debranded_residual_transport/README.md`
2. `GPT55_PRO_RESEARCH_INDEX_20260622.md`
3. `STATE.md`
4. `docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV11_AUDIT_20260625.md`

Command:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT FormalV11 zip" --top-k 8 --project MaoField
```

Top hits included:

1. `docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV11_AUDIT_20260625.md`
2. `GPT55_PRO_RESEARCH_INDEX_20260622.md`
3. `MD_CATALOG.md`
4. `docs/README.md`
5. `docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md`

## Evidence Boundary

This RAG refresh is a locator/indexing operation only. It does not:

- run a full panel;
- load checkpoints;
- run model inference;
- train;
- authorize a new loss;
- observe a MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- upgrade any smoke/dashboard/prose result into evidence.
