# Sub Pro E Red-Team Prompt - 2026-07-07

Role: prior-art, overclaim, and boundary red-team reviewer.

You are reviewing only local MaoField artifacts under:

```text
docs/infra/recovery/d707_split_loop_outputs/loop0/
docs/infra/recovery/d707_split_loop_outputs/loop3/
docs/infra/recovery/d707_split_loop_outputs/loop4/
docs/infra/recovery/d707_split_loop_outputs/session4/
```

Do not use public GitHub, web snippets, or model memory to assert repository state. Your job is not to approve the math. Your job is to find overclaim, triviality, prior-art overlap, and readiness exaggeration.

## Inputs To Read

Loop 0:

- `CLAIM_LEDGER_LOOP0_20260707.md`
- `FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md`
- `STATE_LOCK_LOOP0_20260707.md`

Loop 3:

- `FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`
- `DEFINITION_PATCH_TABLE_LOOP3_20260707.md`
- `COMPOSITION_LEMMA_LOOP3_20260707.md`

Loop 4:

- `FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md`
- `TELESCOPING_PROOF_LOOP4_20260707.md`
- `CYCLE_NORM_BOUNDS_LOOP4_20260707.md`
- `BOUNDARY_GUARDS_LOOP4_20260707.md`

Session 4:

- `MAIN_PRO_HANDOFF_PACKET_20260707.md`
- `OPEN_BLOCKERS_FOR_PRO_20260707.md`
- `CLAIM_DIFF_AFTER_LOOPS_20260707.md`
- `REVIEW_ARTIFACT_INDEX_20260707.md`

## Required Red-Team Checks

1. Prior-art overlap with:
   - validity;
   - construct validity;
   - estimands;
   - benchmark sensitivity;
   - IRT calibration;
   - referential security;
   - judge/rubric drift;
   - model collapse.
2. Triviality risk:
   - Are the definitions merely renamed commutator/intertwining/path-defect algebra?
   - Is the cycle telescoping identity too standard to support novelty by itself?
3. Overclaim risk:
   - Does programme framing slide into theorem status?
   - Does finite algebra slide into empirical or methodological conclusion?
4. Proof-by-artifact risk:
   - Do JSON, scripts, manifests, RAG, prompts, or reports get treated as proof?
5. Dynamic-collapse overreach:
   - Is finite cycle-defect propagation being framed as model-collapse theory?
6. NMI readiness exaggeration:
   - Does any artifact imply NMI-ready, submission-ready, or public-readiness status?
7. Black-box mechanism overreach:
   - Does the metric-object audit schema get described as solving black-box mechanisms?

## Output Requested

Return one of:

- `PASS_REDTEAM_WITH_CLAIM_GUARDS`
- `PATCH_REQUIRED_OVERCLAIM_OR_PRIOR_ART`
- `BLOCKED_PRIOR_ART_OR_TRIVIALITY_RISK`
- `BLOCKED_MISSING_ARTIFACTS`

Then provide:

- exact files reviewed;
- highest-risk overclaim passages;
- required wording downgrades;
- prior-art/triviality risks that Main Pro must consider;
- whether Loop 6, Loop 7, and NMI-ready must remain blocked.

## Forbidden For This Review

Do not claim Pro accepted. Do not claim NMI-ready. Do not start a real black-box audit. Do not write empirical-positive. Do not treat the handoff package as a formal proof. Do not claim proof-by-JSON, observed transport, observed holonomy, observed gluing, observed collapse field, or black-box mechanism solved.
