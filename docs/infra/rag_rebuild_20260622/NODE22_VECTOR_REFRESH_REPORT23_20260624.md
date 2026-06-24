# Node22 Vector Refresh — Report 23 Residual Transport / Holonomy

Date: 2026-06-24 CST

## Boundary

This refresh only updates the default RAG locator index after archiving GPT/PRO
report (23) and its local adoption note.

It did not:

- run a full panel;
- load checkpoints for a new panel;
- train;
- authorize a new loss;
- create an observed residual, interaction, quotient-residual, transport, or
  holonomy field.

RAG remains a locator. Promoted claims still require direct reads of canonical
files, code, JSON/JSONL, logs, or experiment verdicts.

## Inputs

Report (23) archive:

```text
docs/infra/gpt_deep_research/deep_research_residual_transport_holonomy_split_project_20260624.md
attachment_sha256=78ae75a38c5b0a1c8bd2ad2297abf8382ff13550ade972f06cac4eaa779d2de7
canonical_sha256=3025217867b1a70f226ed77f5f22ac4297e1eea4768f5e8613f98a16613753f5
canonical_note=normalized trailing whitespace before commit
```

Adoption note:

```text
docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md
sha256=944a3fc548b293d3698269ac9524d3c0ed2ced42ae05619128b3cfab1602b8f7
```

Scope file:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260624_1555_report23.txt
sha256=fab0ef58b279884c562a0765d66f1ea920193e3e71ed1b16722dea3fff4f1efb
```

Scope counts:

```text
canonical active md files: 347
MaoField active md files: 242
MaoField non-archive md files: 492
scanned files: 7830
```

Build log:

```text
docs/infra/rag_rebuild_20260622/rag_build_node22_20260624_1555_report23.log
sha256=81ee07afbbdaa08e3948d362ae67aa88f53ee86546ab664597f8bd35ff2a5479
```

## Runtime Output

Candidate build:

```text
/home/amd/codex-node36/tmp/maofield-rag-20260624_1555_report23/index
files=347
chunks=9111
vectors=9111
dim=1024
```

Promoted default index:

```text
/media/amd/raid1/rag/index/kb.faiss
sha256=8525c962bab634d370654bf945f2886812af23f969e87e611f53f41873c9f854

/media/amd/raid1/rag/index/kb_meta.jsonl
sha256=321bd7cb58de32bc9fb80a1d321e725eb03c34c0e3cb244976be994edc5aca09
lines=9111
```

Pre-refresh backups from the D624 Pro-prompt runtime:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260624_1555_report23
sha256=d33dade6399e2e545dbb371f8ecfe1415dc89a617a5866ca763a6899085a813b

/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260624_1555_report23
sha256=cedfde51014ff7affedd58e33af6ea7818820e112f67d11c888584b5164156c8
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

Note: after the locator build, node36 normalized trailing whitespace in the
canonical report archive before commit. This changes the canonical file hash but
not the intended report content or RAG's role as a locator. Exact wording and
hash verification must use direct canonical file reads.

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "residual transport holonomy split project square holonomy D_rho H_square" \
  --top-k 6 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `docs/infra/gpt_deep_research/deep_research_residual_transport_holonomy_split_project_20260624.md`
- `MD_CATALOG.md`
- `STATE.md`
- `docs/infra/gpt_deep_research/README_20260622.md`

Second query:

```text
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py \
  "report23 finite scale lattice residual transport adoption note insufficient_artifact smoke_conjecture_only" \
  --top-k 6 --project MaoField
```

Top hits included:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`
- `STATE.md`
- `docs/infra/gpt_deep_research/deep_research_quotient_residual_mainline_debranded_program_20260624.md`
- `docs/infra/gpt_deep_research/deep_research_mode_a_quotient_residual_kill_framework_20260623.md`

## Local Verdict

Report (23) is now discoverable through default RAG. Its local boundary remains:

```text
Mode A recommendation only;
possible debranded finite scale-lattice residual transport / holonomy project;
not a MaoField evidence upgrade;
not an already-approved repo split;
Mode B = insufficient_artifact / smoke_conjecture_only.
```
