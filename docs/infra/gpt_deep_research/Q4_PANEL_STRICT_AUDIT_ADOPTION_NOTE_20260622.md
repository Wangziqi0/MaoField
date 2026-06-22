# Q4 Panel Strict Audit Adoption Note

> Node36 adoption note for
> `deep_research_q4_panel_strict_audit_20260622.md`.
> Classification: canonical interpretation of a GPT/PRO claim-source, not a
> new experiment result.

## Boundary

Report (6) directly inspected the uploaded q4 panel bundle rather than public
GitHub. Its repository-file observations are therefore usable as a bundle
audit, but the bundle remains a claim-source until node36 reproduces or updates
the relevant local artifacts.

The current project verdict does not change:

```text
aggregate verdict = insufficient_artifact
math turn status  = blocked-until-gated
full panel        = not approved
```

2026-06-22 21:43 CST update: fail-fast negative smokes now pass for expected
schema hash mismatch, expected builder hash mismatch, wrong source split,
source hash mismatch, and q4 bin-size mismatch; wording guard also passes.

2026-06-22 21:49 CST update: multi-checkpoint smoke now covers seed1/gen0,
seed2/gen5, and seed42/gen9. All three reproduce old aggregate rows. This is
still generator-alignment evidence only, not a full panel.

## Adopt

- Do not approve full 50-checkpoint q4 panel generation yet.
- Treat the existing q4 schema lock plus manifest-only and seed1/gen0 smoke as
  generator-alignment evidence only.
- Before any full panel run, require:
  - manifest provenance fields including `builder_script_sha256`;
  - a clean account of artifact-generation commit versus recording commit;
  - fail-fast negative smokes for schema/source/split wording gates (done);
  - a separate q4 full-panel analysis script with fold-local LOSO, pairing,
    projection, and control gates.

## Deflate

- q4 is an exploration-aware prospective lock, not a pristine confirmatory
  preregistration.
- The ordered q4 frequency-slope projection is a locked diagnostic carrier,
  not a theory-derived proof object.
- A future 5 seed x 10 generation panel is within-regime diagnostic evidence,
  not 50 independent replications.

## Reject

- Do not repair the q8 empty bin or promote q8 to primary.
- Do not promote old rare/freq masks or any unregistered projection to primary.
- Do not state `LOSO passed`, `F3 positive`, `mean-null vector field survives`,
  `glass box broken`, `training authorized`, or `new loss authorized`.
- Do not call the fixed Wikitext-2 train audit blocks validation/test/eval data.

## Adopted Next Sentence

The q4 locked schema, one-checkpoint smoke, fail-fast negative smokes, and
multi-checkpoint smoke coverage are aligned enough to continue full-panel
implementation review, but not enough to run the full panel. The next local
work is full-panel generator mode plus a separate fold-local q4 analysis path;
only after those are reviewed should PI/PRO decide whether to launch the
50-checkpoint generation.
