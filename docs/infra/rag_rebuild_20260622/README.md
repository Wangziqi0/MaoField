# MaoField RAG Rebuild — 2026-06-22

This directory contains project-side outputs for rebuilding MaoField coverage in
the canonical RAG index.

## Files

- `maofield_file_inventory.tsv` — recursive inventory of MaoField files.
- `maofield_scan_summary.json` — compact scan summary.
- `maofield_data_digest_20260622.md` — markdown digest for RAG indexing.
- `scope_include_maofield_active_md.txt` — active MaoField markdown only.
- `scope_include_maofield_all_nonarchive_md.txt` — non-archive MaoField
  markdown, including superseded entries; not for default RAG.
- `canonical_scope_active_20260622_230118.txt` — global active canonical scope
  used for the D622 post-q4 node22-vector rebuild.
- `canonical_scope_active_20260623_091046.txt` — global active canonical scope
  used for the D623 report(7) node22-vector refresh.
- `canonical_scope_active_20260623_095411.txt` — global active canonical scope
  used for the D623 q4 implementation-gate node22-vector refresh.
- `canonical_scope_active_20260623_1054_report9.txt` — global active canonical
  scope used for the D623 report(9) node22-vector refresh.
- `canonical_scope_active_20260623_1148_report11.txt` — global active canonical
  scope used for the D623 report(11) node22-vector refresh.
- `canonical_scope_active_20260623_1250_report13.txt` — global active canonical
  scope used for the D623 report(13) node22-vector refresh.
- `canonical_scope_active_20260623_1336_report15.txt` — global active canonical
  scope used for the D623 report(15) node22-vector refresh.
- `canonical_scope_active_20260623_1509_report17.txt` — global active canonical
  scope used for the D623 report(17) node22-vector refresh.
- `canonical_scope_active_20260623_1556_modea.txt` — global active canonical
  scope used for the D623 Mode A prompt / Mode B skeleton node22-vector refresh.
- `canonical_scope_active_20260623_1642_report19.txt` — global active canonical
  scope used for the D623 report(19) quotient-residual node22-vector refresh.
- `canonical_scope_active_20260623_1733_report21.txt` — global active canonical
  scope used for the D623 report(21) finite-ANOVA node22-vector refresh.
- `canonical_scope_active_20260624_1322_report22.txt` — global active canonical
  scope used for the D624 report(22) mainline node22-vector refresh.
- `canonical_scope_active_20260624_1530_proprompt.txt` — global active
  canonical scope used for the D624 null-tests contract / updated Pro-prompt
  final node22-vector refresh.
- `canonical_scope_active_20260624_1555_report23.txt` — global active
  canonical scope used for the D624 report(23) residual transport / holonomy
  node22-vector refresh.
- `canonical_scope_active_20260624_1648_transport.txt` — global active
  canonical scope used for the D624 residual transport / holonomy synthetic
  harness node22-vector refresh.
- `canonical_scope_active_20260624_1908_report24.txt` — global active
  canonical scope used for the D624 report(24) transport / holonomy math-turn
  audit node22-vector refresh.
- `canonical_scope_active_20260624_2110_debranded.txt` — global active
  canonical scope used for the D624 debranded residual transport kickoff
  node22-vector refresh.
- `canonical_scope_active_20260625_1044_report25.txt` — global active
  canonical scope used for the D625 report(25) strict-audit / formal-note
  node22-vector refresh.
- `NODE22_VECTOR_REBUILD_20260622.md` — rebuild record, index hashes, backup
  paths, and verification boundary for the temporary node22 GPU vector worker.
