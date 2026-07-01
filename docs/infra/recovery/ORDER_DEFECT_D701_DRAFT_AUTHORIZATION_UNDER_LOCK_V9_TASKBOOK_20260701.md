# Order-Defect D701 Draft Authorization Under Lock V9 Taskbook

Date: 2026-07-01 CST
Authority: node36

## Goal

Create a zero-context V9 bundle for GPT-5.5 Pro after report(13).

Report(13) returned:

```text
HUMAN_DECISION_UNDER_LOCK_ACCEPTED
```

Node36 adopts it only as:

```text
ASK_PI_FOR_SEPARATE_DRAFT_AUTHORIZATION_UNDER_LOCK
```

The V9 question is:

```text
Should the human PI authorize a separate future boundary-locked short-note
drafting prompt, or should node36 patch proof/bibliography/package/status first?
```

This is an authorization-gate task, not a paper-drafting task.

## Current Verdict Chain

```text
report(12): POST_V6_DECISION_GATE_ACCEPTED_KEEP_LOCK
report(13): HUMAN_DECISION_UNDER_LOCK_ACCEPTED
node36 local action: ASK_PI_FOR_SEPARATE_DRAFT_AUTHORIZATION_UNDER_LOCK
node36 live state: LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
overall: KEEP_LOCK_AND_FIX
paper body: LOCKED_NO_PAPER_BODY
Mode B: insufficient_artifact
```

## Required Bundle Contents

The V9 zip must include:

- `PACKAGE_README.md`;
- `SHA256SUMS.txt`;
- `PACKAGE_FILE_MANIFEST.sha256`;
- `STATE.md`;
- `MD_CATALOG.md`;
- project `AGENTS.md`, `CLAUDE.md`, and `GPT55_PRO_RESEARCH_INDEX_20260622.md`;
- report(13) raw report and adoption note;
- report(12) raw report and adoption note;
- V8 taskbook, prompt, and package record;
- report(11), report(10), and report(9) provenance chain with adoption notes;
- V4, V5, V6, V7, and V8 package records as provenance/current identity;
- V9 taskbook, prompt, and package record;
- core formal note and proof-repair candidate;
- exact rational witness Markdown, JSON, and script;
- deterministic harness Markdown, JSON, and script;
- bibliography/positioning;
- wording lock and forbidden-claim scan;
- recovery audits from `docs/infra/recovery/`;
- relevant RAG refresh records and sidecars needed to understand locator status.

The V9 zip must not include checkpoint/model weights, raw full-panel data,
large old recovery zips, training/inference payloads, or any paper-body draft.

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
DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED
PATCH_PROOF_BIBLIO_OR_PACKAGE_BEFORE_AUTHORIZATION
STOP_DO_NOT_DRAFT
INSUFFICIENT_BUNDLE
```

If it returns `DRAFT_AUTHORIZATION_UNDER_LOCK_ACCEPTED`, it may provide:

- a PI decision memo;
- a precise allowed-claims ledger;
- a precise forbidden-claims ledger;
- residual risks;
- exact constraints for a later, separate drafting prompt.

It must not write the short note or any publishable paper prose.

## Forbidden Pro Output

GPT-5.5 Pro must not:

- draft abstract, introduction, theorem exposition, proof prose, or paper body;
- say paper-ready, preprint-ready, posted, or emergency-lock lifted;
- turn deterministic harness or JSON floats into proof;
- upgrade exact witness beyond `CERTIFICATE`;
- upgrade bibliography beyond local draft with medium duplicate risk;
- upgrade Mode B beyond `insufficient_artifact`;
- claim full panel, checkpoint inference, training, new loss, observed field,
  F3, LOSO, glass-box, or completed formal system;
- introduce new broad theory or new theorem statements not already carried by
  the controlled local draft object.

## Exit Criteria

V9 package is complete only if:

1. `unzip -t` passes;
2. internal `sha256sum -c SHA256SUMS.txt` passes;
3. node19 readback matches node36 scratch hashes;
4. RAG is refreshed with node22 one-shot vector worker, then node22 is stopped;
5. smoke queries locate report(13), V9 prompt, V9 package record, and boundary
   wording;
6. the independent audit thread returns no blocker.
