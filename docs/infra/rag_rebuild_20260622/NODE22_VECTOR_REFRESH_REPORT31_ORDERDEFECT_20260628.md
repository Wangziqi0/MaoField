# Node22 Vector Refresh — Report(31) / Formal v1.3 Order-Defect Proof Audit

Superseded: this 16:05 refresh was an intermediate report(31) pass. It is kept
as provenance, but the current final report(31) RAG record is:

```text
NODE22_VECTOR_REFRESH_REPORT31_FINAL_20260628.md
```

Reason: after this index was promoted, `STATE.md` and the node19 package were
corrected to the `1734final` snapshot. The final RAG pass indexes that corrected
STATE/package context.

Date: 2026-06-28 CST
Authority: node36
Temporary vector worker: node22

## Scope

This refresh promotes the report (31) guarded adoption materials and the Formal
v1.3 order-defect proof-audit prompt/package metadata into the default node36
RAG locator.

Primary additions before the final build included:

- `deep_research_formal_residual_transport_v1_3_theorem_strengthening_plan_20260628.md`;
- `FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md`;
- `FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md`;
- `GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md`;
- `README_FOR_PRO_FORMALV13_ORDER_DEFECT_PROOF_20260628.md`;
- `DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_FORMALV13_ORDER_DEFECT_PROOF_20260628.md`;
- updated `STATE.md`, `MD_CATALOG.md`, `GPT55_PRO_RESEARCH_INDEX_20260622.md`,
  and current README/navigation files.

## Method

Node36:

- generated file inventory and digest under SSD scratch first;
- generated canonical active markdown scope;
- chunked markdown, wrote FAISS and metadata, and verified/promoted the final
  index;
- retained scope, logs, hashes, and smoke results under
  `docs/infra/rag_rebuild_20260622/`.

Node22:

- ran a temporary llama.cpp bge-m3 embedding HTTP worker only;
- did not own scope, manifests, promotion, or final verification;
- was stopped after use.

Final node22 worker status:

```text
stopped pid=2457896
not running port=18080
```

## Final Promoted Index

```text
active canonical markdown files: 427
chunks: 10064
kb.faiss sha256=ff20bd2885908a599dce3d4c05fc71c161435f3db916c1556fdd9a6c016b5a82
kb_meta.jsonl sha256=c55fa3d37bbbea2fa06baff4652722f7e64ee74615bb2787f04895ed1eb5ffe9
canonical scope sha256=f06c5cc70e226829ecd63b59283a00c35700483a47b83d295171f009e3a9d70d
```

Candidate build stats:

```text
files=427
chunks=10064
embedding endpoint=http://192.168.31.22:18080
embedding model=bge-m3-temp
embedding rate=95.894 text/s
```

Final artifacts promoted to `/media/amd/raid1/rag/index`:

```text
/media/amd/raid1/rag/index/kb.faiss
/media/amd/raid1/rag/index/kb_meta.jsonl
```

Pre-refresh backups:

```text
/media/amd/raid1/rag/index/kb.faiss.bak_pre_20260628_1605_report31orderdefect
/media/amd/raid1/rag/index/kb_meta.jsonl.bak_pre_20260628_1605_report31orderdefect
```

## Logs And Manifests

```text
docs/infra/rag_rebuild_20260622/canonical_scope_active_20260628_1605_report31orderdefect.txt
docs/infra/rag_rebuild_20260622/rag_scan_20260628_1605_report31orderdefect.log
docs/infra/rag_rebuild_20260622/rag_build_node22_candidate_20260628_1605_report31orderdefect.log
docs/infra/rag_rebuild_20260622/candidate_hashes_20260628_1605_report31orderdefect.txt
docs/infra/rag_rebuild_20260622/promoted_hashes_20260628_1605_report31orderdefect.txt
docs/infra/rag_rebuild_20260622/rag_smoke_report31_orderdefect_20260628_1605_report31orderdefect.txt
docs/infra/rag_rebuild_20260622/rag_smoke_state_report31_20260628_1605_report31orderdefect.txt
docs/infra/rag_rebuild_20260622/rag_smoke_package_report31_20260628_1605_report31orderdefect.txt
```

## Smoke Queries

The first smoke query:

```text
D628 report31 Formal v1.3 order defect product non-product weight boundary proof audit
```

returned top hits including:

- `MD_CATALOG.md`;
- `FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md`;
- `docs/infra/debranded_residual_transport/README.md`;
- `FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md`;
- `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- `STATE.md`.

The second smoke query:

```text
node19 desktop OrderDefectProof Report31 insufficient_artifact no full panel no training
```

returned top hits including:

- `STATE.md` with the node19 desktop package, zip hash, prompt hash, and
  `insufficient_artifact` boundary;
- `MD_CATALOG.md` with the guarded report (31) adoption and forbidden-upgrade
  boundaries.

The third smoke query:

```text
DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_FORMALV13_ORDER_DEFECT_PROOF zip sha256 prompt sha256
```

returned the package record in the top results:

- `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_FORMALV13_ORDER_DEFECT_PROOF_20260628.md`.

## Evidence Boundary

RAG is a locator only. Claims still require primary files, code, JSON/JSONL,
logs, verdicts, or formal proofs. This refresh does not authorize full-panel,
training, new-loss, observed-field, glass-box, F3/LOSO-positive, or
completed-formal-system claims. Report (31) remains a guarded proof-audit plan,
not a completed theorem.
