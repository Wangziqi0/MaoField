# OI Quantitative Norm Result Report33 Adoption Note

Date verified: 2026-07-06 22:30:01 CST on node36.

Source attachment:

```text
/home/amd/.codex/attachments/3f9f8ab0-09b9-43ca-bc9b-6dc4f8b31a78/pasted-text.txt
```

Archived normalized report:

```text
docs/infra/gpt_deep_research/deep_research_oi_quantitative_norm_result_report33_20260706.md
```

Source sha256:

```text
b100f3791e52dc49557acb4d3bc8450c408496c1b59c3e68082108a023294501
```

## Pro Verdict

Pro selected:

```text
PROVE_QUANTITATIVE_OI_NORM_RESULT
```

Core proposal:

```text
OI^{op}_{N_add}(w)
  = ||D_w restricted to N_add||
  = max_j rho_j * sqrt(1 - rho_j^2),
```

where `rho_j` are the canonical correlations, equivalently cosines of principal
angles, between the centered main-effect spaces `A` and `B0`.

## Local Adoption

Node36 action:

```text
ARCHIVE_AS_REPORT33_AND_QUEUE_PROOF_CHECK
```

This is not yet a new formal note and not a current Zenodo V2.5 patch. It is a
mathematical next-candidate for a future bounded companion or exact addendum to
the D706 OI corollary companion.

## What The Report Means

The report says the previous zero/nonzero companion can be strengthened without
leaving the finite v1.3 object:

- previous implemented result: `OI^{op}_{N_add}(w)=0 iff w is product form`;
- proposed quantitative refinement: exact operator norm of the commutator
  `P_B0 P_A - P_A P_B0` restricted to additive nuisance;
- geometric invariant: principal angles / canonical correlations between `A`
  and `B0`;
- dependence invariant: singular spectrum of the normalized dependence tensor
  `Z_w=(w-w_Q otimes w_B)/sqrt(w_Q w_B)`;
- finite `2 x 2` special case: exact formula via `ad-bc`;
- near-product case: if `||Z_w||_2 <= 1/sqrt(2)`, then the OI value is
  `epsilon sqrt(1-epsilon^2)`.

This is a stronger exact-math candidate, not an empirical or philosophical
claim upgrade.

## Immediate Local Check

Node36 ran a small rational arithmetic check in SSD scratch:

```text
/home/amd/codex-node36/tmp/oi_quantitative_report33_20260706/
```

For the table `w=(1/11)[[1,2],[3,5]]`, the report's arithmetic is correct:

```text
tau = -1/121
rho^2 = 1/672
(OI^{op}_{N_add}(w))^2 = 671/451584
```

However, node36 also confirmed this is not identical to the old v1.4 witness
artifact norm:

```text
old witness artifact norm squared = 61/177408
(671/451584) / (61/177408) = 121/28
```

Reason: the old value is the weighted output norm of a particular witness,
while the proposed quantitative OI value is an operator norm with input
normalization. A future formal note must keep this normalization distinction
explicit.

## Proof Status

Current local status:

```text
PROMISING_CANDIDATE_NOT_YET_IMPLEMENTED
```

The principal-angle block proof is standard-looking and plausible, but node36
has not yet written or audited a canonical formal proof note. The report should
be used as a candidate theorem map for a future proof-check pass.

## Claim Boundary

Do not claim yet:

- formal note implemented;
- current V2.5 Zenodo preprint patched;
- broad ANOVA / dependent-input / projection / contextuality / sheaf /
  consistency-radius / dynamic-collapse theory;
- empirical MaoField positive result;
- observed residual, interaction, transport, holonomy, or gluing field;
- proof by JSON, harness, or model output.

Mode B remains:

```text
insufficient_artifact
```

Duplicate risk remains:

```text
MEDIUM
```

## Recommended Next Action

If PI wants to continue this branch, the next node36 task should be:

```text
WRITE_AND_AUDIT_FORMAL_NOTE_OI_QUANTITATIVE_NORM_COMPANION
```

The proof must:

1. stay inside finite positive weighted two-way tables;
2. explicitly identify the two-projection principal-angle theorem as standard;
3. prove the `Z_w` singular-value representation;
4. separate operator norm from fixed-witness artifact norm;
5. keep the old OI zero/nonzero companion and v1.5 GQ-FCR as separate notes.
