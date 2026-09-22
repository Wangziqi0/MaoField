# Fresh mathematical proof audit

## Verdict

**WARN — the exact finite separation, compact local repair, source-relative `hclose` closure, and recorded successor-program identities survive this review. No FATAL or CRITICAL issue was found. The audit is not a clean proof PASS because the general finite-horizon sufficient-state proposition omits matching assumptions needed by its induction, and the asymptotic statements do not explicitly declare their fixed-parameter/uniformity scope.**

- Proof-checker acceptance gate: **NOT MET**.
  - Zero open FATAL/CRITICAL issues: **yes**.
  - Every theorem has fully explicit hypotheses: **no** (PA-01).
  - Every `O(...)` statement declares parameter dependence/uniformity: **no** (PA-02).
  - Counterexample pass executed on every key lemma: **yes**.
- Review independence: **same-family**.
- Acceptance status: **provisional**.
- Reviewer route: this task's fresh Codex reviewer. The explicit task prohibition on further agents superseded the skill's normal additional-agent round.
- Manuscript/source edits: **none**.
- New experiment/model/API calls: **none**.
- Fresh Lean/kernel certification: **not run**; Lean and Lake were absent from the review environment.

The one material mathematical repair is small and does not require new evidence: strengthen the sufficient-state proposition so the two compared systems share the same exogenous-input mechanism, initial visible history (or a policy whose history dependence factors through the compact record), and common measurable joint kernels. The finite two-state theorem and the explicit state-aware correction do not depend on that proposition.

## Declared inputs and actual hashes

All paths are absolute because the reviewed inputs lie outside the audit directory.

| Input | SHA-256 |
|---|---|
| `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SUBMISSION/manuscript.md` | `1284d72b97dada6188e7e205c64e6f1b0dd9cd9351a007356c996b696f899d09` |
| `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SUBMISSION/supplementary_information.md` | `7b0cfd72c8148c5430606c98f8a98815abfa6d56b4a8f82663d73e220860471a` |
| `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/REPRODUCIBILITY/math/exact_checks.py` | `5486235af62d3aa957b4ff24cea0094a92c8959b1a12376bb6856bdc19a4f3e5` |
| `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/REPRODUCIBILITY/experiment/math_checks.py` | `d99412666de87244c8680cd55cd6bc4765f3fc978bcd0a20d285e79d2977a0d4` |
| `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/history/workspace/NavierStokes/PrimaryCovarianceBounds.lean` | `e4fd1e46d1ff6b09da37b0eb453151c75454b0df5fbbd342380a178135767a73` |
| `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/history/public/Checkpoint/NodeGoal.lean` | `571a45c575a39523475c96b3789d331ba2c07a0c80e8fb477790a5d6e1b299d7` |
| successor input catalog `.../successor/inputs/catalog.json` | `aa054ae57ff3c59395001fc28c7165617fd850c82ddc956c0f14c1fc039a9cc6` |
| successor plan A `.../successor/inputs/A/PLAN.json` | `37640ffcd45fa52d9b662b15ad74cc1448e9ec3aeba9e968a8681cc4a87ad9ad` |
| successor plan B `.../successor/inputs/B/PLAN.json` | `e95bc67c00781013bbfc8130ba4a1289b7e11ad2da88657eafa3a304a21d6199` |
| canonical successor-directory tree manifest (419 files) | `0ca88ee8ce9c8ae494c2678c6c1adbe65d76169629d018235bfda24e28996e0b` |

The tree digest is SHA-256 over newline-delimited records

`<file_sha256><two spaces><relative_path>\n`

sorted bytewise by relative path and including `catalog.json`. The catalog contains 418 declared payload entries; all 418 current file hashes equal their catalog values. The only file outside its own payload list is `catalog.json`, as expected.

## Issue ledger

### PA-01 — finite-horizon sufficiency lacks the matching assumptions used by the induction

