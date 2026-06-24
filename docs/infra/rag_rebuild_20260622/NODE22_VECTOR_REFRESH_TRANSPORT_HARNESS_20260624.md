# Node22 Vector Refresh — Residual Transport / Holonomy Synthetic Harness

Date: 2026-06-24 CST

## Boundary

This refresh only updates the default RAG locator index after adding the
zero-GPU synthetic harness for report (23)'s residual transport / holonomy
proposal.

It did not:

- run a full panel;
- read a MaoField aggregate;
- load checkpoints;
- run model inference;
- train;
- authorize a new loss;
- create an observed residual, interaction, quotient-residual, transport, or
  holonomy field.

RAG remains a locator. Promoted claims still require direct reads of canonical
files, code, JSON/JSONL, logs, or experiment verdicts.

## Inputs

Synthetic harness taskbook:

```text
docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_HARNESS_20260624.md
sha256=1a5a777fea61e7a3d4fcd6d75cc85df0e84efd1ccf90011fab4eef633a6d64f3
```

Synthetic result:

```text
docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md
sha256=b8348aec708fb9d6480ab0c2d44f90ad38a4b0f348b70538049ba9221c906000

docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.json
sha256=5c0d9586f31c60512a645020d4b1f0ee0a516a2fa8437c10db30e7f59f8884fd
```

Synthetic script:

```text
scripts/residual_transport_holonomy_synthetic.py
sha256=a60e4069a821ac5ae8e8af05729e97fbf9c264bdd31bfd6c5dc192f25a16d4af
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260624_1648_transport.txt
sha256=683b519fae72ce9d03a98fdc0727e66bf0943e2b1963d7f9c8ae396f3be1738f
```

Scope counts:

```text
canonical active md files: 349
MaoField active md files: 245
MaoField non-archive md files: 495
scanned files: 7836
```

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260624_1648_transport.log
sha256=9383e2c4cafaae867ed7d800981b5c31abcc8ac0200d4bea0a15a057fa96a13d
```

## Runtime Output

Candidate build:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260624_1648_transport/index
files=349
chunks=9128
vectors=9128
dim=1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=797e1186a446c5ee3339b1c4d0c8ebd9f238d943fb1610bd396992188448cda2

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=752293de7ddc582e326d9adf6de9746992affce574162f038af375297b606533
lines=9128
```

Pre-refresh backups from the report(23) runtime:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_1648_transport
sha256=8525c962bab634d370654bf945f2886812af23f969e87e611f53f41873c9f854

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_1648_transport
sha256=321bd7cb58de32bc9fb80a1d321e725eb03c34c0e3cb244976be994edc5aca09
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
  "residual transport holonomy synthetic harness scale_square_holonomy rank1_angle_vacuity_guard" \
  --top-k 6 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md`
- `docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_HARNESS_20260624.md`
- `docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md`
- `MD_CATALOG.md`

Second query:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "synthetic_harness_only_no_maofield_claim random_same_dim_angle_gap nuisance_functoriality_digest" \
  --top-k 6 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md`
- `docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_HARNESS_20260624.md`
- `MD_CATALOG.md`
- `STATE.md`

## Local Verdict

The residual transport / holonomy synthetic harness is now discoverable through
default RAG. Its local boundary remains:

```text
synthetic_harness_only_no_maofield_claim;
definition/code viability only;
not a MaoField evidence upgrade;
Mode B = insufficient_artifact / smoke_conjecture_only.
```
