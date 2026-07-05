# MaoField D705 Two-Chart Glue Certificate Taskbook

Date verified on node36: 2026-07-05 12:29:43 CST

## Task

Prepare the next GPT-5.5 Pro package after Report27. The package must carry
Report27's decision:

```text
DESIGN_TWO_CHART_GLUE_CERTIFICATE
```

This taskbook is a handoff for PI decision and next Pro review. It does not
authorize node36 to implement the certificate until the PI chooses that branch.

## Goal

Ask Pro to perform a strict implementation-gate review for a minimal exact
rational two-chart gluing obstruction certificate:

```text
Obs_12(s_1, s_2)
```

The primitive input is two local sections. A global-source `Obs_12(K)` subtype
may be added later only after extraction maps and local section maps are
declared.

## Required Inputs

The package must include:

- Report27 archive and adoption note;
- Report26 and Report25 provenance;
- current `STATE.md`, `MD_CATALOG.md`, `AGENTS.md`, and `CLAUDE.md`;
- the metric-identity programme note;
- finite order-defect formal note, exact 2x2 witness, exact witness
  script/JSON, and deterministic harness v1.3;
- older residual transport / holonomy / gluing notes and scripts as historical
  scaffolding;
- node36 request-result sidecars from Report26;
- current RAG rebuild records and smoke outputs;
- forbidden-claim and duplicate-risk guardrails.

## Pro Must Decide

Pro must choose exactly one:

```text
APPROVE_IMPLEMENT_TWO_CHART_CERTIFICATE
PATCH_DEFINITION_BEFORE_IMPLEMENTATION
ADD_PRODUCT_AND_OI_COMPANION_CONTROLS_FIRST
REQUEST_NODE36_FILES
STOP_BRANCH_INSUFFICIENT_RIGOR
```

## Candidate Implementation

If approved, node36 should create only bounded exact rational artifacts:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_TWO_CHART_GLUE_CERTIFICATE_20260705.md
scripts/debranded_residual_transport_exact_glue_certificate_v1_5.py
docs/infra/debranded_residual_transport/exact_glue_certificate_v1_5_20260705.json
docs/infra/debranded_residual_transport/EXACT_GLUE_CERTIFICATE_V1_5_20260705.md
```

## Required Exact Controls

Use a 2x2 overlap in row-major order:

```text
(q1,b1), (q1,b2), (q2,b1), (q2,b2)
```

Use positive rational uniform overlap weights:

```text
(1/4, 1/4, 1/4, 1/4)
```

Use additive overlap gauge:

```text
Gamma_12 = N_add(O_12) = span{1, q-centered, b-centered}
```

Controls:

```text
m_plus  = (1, 2, 3/2, 5/2) -> Obs^2 = 0
m_minus = (1, -1, -1, 1)    -> Obs^2 = 1
```

## Construction Constraints

- Zero GPU.
- Exact rational arithmetic via `fractions.Fraction`.
- JSON rational strings only for exact data.
- Positive and negative controls must be fail-closed.
- Any float harness is regression support only.
- No broad sheaf, holonomy, ANOVA, dependent-input, or projection theory.
- No empirical MaoField upgrade.

## Forbidden Outputs

Pro must not draft a paper body in this round.

Pro must not claim:

- MaoField empirical positive evidence;
- observed residual/transport/holonomy/gluing field;
- broad ANOVA, sheaf, holonomy, dependent-input, or projection theory;
- training, inference, new loss, full panel, F3-positive, LOSO-passed, or
  checkpoint result;
- that JSON floats or deterministic harnesses prove a theorem.

## Node36 Follow-Up After Pro

If Pro returns `APPROVE_IMPLEMENT_TWO_CHART_CERTIFICATE`, node36 can implement
the four bounded exact artifacts above, run exact assertions, update RAG and
`STATE.md`, then commit from node36 only.

If Pro returns any blocker, node36 must record the blocker and avoid
implementation until PI chooses a branch.
