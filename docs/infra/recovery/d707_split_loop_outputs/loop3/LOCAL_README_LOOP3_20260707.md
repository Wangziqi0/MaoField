# Local README - Loop 3 - 2026-07-07

Loop: `Session 2 / Loop 3 - Typed Chart/Path Definitions Patch`

Current local status: `READY_FOR_LOOP4`, conditional on downstream Pro review of the finite linear-algebra details.

## Inputs Consumed

- `AGENTS.md`
- `/media/amd/raid1/canonical/AGENTS.md`
- `STATE.md`
- `CLAUDE.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/STATE_LOCK_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/CLAIM_LEDGER_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md`
- `docs/infra/recovery/d707_split_loop_outputs/loop0/SOURCE_ANCHOR_TABLE_LOOP0_20260707.md`
- `docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md`
- Local Report35 / Report36 path-closure review files for the typed-definition target and claim boundary.

The Loop 0 status file was checked at byte level and contains the single status line `READY_FOR_LOOP3` with a trailing newline.

## Files in This Directory

- `FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`: typed chart, edge, path, defect, and norm conventions.
- `DEFINITION_PATCH_TABLE_LOOP3_20260707.md`: patch table mapping each hygiene issue to the Loop 3 definition.
- `COMPOSITION_LEMMA_LOOP3_20260707.md`: typed proof of `Delta_{beta circ alpha}=T_beta Delta_alpha+Delta_beta U_alpha`.
- `LOCAL_README_LOOP3_20260707.md`: this local orientation file.
- `ARTIFACT_MANIFEST_LOOP3_20260707.md`: artifact classification and source/evidence manifest.
- `LOOP_STATUS_LOOP3_20260707.md`: exact status line for the orchestrator.

## What Loop 3 Did

- Defined each chart `c` by `H_c`, `O_c`, declared norms, and `Phi_c:H_c->O_c`.
- Defined each edge `e:c->c'` by raw transport `U_e:H_c->H_{c'}` and object transport `T_e:O_c->O_{c'}`.
- Defined path transports `U_alpha` and `T_alpha`, including empty-path identities.
- Defined `Delta_alpha=T_alpha Phi_{c_0}-Phi_{c_k}U_alpha:H_{c_0}->O_{c_k}`.
- Defined restriction and norm conventions for `Delta_alpha|_S:S->O_{c_k}`.
- Proved the finite linear-algebra composition lemma and marked it for Pro A review.

## What Loop 3 Did Not Do

- No experiment was started.
- No empirical-positive MaoField claim was made.
- No black-box mechanism was solved.
- No dynamic-collapse theory was stated.
- No observed transport, holonomy, gluing, residual, or collapse field was asserted.
- No NMI-ready or paper-ready status was asserted.
- No broad ANOVA, sheaf, contextuality, dependent-input, or general projection theory was introduced.

## Loop 4 Prompt Summary

Use Loop 0 and Loop 3 only. Define a cycle `gamma:c_0->...->c_0`, then define `U_gamma`, `T_gamma`, `Delta_gamma`, `CID_gamma(S)`, iterated defects `Delta_{gamma,n}=T_gamma^n Phi_{c_0}-Phi_{c_0}U_gamma^n`, and `CIC_N(gamma,S)`. Prove the telescoping identity from the Loop 3 composition lemma, state that `Delta_gamma=0` implies all iterated defects vanish, and give only finite-horizon norm bounds with explicit hypotheses on `||T_gamma||`, `||U_gamma||`, and any control of `U_gamma^j(S)`.

Loop 4 must not turn cycle defect into model-collapse theory, empirical evidence, or black-box mechanism explanation.
