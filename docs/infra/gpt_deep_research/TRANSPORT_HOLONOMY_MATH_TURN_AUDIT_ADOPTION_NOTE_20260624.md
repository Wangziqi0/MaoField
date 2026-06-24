# Transport / Holonomy Math-Turn Audit Adoption Note

Date: 2026-06-24 CST

## Source

Archived GPT/PRO report (24):

```text
docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md
```

Attachment SHA256:

```text
b081f8e9536f23265848188af7a8a345d351625558e20afe5943e7febad12913
```

Canonical archive SHA256 after trailing-whitespace normalization:

```text
e552b734be62caae86c0d6ecdfb7015f43369aeefb3e3a7fbf2615332c152263
```

This note is the node36 interpretation layer. Treat report (24) as a
claim-source Mode A mathematical audit, not as new MaoField evidence.

## Local Decision

Adopt report (24)'s professor verdict as the strongest current recommendation:

```text
E. split into a debranded project independent from MaoField.
```

This is still a recommendation to PI, not an already-executed repository or
project-management action.

## Product-Weight Boundary

Adopt report (24)'s warning that the current q4 x tokenpos4 schema weights are
not exact product-form weights.

Node36 direct check against:

```text
docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json
```

found:

```text
schema_id = q4_tokenpos4_hypercube_20260623
total_weight = 1.0
max_abs_error_vs_q_marginal_outer_b_marginal = 0.0045863252708490815
max_rel_error_vs_actual = 0.06724386724386727
max_rel_error_vs_product_expected = 0.07209158415841586
argmax = slice_id 2, position_bin 0
actual = 0.06820436507936507
product_expected = 0.06361803980851599
```

Therefore the current carrier must be described as:

```text
non-product weighted hierarchical projection / residual program
```

Do not describe the current q4 x tokenpos4 carrier as a canonical
product-measure Hoeffding decomposition unless a future schema supplies exact
product weights or an explicit product-measure reweighting.

## Adopted Mathematical Direction

Keep report (23)'s finite scale-lattice residual transport system as the current
best object:

```text
local residual R_s(K) = P_s K_s
edge defect D_rho(K) = C_rho P_s K - P_s' C_rho K
square holonomy defect H_square(K)
```

Report (24) sharpens its role:

- single-scale residuals and scalar norms are too weak;
- edge defects and square holonomy express object identity across scales;
- rank-1 shadows, random same-dimension subspaces, non-product weights, and
  absorbable gluing mismatch must be treated as no-go threats;
- synthetic harness pass means only definition/code viability.

## Mode B Boundary

MaoField-specific verdict remains unchanged:

```text
stable non-scalar residual object = insufficient_artifact
existing interaction smoke = smoke_conjecture_only
```

Blocked claims remain blocked:

- no full panel has run;
- no 16-cell full-panel aggregate exists;
- no residual, interaction, quotient-residual, transport, or holonomy field has
  been observed;
- no LOSO pass, F3 positive, or glass-box breakthrough is authorized;
- no training or new loss work is authorized.

## Local Consequence

Next local work should stay zero-GPU and Mode A:

1. Draft a debranded project charter around finite weighted residual transport,
   edge defects, square holonomy, random-subspace calibration, and no-go
   classification.
2. Extend the synthetic harness to include non-product weighted hierarchical
   projection controls, so product-Hoeffding language cannot sneak back in.
3. Keep any future MaoField full-panel request PI-gated and separate from the
   debranded math project decision.

Do not use report (24) to request full-panel generation, training, or new-loss
work.
