# Node22 Vector Refresh -- D706 Pro Decision Package Final

Date verified on node36: 2026-07-06 12:09:37 CST

Status:

```text
PROMOTED_AND_NODE22_STOPPED_FINAL_PRO_PACKAGE_SYNC
```

This final sync was run after adding the Pro decision brief and updating the
zero-context prompt to state that GPT-5.5 Pro has the primary mathematical
decision role for this round. RAG remains a locator only.

## Tag

```text
20260706_1210_pro_decision_package_final
```

## Scope

Scan command:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python scripts/rag_scan_maofield.py --out-dir /home/amd/codex-node36/tmp/rag_20260706_1210_pro_decision_package_final
```

Scope outputs:

```text
scanned_files=8711
active_md_files=523
all_nonarchive_md_files=772
active_scope_sha256=64cf0172ea0e9a810399df849898d5df89bed4ce99de4743578457e40647c8c3
all_nonarchive_scope_sha256=15682158a17ffe9d9bb43426112284b03446bced73d5f6a9c4a592b544ff19f6
```

Canonical sidecars:

```text
docs/infra/rag_rebuild_20260622/rag_scan_20260706_1210_pro_decision_package_final.log
docs/infra/rag_rebuild_20260622/scope_include_maofield_active_md_20260706_1210_pro_decision_package_final.txt
docs/infra/rag_rebuild_20260622/scope_include_maofield_all_nonarchive_md_20260706_1210_pro_decision_package_final.txt
docs/infra/rag_rebuild_20260622/scope_counts_20260706_1210_pro_decision_package_final.txt
docs/infra/rag_rebuild_20260622/scope_sha256_20260706_1210_pro_decision_package_final.txt
```

## Node22 One-Shot Worker

Node36 owned scope, manifests, index verification, promotion, and sidecar
recording. Node22 served temporary `bge-m3` embeddings only.

Start log:

```text
docs/infra/rag_rebuild_20260622/node22_start_20260706_1210_pro_decision_package_final.log
```

Stop/status logs:

```text
docs/infra/rag_rebuild_20260622/node22_stop_20260706_1210_pro_decision_package_final.log
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260706_1210_pro_decision_package_final.log
```

Stop verification:

```text
stopped pid=3526386
not running port=18080
```

## Build

Build command:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python scripts/rag_build_index_node22_http.py \
  --file-list /home/amd/codex-node36/tmp/rag_20260706_1210_pro_decision_package_final/scope_include_maofield_active_md.txt \
  --index-dir /home/amd/codex-node36/tmp/rag_20260706_1210_pro_decision_package_final/candidate_index \
  --endpoint http://192.168.31.22:18080 \
  --model bge-m3-temp \
  --batch-size 32
```

Build result:

```text
files=523
chunks=9813
dim=1024
candidate_kb.faiss_sha256=36f4e50ffae82c2d033f68beaf0c141724820b851cea2e72a5b6cf8fddf6bba1
candidate_kb_meta.jsonl_sha256=7507eee8f18b37b886ff0df7f60d0da26534d440a02916e966c614f93cb7813b
candidate_meta_lines=9813
```

Verification:

```text
faiss_ntotal=9813
meta_lines=9813
VERIFY_PASS
```

Risk note: the build log contains one tokenizer warning for an overlong source
sequence. The builder embeds truncated text with `max_input_chars=3000` while
metadata keeps the original chunk text; this affects retrieval only, not proof
or claim authority.

Canonical build sidecars:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260706_1210_pro_decision_package_final.log
docs/infra/rag_rebuild_20260622/candidate_index_sha256_20260706_1210_pro_decision_package_final.txt
docs/infra/rag_rebuild_20260622/candidate_meta_count_20260706_1210_pro_decision_package_final.txt
```

## Promotion

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_node22_20260706_1210_pro_decision_package_final
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_node22_20260706_1210_pro_decision_package_final
```

Promoted hashes:

```text
36f4e50ffae82c2d033f68beaf0c141724820b851cea2e72a5b6cf8fddf6bba1  /media/amd/raid1/rag/index/kb.faiss
7507eee8f18b37b886ff0df7f60d0da26534d440a02916e966c614f93cb7813b  /media/amd/raid1/rag/index/kb_meta.jsonl
9813 /media/amd/raid1/rag/index/kb_meta.jsonl
```

Canonical promotion sidecars:

```text
docs/infra/rag_rebuild_20260622/promoted_index_sha256_20260706_1210_pro_decision_package_final.txt
docs/infra/rag_rebuild_20260622/promoted_meta_count_20260706_1210_pro_decision_package_final.txt
```

## Smoke Queries

Smoke log:

```text
docs/infra/rag_rebuild_20260622/rag_smoke_20260706_1210_pro_decision_package_final.log
```

Queries:

```text
D706 Pro decision brief RAG status memory primary decision role
D706 external math object scan gauge quotiented finite consistency radius
GQ-FCR Delta squared m_plus m_minus exact rational
Robinson consistency radius MaoField gauge quotient residual audit
support rank ANOVA identifiability defect contextuality global section prior art
```

Smoke verdict:

```text
PASS_LOCATOR
```

The smoke queries locate the Pro decision brief, updated `MD_CATALOG.md`,
updated `STATE.md`, GQ-FCR draft, D706 taskbook, external-prior-art scan, and
exact-control language.

## Boundary

This refresh does not authorize new claims. It only makes the current D706
Pro-decision package materials findable in canonical RAG. Session memory inside
the decision brief is orientation only; it is not evidence.