- `NODE22_VECTOR_REFRESH_REPORT7_20260623.md` — D623 refresh record proving
  report(7) and its adoption note are discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_Q4_GATE_20260623.md` — D623 refresh record proving the
  q4 implementation gate and updated pointers are discoverable through default
  RAG.
- `NODE22_VECTOR_REFRESH_REPORT9_20260623.md` — D623 refresh record proving
  report(9), its adoption note, and residual-field q4 pointers are discoverable
  through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT11_20260623.md` — D623 refresh record proving
  report(11), its adoption note, and q4 hypercube zero-GPU feasibility artifacts
  are discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT13_20260623.md` — D623 refresh record proving
  report(13), its adoption note, and current-repo q4 hypercube guardrails are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT15_20260623.md` — D623 refresh record proving
  report(15), its adoption note, and the interaction-field smoke audit are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT17_20260623.md` — D623 refresh record proving
  report(17), its adoption note, and the hypercube interaction prereg design are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_MODEA_20260623.md` — D623 refresh record proving the
  Mode A GPT-5.5 Pro prompt and Mode B skeleton pointers are discoverable
  through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT19_20260623.md` — D623 refresh record proving
  report(19), its adoption note, and the follow-up quotient-residual Pro prompt
  are discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT21_20260623.md` — D623 refresh record proving
  report(21), its adoption note, and finite-ANOVA/no-go guardrails are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT22_20260624.md` — D624 refresh record proving
  report(22), its adoption note, and mainline no-go guardrails are discoverable
  through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT23_20260624.md` — D624 refresh record proving
  report(23), its adoption note, and residual transport / holonomy pointers are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_TRANSPORT_HARNESS_20260624.md` — D624 refresh record
  proving the report(23) zero-GPU synthetic harness and result are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT24_20260624.md` — D624 refresh record proving
  report(24), its adoption note, and the non-product-weight boundary are
  discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_DEBRANDED_20260624.md` — D624 refresh record proving
  the debranded residual transport status, core description, and highest prompt
  are discoverable through default RAG.
- `NODE22_VECTOR_REFRESH_REPORT25_20260625.md` — D625 refresh record proving
  report(25), its adoption note, and the first formal-note outline are
  discoverable through default RAG.
- `rag_build_node22_20260624_1530_proprompt.log` — D624 final node22 build log
  after `GPT55_PRO_MODE_A_MATH_DISCOVERY_PROMPT_20260623.md` was updated to
  include report(21), report(22), public-404 guardrails, smoke-not-evidence
  wording, and `NULL_TESTS_CONTRACT_20260624.md`.
- `rag_build_node22_20260624_1555_report23.log` — D624 node22 build log after
  archiving report(23) and its adoption note.
- `rag_build_node22_20260624_1648_transport.log` — D624 node22 build log after
  adding the residual transport / holonomy synthetic harness and result.
- `rag_build_node22_20260624_1908_report24.log` — D624 node22 build log after
  archiving report(24) and its adoption note.
- `rag_build_node22_20260624_2110_debranded.log` — D624 node22 build log after
  adding the debranded residual transport kickoff documents and highest prompt.
- `rag_build_node22_20260625_1044_report25.log` — D625 node22 build log after
  archiving report(25), its adoption note, and the first formal-note outline.

## Policy

Default RAG should index active markdown and this digest. Raw JSON/JSONL/log
files and checkpoints are evidence targets, not embedding targets.

D622 post-q4: default `/media/amd/raid1/rag/index` was refreshed from a
node36-controlled rebuild that used node22 only for temporary bge-m3 vector
generation. See `NODE22_VECTOR_REBUILD_20260622.md`.

D623 report(7): default `/media/amd/raid1/rag/index` was refreshed again after
archiving the q4 object strict math audit and adoption note. See
`NODE22_VECTOR_REFRESH_REPORT7_20260623.md`.

D623 q4 gate: default `/media/amd/raid1/rag/index` was refreshed after the q4
implementation gate commit. See `NODE22_VECTOR_REFRESH_Q4_GATE_20260623.md`.

D623 report(9): default `/media/amd/raid1/rag/index` was refreshed after the q4
residual-field strict math audit and code guard updates. See
`NODE22_VECTOR_REFRESH_REPORT9_20260623.md`.

D623 report(11): default `/media/amd/raid1/rag/index` was refreshed after the
q4 hypercube extension strict math audit and zero-GPU feasibility artifacts. See
`NODE22_VECTOR_REFRESH_REPORT11_20260623.md`.

D623 report(13): default `/media/amd/raid1/rag/index` was refreshed after the
current-repo q4 hypercube strict audit and adoption note. See
`NODE22_VECTOR_REFRESH_REPORT13_20260623.md`.

D623 report(15): default `/media/amd/raid1/rag/index` was refreshed after the
future math-object / interaction-field audit and smoke reproduction. See
`NODE22_VECTOR_REFRESH_REPORT15_20260623.md`.

D623 report(17): default `/media/amd/raid1/rag/index` was refreshed after the
math-ore quotient residual strict audit and zero-GPU prereg design. See
`NODE22_VECTOR_REFRESH_REPORT17_20260623.md`.

D623 ModeA: default `/media/amd/raid1/rag/index` was refreshed after adding the
GPT-5.5 Pro Mode A prompt and future-only Mode B skeleton. See
`NODE22_VECTOR_REFRESH_MODEA_20260623.md`.

D623 report(19): default `/media/amd/raid1/rag/index` was refreshed after
adding the quotient-residual kill-framework report, adoption note, and follow-up
Pro prompt. See `NODE22_VECTOR_REFRESH_REPORT19_20260623.md`.

D623 report(21): default `/media/amd/raid1/rag/index` was refreshed after
adding the quotient-residual finite-ANOVA/no-go formalization report and
adoption note. See `NODE22_VECTOR_REFRESH_REPORT21_20260623.md`.

D624 report(22): default `/media/amd/raid1/rag/index` was refreshed after
adding the quotient-residual mainline / debranded program report and adoption
note. See `NODE22_VECTOR_REFRESH_REPORT22_20260624.md`.

D624 null-tests / Pro prompt final: default `/media/amd/raid1/rag/index` was
refreshed with a node36-controlled, node22-temporary bge-m3 build after updating
the Mode A Pro prompt and D624 null-tests contract. Final runtime index:
345 active canonical markdown files / 9073 chunks; `kb.faiss=d33dade...`,
`kb_meta=cedfde51...`. The earlier node36 CPU rebuild attempt was stopped
before promotion and did not overwrite the default index.

D624 report(23): default `/media/amd/raid1/rag/index` was refreshed after
adding the residual transport / holonomy split-project proposal and adoption
note. See `NODE22_VECTOR_REFRESH_REPORT23_20260624.md`. Runtime index:
347 active canonical markdown files / 9111 chunks; `kb.faiss=8525c962...`,
`kb_meta=321bd7cb...`. Node22 was used only as a temporary bge-m3 worker and
the service was stopped after build.

D624 residual transport / holonomy harness: default
`/media/amd/raid1/rag/index` was refreshed after adding the zero-GPU synthetic
harness and result for report(23)'s transport/holonomy definitions. See
`NODE22_VECTOR_REFRESH_TRANSPORT_HARNESS_20260624.md`. Runtime index:
349 active canonical markdown files / 9128 chunks; `kb.faiss=797e1186...`,
`kb_meta=752293de...`. Node22 was used only as a temporary bge-m3 worker and
the service was stopped after build.

D624 report(24): default `/media/amd/raid1/rag/index` was refreshed after
archiving the transport / holonomy math-turn audit and adoption note. See
`NODE22_VECTOR_REFRESH_REPORT24_20260624.md`. Runtime index: 351 active
canonical markdown files / 9171 chunks; `kb.faiss=e89ec4eb...`,
`kb_meta=7e077d59...`. Node22 was used only as a temporary bge-m3 worker and
the service was stopped after build.

D624 debranded residual transport kickoff: default `/media/amd/raid1/rag/index`
was refreshed after adding the debranded status snapshot, core description, and
highest GPT-5.5 Pro prompt. See `NODE22_VECTOR_REFRESH_DEBRANDED_20260624.md`.
Runtime index: 357 active canonical markdown files / 9228 chunks;
`kb.faiss=98a9ca4c...`, `kb_meta=90b01342...`. Node22 was used only as a
temporary bge-m3 worker and the service was stopped after build.

D625 report(25): default `/media/amd/raid1/rag/index` was refreshed after
adding the debranded strict-audit report, adoption note, and first formal-note
outline. See `NODE22_VECTOR_REFRESH_REPORT25_20260625.md`. Runtime index:
362 active canonical markdown files / 9301 chunks; `kb.faiss=546a3fd5...`,
`kb_meta=f9436c5e...`. Node22 was used only as a temporary bge-m3 worker and
the service was stopped after build.

Rebuild entry point:

```bash
/media/amd/raid1/canonical/projects/MaoField/scripts/rag_rebuild_maofield_36.sh
```

Optional node22 handoff/probe:

```bash
/media/amd/raid1/canonical/projects/MaoField/scripts/rag_rebuild_node22_runner.sh
```
