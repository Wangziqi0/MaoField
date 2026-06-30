# Order-Defect Recovery Repair Dual-Pro Audit Adoption Note

Date: 2026-06-30 CST
Authority: node36
Status: local adoption note for two external Pro reports; gate-only audit, not
paper authority.

## Inputs

Two zero-context Pro reports were returned against the D630 final3
recovery-repair bundle and v2 prompt:

```text
docs/infra/gpt_deep_research/deep_research_order_defect_recovery_repair_dual_pro_report6_20260630.md
sha256=23a1d3996bff38a2360457e09990b4ac40eee3dd84afb8e022c48395adf07807

docs/infra/gpt_deep_research/deep_research_order_defect_recovery_repair_dual_pro_report7_20260630.md
sha256=8d39d7ab9bf64cbf7d871dde7e21842e0a2d7a80b6cbae6aaeadb54a7a26792b
```

They are model outputs. Under the current emergency lock they are
`non_authoritative_scratch` / `gate_only_audit` only.

## Local Verdict

Adopt the shared verdict:

```text
KEEP_LOCK_AND_FIX
```

This means:

- Gate 1 wording lock remains supported by current files.
- Gate 2 evidence and scope boundaries remain supported.
- The old v1.6 paper-draft prompt is superseded-risk provenance.
- The current task is recovery / proof / bibliography repair only.
- Do not write a paper body while the external-model emergency lock is active.

## Accepted Findings

Accepted with local evidence:

- `README.md` still had a stale bottom `Current Next Step` pointing to the v1.6
  wording-lock / paper-drafting package, even though its top entry already
  pointed to D630 recovery repair. This is a real drift and is patched in this
  adoption round.
- Lamboni 2026 must be cited conservatively as DOI / publisher online record
  status only for current drafting. The v1.5 bibliography table previously used
  fuller volume / issue / page metadata; this is downgraded in this adoption
  round.
- Proposition 1 remains the strongest local draft theorem; Proposition 2 and
  Proposition 3 remain `PLAUSIBLE_LOCAL_DRAFT` under the rescue audit; the exact
  2 x 2 rational witness remains `CERTIFICATE`.
- The deterministic floating-point harness and JSON are regression support
  only. The analytic proof draft and exact rational certificate carry the
  mathematical burden.
- Mode B remains `insufficient_artifact`; no full panel, checkpoint inference,
  training, new loss, observed field, F3 positive, LOSO pass, glass-box, posted
  preprint, or completed formal system is authorized.

## Local Corrections To The Reports

The reports correctly judged the final3 bundle they received, where the recovery
timeline still contained a historical dirty freeze. Node36 has since committed
the final3 package self-consistency correction at:

```text
a0adf14 docs(math): make recovery repair package self-consistent
```

Therefore the old bundle-local `M STATE.md` / `?? docs/infra/recovery/` dirty
description is historical, not the current tracked-file state. However, node36
must still not claim a fully clean worktree until this dual-report adoption
round is committed and the unrelated untracked `.codex/` and root `AGENTS.md`
are explicitly excluded from the research snapshot.

Clean-snapshot evidence lives in git status and commit history, not in a zip
self-hash or model report.

## Rejected Upgrades

Reject:

- paper body drafting under the active emergency lock;
- completed formal system;
- proof authority from Pro output;
- bibliography authority from Pro output;
- JSON floats or deterministic harness as proof;
- universal non-product order-dependence for every input;
- broad new ANOVA, dependent-input decomposition, or noncommuting projection
  theory;
- any MaoField empirical positive result or observed residual / interaction /
  quotient-residual / transport / holonomy field.

## Local Smoke Checks

Short checks were run under node36 SSD scratch:

```text
/home/amd/codex-node36/tmp/orderdefect_dualpro_20260630_1144/
```

Exact rational witness:

```text
script=scripts/debranded_residual_transport_exact_witness_v1_4.py
all_checks_passed=True
json_sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
markdown_sha256=744496e5a6de784ca77e88f05f9655c9a56a91d1bf4aadbfd77e9a1e6e59453f
```

Deterministic harness:

```text
script=scripts/debranded_residual_transport_harness_v1_3.py
all_synthetic_controls_passed=True
threshold_contract_sha256=ec2a3a70dce8d19be5635b2b2a7f51caae17ee8e0a8bce2ec20ed4a55f9a82f6
summary_markdown_sha256=361e55f4ae813f1e23f9a1dc6f54584cfa5a648e3c925ef31b678e26e7d8fcec
```

The regenerated harness JSON has a fresh `created_utc`, so its file hash is not
used as a stable certificate here. This remains harness-only regression support.

## Next Local Action

Before any future paper-draft consideration:

1. Commit the dual-report adoption and status repair.
2. Refresh RAG using node22 one-shot vector service, then stop node22.
3. Run smoke RAG queries for dual-Pro reports, README supersession, Lamboni
   conservative status, and `KEEP_LOCK_AND_FIX`.
4. Keep the external-model emergency lock unless the user explicitly lifts it.
5. If the lock is lifted later, start with a separate proof-repair audit of
   Proposition 2 and Proposition 3 before drafting.
