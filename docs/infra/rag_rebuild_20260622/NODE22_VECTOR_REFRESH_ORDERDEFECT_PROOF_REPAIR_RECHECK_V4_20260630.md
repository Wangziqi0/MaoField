# Node22 Vector Refresh -- Order-Defect Proof-Repair Recheck V4

Date: 2026-06-30 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh indexes the D630 report(8) proof-repair recheck state after
archiving report(8), adding the adoption note, adding the proof-repair
taskbook, adding the proof-repair candidate, updating `STATE.md`,
`MD_CATALOG.md`, and the debranded residual transport README, and adding the
V4 zero-context Pro recheck prompt.

The scope used the previous default dual-Pro canonical scope as the base and
added these five files:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_proof_biblio_repair_audit_report8_20260630.md
docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md
docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md
docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_PROMPT_20260630.md
```

Primary indexed context includes current on-disk versions of `STATE.md`,
`MD_CATALOG.md`, and `docs/infra/debranded_residual_transport/README.md`.

RAG remains a locator only. These hits do not prove mathematical claims or
empirical MaoField claims; primary files, exact certificates, scripts, JSON,
logs, and verdicts remain the evidence sources.

## Method

Node36 owned scope selection, chunking, metadata, FAISS writing, hash
verification, promotion, and smoke queries. Node22 only ran a temporary
`llama.cpp` bge-m3 HTTP embedding worker.

```text
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
node22 temporary root=/home/amd/codex-node22/tmp/maofield-rag-vector-20260630_1303_proofrepair_v4
node36 scratch=/home/amd/codex-node36/tmp/orderdefect_proof_repair_recheck_v4_20260630_1303/rag
```

## Promoted Index

```text
default canonical scope files: 485
chunks: 10934
kb.faiss sha256=d02422922692d09c42864fcd41f479bd057b928fae5510f02413135baad126a4
kb_meta.jsonl sha256=4d006e2b04515b8e31ffc60bbfccbc11e95b5c6ab3b4ca7d50902ca89a5bd1c9
canonical scope sha256=bb519998e0ece8363cc96af4aeb0b5a8d682b1b73a896fa713a23d1064f8f0be
embedding rate=94.229 text/s
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/backups/pre_proofrepair_v4_20260630_1303/kb.faiss.bak
/media/amd/raid1/rag/index/backups/pre_proofrepair_v4_20260630_1303/kb_meta.jsonl.bak
```

Backup hashes:

```text
kb.faiss.bak sha256=faa520c338b6eabdc2de9037f6eff60ce7463d196788a43c406e3644f065f70f
kb_meta.jsonl.bak sha256=4b6151cddb0eaaba89fe717055b2813fb3cb210756e499e444045af0e58f5670
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1303_proofrepair_v4.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1303_proofrepair_v4.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1303_proofrepair_v4.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1303_proofrepair_v4.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1303_proofrepair_v4.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1303_proofrepair_v4.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_report8_20260630_1303.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_candidate_20260630_1303.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_lock_modeb_20260630_1303.txt
```

Candidate hashes:

```text
d02422922692d09c42864fcd41f479bd057b928fae5510f02413135baad126a4  candidate_index/kb.faiss
4d006e2b04515b8e31ffc60bbfccbc11e95b5c6ab3b4ca7d50902ca89a5bd1c9  candidate_index/kb_meta.jsonl
bb519998e0ece8363cc96af4aeb0b5a8d682b1b73a896fa713a23d1064f8f0be  canonical_scope_active_20260630_1303_proofrepair_v4.txt
74f29577aa30f957cae393c9ddee89b4550443feac084fed52cdf9dc23785cb8  rag_build_node22_candidate_20260630_1303_proofrepair_v4.log
```

## Node22 Stop Status

The temporary HTTP service was stopped after build and before final reporting.

Second status check:

```text
not running port=18080
GPU[0] use: 0%
GPU[1] use: 0%
```

## Smoke Checks

Smoke query:

```text
PATCH_PROOFS_THEN_RECHECK report8 proof repair candidate
```

returned top hits including:

- `docs/infra/gpt_deep_research/deep_research_order_defect_proof_biblio_repair_audit_report8_20260630.md`;
- `docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md`;
- `docs/infra/debranded_residual_transport/README.md`;
- `MD_CATALOG.md`;
- `STATE.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_PROMPT_20260630.md`;
- `docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md`.

Smoke query:

```text
Proposition 2 Proposition 3 PROOF_REPAIR_CANDIDATE A cap B0 D_w
```

returned top hits including:

- `docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md`;
- `docs/infra/gpt_deep_research/GPT55_PRO_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_PROMPT_20260630.md`;
- `docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md`;
- `docs/infra/debranded_residual_transport/README.md`.

Smoke query:

```text
Mode B insufficient_artifact no full panel no training no observed field
```

returned top hits including:

- `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- Formal residual transport audit/adoption boundary files;
- Mode A / Mode B boundary notes.

