# Order-Defect v1.4 Exact/Bibliography Audit — Adoption Note

Date: 2026-06-29 CST
Node: node36 canonical MaoField
Source report:
`docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md`
Attachment sha256:
`2dd42dbd323e21e54b730e90d38e58402f521077a8d0f89de1f8b2a5f6acbccc`

## Local Adoption Verdict

```text
math_core_pass_but_preprint_requires_minor_bibliography_or_wording_fixes
posting_decision=revise_first
```

The report is adopted as a strict claim-source audit of the v1.4
exact/bibliography package. It does not create MaoField empirical evidence and
does not authorize training, checkpoint loading, full-panel generation, or a new
loss.

## Accepted

The following items are accepted as the report's useful findings:

- The exact rational appendix/certificate passes the Pro audit:
  `exact_fraction_certificate=PASS`.
- The exact projection matrix dump passes:
  `exact_projection_matrix_dump=PASS`.
- v1.4 did not silently alter the v1.3 T1/T2/T3 proof boundary:
  `T1_T2_T3_unchanged_after_edits=PASS`.
- Evidence boundary remains intact:
  `definitions_and_harness_viable_only` and Mode B
  `insufficient_artifact`.
- No exact duplicate was identified by the report, but the nearby literature is
  dense enough that the note must keep a very narrow contribution claim.

## Remaining WARN Items

The local revision target is not more mathematics first; it is publication
positioning and boundary cleanup:

1. Make bibliography and novelty positioning durable, including Lamboni 2026
   DOI `10.1137/24M1712680`.
2. Make the harness boundary uniform across markdown, JSON, and source script:

```text
The floating-point harness is deterministic regression support only; the
mathematical claims are carried by the analytic proof and exact rational
certificate, not by JSON floats.
```

3. Replace project-internal wording such as "diagnostic field" or broad
   "stable non-additive field" language with finite weighted two-way table /
   finite weighted two-way array language.
4. Keep the novelty sentence at:

```text
a compact finite weighted projection-order artifact note with an exact 2 x 2 witness
```

## Local Actions Taken

- Archived the raw Pro report while preserving its attachment hash.
- Added a local DOI/arXiv-backed bibliography and positioning record:
  `docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`.
- Updated the preprint placeholder with the final safety sentence:
  not a new dependent-input ANOVA or Hoeffding decomposition theory.
- Updated the v1.3 harness script boundary so regenerated JSON/summary records
  explicitly state that the analytic proof and exact rational certificate carry
  the mathematical claims.
- Updated the debranded residual transport README to point the next Pro pass at
  a v1.5 final-gate check rather than a roadmap pass.

## Rejected Upgrades

Do not claim:

- preprint posted;
- ready without fixes;
- broad new ANOVA theory;
- broad new dependent-input decomposition theory;
- broad new noncommuting projection theory;
- completed formal system;
- MaoField empirical positive result;
- observed MaoField residual / interaction / quotient-residual / transport /
  holonomy field;
- full panel completion, 16-cell aggregate, LOSO pass, F3 positive, glass-box
  breakage, checkpoint inference, training, or new-loss authorization.

## RAG State

The default MaoField RAG locator still trails the newest D629 files unless a
node22 one-shot vector refresh is run. RAG may locate older context, but it is
not evidence. For this report and the v1.5 fixes, use the direct paths above
until a refresh record is promoted.
