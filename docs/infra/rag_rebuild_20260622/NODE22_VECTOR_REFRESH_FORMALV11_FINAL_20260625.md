# Node22 Vector Refresh -- Formal v1.1 Final Pro Package

Date: 2026-06-25 CST

## Verdict

Default MaoField RAG was refreshed after the final Formal v1.1 strict-audit
package was rebuilt as the `2315` package, copied to node142, and verified by
hash.

The runtime index contains the current final package record and prompt hash
material. This record itself is written after the index promotion, so it is a
post-build audit note rather than a self-indexed proof of itself.

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
- Scan time: 2026-06-25 23:21 CST
- Scanned files: 7897
- Active canonical scope: 392 files
- Candidate chunks: 9660
- Embedding model: temporary node22 `bge-m3-temp`
- Embedding endpoint: `http://192.168.31.22:18080`
- Build batch size: 32

Primary final package artifacts indexed by this build:

- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV11_AUDIT_20260625.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md`
- `docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV11_AUDIT_20260625.md`
- `STATE.md`
- `MD_CATALOG.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`

## Final Node142 Package

```text
C:\Users\amd\Desktop\MaoField_PRO_FoundationalResidualTransport_FormalV11_Audit_20260625_2315.zip
zip sha256=8afb1e4a86750d406fc3f16a18be8bd74b0b96c60f84dd9ca589f02e5beaac06

C:\Users\amd\Desktop\GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md
prompt sha256=89f43026b87145aa91c199ad94cf4fb45bc2422c4055db45b777019ea88b6a87
```

Remote `certutil -hashfile` on node142 matched both hashes.

## Build Log

```text
[1/4] files=392
[2/4] chunks=9660 chunk_seconds=13.2
[3/4] remote_embed endpoint=http://192.168.31.22:18080 model=bge-m3-temp batch=32 batches=302
[4/4] wrote index
      faiss=/home/amd/codex-node36/tmp/maofield-rag-20260625_2320_formalv11final/index/kb.faiss bytes=39567405 vectors=9660 dim=1024
      meta=/home/amd/codex-node36/tmp/maofield-rag-20260625_2320_formalv11final/index/kb_meta.jsonl bytes=11853490
[stat] files=392 chunks=9660 embed_seconds=99.6 rate=96.985text/s
```

Full copied build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260625_2320_formalv11final.log
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260625_2320_formalv11final.txt
```

## Hashes

Promoted default RAG index:

```text
kb.faiss=9a652b4e67c6eace0bcbe753fecd9d52c49ca919e78a8a1d852c5e3ac0e6caa1
kb_meta.jsonl=581753b052f7a99f310e525aa4274348530a3c9777377e51983fde4d5e479378
```

Previous default RAG backup:

```text
/media/amd/raid1/rag/index/backups/pre_formalv11final_20260625_2320/kb.faiss.bak
sha256=63e1bc9713e53c5677f7e1ddbe53a1df2bf69cd7e61e070c27c7f8572a23f5c2

/media/amd/raid1/rag/index/backups/pre_formalv11final_20260625_2320/kb_meta.jsonl.bak
sha256=3d5b0c8051fea10e079b67a02be0e4d98337af6e5f8ccaa2bbd4132cc9ed7d79
```

## Node22 Worker Boundary

Node36 owned scope, scan, build command, hashes, backup, promotion, and smoke
verification. Node22 was used only as a temporary vector worker.

After promotion, the node22 service reported:

```text
not running port=18080
GPU[0] : GPU use (%): 0
GPU[1] : GPU use (%): 0
```

## Smoke Queries

Command:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "Formal v1.1 strict audit Pro package 2315 prompt hash RAG final" --top-k 8 --project MaoField
```

Top hits included:

1. `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV11_AUDIT_20260625.md`
2. `docs/infra/debranded_residual_transport/README.md`
3. `MD_CATALOG.md`
4. `STATE.md`
5. `docs/infra/debranded_residual_transport/README_FOR_PRO_FORMALV11_AUDIT_20260625.md`

Command:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "MaoField_PRO_FoundationalResidualTransport_FormalV11_Audit_20260625_2315 zip 89f43026" --top-k 8 --project MaoField
```

Top hits included:

1. `GPT55_PRO_RESEARCH_INDEX_20260622.md`
2. `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV11_AUDIT_20260625.md`
3. `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md`
4. `docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md`

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
