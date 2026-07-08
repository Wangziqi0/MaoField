# GPT-5.5 Pro Prompt - D708 Internal V0 Promotion Gate

You are GPT-5.5 Pro acting as a strict mathematical reviewer for a local
MaoField research package. Use only the files in the uploaded package. Do not use
public GitHub, web browsing, memory, or guesses about the repository. Treat RAG
records as locators only; primary authority is the included markdown source
files and exact local records.

## Your Task

Review whether the internal v0 note

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md
```

is mathematically correct, well-scoped, and safe to keep as an internal bounded
formal note.

This is not a public-paper review. Do not write a paper. Do not upgrade the
project to public-ready, paper-ready, submission-ready, or NMI-ready.

## Read First

1. `STATE.md`
2. `docs/infra/recovery/D708_INTERNAL_V0_PROMOTION_GATE_TASKBOOK_20260708.md`
3. `docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md`
4. `docs/infra/gpt_deep_research/deep_research_d707_bounded_formal_note_v0_draft_report38_20260707.md`
5. `docs/infra/gpt_deep_research/D707_BOUNDED_FORMAL_NOTE_V0_DRAFT_REPORT38_ADOPTION_NOTE_20260707.md`
6. `docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md`

Then read the Loop0/3/4 and Session4 source files included in the package,
especially:

- `docs/infra/recovery/d707_split_loop_outputs/loop0/CLAIM_LEDGER_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/COMPOSITION_LEMMA_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop3/ARTIFACT_MANIFEST_LOOP3_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/TELESCOPING_PROOF_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/BOUNDARY_GUARDS_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop4/ARTIFACT_MANIFEST_LOOP4_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/MAIN_PRO_HANDOFF_PACKET_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/OPEN_BLOCKERS_FOR_PRO_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/CLAIM_DIFF_AFTER_LOOPS_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_A_FINITE_MATH_PROMPT_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_E_REDTEAM_PROMPT_20260707.md`

## Mathematical Object Under Review

The internal v0 note claims only a finite declared-transport calculus:

- finite directed graph `G=(C,E)`;
- finite-dimensional real normed spaces `H_c` and `O_c`;
- linear chart maps `Phi_c:H_c->O_c`;
- declared linear edge transports `U_e:H_c->H_c'` and `T_e:O_c->O_c'`;
- path composites `U_alpha`, `T_alpha`;
- path defect

```text
Delta_alpha = T_alpha Phi_c0 - Phi_ck U_alpha : H_c0 -> O_ck;
```

- path-defect composition identity

```text
Delta_{beta circ alpha} = T_beta Delta_alpha + Delta_beta U_alpha;
```

- cycle defect and iterated cycle defect

```text
Delta_gamma = T_gamma Phi_c0 - Phi_c0 U_gamma
Delta_{gamma,n} = T_gamma^n Phi_c0 - Phi_c0 U_gamma^n;
```

- finite cycle telescoping identity

```text
Delta_{gamma,n}
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j;
```

- finite-horizon global bound

```text
||Delta_{gamma,n}|_S||
  <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||.
```

The restricted-norm warning is essential: for arbitrary `S`, the right side must
use global `||Delta_gamma||`. Replacing it with `||Delta_gamma|_S||` requires
extra image-control or invariance assumptions such as `U_gamma(S) subset S`.

## Required Audit

Check all of the following:

1. Type correctness for every map.
2. Empty-path convention.
3. Composition-order convention.
4. Path-defect composition proof.
5. Cycle definitions and domains/codomains.
6. Telescoping induction proof.
7. Global norm bound proof.
8. Restricted-subset and restricted-subspace language.
9. Whether `CID` / `CIC_N` are only bookkeeping quantities.
10. Whether prior-art/triviality risk is acknowledged enough.
11. Whether any line overclaims novelty or empirical meaning.
12. Whether any line should be deleted or rewritten before the note is kept as
    an internal v0.

## Hard Boundaries

You must preserve these boundaries:

- Mode B remains `insufficient_artifact`.
- Duplicate risk remains at least `MEDIUM` unless you give strong evidence from
  the package itself. You probably cannot lower it.
- This is not peer review.
- This is not public-ready, paper-ready, submission-ready, or NMI-ready.
- This is not a MaoField empirical positive result.
- This does not observe residual, interaction, transport, holonomy, gluing, or
  collapse fields.
- This does not solve a black-box mechanism.
- This does not establish dynamic-collapse theory.
- This does not establish broad ANOVA, dependent-input, projection, sheaf,
  contextuality, or path-closure theory.
- RAG, JSON, harness, prompts, handoffs, manifests, and model outputs are not
  proofs.

## Choose Exactly One Verdict

Return exactly one:

```text
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY
PATCH_INTERNAL_V0_THEN_RECHECK
REJECT_OR_STOP_PARK
REQUEST_NODE36_FILES
```

## Output Format

Use this structure:

1. `Verdict`: exactly one of the four allowed verdicts.
2. `Mathematical Audit`: line-by-line or theorem-by-theorem review.
3. `Boundary Audit`: overclaim, forbidden-claim, and wording-risk review.
4. `Prior-Art / Triviality Risk`: LOW / MEDIUM / HIGH / UNKNOWN, with reasons.
5. `Blockers`: exact blockers if any.
6. `Patch Instructions`: exact edits needed if any.
7. `Minimal Safe Wording`: 5-8 sentences if accepted or patchable.
8. `Next Action`: exactly one of:

```text
KEEP_INTERNAL_ONLY
PATCH_AND_RECHECK
STOP_PARK
REQUEST_MORE_FILES
```
