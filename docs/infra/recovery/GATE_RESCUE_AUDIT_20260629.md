# Gate Rescue Audit 2026-06-29

Generated: `2026-06-29 21:28:29 CST +0800`

Path mapping: user-specified `from_repo/...` is mapped to current repository root `/media/amd/raid1/canonical/projects/MaoField`. Example: `from_repo/docs/...` -> `docs/...`.

## Gate 1 -- v1.6 Wording Lock

Result: **PASS**

| file | exists | result | match lines |
| --- | --- | --- | --- |
| docs/infra/debranded_residual_transport/README.md | True | PASS | L234: The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats. |
| docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md | True | PASS | L77: The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats. |
| docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md | True | PASS | L12: The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats. |
| docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json | True | PASS | L13: "harness_boundary": "The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.",; L14: "proof_responsibility": "The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.",; L210: "canonical_harness_boundary_sentence": "The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.",; L211: "proof_responsibility": "The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.", |
| scripts/debranded_residual_transport_harness_v1_3.py | True | PASS | L6: inference, train, or authorize a new loss. The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.; L25: CANONICAL_HARNESS_BOUNDARY_SENTENCE = "The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats." |

## Gate 2 -- Evidence And Scope Boundary

Result: **PASS**

| boundary item | result | supporting line refs | risk notes |
| --- | --- | --- | --- |
| finite positive weighted two-way table only | PASS | `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:43` Let `Q` and `B` be finite sets, let `X=Q x B`, and let `w(q,b)>0` with<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:43` Let `Q` and `B` be finite sets, let `X=Q x B`, and let `w(q,b)>0` with<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:6` This is not a MaoField empirical result. | OK |
| product-weight iff centered main-effect orthogonality | PASS | `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:106` ### Proposition 1<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:111` w(q,b) = w_Q(q) w_B(b) for all q,b<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:112` A is orthogonal to B0 under <.,.>_w | OK |
| order-independence iff product weights | PASS | `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:177` ### Proposition 2<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:182` D_w = 0 iff w is product form | OK |
| existential pure-main-effect witness, not universal | PASS | `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:229` ### Quantifier Guard<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:234` there exists a witness signal f with R_Q_then_B f != R_B_then_Q f.<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:237` It is false to claim that every input differs. Constants lie in the kernel of | OK |
| wrong-order output is artifact, not true interaction residual | PASS | `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:254` The nonzero wrong-order output is a sequential stripping artifact, not a true | OK |
| exact 2 x 2 rational witness | PASS | `docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:285` ## 5. Minimal 2 x 2 Witness<br>`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:321` \|\|R_Q_then_B K\|\|_w^2 = 61/177408 | OK |
| harness regression support only | PASS | `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:12` The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, n | OK |
| local ceiling definitions_and_harness_viable_only | PASS | `STATE.md:16` \| 最后更新 \| **2026-06-29 D629 17:16 CST** (`date` verified 17:16 CST; source HEAD before update `67e8577`)。**外部模型紧急锁定**: 用户报告当前 OpenAI/Pro 模型能力/身份异常；该平台状态未作为独立事实写入 | OK |
| Mode B status insufficient_artifact | PASS | `STATE.md:16` \| 最后更新 \| **2026-06-29 D629 17:16 CST** (`date` verified 17:16 CST; source HEAD before update `67e8577`)。**外部模型紧急锁定**: 用户报告当前 OpenAI/Pro 模型能力/身份异常；该平台状态未作为独立事实写入 | OK |

## Boundary Violations / Blockers

BLOCKER scan count: `0`.

No BLOCKER severity line was found by the automated scan. Review WARNING lines separately.

## Gate Consequence

If Gate 1 or Gate 2 fails, do not write a paper draft. Current automated gate result: `Gate1=PASS`, `Gate2=PASS`.