- Severity: **MAJOR**
- Proof status: **UNDERSTATED**
- Impact: **GLOBAL** for the general compact-inheritance proposition; it does **not** affect the finite minimax witness or explicit local repair.
- Category: **HIDDEN_ASSUMPTION / QUANTIFIER_ERROR / LOGICAL_GAP**
- Location: `manuscript.md:L81`; `supplementary_information.md:L129-L139`, especially `L135-L137`.
- Claimed statement: equal initial compact states imply the same joint finite-horizon law under the three listed factorisation/update/policy conditions.
- Why the proof does not follow literally: the first proof sentence says condition (iii) gives equal action laws. Condition (iii) only says the policy agrees when supplied the same compact state **and observed history**, while the theorem assumes equality only of the compact state. It also quantifies “for each ... future input” but never requires the two systems to receive the same future input or the same future-input kernel. Finally, “law” and conditional update are used without declaring a common joint measurable kernel.
- Algebraically verified counterexample: **YES**.
  1. Let `C(x)=0`, use one fixed action, and set the next observation equal to the exogenous input. For each fixed input, the observation law is independent of hidden `x`; the compact update is constant; the policy is identical. Give system A future input `0` and system B future input `1`. Equal initial `C` does not give equal observation laws.
  2. Let `C(x)=0` and let the common policy choose the last bit of the visible pre-horizon history. Start the systems with histories ending in `0` and `1`. Condition (iii) is true for equal supplied histories, but equal `C` alone does not make the first action laws equal.
- Downstream effect: the broad standard sufficient-state composition claim is not fully stated. The explicit `(r,u)` repair remains valid, so the paper still has a concrete compact sufficient case.
- Minimal fix strategy: **STRENGTHEN_ASSUMPTION**.
- Exact minimal prose fix:

  > Fix a common measurable exogenous-input kernel and common joint action, observation-cost and compact-state update kernels for the compared systems. Assume that the systems begin with the same compact state and the same policy-visible history (or that all policy dependence on prior history factors through the compact state). Conditional on every shared compact state, visible history and input, these kernels are identical. Then the two systems have the same joint law of inputs, actions, observations, costs and compact successor states at every fixed finite horizon.

  The induction should then condition on the full shared finite history and apply the common joint kernel at each step. A finite/discrete formulation is enough if the paper does not want to introduce measurable-space notation.

### PA-02 — asymptotic `O(...)` terms omit the limit and constant-dependence declaration

- Severity: **MINOR**
- Proof status: **UNCLEAR**
- Impact: **LOCAL**
- Category: **NONUNIFORM_CONVERGENCE / CONSTANT_DEPENDENCE_HIDDEN**
- Location: `supplementary_information.md:L81-L83`, `L107-L109`, `L631-L639`; corresponding prose at `manuscript.md:L95`.
- Claimed statements: the one-variable obstruction and the three P07 residual orders.
- Audit result: exact symbolic expansion confirms every displayed coefficient and order. No false series coefficient was found. The text does not say explicitly that `tau -> 0` with fixed `a,b` and fixed chosen coefficient functions/cutoffs, and it states no uniformity over a function class or unbounded `a,b`.
- Counterexample: **NO within the intended fixed-data reading**. If uniformity over arbitrary `a,b` or arbitrary smooth `B,C` were inferred, it would be unsupported.
- Downstream effect: none after the intended pointwise reading; this is a quantifier/constant bookkeeping defect.
- Minimal fix strategy: **STRENGTHEN_ASSUMPTION**.
- Exact minimal prose fix before the first such expansion and again or by cross-reference in Note 9:

  > All asymptotic statements in this note are as `tau -> 0` for fixed real coefficients `a,b` and the displayed fixed coefficient functions and cutoffs. The implied constants may depend on these fixed data; no uniformity over `a,b` or over a class of programs is claimed.

### PA-03 — the ancillary basis-rescaling invariance leaves its action map implicit

