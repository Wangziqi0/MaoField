# Node22 Vector Refresh — Report (24) Transport / Holonomy Audit

Date: 2026-06-24 CST

## Boundary

This refresh only updates the default RAG locator index after archiving GPT/PRO
report (24) and the node36 adoption note for its transport / holonomy
math-turn audit.

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

Archived report (24):

```text
docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md
sha256=e552b734be62caae86c0d6ecdfb7015f43369aeefb3e3a7fbf2615332c152263
```

Adoption note:

```text
docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md
sha256=5bffc39b01840850a1391234167933a43ba71fb0dcd2e5b2d020a57001a50134
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260624_1908_report24.txt
sha256=1a2a237d359f9ee1f923af154438fe59297deb3d4ced363fb323862521993667
```

Scope counts:

```text
canonical active md files: 351
MaoField active md files: 248
MaoField non-archive md files: 498
scanned files: 7840
scan summary sha256=f8dd265deba564a1eabc670a9d34fa02531d1be5fd47e5ff8a8a6ec6f979ef42
```

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260624_1908_report24.log
sha256=19c731d6b2b62ff2b9c4470890d489a694b6251ea394ad570fb12a6c41bf5be2
```

## Product-Weight Check

Report (24)'s warning about current q4 x tokenpos4 weights was verified
directly on node36 against:

```text
docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json
```

Direct local values:

```text
schema_id=q4_tokenpos4_hypercube_20260623
total_weight=1.0
max_abs_error=0.0045863252708490815
max_rel_error_vs_actual=0.06724386724386727
max_rel_error_vs_product_expected=0.07209158415841586
argmax: slice_id=2, position_bin=0, actual=0.06820436507936507, product_expected=0.06361803980851599
```

Current local language should therefore be non-product weighted hierarchical
projection / residual program unless future exact product weights or explicit
reweighting are supplied. Do not call the current q4 x tokenpos4 carrier a
canonical product-measure Hoeffding decomposition.

## Runtime Output

Candidate build:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260624_1908_report24/index
files=351
chunks=9171
vectors=9171
dim=1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=e89ec4ebb6e2bd3cdad9c411bfff82d7b647be1dfaadb2a808683c8cd160e556

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=7e077d59f41d7dad2a813bba8146f86a96269c9844fb83efc53bfa0b203915bd
lines=9171
```

Pre-refresh backups from the synthetic-harness runtime:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_1908_report24
sha256=797e1186a446c5ee3339b1c4d0c8ebd9f238d943fb1610bd396992188448cda2

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_1908_report24
sha256=752293de7ddc582e326d9adf6de9746992affce574162f038af375297b606533
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
  "report24 transport holonomy math-turn audit non-product weights hierarchical projection professor verdict E" \
  --top-k 6 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/README_20260622.md`
- `STATE.md`
- `docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`

Second query:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "q4 tokenpos4 weights not product-form canonical Hoeffding non-product weighted hierarchical projection" \
  --top-k 6 --project MaoField
```

Top hits included:

- `docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`
- `docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md`
- `docs/infra/gpt_deep_research/deep_research_quotient_residual_mainline_debranded_program_20260624.md`
- `docs/infra/gpt_deep_research/deep_research_residual_transport_holonomy_split_project_20260624.md`
- `docs/infra/gpt_deep_research/README_20260622.md`

## Local Verdict

Report (24) and its product-weight warning are now discoverable through default
RAG. Its local boundary remains:

```text
Mode A professor verdict E = recommendation only;
PI has not executed a project split;
current q4 x tokenpos4 carrier = non-product weighted hierarchical projection / residual program;
not canonical product-measure Hoeffding;
Mode B = insufficient_artifact / smoke_conjecture_only;
no full panel / no training / no new loss / no observed residual field.
```
