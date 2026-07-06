# Node22 Vector Refresh -- D706 Report29 Final Sync

Date verified on node36: 2026-07-06 14:05 CST

Status:

```text
FINAL_SYNC_RECORD_CREATED_BEFORE_VECTOR_BUILD
```

This is the final RAG-sync record for the D706 report29 adoption round. It is
written before the vector build so that the record itself, the updated
`STATE.md`, the updated `MD_CATALOG.md`, the report29 archive, the adoption
note, the README cross-index, and the Gram-inverse script cleanup are all
discoverable in the promoted index.

To avoid self-referential hash drift, exact live hashes, line counts, scope
counts, candidate verification, node22 start/stop logs, and smoke output are
stored in non-Markdown sidecars with this tag:

```text
20260706_1408_report29_final_sync
```

Canonical sidecar pattern:

```text
docs/infra/rag_rebuild_20260622/*_20260706_1408_report29_final_sync.*
```

Required final checks for this sync:

- node22 is used only as a temporary embedding worker;
- node36 owns scope, build logs, verification, promotion, and smoke queries;
- node22 temporary service is stopped after use;
- smoke must locate report29, its adoption note, the separate-exact-note
  verdict, and the no-current-V2.5-preprint-patch boundary.

RAG remains a locator only. Proof authority remains in the formal note, exact
script, exact JSON/Markdown certificate, and local script output.

## Claim Boundary

This refresh supports discovery of the report29 adoption and GQ-FCR separate
exact-note boundary only. It does not authorize:

- current Zenodo V2.5 preprint patching;
- broad sheaf theory;
- broad consistency-radius theory;
- broad contextuality theory;
- broad dependent-input ANOVA theory;
- broad noncommuting projection theory;
- MaoField empirical positive claims;
- full panel, checkpoint loading, inference, training, or new loss;
- observed residual, transport, holonomy, or gluing fields;
- proof-by-JSON or proof-by-deterministic-harness wording.

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```
