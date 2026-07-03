# Formal Preprint V2.2 Strict Review Report23 Adoption Note

Date: 2026-07-03

Source report: `docs/infra/gpt_deep_research/deep_research_formal_preprint_v2_2_strict_review_report23_20260703.md`

Source attachment SHA256:

```text
ce1375ed6b9d3442b273cf4c6461a5ce9c3ce5a2953dd522d26040ad67edb84b
```

Archived normalized report SHA256:

```text
93a56bd586cdd4ba7bc02d5e9406fd61518069d630517aecbf5563dbee8cc318
```

## External Verdict

```text
REQUEST_BOUNDARY_WORDING_PATCH_BEFORE_PI_REVIEW
```

## Node36 Adoption

Adopt narrowly.

Report23 is accepted as a strict review of the V2.2 formal preprint draft package.
It does not authorize public posting, preprint submission, paper-ready status,
proof-authority promotion, bibliography finality, or any Mode B empirical
upgrade.

## Accepted Findings

- The finite positive weighted two-way-table theorem statements and proofs in
  the V2.2 TeX draft are accepted by the reviewer as locally correct under the
  stated assumptions.
- The exact 2 x 2 rational witness arithmetic, including
  `||R_{Q->B}K||_w^2 = 61/177408`, is accepted as consistent with the package.
- The canonical floating-point harness boundary sentence is present in the
  draft.
- The internal duplicate-risk status remains `MEDIUM duplicate risk`.
- No positive MaoField empirical claim is authorized.

## Required Patch Adopted

The V2.2 TeX draft must state the package-global Mode B boundary explicitly:

```text
Mode B MaoField empirical status remains insufficient_artifact; accordingly,
no MaoField empirical positive claim is made or authorized anywhere in this
draft.
```

This is a boundary patch only. It does not change the mathematical claim.

## Bibliography / Spelling Patch Adopted

- Update the Lamboni reference wording to include the title subtitle and
  journal name while keeping the publisher-online / DOI-record caveat.
- Align the package spelling of Boettcher/Spitkovsky between the current TeX
  draft and the current positioning file. Historical reports are not rewritten.

## Antithesis Wording Cleanup

The local antithesis review also flagged status and scope leakage that was
adjacent to, but not identical with, report23's required Mode B patch. The
following cleanup is adopted:

- replace the title phrase `Minimal Obstructions` with a non-minimality title;
- replace affiliation status `preprint candidate, local version` with `local
  draft candidate under lock`;
- replace `The paper makes` with `This note makes`.

These edits are claim-boundary edits only. They do not add a mathematical
claim, release claim, or empirical claim.

## Current Action After Patch

```text
FORMAL_PREPRINT_DRAFT_BOUNDARY_PATCHED_UNDER_LOCK
```

The next allowed decision is PI/local final review under lock. The project
still must not claim:

- paper-ready or preprint-ready status;
- public posting, submission, acceptance, or release authorization;
- broad new ANOVA, dependent-input decomposition, or projection theory;
- MaoField empirical positive results;
- full panel, checkpoint inference, training, new loss, F3 positive, LOSO
  passed, glass-box breakage, or observed residual/interaction/transport/
  holonomy fields;
- theorem proof by JSON floats or deterministic harness output.
