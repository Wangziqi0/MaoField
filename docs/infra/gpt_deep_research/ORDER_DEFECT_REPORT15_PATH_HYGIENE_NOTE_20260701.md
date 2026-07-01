# Order-Defect Report(15) Path Hygiene Note

Date: 2026-07-01 CST
Node: node36
Related report: `docs/infra/gpt_deep_research/deep_research_order_defect_boundary_locked_draft_v10_report15_20260701.md`
Related review: `docs/infra/gpt_deep_research/deep_research_order_defect_draft_candidate_review_v11_report16_20260701.md`

## Issue

Report(16) identified one archival hygiene risk in report(15): report(15)
references a package-external scratch path:

```text
/tmp/orderdefect_v10/rerun/harness.json
```

This is not a stable bundle or canonical repository path. It must not be treated
as durable evidence in future packages or drafts.

## Stable Replacement Evidence

Use canonical or bundle-internal evidence instead:

```text
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
scripts/debranded_residual_transport_harness_v1_3.py
docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md
```

Inside a Pro zip, the corresponding paths should be:

```text
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md
```

## Policy

Do not edit report(15) itself; it is an archived external-model output. Future
adoption notes, package records, prompts, and local drafts should cite the
stable paths above and mention this hygiene note when explaining the correction.
