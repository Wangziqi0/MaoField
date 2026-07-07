# D707 Bounded Formal Note V0 Revision Taskbook

Date verified: 2026-07-07 16:55:44 CST on node36.

Inputs:

- `docs/infra/gpt_deep_research/deep_research_d707_split_loop_bounded_formal_note_review_report37_20260707.md`
- `docs/infra/gpt_deep_research/D707_SPLIT_LOOP_BOUNDED_FORMAL_NOTE_REVIEW_REPORT37_ADOPTION_NOTE_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/COMPOSITION_LEMMA_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/TELESCOPING_PROOF_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/BOUNDARY_GUARDS_LOOP4_20260707.md`

## Verdict To Implement

```text
REVISE_BEFORE_FORMAL_NOTE
```

The Loop 0/3/4 packet is coherent enough to revise into a bounded internal formal note, but not ready to publish or promote as-is.

## Target

Create a narrow internal v0 note only after applying the following constraints:

- Object name: finite chart/path/cycle defect calculus under declared transports.
- Setting: finite-dimensional real normed spaces.
- Body: definitions, composition lemma, cycle telescoping proposition, finite-horizon global norm estimate, boundary/non-claim note.
- Length target: 2-4 pages equivalent.
- No RAG, prompt, handoff, JSON, harness, status, or manifest as proof authority.

## Required Mathematical Shape

Let `G=(C,E)` be a finite directed graph. For each chart `c`, provide finite-dimensional real normed spaces `H_c`, `O_c` and a linear map `Phi_c:H_c -> O_c`. For each edge `e:c -> c'`, provide declared linear transports `U_e:H_c -> H_c'` and `T_e:O_c -> O_c'`.

For a path `alpha:c_0 -> ... -> c_k`, define:

```text
Delta_alpha = T_alpha Phi_{c_0} - Phi_{c_k} U_alpha : H_{c_0} -> O_{c_k}.
```

For composable paths `alpha:c_0 -> c_1` and `beta:c_1 -> c_2`, prove:

```text
Delta_{beta o alpha} = T_beta Delta_alpha + Delta_beta U_alpha.
```

For a cycle `gamma:c_0 -> ... -> c_0`, define:

```text
Delta_gamma = T_gamma Phi_{c_0} - Phi_{c_0} U_gamma.
Delta_{gamma,n} = T_gamma^n Phi_{c_0} - Phi_{c_0} U_gamma^n.
```

Prove:

```text
Delta_{gamma,n} = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j.
```

If `||T_gamma|| <= a` and `||U_gamma|| <= b`, the safe global bound is:

```text
||Delta_{gamma,n}|_S|| <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||
```

for arbitrary `S`, provided `||Delta_{gamma,n}|_S||` is defined as the restricted sup-ratio over nonzero elements of `S`.

Do not replace the right-hand global `||Delta_gamma||` by `||Delta_gamma|_S||` unless the note states explicit image-control hypotheses such as `U_gamma^j(S) subset S`, or narrows `S` to a subspace with appropriate invariance.

## Forbidden In The V0 Note

- MaoField empirical-positive claims.
- Observed residual, interaction, transport, holonomy, gluing, or collapse field.
- Broad black-box mechanism solved.
- NMI-ready / submission-ready claims.
- Broad ANOVA, dependent-input, projection, sheaf, contextuality, or dynamic-collapse theory.
- Proof by JSON, harness, RAG, prompt, handoff, manifest, status, or model output.

## Output Gate

The next node36 action may draft an internal v0 only if it keeps this taskbook's narrow object and boundaries. Any broader programme text must be moved to motivation or boundary remarks and explicitly marked non-theorem.
