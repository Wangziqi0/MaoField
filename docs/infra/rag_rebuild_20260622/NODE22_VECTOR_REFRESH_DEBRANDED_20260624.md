# Node22 Vector Refresh — Debranded Residual Transport Kickoff

Date: 2026-06-24 CST

## Boundary

This refresh only updates the default RAG locator index after adding the
debranded residual transport / holonomy / no-go project kickoff documents and
the GPT-5.5 Pro highest prompt.

It did not:

- run a full panel;
- read or create a MaoField full-panel aggregate;
- load checkpoints;
- run model inference;
- train;
- authorize a new loss;
- create an observed residual, interaction, quotient-residual, transport, or
  holonomy field.

RAG remains a locator. Promoted claims still require direct reads of canonical
files, code, JSON/JSONL, logs, or experiment verdicts.

## Inputs

Status snapshot:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md
sha256=3d4334c9393da56fefc32568242ae26c35d7d6ab508947632fc7339d58d8a3fa
```

Core description:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md
sha256=e21d8bd252e8bde5ac4101cb700b5f7221887866fbdb295ee51f32b496c7668c
```

Highest prompt:

```text
docs/infra/gpt_deep_research/GPT55_PRO_DEBRANDED_RESIDUAL_TRANSPORT_HIGHEST_PROMPT_20260624.md
sha256=72a361219870b723d24b58b13b6ba7f61f46c89aa8937a9489e43c7005d94aee
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260624_2110_debranded.txt
sha256=165a4ef4ff694486a2766a3fd5faebba223def8429ec597b323dc74cf1ff8f63
```

Scope counts:

```text
canonical active md files: 357
MaoField active md files: 252
MaoField non-archive md files: 502
scanned files: 7845
scan summary sha256=fb0b846466e14910129d2e31bee42ecf5ed2adcbfbd18d27ac013f2d1e6173ef
```

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260624_2110_debranded.log
sha256=78fc620e7fff846dec72ecf1d40dc9508d2e9ad67eb1da613efe83b2eb2f239e
```

## Runtime Output

Candidate build:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260624_2110_debranded/index
files=357
chunks=9228
vectors=9228
dim=1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=98a9ca4c2b862119861aae5c744fa982d2bab51fa4084c79700e2520a5a44437

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=90b01342951d1b31da89fc25dceaa1dc8c76a0f5c9fa217923ca207fd467cce3
lines=9228
```

Pre-refresh backups from the report(24) runtime:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_2110_debranded
sha256=e89ec4ebb6e2bd3cdad9c411bfff82d7b647be1dfaadb2a808683c8cd160e556

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_2110_debranded
sha256=7e077d59f41d7dad2a813bba8146f86a96269c9844fb83efc53bfa0b203915bd
```

## Node22 State

Temporary node22 bge-m3 HTTP service:

```text
started: yes, for build only
stopped after build: yes
status after build: not running port=18080
```

The default SSH configuration on node36 still reports a system config
permission warning for `/etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf`, so
this refresh used `ssh -F /dev/null` / `rsync -e 'ssh -F /dev/null'`. No system
SSH config was edited.

## Verification Queries

The promoted default RAG index was smoke-tested with:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "debranded residual transport highest prompt finite weighted holonomy no-go MaoField negative pilot" \
  --top-k 8 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `STATE.md`
- `MD_CATALOG.md`
- `README_zh.md`
- `docs/README.md`

Second query:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "Core Description admissible triple X_s w_s N_s P_s D_rho H_square success conditions" \
  --top-k 6 --project MaoField
```

Top hits included:

- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`
- `docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md`
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`

Third query:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "GPT55_PRO_DEBRANDED_RESIDUAL_TRANSPORT_HIGHEST_PROMPT Section 7 Best next action Junior-high explanation" \
  --top-k 6 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/README_20260622.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_DEBRANDED_RESIDUAL_TRANSPORT_HIGHEST_PROMPT_20260624.md`
- `docs/infra/gpt_deep_research/GPT55_PRO_MODE_A_MATH_DISCOVERY_PROMPT_20260623.md`

## Local Verdict

The debranded direction documents and highest prompt are discoverable through
default RAG. The local boundary remains:

```text
MaoField empirical line = negative-centered pilot / measurement-audit case;
Mode A new line = debranded finite weighted residual transport / holonomy / no-go mathematics;
Mode B = insufficient_artifact / smoke_conjecture_only;
no full panel / no training / no new loss / no observed residual field.
```