- Severity: **MINOR**
- Proof status: **UNCLEAR**
- Impact: **LOCAL**
- Category: **MISSING_DERIVATION / MISSING_DEFINITION**
- Location: `supplementary_information.md:L119-L123`; deterministic matrix check at `exact_checks.py:L35-L37`.
- Claimed statement: a compatible positive slow rescaling leaves the represented physical action unchanged.
- Audit result: the displayed transformations prove `d'/y'=d/y` and `H' y'=H y`. The phrase “with the corresponding amplitude transformation” does not define that transformation or the represented action, so the remaining invariance cannot be restated as a complete theorem from this text alone.
- Counterexample: **CANDIDATE OUTSIDE THE INTENDED CONDITION**. Rescaling the basis without inversely rescaling its amplitude changes the represented field. The manuscript already signals that a corresponding transformation is required; it should display it.
- Downstream effect: none; no main theorem uses this paragraph.
- Minimal fix strategy: **ADD_DERIVATION**.
- Exact minimal fix:

  > If the represented component is `a_i b_i`, set `a_i'=a_i/lambda_i` together with `b_i'=lambda_i b_i`. Then `a_i'b_i'=a_i b_i`; with `y_i=a_i²`, the displayed `y_i'=y_i/lambda_i²` gives `H'y'=Hy` and `d_i'/y_i'=d_i/y_i`. State `lambda_i>0` and the exact slow-multiplier/inverse-derivative bounds used by the source extension.

### PA-04 — one symbolic quantity in the HClose deterministic harness is computed but never asserted

- Severity: **MINOR**
- Proof status: **UNCLEAR (HARNESS COVERAGE ONLY)**
- Impact: **COSMETIC** for the mathematical claim
- Category: **UNPROVEN_SUBCLAIM IN CHECK CODE**
- Location: `math_checks.py:L10-L14`.
- Observation: `positive_case` is computed at line 11 but not asserted or returned. The universal scalar inequality is nevertheless proved correctly in the manuscript at `supplementary_information.md:L181-L189` and in the accepted semantic chain at `L423-L435`; 36 rational edge cases also pass.
- Counterexample: **NO**; the inequality is valid under `D>=0` and `R>0`.
- Downstream effect: none on the proof; only the executable check's transparency.
- Minimal fix strategy: **ADD_DERIVATION/CHECK**.
- Exact minimal code change (not applied): add `assert sp.simplify(positive_case) == 0` after line 11, or remove the unused variable and state that only the negative-`c` symbolic difference is being checked.

## Verified mathematical chains

### 1. Exact finite separation

The definitions and identity at `manuscript.md:L39-L43` are exact. With the two states at `L47-L50`,

`max(|E_+|,|E_-|)=|g²+2g-r|+2v|g|`.

The proof in `supplementary_information.md:L57-L71` partitions all of `R`:

1. On `g>=0`, the function strictly decreases to `g0=sqrt(1+r)-1` and strictly increases afterwards.
2. On `[-2,0]`, it is at least `r=g0(g0+2)>2vg0`.
3. On `g<=-2`, the substitution `h=-g-2` gives `F(g)=F(h)+4v`.

The minimum is therefore attained at `g0` and equals `2vg0>0`. The restrictions `r>0` and `v>0` are necessary: the separation collapses at either boundary. The upper bounds are sufficient for the comparison; the paper does not claim they are sharp.

### 2. Compact exact repair and domain safety

At the worst outer corner `r=-1/2,u=-1/4`, `z=3/4`, `z²+r=1/16`, `w=1/4`, and `w+z=1`. Hence all denominators in `B_*` and `C_*` stay non-zero on a neighbourhood of the closed outer rectangle. The two rationalisations in `supplementary_information.md:L97-L101` give exactly

`r/2+r²B_*+urC_* = w-z`.

Thus `z+g=w` and `E=0` wherever the cutoff equals one. The formula remains well-defined at `r=0` and `u=0`. The statement correctly limits exactness to the inner rectangle and does not infer global PDE admissibility or norm improvement (`manuscript.md:L75-L77`; `supplementary_information.md:L113-L117`).

### 3. Source-relative `hclose` proof

