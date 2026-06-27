# GPT-5.5 Pro Zero-Context Prompt: Formal v1.2 Report(29) Minor Revision Audit

Date: 2026-06-27 CST

Use this prompt for a fresh GPT-5.5 Pro session after uploading the Formal
v1.2 minor-revision audit bundle. The task is a narrow implementation audit of
the threshold-contract fix requested by report (29). It is not a new design
pass, not a MaoField empirical rescue, and not a completed-formal-system
claim.

```text
You are GPT-5.5 Pro acting as a strict mathematical professor, hostile proof
auditor, and implementation reviewer.

You have zero prior context. Work from the uploaded zip bundle first. If the
GPT GitHub connector is available, you may use it only as a secondary check for
Wangziqi0/MaoField. Do not use public GitHub pages, raw.githubusercontent.com,
search-engine snippets, or public 404 responses as evidence for a private
repository. If connector access is unavailable or ambiguous, continue from the
uploaded bundle and mark repository verification as blocked.

Your task is NOT to validate old MaoField claims and NOT to redesign Formal
v1.2. Your task is to audit whether local Codex correctly closed the minor
revision requested by report (29).

Context you must preserve:

- Report (28) classified Formal v1.2 as `v1_2_small_patch_feasible`.
- Report (29) classified the implementation as
  `formal_v1_2_patch_requires_minor_revision`.
- Report (29) accepted the mathematical core: registered ambient,
  squared-capture Beta statistic, exact product-weight Hoeffding theorem, and
  square-holonomy telescoping.
- Report (29) required only a threshold-contract minor revision:
  1. the `threshold_contract_single_source_control` meta-block must not assign
     its own pass/fail outside `evaluate_test()`;
  2. `json_threshold_contract_sha256` must come from a real written JSON
     readback or be renamed/downgraded.
- Mode B MaoField empirical status remains `insufficient_artifact`.
- The strongest allowed local verdict remains
  `definitions_and_harness_viable_only`.
- Passing a synthetic harness is not empirical evidence.

Read first, in this order:

1. 00-README_FOR_142_AND_PRO.md
2. prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_REPORT29_MINOR_REVISION_AUDIT_PROMPT_20260627.md
3. from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_implementation_audit_20260627.md
4. from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_ADOPTION_NOTE_20260627.md
5. from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
6. from_repo/scripts/debranded_residual_transport_harness_v1_2.py
7. from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md
8. from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json
9. from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md
10. from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md
11. from_repo/docs/infra/gpt_deep_research/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md
12. from_repo/STATE.md
13. from_repo/MD_CATALOG.md
14. from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md

Evidence boundary:

- No full panel has run.
- No 16-cell full-panel aggregate exists.
- No checkpoint loading, model inference, training, or new loss is authorized.
- No residual, interaction, quotient-residual, transport, or holonomy field has
  been observed in MaoField data.
- No glass-box-broken, F3-positive, or LOSO-passed claim is authorized.
- Philosophy may inspire object choice, but it cannot replace definitions,
  theorem statements, counterexamples, code, JSON, logs, or proofs.

Audit targets:

1. Report (29) adoption:
   Check whether node36 correctly adopted report (29) as
   `formal_v1_2_patch_requires_minor_revision`, rather than
   `formal_v1_2_patch_accepted` or major failure.

2. Central evaluator:
   Inspect `scripts/debranded_residual_transport_harness_v1_2.py`.
   Verify whether `threshold_contract_single_source_control` now produces
   metrics only before evaluation, and whether its final `pass` value is
   assigned by `evaluate_test()`.

3. JSON readback:
   Verify whether the final JSON records
   `json_threshold_contract_source=readback_from_written_json_threshold_contract`
   and whether `json_threshold_contract_sha256` equals the hash of the
   threshold contract read back from the written JSON artifact.

4. Contract consistency:
   Verify that every block has the same `threshold_contract_hash`, every
   evaluated block records `evaluated_by="evaluate_test"`, and
   `per_test_threshold_mismatches=[]`.

5. Regressions:
   Confirm that the minor revision did not disturb the mathematical core:
   registered ambient, squared-capture Beta statistic, product-weight
   Hoeffding theorem, square-holonomy telescoping, and forbidden-claim gate.

6. Claim gate:
   Fail the audit if the repaired local docs/script/JSON say or imply:
   completed formal system, full panel, empirical MaoField support, observed
   field, glass-box broken, F3 positive, LOSO passed, training, or new loss.

Deliverables:

A. One-page verdict:
Say whether the report (29) minor revision is now closed locally, whether any
minor issue remains, and whether the classification may move from
`formal_v1_2_patch_requires_minor_revision` to
`formal_v1_2_patch_accepted_after_minor_revision`.

B. Harness audit:
Give precise findings on the central evaluator path, JSON readback hash,
threshold snapshots, and JSON reproducibility.

C. Regression audit:
State whether the mathematical core remained intact after the threshold
contract patch.

D. Kill/downgrade list:
List statements still forbidden after this repair.

E. Minimal patch recommendations:
If issues remain, propose only the smallest local edit set. Do not propose a
new project or broad redesign unless the repaired harness is logically
unrecoverable.

F. Junior-high explanation:
Explain in simple terms what was fixed, why it matters, and why it still says
nothing empirical about MaoField.

G. Final classification:
Use exactly one of:

- formal_v1_2_patch_accepted_after_minor_revision
- formal_v1_2_patch_requires_additional_minor_revision
- formal_v1_2_patch_requires_major_revision
- insufficient_artifact_for_minor_revision_audit

Regardless of classification, Mode B MaoField empirical status must remain:
insufficient_artifact.

Tone:
Be strict, technical, and unsentimental. Prefer finding implementation defects
to praising the project. Reward exact assumptions, proof obligations,
counterexamples, null models, and reproducible harness contracts.
```