The third query is intentionally broad; exact Mode B boundaries must still be
read from `STATE.md`, formal notes, adoption notes, and recovery files.

## Final Package-Record Sync Refresh

After the V4 zip was rebuilt to avoid zip self-hash drift, node36 added the
external package record to the RAG scope and rebuilt the default index one more
time. This final refresh is the authoritative promoted index for this round.

Additional file added to the previous V4 scope:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md
```

Final promoted index:

```text
default canonical scope files: 486
chunks: 10945
kb.faiss sha256=cb62eddb5d130759a091811600af4601c3cc7eb1fae07c2048681162df570309
kb_meta.jsonl sha256=87da38278a6bea6de8b6c51d46c950dcbc005c48be697d7fd115e4105e8ee9da
canonical scope sha256=a9064c519bcdfd95de7b6278e17837fa880c6eac589352e6f89d5977340e75a1
embedding rate=93.839 text/s
```

Final logs and manifests:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1320_proofrepair_v4_finalpkg.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1320_proofrepair_v4_finalpkg.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1320_proofrepair_v4_finalpkg.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1320_proofrepair_v4_finalpkg.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1320_proofrepair_v4_finalpkg.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1320_proofrepair_v4_finalpkg.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_package_record_20260630_1320.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_report8_20260630_1320.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_lock_modeb_20260630_1320.txt
```

Final pre-refresh backups:

```text
/media/amd/raid1/rag/index/backups/pre_proofrepair_v4_finalpkg_20260630_1320/kb.faiss.bak
/media/amd/raid1/rag/index/backups/pre_proofrepair_v4_finalpkg_20260630_1320/kb_meta.jsonl.bak
```

Final backup hashes:

```text
kb.faiss.bak sha256=d02422922692d09c42864fcd41f479bd057b928fae5510f02413135baad126a4
kb_meta.jsonl.bak sha256=4d006e2b04515b8e31ffc60bbfccbc11e95b5c6ab3b4ca7d50902ca89a5bd1c9
```

Final node22 second status check:

```text
not running port=18080
GPU[0] use: 0%
GPU[1] use: 0%
```

Superseded final smoke query, run before the package record was corrected from
the intermediate `e866971c...` package digest to the then-final `e1a0c03e...`
package digest. The `e1a0...` package was later superseded by the
post-finalclean repack described below:

```text
ProofRepairRecheck V4 e866971c package record node19 desktop
```

returned top hits including:

- `MD_CATALOG.md`;
- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md`;
- `STATE.md`;
- `docs/infra/debranded_residual_transport/README.md`;
- report(8).

This smoke is kept as provenance only. A later finalfix refresh must be used
for the authoritative package-record locator.

Final smoke query:

```text
PATCH_PROOFS_THEN_RECHECK report8 proof repair candidate
```

returned top hits including report(8), the proof-repair taskbook, README,
`STATE.md`, the V4 prompt, the report(8) adoption note, and `MD_CATALOG.md`.

Final smoke query:

```text
Mode B insufficient_artifact no full panel no training no observed field
```

returned boundary and guardrail hits. As before, exact Mode B boundaries remain
primary-file claims, not RAG claims.

## Finalfix Package-Record Locator Refresh

Reason: independent verification found that the previous live RAG
package-record locator still returned the intermediate `e866971c...` package
digest even though the direct package record and node19 readback had already
been corrected to the then-final `e1a0c03e...` package digest. This `e1a0...`
package is now provenance only; the final Pro bundle is the post-finalclean
repack with hash `0285cf26...`.

This finalfix refresh was run after:

- `MD_CATALOG.md` was corrected so the D630 dual-Pro recovery-repair index is
  provenance, not the current authoritative index;
- the superseded `e866971c...` smoke query above was explicitly labelled as
  provenance only;
- the package record already contained the then-final zip hash
  `e1a0c03e6f574ff4355511a790e54f8fc81014cedb283007176fe1176d53697a`.

Finalfix scope and build:

```text
intermediate locator repair; exact hashes/counts: see
promoted_hashes_20260630_1330_proofrepair_v4_finalfix.txt,
canonical_scope_active_20260630_1330_proofrepair_v4_finalfix.txt, and
rag_build_node22_candidate_20260630_1330_proofrepair_v4_finalfix.log
```

Finalfix logs and manifests:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1330_proofrepair_v4_finalfix.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1330_proofrepair_v4_finalfix.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1330_proofrepair_v4_finalfix.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1330_proofrepair_v4_finalfix.txt
docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1330_proofrepair_v4_finalfix.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1330_proofrepair_v4_finalfix.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1330_proofrepair_v4_finalfix.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalfix_package_record_20260630_1330.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalfix_report8_20260630_1330.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalfix_modeb_20260630_1330.txt
```

Finalfix pre-refresh backups:

```text
/media/amd/raid1/rag/index/backups/pre_proofrepair_v4_finalfix_20260630_1330/kb.faiss.bak
/media/amd/raid1/rag/index/backups/pre_proofrepair_v4_finalfix_20260630_1330/kb_meta.jsonl.bak
```