The formal target in `NodeGoal.lean:L10-L29` selects `N,detGap,entryBound,inverseLower` before `n,p,P,zeta`, matching the manuscript's uniformity description. The two actual source lemmas are present at `PrimaryCovarianceBounds.lean:L173-L175` and `L321-L333`.

The successful body at `supplementary_information.md:L417-L435` performs both required transports:

- it rewrites membership from `[0,R_n²]` to `[0,L_n]`;
- after applying the supplied ratio hypothesis, it rewrites the entire dependent inequality back to `R_n²`.

It then applies the source integral lemma and uses `d>=0`, `c<=|c|`, and `R_n>0` to reach `Q/R_n<=rho`. The `Q=0` case is retained because the proof never divides by `Q`. The immediate line `hmargin ... hclose` at `supplementary_information.md:L297-L299` is a genuine source-level consumer; `column_scale_bounds` at `PrimaryCovarianceBounds.lean:L99-L140` supplies the remaining zero-order bounds.

No `sorry`, `admit`, locally declared `axiom`, `unsafe`, or `partial` token appears in the two supplied Lean files. This is a semantic/source audit, not a fresh kernel run. The manuscript itself makes only the narrower claim of retained compilation acceptance and explicitly denies new kernel certification (`manuscript.md:L201-L205`), so the absence of a local toolchain is a verification limitation rather than a contradiction.

### 4. Recorded successor formulas

The P00 program is directly present in `I/A/stages/P00_s0_W1/artifact.json:L3-L10`. Exact simplification confirms both:

- the draft `C1=-1/[s(1+s)]` gives `E=-u²r/(1+r)`;
- the final secant expression gives `urC2=w-s-u`, hence `g=w-(1+u)` and exact core residual zero.

The next duty's parent snapshot carries the same program hash and exact expression (`I/A/stages/P00_s0_W2/parent_snapshot.json:L2-L18`), and its artifact retains the program (`artifact.json:L3-L10`). At the displayed coordinate, the initial, draft and final rows share the same `r,u,target,z_before` but have residuals about `1.501127e-6`, `-1.168041e-8`, and `1.811136e-71`, respectively (`initial.json:L603-L625`, `draft.json:L603-L625`, `effect.json:L603-L625`). The final pure and cross terms are equal and opposite to saved precision; the manuscript correctly calls the tiny remainder roundoff rather than a mathematical non-zero effect.

For P07, the three programs are present in `P07_W0/artifact.json:L3-L10`, `P07_W1/artifact.json:L3-L10`, and `P07_s0_W2/artifact.json:L3-L10`. Fresh exact expansion gives:

`E_C0 = -a²b tau^5 - (3/4)ab² tau^7 + (1/4)a²b² tau^8 - (1/8)b³ tau^9`,

`E_C1 = a³b tau^6 - (3/4)ab² tau^7 + (3/4)a²b² tau^8 + ...`,

`E_C2 = -(a^4b+3ab²/4)tau^7 + (3/4)a²b² tau^8 + ...`.

These imply exactly the three displayed orders in `supplementary_information.md:L631-L637`. The saved source response says the leading `ur²` sign is positive, while the actual expansion is negative; the manuscript explicitly preserves and corrects this distinction at `L639-L641`.

## Deterministic checks versus semantic proof judgement

### Deterministic checks executed in this audit

- `exact_checks.py` ran with SymPy 1.14.0: **14/14 identities passed**, 0 failed. The script itself says the written piecewise argument supplies the global minimax proof (`exact_checks.py:L1-L3`, `L38`).
- `math_checks.py`: **36 rational scalar cases and 3 symbolic matrix identities passed**. This is not a Lean run (`math_checks.py:L1-L3`, `L29-L34`).
- Fresh independent symbolic simplification returned exact zero for:
  - the state-aware root correction;
  - its complete residual;
  - the P00 draft residual identity;
  - the P00 final secant increment and residual;
  - all displayed P07 leading coefficients.
