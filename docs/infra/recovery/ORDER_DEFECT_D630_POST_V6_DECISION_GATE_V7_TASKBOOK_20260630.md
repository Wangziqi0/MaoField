# Order-Defect D630 Post-V6 Decision Gate V7 Taskbook

Date: 2026-06-30 CST
Authority: node36

## Goal

Create a zero-context V7 bundle for GPT-5.5 Pro that starts from report(11)'s
V6 metadata/label acceptance and asks for a narrow decision-gate audit.

The question is not "write the paper." The question is:

```text
After V6 metadata/label/package-identity closure, is there any remaining
proof, bibliography, package, status, or forbidden-claim blocker that should
prevent a human from deciding whether to prepare a short-note draft under the
emergency lock?
```

## Current Verdict Chain

```text
report(10): PATCH_METADATA_OR_LABELS_AGAIN
report(11): METADATA_LABEL_PATCH_ACCEPTED_KEEP_LOCK
node36 live state: LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
overall: KEEP_LOCK_AND_FIX
paper body: LOCKED_NO_PAPER_BODY
Mode B: insufficient_artifact
```

## Required Bundle Contents

The V7 zip must include:

- `PACKAGE_README.md`;
- `SHA256SUMS.txt`;
- `PACKAGE_FILE_MANIFEST.sha256`;
- `STATE.md`;
- `MD_CATALOG.md`;
- project `AGENTS.md`, `CLAUDE.md`, and `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- report(11) raw report and adoption note;
- report(10) raw report and adoption note;
- report(9) erratum, raw report, adoption note, taskbook, and local
  verification;
- V4, V5, V6, and V7 package records;
- core formal note and proof-repair candidate;
- exact rational witness Markdown, JSON, and script;
- deterministic harness Markdown, JSON, and script;
- bibliography/positioning;
- wording lock and forbidden-claim scan;
- recovery audits from `docs/infra/recovery/`;
- relevant RAG refresh records and sidecars needed to understand locator
  status.

The V7 zip must not include checkpoint/model weights, raw full-panel data,
large old recovery zips, or training/inference payloads.

## Correct Live Labels

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall paper status: LOCKED_NO_PAPER_BODY
Mode B MaoField empirical status: insufficient_artifact
```

## Allowed Pro Output

GPT-5.5 Pro may return exactly one of:

```text
POST_V6_DECISION_GATE_ACCEPTED_KEEP_LOCK
PATCH_PROOF_OR_BIBLIO_BEFORE_DECISION
PATCH_PACKAGE_OR_STATUS_BEFORE_DECISION
DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT
```

## Forbidden Pro Output

GPT-5.5 Pro must not:

- draft abstract, introduction, theorem exposition, or paper body;
- say paper-ready, preprint-ready, posted, or emergency-lock lifted;
- turn deterministic harness or JSON floats into proof;
- upgrade exact witness beyond certificate;
- upgrade bibliography beyond local draft with medium duplicate risk;
- upgrade Mode B beyond `insufficient_artifact`;
- claim full panel, checkpoint inference, training, new loss, observed field,
  F3, LOSO, glass-box, or completed formal system.

## Exit Criteria

V7 package is complete only if:

1. `unzip -t` passes;
2. internal `sha256sum -c SHA256SUMS.txt` passes;
3. node19 readback matches node36 scratch hashes;
4. RAG is refreshed with node22 one-shot vector worker, then node22 is stopped;
5. smoke queries locate report(11), V7 prompt, V7 package record, and boundary
   wording;
6. an independent audit thread returns no blocker.
