# Open-MaoField Public Repository Seed

Date verified on node36: 2026-07-03 15:35 CST

## Repository

```text
https://github.com/Wangziqi0/Open-MaoField
```

Public repository commit pushed from node36:

```text
8c3cfaf seed public order-defect draft
```

Repository description set by `gh repo edit`:

```text
Public sanitized research surface for black-box LLM evaluation via finite-dimensional residual metric audits and exact projection order-defect certificates.
```

## Purpose

`Open-MaoField` is the public sanitized release surface. It is not a mirror of
the private canonical MaoField repository and does not contain the private git
history, `STATE.md`, RAG indexes, handoff files, checkpoints, model weights,
raw empirical pilot data, or old recovery bundles.

## Included Public Files

```text
README.md
LICENSE
CITATION.cff
MANIFEST.sha256
paper/preprint.tex
paper/README.md
certificate/exact_witness_certificate.py
certificate/exact_witness_v1_4_20260629.json
harness/deterministic_harness.py
harness/synthetic_harness_v1_3_20260628.json
docs/claim_boundary_note.md
docs/duplicate_risk_note.md
docs/release_notes_v0.1.md
```

## Checks Run Before Push

Exact witness rerun:

```text
all_checks_passed=True
json_sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
```

The generated exact JSON matched the included public JSON byte hash.

Harness rerun:

```text
all_synthetic_controls_passed=True
```

The harness JSON hash is not expected to remain byte-stable across reruns
because the script records runtime metadata such as UTC timestamp, Python
version, NumPy version and platform. This does not promote JSON floats into
proof evidence.

Forbidden-claim scan:

```text
/home/amd/codex-node36/tmp/open_maofield_public_seed_20260703/public_seed_forbidden_scan_v3.txt
```

Result: no positive public claim was found for full-panel execution, empirical
MaoField success, deployed-model residual/interaction/transport/holonomy
measurements, glass-box success, F3/LOSO success, broad ANOVA/dependent-input
theory, JSON-float proof, or harness proof. Remaining hits are boundary strings
inside the public scripts/JSON, e.g. blocked/forbidden interpretation fields.

## Current Release Boundary

Published to public GitHub main:

```text
YES
```

Created GitHub Release:

```text
NO
```

Created Zenodo DOI:

```text
NO
```

Compiled V2.4 PDF:

```text
NO
```

Reason: node36 did not have a local LaTeX toolchain during this seed export.
The public repository currently carries TeX source, exact certificate, harness
and boundary documentation only.

## Safe Public Position

This is a public sanitized draft surface for the finite order-defect note and
its reproducibility artifacts. It is not an arXiv submission, not a Zenodo DOI
release, not a journal submission, not a public copy of canonical MaoField, and
not an empirical MaoField positive result.