- Successor input integrity:
  - 419 files total; catalog 418 payloads; **0 hash mismatches**;
  - 52 stage artifacts, 104 response records, 52 effect files;
  - all 104 response records have `finish_reason=stop`;
  - 47 captured programs and 5 `EMPTY_RESPONSE` artifacts;
  - every effect file has 360 rows, totalling **18,720**;
  - 40 local parent-state arrays match their predecessor `z_after` strings exactly, with 0 parent hash or program-metadata mismatches;
  - 7 of 8 adoption `W0/W1` program pairs are bytewise expression-equal; P07 is the sole changed pair;
  - all artifact `terminal_sha256` values match the actual terminal files.
- Recomputed stored-row arithmetic across all 18,720 effect rows agrees within the saved decimal precision. The largest observed discrepancies were approximately `5.76e-67` for `z_after-(z_before+increment)`, `7.82e-62` for `residual-(z_after²-target)`, and `1.63e-61` for `residual-(pure+cross)`.

### What these checks do not decide

The scripts and stored-row arithmetic do not prove the all-real minimax result, smooth global gluing, stochastic sufficient-state proposition, imported Lean theorem semantics, kernel acceptance, full PDE construction, or any causal history effect. Those were judged from the written arguments and exact source declarations. Conversely, the semantic proof review does not certify that a historical compiler log was produced; the manuscript carefully limits that empirical assertion to the retained record.

## Counterexample red-team log

| Target | Adversarial construction | Result |
|---|---|---|
| ALG-2/3 | `r=0` | shared `g=0` is exact; outside the hypothesis and shows `r>0` is necessary |
| ALG-2/3 | `v=0` | two states coincide; outside the hypothesis and shows `v>0` is necessary |
| ALG-3 | all negative `g`, including `[-2,0]` and reflection past `-2` | no smaller value; fully covered by the proof |
| ALG-5 | worst radicand corner `(-1/2,-1/4)` | radicand `1/16`; no singularity |
| ALG-5/SUCC-2 | `r=0` and `u=0` separately | exact identity extends; no hidden division by either variable |
| ALG-5 | use the source-only root at `z=0.9,r=0.2` | complete residual magnitude increases from `0.01` under `g=r/2` to about `0.01909`; this is the manuscript's preserved counterexample and supports its no-global-improvement boundary (`S:L113-L117`) |
| LEAN-4 | `c<0` | numerator comparison still holds because `d>=0` |
| LEAN-4 | `Q=0` | no failure and no `0/0`; only positive `R_n` is a divisor |
| LEAN-5 | `zeta=0` | weight lower bound becomes zero; no strict positivity is overclaimed |
| STATE-1 | different exogenous input laws with equal `C` | **counterexample found** to the literal statement (PA-01) |
| STATE-1 | different policy-visible initial histories with equal `C` | **counterexample found** to the literal statement (PA-01) |
| SUCC-3 | `a=0`, `b=0`, or coefficient cancellation | leading order can rise; the paper already says “generally” and notes vanishing coefficients |
| REP-1 | rescale basis but not amplitude | represented action changes; outside intended “corresponding transformation” but exposes PA-03's missing definition |

## Exact action list before submission

1. Add the common-input/common-kernel/equal-visible-history clause in PA-01 and adjust the one-sentence proof to condition on the full shared finite history.
2. Add the fixed-data `tau -> 0` and non-uniformity sentence in PA-02.
3. Display the inverse amplitude transformation in the ancillary rescaling paragraph, or delete the “represented action is unchanged” sentence if that claim is unnecessary.
4. Add the unused `positive_case` assertion in `math_checks.py` for transparent executable coverage.
5. If independent formal acceptance is desired, run the supplied candidate in the pinned Lean 4.34.0-rc2 dependency environment and retain the new kernel receipt. This is verification of an existing claim, not a new scientific experiment. Until then, keep the manuscript's current “retained compilation / no new kernel certification” boundary unchanged.

No further research round, external review call, manuscript edit, or publication action is authorised or implied by this list.

