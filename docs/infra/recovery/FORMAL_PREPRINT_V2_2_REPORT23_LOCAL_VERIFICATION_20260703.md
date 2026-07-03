# Formal Preprint V2.2 Report23 Local Verification

Date: 2026-07-03
Node: node36
Scratch: `/home/amd/codex-node36/tmp/formal_preprint_report23_20260703/`

## Scope

This local verification follows Pro report23 and the two local subagent
reviews. It checks only the local V2.2 draft and supporting scripts after the
boundary patch. It is not release, posting, submission, or preprint-ready
authorization.

## Source Report

```text
docs/infra/gpt_deep_research/deep_research_formal_preprint_v2_2_strict_review_report23_20260703.md
source attachment sha256: ce1375ed6b9d3442b273cf4c6461a5ce9c3ce5a2953dd522d26040ad67edb84b
archived normalized sha256: 93a56bd586cdd4ba7bc02d5e9406fd61518069d630517aecbf5563dbee8cc318
verdict: REQUEST_BOUNDARY_WORDING_PATCH_BEFORE_PI_REVIEW
```

## Applied Local Patches

- Added explicit Mode B boundary to the TeX draft:
  `Mode B MaoField empirical status remains insufficient_artifact; accordingly,
  no MaoField empirical positive claim is made or authorized anywhere in this
  draft.`
- Removed title/status leakage flagged by antithesis review:
  `Minimal Obstructions` -> `Finite Projection Order Defects`; affiliation now
  says `local draft candidate under lock`; `The paper makes` -> `This note
  makes`.
- Updated Lamboni bibliography wording while preserving the
  `publisher online record / DOI record` caveat.
- Aligned current-package `Boettcher` spelling between the TeX draft and the
  current positioning file.

## Exact Witness Check

Command run from canonical repo with output under SSD scratch:

```bash
python3 scripts/debranded_residual_transport_exact_witness_v1_4.py \
  --out-dir /home/amd/codex-node36/tmp/formal_preprint_report23_20260703/exact
```

Result:

```text
all_checks_passed=True
json_sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
```

The exact witness remains the certificate-level example. JSON output is a
reproducibility artifact, not a proof substitute.

## Harness Check

Command:

```bash
python3 scripts/debranded_residual_transport_harness_v1_3.py \
  --out /home/amd/codex-node36/tmp/formal_preprint_report23_20260703/harness/synthetic_harness_v1_3_20260628.json \
  --summary-md /home/amd/codex-node36/tmp/formal_preprint_report23_20260703/harness/SYNTHETIC_HARNESS_V1_3_20260628.md
```

Result:

```text
all_synthetic_controls_passed=True
```

The floating-point harness remains deterministic regression support only; the
mathematical claims are carried by the analytic proof and exact rational
certificate, not by JSON floats.

## Boundary Scan

Scan output:

```text
/home/amd/codex-node36/tmp/formal_preprint_report23_20260703/scan/tex_boundary_scan.txt
```

Matches after patch:

```text
41:This document is a local draft candidate under lock. It is not paper-ready,
42:preprint-ready, public-postable, submitted, accepted, or submission-authorized.
```

No positive `Minimal Obstructions`, `preprint candidate`, `The paper makes`,
`glass box`, `F3 positive`, `LOSO passed`, `full panel has run`, `training`,
`new loss`, `JSON floats prove`, `harness proves`, or `broad new` matches were
found in the TeX draft.

## Compile Status

No local LaTeX compiler was found via:

```bash
command -v latexmk
command -v pdflatex
command -v tectonic
```

Therefore no PDF compile result is claimed in this verification.

## Local Verdict

```text
PI_FINAL_LOCAL_REVIEW_UNDER_LOCK_ALLOWED_AFTER_COMMIT
```

This means only that the report23 boundary blocker and antithesis wording
leaks have been locally patched. It still does not authorize public posting,
preprint submission, paper-ready status, bibliography finality, proof-authority
promotion, or Mode B empirical upgrade.