Finalfix backup hashes:

```text
backup hashes: see backup_hashes_20260630_1330_proofrepair_v4_finalfix.txt
```

Finalfix node22 second status check:

```text
not running port=18080
GPU[0] use: 0%
GPU[1] use: 0%
```

Finalfix smoke query:

```text
e1a0c03e6f574ff4355511a790e54f8fc81014cedb283007176fe1176d53697a ProofRepairRecheck V4 package record node19 desktop
```

returned top hit:

- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md`;
- section `Hashes`, showing the then-final node36 zip hash
  `e1a0c03e6f574ff4355511a790e54f8fc81014cedb283007176fe1176d53697a`.

Finalfix smoke query:

```text
PATCH_PROOFS_THEN_RECHECK report8 proof repair candidate Prop2 Prop3
```

returned top hits including the RAG record, report(8), `STATE.md`, README, the
proof-repair taskbook, `MD_CATALOG.md`, and current proof-repair boundary files.

Finalfix smoke query:

```text
Mode B insufficient_artifact no full panel no training no observed field
```

returned boundary hits that keep Mode B at `insufficient_artifact`; as always,
the direct canonical boundary remains `STATE.md` plus the package record and
adoption notes.

## Finalclean Self-Reference-Safe Refresh

Reason: after finalfix, `STATE.md` and `MD_CATALOG.md` were changed to avoid
embedding exact RAG hashes or chunk counts inside indexed status/catalog text.
This prevents a self-reference loop where the index changes because the indexed
status file tries to certify the index itself.

For exact finalclean scope, chunk count, promoted hashes, build log, and smoke
outputs, use these non-index-authority files:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1350_proofrepair_v4_finalclean.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1350_proofrepair_v4_finalclean.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1350_proofrepair_v4_finalclean.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1350_proofrepair_v4_finalclean.txt
docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1350_proofrepair_v4_finalclean.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1350_proofrepair_v4_finalclean.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1350_proofrepair_v4_finalclean.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalclean_package_record_20260630_1350.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalclean_state_20260630_1350.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalclean_modeb_20260630_1350.txt
```

Finalclean expected locator checks at that stage:

- the then-current `e1a0c03e...` package query should return the v4 package
  record as top hit;
- current-state query should return `STATE.md` with the finalclean
  self-reference-safe wording;
- Mode B query should continue to return `insufficient_artifact` boundary
  hits.

## Post-Finalclean Repack And Finalrepack Clean Locator Refresh

Independent verification then found that the earlier `1303` / `e1a0...` zip
contained pre-finalclean copies of `STATE.md`, `MD_CATALOG.md`, and report(8).
Node36 therefore rebuilt the Pro bundle as a post-finalclean package:

```text
MaoField_PRO_OrderDefect_ProofRepairRecheck_V4_FINAL_20260630_1358.zip
sha256=0285cf2678f149eddf2caaf8ffd94032e3e47b2c3b9d4ebdfe0e3aaaf46d512c
prompt sha256=25b16d9d4f9ca1c160222c31ea1698e7b77b9681c30fb6b17277ee231e515d7b
```

The final package record is:

```text
docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md
```

The package record explicitly supersedes the earlier `1303` zip and records
the final node19 readback hash. The final zip contains 93 non-directory files
and 102 zip entries including directories, passes `unzip -t`, matches the
canonical report(8), `STATE.md`, and `MD_CATALOG.md` snapshots at package-build
time, and contains no checkpoint/model-weight/old-recovery-zip payload.

Finalrepack clean RAG evidence files:

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260630_1415_proofrepair_v4_finalrepack_clean.txt
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260630_1415_proofrepair_v4_finalrepack_clean.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260630_1415_proofrepair_v4_finalrepack_clean.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260630_1415_proofrepair_v4_finalrepack_clean.txt
docs/infra/rag_rebuild_20260622/backup_hashes_20260630_1415_proofrepair_v4_finalrepack_clean.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop_20260630_1415_proofrepair_v4_finalrepack_clean.txt
docs/infra/rag_rebuild_20260622/node22_status_after_stop2_20260630_1415_proofrepair_v4_finalrepack_clean.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalrepack_clean_package_record_20260630_1415.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalrepack_clean_state_20260630_1415.txt
docs/infra/rag_rebuild_20260622/rag_smoke_proofrepair_v4_finalrepack_clean_modeb_20260630_1415.txt
```

Finalrepack clean locator checks:

- final package filename query returns the package record as top hit and shows
  `0285cf2678f149eddf2caaf8ffd94032e3e47b2c3b9d4ebdfe0e3aaaf46d512c`;
- proof-label query returns `ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md`
  as top hit, preserving `PROOF_REPAIR_CANDIDATE` / `CERTIFICATE` /
  `HARNESS_ONLY`;
- Mode B query continues to preserve `insufficient_artifact`.
