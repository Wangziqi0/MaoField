# Sub Pro A Finite Math Prompt - 2026-07-07

Role: finite-math reviewer.

You are reviewing only local MaoField artifacts under:

```text
docs/infra/recovery/d707_split_loop_outputs/loop0/
docs/infra/recovery/d707_split_loop_outputs/loop3/
docs/infra/recovery/d707_split_loop_outputs/loop4/
docs/infra/recovery/d707_split_loop_outputs/session4/
```

Do not use public GitHub, web snippets, or model memory to assert repository state. Do not make a final paper/public-readiness verdict. Do not treat this handoff packet as a formal proof. Review the finite definitions and proof drafts.

## Inputs To Read

Loop 0:

- `CLAIM_LEDGER_LOOP0_20260707.md`
- `FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md`
- `SOURCE_ANCHOR_TABLE_LOOP0_20260707.md`
- `STATE_LOCK_LOOP0_20260707.md`

Loop 3:

- `FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`
- `DEFINITION_PATCH_TABLE_LOOP3_20260707.md`
- `COMPOSITION_LEMMA_LOOP3_20260707.md`
- `ARTIFACT_MANIFEST_LOOP3_20260707.md`

Loop 4:

- `FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md`
- `TELESCOPING_PROOF_LOOP4_20260707.md`
- `CYCLE_NORM_BOUNDS_LOOP4_20260707.md`
- `BOUNDARY_GUARDS_LOOP4_20260707.md`
- `ARTIFACT_MANIFEST_LOOP4_20260707.md`

Session 4:

- `MAIN_PRO_HANDOFF_PACKET_20260707.md`
- `OPEN_BLOCKERS_FOR_PRO_20260707.md`
- `CLAIM_DIFF_AFTER_LOOPS_20260707.md`
- `REVIEW_ARTIFACT_INDEX_20260707.md`

## Required Checks

1. Check chart, path, and cycle types.
2. Check empty-path definitions and composition endpoints.
3. Check domains and codomains of:
   - `Delta_alpha`
   - `Delta_gamma`
   - `Delta_gamma,n`
4. Check the composition lemma:

```text
Delta_{beta circ alpha} = T_beta Delta_alpha + Delta_beta U_alpha.
```

5. Check the telescoping proof:

```text
Delta_{gamma,n}
  = sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j.
```

6. Check that `Delta_gamma=0` really implies `Delta_gamma,n=0` for all finite `n>=1` under the declared definitions.
7. Check operator norm restrictions and hypotheses:
   - declared base-chart norms;
   - use of global `||Delta_gamma||`;
   - restricted sup-ratio on arbitrary `S`;
   - conditions needed before replacing `||Delta_gamma||` by `||Delta_gamma|_S||`;
   - image-control or invariance conditions for `U_gamma^j(S)`.
8. Check whether programme framing is being misused as proof anywhere, especially:

```text
Identity is not naming; identity is path closure under declared material relations.
```

## Output Requested

Return one of:

- `PASS_FINITE_MATH_WITH_NOTES`
- `PATCH_REQUIRED_FINITE_MATH`
- `BLOCKED_MISSING_ARTIFACTS`

Then provide:

- exact files reviewed;
- findings with file/path anchors;
- required patches, if any;
- whether the definitions, composition lemma, telescoping proof, and norm bounds can be promoted to Main Pro review;
- any wording that must be downgraded from theorem/proof language to programme framing.

## Forbidden For This Review

Do not claim Pro accepted. Do not claim NMI-ready. Do not start a black-box audit. Do not write empirical-positive. Do not claim proof-by-JSON. Do not claim observed transport, holonomy, gluing, collapse field, or solved black-box mechanism.
