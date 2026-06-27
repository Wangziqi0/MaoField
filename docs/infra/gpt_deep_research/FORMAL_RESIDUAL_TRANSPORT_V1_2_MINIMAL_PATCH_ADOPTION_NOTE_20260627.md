# Formal Residual Transport v1.2 Minimal Patch Adoption Note

Date: 2026-06-27 CST

Source report:

```text
docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md
```

## Classification

Node36 adopts report (28) as a Mode A claim-source and implementation guide:

```text
v1_2_small_patch_feasible
```

This means Formal v1.2 is feasible as a small finite-dimensional mathematical
patch. It does not mean the formal system is complete, and it does not change
MaoField empirical status.

## Adopted Local Actions

Report (28) required a narrow implementation, not a broad project expansion.
Node36 therefore added:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
scripts/debranded_residual_transport_harness_v1_2.py
docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md
docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json
```

The v1.2 patch closes the report (27)/(28) gaps at synthetic formal-design
level:

1. registered ambient data before stack/spectrum/angle/norm language;
2. squared-capture random-subspace statistic aligned with the Beta law;
3. product-weight Hoeffding equivalence theorem under exact product weights;
4. finite per-edge telescoping identity for square holonomy defects;
5. single-source threshold contract with central pass/fail evaluation.

## Verification

The v1.2 harness was run from node36 SSD scratch:

```text
/home/amd/codex-node36/tmp/maofield-formal-v12-impl-20260627_1255/
```

Validation commands:

```text
PYTHONPYCACHEPREFIX=/home/amd/codex-node36/tmp/maofield-formal-v12-impl-20260627_1255/pycache \
  /home/amd/venv/bin/python -m py_compile scripts/debranded_residual_transport_harness_v1_2.py

/home/amd/venv/bin/python scripts/debranded_residual_transport_harness_v1_2.py \
  --out /home/amd/codex-node36/tmp/maofield-formal-v12-impl-20260627_1255/out/synthetic_harness_v1_2_20260627.json \
  --summary-md /home/amd/codex-node36/tmp/maofield-formal-v12-impl-20260627_1255/out/SYNTHETIC_HARNESS_V1_2_20260627.md \
  --json-rel docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json

/home/amd/venv/bin/python -m json.tool \
  /home/amd/codex-node36/tmp/maofield-formal-v12-impl-20260627_1255/out/synthetic_harness_v1_2_20260627.json
```

Result:

```text
all_synthetic_controls_passed=true
block_count=12
threshold_contract_sha256=0bb99a4a711405fb65e81413cfd283d6e68d0ecd4e9c34dc027c052f332110e0
```

## Evidence Boundary

The strongest local verdict remains:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

This adoption does not authorize or imply:

```text
full panel has run
16-cell full-panel aggregate exists
MaoField residual field observed
MaoField interaction field observed
MaoField quotient-residual field observed
MaoField transport field observed
MaoField holonomy field observed
glass box broken
F3 positive
LOSO passed
checkpoint loading
model inference
training
new loss
completed formal system
```

## Next Correct Pro Task

The next GPT-5.5 Pro task should not repeat report (28)'s design pass. It
should perform a strict implementation audit of Formal v1.2:

- verify the note definitions and theorem statements;
- check the square-holonomy telescoping formula against the script;
- check squared-capture/Beta closure and product-weight boundaries;
- inspect the single-source threshold contract;
- decide whether local v1.2 is `formal_v1_2_patch_accepted`,
  `formal_v1_2_patch_requires_minor_revision`,
  `formal_v1_2_patch_requires_major_revision`, or
  `insufficient_artifact_for_v1_2_implementation_audit`.
