# Node22 Vector Refresh — Report 22 Mainline

Date: 2026-06-24 CST

## Boundary

This refresh only updates the default RAG locator index after archiving GPT/PRO
report (22) and its local adoption note.

It did not:

- run a full panel;
- load checkpoints for a new panel;
- train;
- authorize a new loss;
- create an observed residual / interaction / quotient-residual field.

RAG remains a locator. Promoted claims still require direct reads of canonical
files, code, JSON/JSONL, logs, or experiment verdicts.

## Inputs

Report (22) archive:

```text
docs/infra/gpt_deep_research/deep_research_quotient_residual_mainline_debranded_program_20260624.md
attachment_sha256=dc11d5aa4fd7ff1e3dbe1d94aad9e47123629c003c5867a0a048916f04903c7b
canonical_sha256=792134c7e207dfb9bc290d674abb4e96d46c1ecf3937e45228f20f3dfc836335
```

Adoption note:

```text
docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260624_1322_report22.txt
```

Scope counts:

```text
canonical active md files: 342
MaoField active md files: 238
scanned files: 7821
```

Build logs:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_report22_20260624_1322.log
docs/infra/rag_rebuild_20260622/rag_build_node22_report22_20260624_1333_norm.log
docs/infra/rag_rebuild_20260622/rag_build_node22_report22_20260624_1338_final.log
```

The second and third builds were run after normalizing trailing whitespace in
the canonical archive copy of report (22). The promoted default index is from
the final normalized build.

## Runtime Output

Candidate build:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260624_1338_report22_final/index
files=342
chunks=9027
vectors=9027
dim=1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=b4492a73764d67e9bd104047c49ec7d4d8c6e84af7335b9af998e312db245f88

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=77efe884b4f704e41b4c1e959d97b1e20221d28e0ae36a7e16b042eae5f14b6f
lines=9027
```

Pre-refresh backups from report(21) runtime:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_1322_report22
sha256=e522eccb5ed21554f33a9ec9fe567fb3821664c7eb2ec20419ce49535ee090d2

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_1322_report22
sha256=2920ce4dcf36eeda9c813d128fd5805a61c87491afc36ecac49ff301a65c391b
```

Intermediate pre-normalization report(22) backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_1333_report22_norm
sha256=81172338a29911d7013867663b19fd0211fc7fb47ab4572f02a73d24077df65d

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_1333_report22_norm
sha256=0f19d2fd2fcbcde90d5a4484875874382ab70dca68b4f6c0d431b8953ecd648e
```

Final pre-promotion normalized backup:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_1338_report22_final
sha256=6a20790d79f099e83fc095b938347b20dae85da952a5506717e4dd3367facaba

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_1338_report22_final
sha256=385b8f976070c5178be982c661ce4dec2de24a8fd970b7de2f1a672e5af464a0
```

## Node22 State

Temporary node22 bge-m3 HTTP service:

```text
started: yes, for build only
stopped after build: yes
status after build: not running port=18080
```

## Verification Queries

The promoted default RAG index was smoke-tested with:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report22 quotient residual mainline debranded negative-centered measurement-audit no-go" \
  --top-k 6 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/README_20260622.md`
- `STATE.md`
- `docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Second query:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE report17 report19 report21 mainline insufficient_artifact" \
  --top-k 6 --project MaoField
```

Top hits included:

- `STATE.md`
- `QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `README_20260622.md`

## Local Verdict

Report (22) is now discoverable through default RAG. Its local boundary remains:

```text
negative-centered measurement-audit / no-go framework;
no current observed residual field;
Mode B = insufficient_artifact / smoke_conjecture_only.
```
