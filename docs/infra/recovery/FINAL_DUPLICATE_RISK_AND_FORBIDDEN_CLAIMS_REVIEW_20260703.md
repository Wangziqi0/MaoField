# Final Duplicate-Risk and Forbidden-Claims Review for V2.4

Date verified on node36: 2026-07-03 14:32 CST
Target:
`docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_4_UNDER_LOCK_20260703.tex`

## Verdict

```text
LOCAL_PI_REVIEW_ONLY_PASS_AFTER_PATCHES
PUBLIC_RELEASE_NOT_AUTHORIZED
```

The V2.4 TeX removed the V2.3 lexical risks around `observed ... field`,
`measurement field`, and `Metrics as fields`. It also sets author metadata to
`Yifan Chen`, updates the title, updates bibliography metadata, and preserves
the core status boundary.

## Duplicate Risk

Current duplicate risk:

```text
MEDIUM duplicate risk
```

Do not lower this before public release. The project may say the draft is a
narrow finite illustrative order-defect note. It must not say that no close
work exists or that the note establishes a broad new theory.

## Forbidden-Claim Scan

Command run from the canonical repo:

```bash
rg -n -i "MaoField empirical positive result|broad new ANOVA|broad new dependent-input|broad new .*projection|harness proves|JSON floats prove|observed residual|interaction observed|transport field observed|holonomy field observed|glass box broken|F3 positive|LOSO passed|full panel has run|16-cell aggregate exists|checkpoint loading|\\binference\\b|\\btraining\\b|new loss|MaoField residual observed|quotient-residual observed|completed formal system|preprint-ready|paper-ready|public-postable|submission-authorized|submitted|posted|accepted" docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_4_UNDER_LOCK_20260703.tex
```

Result:

```text
no matches
```

Interpretation: the exact risk phrases above do not occur in the V2.4 TeX.
This is a lexical gate only. It does not replace human mathematical review.

## Required Boundary Text Present

The V2.4 TeX still includes the canonical harness sentence:

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

It also preserves:

- `PROGRAMMATIC_PREPRINT_DRAFT_CANDIDATE_UNDER_LOCK`;
- `MEDIUM duplicate risk`;
- `Mode B MaoField empirical status remains insufficient_artifact`;
- no empirical MaoField positive claim.

## Remaining Blockers Before Public Release

- no local PDF compile was possible on node36 because LaTeX tooling was not
  installed;
- the attached V2.3 PDF is stale after V2.4 source edits and must not be used
  as the final V2.4 PDF;
- human PI must inspect final author list, acknowledgements, title, venue and
  release policy;
- final Pro review must not be treated as proof authority or release
  authority;
- repository visibility/admin status must be checked immediately before any
  public GitHub, Zenodo, OSF, or arXiv action.
