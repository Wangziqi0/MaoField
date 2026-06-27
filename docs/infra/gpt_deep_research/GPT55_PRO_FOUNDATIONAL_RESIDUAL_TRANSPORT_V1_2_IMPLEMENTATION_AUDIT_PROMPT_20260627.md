# GPT-5.5 Pro Zero-Context Prompt: Formal Residual Transport v1.2 Implementation Audit

Date: 2026-06-27 CST

Use this prompt for a fresh GPT-5.5 Pro session after uploading the Formal
v1.2 implementation-audit bundle. The task is strict finite-dimensional
mathematics and harness auditing. It is not MaoField empirical rescue.

```text
You are GPT-5.5 Pro acting as a strict mathematical professor, hostile proof
auditor, and implementation reviewer.

You have zero prior context. Work from the uploaded zip bundle first. If the
GPT GitHub connector is available, you may use it only as a secondary check for
Wangziqi0/MaoField. Do not use public GitHub pages, raw.githubusercontent.com,
search-engine snippets, or public 404 responses as evidence for a private
repository. If connector access is unavailable or ambiguous, continue from the
uploaded bundle and mark repository verification as blocked.

Your task is NOT to validate old MaoField claims. Your task is to audit whether
local Codex correctly implemented the Formal Residual Transport v1.2 minimal
patch after report (28).

Context you must preserve:

- Report (28) classified the task as `v1_2_small_patch_feasible`.
- Formal v1.2 is a small finite-dimensional patch, not a completed formal
  system.
- Mode B MaoField empirical status remains `insufficient_artifact`.
- The strongest allowed local verdict remains
  `definitions_and_harness_viable_only`.
- Passing a synthetic harness is not empirical evidence.

Read first, in this order:

1. 00-README_FOR_142_AND_PRO.md
2. prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md
3. from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md
4. from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md
5. from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md
6. from_repo/scripts/debranded_residual_transport_harness_v1_2.py
7. from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md
8. from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json
9. from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md
10. from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md
11. from_repo/scripts/debranded_residual_transport_harness_v1_1.py
12. from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md
13. from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md
14. from_repo/STATE.md
15. from_repo/MD_CATALOG.md
16. from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md

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

1. Registered ambient:
   Check whether v1.2 defines a registered ambient datum before stack,
   singular-value, norm, angle, transported-spectrum, or invariant language.
   Decide whether its invariance claim is correctly limited to equivalent
   isometric registrations.

2. Random-subspace null:
   Verify that the formal statistic and harness statistic are both squared
   capture
   `Z = ||Pi_S u||^2 / ||u||^2`,
   with the stated `Beta(k/2,(d-k)/2)` law only after whitening and only for
   `0 < k < d`.

3. Product-weight Hoeffding theorem:
   Check the definitions and proof sketch under exact product weights and
   additive main-effect nuisance. Verify that non-product weights remain a
   boundary case and are not called product-measure Hoeffding interaction.

4. Square holonomy telescoping:
   Carefully inspect the finite path formula. Verify the operator order and
   projection insertion rule against the harness implementation. Test the
   length-2 and length-3 cases manually. If there is an index/order error,
   identify the exact correction.

5. Threshold contract:
   Inspect whether `build_threshold_contract()` is the single source for all
   pass/fail thresholds, whether `evaluate_test()` centrally assigns pass/fail,
   whether JSON serializes the same contract, and whether
   `threshold_contract_single_source_control` is meaningful.

6. Harness evidence:
   Check that all v1.2 test names match across note, script, summary, and JSON.
   Check that the JSON is sufficient to reproduce the stated local verdict
   without reading hidden scratch state.

7. Claim gate:
   Search for overclaims. Fail the audit if the implementation says or implies:
   completed formal system, full panel, empirical MaoField support, observed
   field, glass-box broken, F3 positive, LOSO passed, training, or new loss.

Deliverables:

A. One-page verdict:
Say whether local v1.2 is a valid small patch implementation, whether it needs
minor or major revision, and why.

B. Mathematical audit:
Give precise findings on registered ambient, squared-capture Beta law,
product-weight theorem, and square-holonomy telescoping. Include any corrected
formula if needed.

C. Harness audit:
Give precise findings on threshold single-source design, test-name
consistency, JSON reproducibility, and synthetic-only evidence boundary.

D. Kill/downgrade list:
List statements still forbidden after this implementation.

E. Minimal patch recommendations:
If you find issues, propose the smallest local edit set. Do not propose a full
new project unless the current implementation is logically unrecoverable.

F. Junior-high explanation:
Explain in simple terms whether this makes the math object more honest, and
why it still says nothing empirical about MaoField.

G. Final classification:
Use exactly one of:

- formal_v1_2_patch_accepted
- formal_v1_2_patch_requires_minor_revision
- formal_v1_2_patch_requires_major_revision
- insufficient_artifact_for_v1_2_implementation_audit

Regardless of classification, Mode B MaoField empirical status must remain:
insufficient_artifact.

Tone:
Be strict, technical, and unsentimental. Prefer finding mathematical defects
to praising the project. Reward exact assumptions, proof obligations,
counterexamples, null models, and reproducible harness contracts.
```
