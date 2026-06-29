# README For GPT-5.5 Pro -- Order-Defect Paper Draft v1.6

Date: 2026-06-29 CST
Package target: GPT-5.5 Pro zero-context paper-drafting gate
Project container: MaoField, Mode A debranded finite-dimensional mathematics

## Purpose

This package follows the v1.5 final-gate audit.  That audit did not reject the
math core or the bibliography floor; it held the short-note gate because the
harness boundary sentence had not been written verbatim across the requested
artifacts.

The v1.6 local cleanup is intentionally small:

- canonicalize the harness sentence across README, placeholder, harness
  markdown, harness JSON, and harness script;
- rerun the deterministic harness under node36 SSD scratch;
- preserve the finite weighted two-way table scope;
- prepare a gate-conditioned GPT-5.5 Pro prompt that drafts a short note only
  after the wording and evidence gates pass.

## Canonical Harness Sentence

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

## Evidence Boundary

This is not MaoField empirical validation. It does not authorize:

- checkpoint loading;
- inference;
- training;
- full-panel generation;
- a new loss;
- claims that any MaoField residual / interaction / quotient-residual /
  transport / holonomy field has been observed.

Allowed local ceiling:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical state:

```text
insufficient_artifact
```

## Primary Files

```text
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/debranded_residual_transport/README.md
from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_5_final_gate_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_ADOPTION_NOTE_20260629.md
```

Use the standalone prompt in:

```text
prompt/GPT55_PRO_ORDER_DEFECT_PAPER_DRAFT_V16_PROMPT_20260629.md
```

The prompt is gate-conditioned.  If the wording or evidence gate fails, Pro
must not write the paper.
