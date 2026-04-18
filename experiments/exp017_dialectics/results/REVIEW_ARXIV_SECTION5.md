# Review — arXiv v1 Section 5 (Roadmap)

**Reviewer**: independent paper-review subagent
**Date**: 2026-04-14
**Scope**: `arxiv_v1_section5_DRAFT.md` (OP1 falsification / OP2 three-fold refinement / Block V Phase A program / three-stage publication plan)
**Cross-references consulted**: §3 DRAFT, §4 (Linux), `BLOCK_V_DESIGN.md` v2, `block4_5/a1_4/VERDICT.md`, `open_problems_followup.md`, `REVIEW_BLOCK_V_PHASE_A.md`
**Verdict**: **release-ready after P1 fixes (2 items) and P2 polish (3 items)**. No P0 blockers. §5 is the most honest section of the draft — consistent with all upstream docs and with the earlier Block V review.

---

## 0. TL;DR

§5 executes the hardest job in the paper — stating OP1 and OP2 as explicitly unresolved while still giving the reader a credible forward program — and does so without the two classical failure modes (over-claiming "framework-in-progress" as "framework-validated", or under-claiming results by hiding the program). The OP1 falsification (§5.1) is tight. The OP2 three-axis reframing (§5.2) is faithful to `VERDICT.md`. The Block V Phase A writeup (§5.3) correctly inherits the v2 fixes from `REVIEW_BLOCK_V_PHASE_A.md`. The publication plan (§5.5) and status note (§5.6) are honest.

Two P1 items need fixing; three P2 items improve signal. Nothing blocks submission.

---

## 1. OP1 Falsification (§5.1) — PASS with one P2

**Argument**. `T_ψ(λS) = T_ψ(S)` for `λ>0` ⇒ contraction coefficient between any two points on a ray is 0, while their distance is not; so Banach contraction in `ℂ^N` trivially fails. The descended map on `ℂP^{N-1}` in Fubini-Study metric is flagged as **open**, with Appendix A.4 of `open_problems_followup.md` providing linear-convergence-rate *evidence* but not a Lipschitz estimate.

**Consistency**. `open_problems_followup.md` §A.3–A.5 proves `T_ψ^n(S^{(0)}) → [e_{k*}]` at rate `(|ψ_{k2}|/|ψ_{k*}|)^{2n}` on `ℂP^{N-1}`, and crucially notes this limit is **degenerate (one-hot)**, which "fails to capture the refinement intent of Axiom 6." §5.1 does not mention this degeneracy.

### P2-1 — Disclose the one-hot degeneracy of the projective limit

Currently §5.1 says the `ℂP^{N-1}` reformulation is "meaningful" and "contraction-like behavior" is consistent with observation. This is accurate but incomplete: `open_problems_followup.md` has already established that *even if* contraction holds on `ℂP^{N-1}`, the fixed point is a one-hot concentration — **physically unsatisfactory** as an Axiom-6 formalization. §5.1 should add one sentence:

> "Moreover, Appendix A (cf. `open_problems_followup.md`) shows the projective limit is a one-hot concentration on the dominant eigenvector of `conj(ψ_q) · ψ_d`, which does not capture Axiom 6's 'refinement' intent; hence even a successful Fubini-Study contraction proof would not close OP1 — it would only clarify why M2 is the wrong candidate."

This strengthens rather than weakens the honesty claim in §5.6.

**P0/P1/P2 classification**: P2 (polish, not correctness).

---

## 2. OP2 Three-Fold Co-Design (§5.2) — PASS with one P1

**Structure**. §5.2.1 (pre-A1.4), §5.2.2 (three axes a/b/c), §5.2.3 (coupling table), §5.2.4 (connection to §2.3.3).

### §5.2.2 axes — all three align with `VERDICT.md` §3

| Axis | §5.2.2 claim | VERDICT §3 anchor |
|---|---|---|
| (a) source statistics | `⟨Sb⟩` `t=-17.1, p<10⁻²⁵`; σ=0 gives 66% u=2 | VERDICT §3.1, §2.3 |
| (b) potential geometry | `u⁵` tail vs `σ√dt=0.112` noise step | VERDICT §3.2 |
| (c) numerical scheme | `J≈1.5×10⁵` at λ=10, dt=0.05 violates CFL by 750× | VERDICT §3.3 |

Numerical claim **"750× violation"** in §5.2.2 (c) needs a cross-check: VERDICT §3.3 states `~380× (λ=1) / ~3800× (λ=10)`. §5 reports "750×" without specifying λ. If "750×" refers to average or a geometric mean, it should be disambiguated.

### P1-1 — Disambiguate CFL violation factor in §5.2.2 (c)

Replace the bare `750×` with one of:
- "≈380× at λ=1, ≈3800× at λ=10 (VERDICT §3.3)", or
- "≈750× at the wall stiffness used in A1.4 walled experiments" (if that is the intended reference value)

This is a numerical-traceability fix, not a narrative issue. **P1** (inconsistency with cited source).

### §5.2.3 coupling — rigorous enough

The table "fix attempted → why still fails" is **not rhetorical**: each row corresponds to a concrete axis-held-fixed calculation in VERDICT §3.4. The argument is rigorous modulo the framing "proven by elimination" (VERDICT §3.4), which is *itself* an inference rather than a constructive proof that no single-axis fix exists. §5.2.3 inherits this epistemic status correctly — it says "fixing any axis in isolation does not restore equilibrium" grounded in the three configurations actually tested in A1.4, not in a mathematical theorem of impossibility.

**Recommend**: keep current wording; optionally add a one-line footnote: "'Not independent' here is an empirical claim at the A1.4 configuration; axis decoupling under other parameter regimes is not excluded." This is P3 (optional).

### §5.2.4 three-faces convergence

Same `P ∘ T_•` / Giry-monad lift appears in §2.3.3. §5.2.4 does add value: it maps the categorical conjecture onto the three empirical axes, which §2.3.3 does not. The framing "most coherent organizing conjecture currently visible" is appropriately hedged. No redundancy concern; the two subsections serve different argumentative purposes (§2.3.3 introduces the categorical object, §5.2.4 uses it to unify the experimental program).

---

## 3. Block V Phase A Program (§5.3) — PASS, propagation of Phase A review fixes verified

### Sub-block structure vs `BLOCK_V_DESIGN.md` v2 + `REVIEW_BLOCK_V_PHASE_A.md`

| Phase A sub-block | §5.3 coverage | v2 design | Review fix propagated? |
|---|---|---|---|
| A-0 reachability pre-check | ✓ Kramers + MC pre-flight | BLOCK_V §4.5.0 | ✓ (new in v2, review fix #3) |
| A-1 source stats | ✓ mean-subtract + Hodge + whitening | §4.5.1 | ✓ (success criterion now quantitative, review fix #4) |
| A-2 potential geometry | ✓ a=additive quartic, b=Z_n angular, c=piecewise | §4.5.2 | ✓ (additive form, review fix #1) |
| A-3 numerical scheme | ✓ IMEX 2×2 Jacobian + Skorokhod projection | §4.5.3 | ✓ (IMEX Jacobian + Skorokhod, review fixes #2, #5) |
| A-joint | ✓ confirmatory (1 config), A-grid fallback | §4.5.4 | ✓ (review fix #6) |

**All six review fixes propagate to §5.3.** This is evidence of careful editorial handoff.

### One inconsistency in A-2 sub-experiments

§5.3 A-2 lists **three** sub-experiments: **A-2.a (deeper polynomial tail)**, **A-2.b (Z_n angular)**, **A-2.c (piecewise/non-polynomial)**. BLOCK_V_DESIGN.md v2 §4.5.2 after review deleted A-2.c and moved its reflecting-BC content to **A-3.c (Skorokhod)**. §5.3's A-2.c is therefore a leftover reference.

### P1-2 — Reconcile §5.3 A-2 with BLOCK_V_DESIGN v2

Either:
- **(preferred)** Delete A-2.c from §5.3 and state "a reflecting-BC alternative is treated in A-3.c as a numerical scheme, see `BLOCK_V_DESIGN.md` v2 §4.5.3", matching v2's structure; or
- **(alternative)** Keep A-2.c but explicitly note "A-2.c overlaps with A-3.c; final implementation folds reflecting-BC into A-3".

Current §5.3 wording creates a concept duplication that the earlier Block V review explicitly flagged (review blocker #7). **P1** because this is exactly the error review #7 corrected downstream.

### A-joint outcomes (§5.3 last subsection) — no strawman

Three outcomes listed: full success → OP2 solvable in gradient-flow regime; partial success → two of three basins; full failure → Phase B mandatory. **None is a strawman**:
- "Full success" is plausible (axes are addressable in principle; the issue is joint calibration)
- "Partial" is the most likely outcome given A1.4's residual uncertainty about detailed-balance at small p(0)
- "Full failure" is plausible and maps onto axis-D candidates already enumerated in BLOCK_V v2 §4.5.4 (D-1/D-2/D-3/D-4)

"All three are informative" claim is honest: A-0 reachability pre-check + KL success gate means every outcome produces a decomposable verdict.

---

## 4. Phase B and C Outlook (§5.4) — PASS

**Scope**: B-H / B-A / B-N (directed non-equilibrium), C-V / C-S (dynamic V + SCAN). Scheduled 2026-Q3/Q4 internally. arXiv v1 documents Phase A only; B/C signposted as future work.

No over-claim. The 2026-Q3/Q4 timeline is **not** over-promised because (i) it appears only as "internal planning," not as a commitment in the paper's forward claims, and (ii) the Phase B gate in BLOCK_V v2 §4.5.6 is explicitly conditioned on A-joint outcome.

### P2-2 — Phase B "adds capabilities" claim

Current wording: "Phase B tests whether directed driving adds capabilities beyond Laplace equilibrium (e.g., accessing attractors not connected by gradient flow even with horizon-adequate thermal driving)." This is fine. Optional tightening: "tests whether directed driving adds reachable attractors beyond those accessible under gradient-flow + isotropic-Langevin at thermally-adequate horizon." Strictly a phrasing preference.

---

## 5. Three-Stage Publication Plan (§5.5) — PASS

**Stages**: v0.1.0 skeleton (already on Zenodo DOI 10.5281/zenodo.19550342, 2026-04-13) → v0.1.1 arXiv PDF (target 2026-04-20) → IPM mechanism paper (2026-07/08) → generalist top-tier (2027-Q1/Q2).

**Deferral justification** ("deferred to allow Block V experimental program to mature; deferral is a methodological decision, not a timeline slip") is **honestly worded**. It frames a 9-18-month gap as intentional, which is correct given that the generalist paper depends on Phase B outcome (which depends on Phase A outcome, which depends on this paper's publication catalyzing review feedback).

### P2-3 — 2026-04-20 target for v0.1.1 PDF — conservative?

v0.1.1 is the paper this review is reviewing. Current date is 2026-04-14 (6 days to target). Given §4 review has flagged at least P1 items (separately), §5's P1-1 and P1-2 fixes are trivial (~30 minutes), but aggregate PDF compilation + remaining sections + internal cross-review may need more headroom. **Not a §5 concern per se**, but flag: if 2026-04-20 slips to 2026-04-22, this should not be characterized anywhere as "delay" — it's within the normal variance of a publication workflow.

---

## 6. §5.6 Status Note — PASS, strong enough

"OP1 candidate M2 falsified; OP1 itself not solved or refuted" — correct.
"OP2 refined to three-axis co-design; not solved" — correct.
"A framework whose research program lies entirely in its open problems is not an evasion — it is the honest representation of a research stage" — this sentence is the single best line in the draft. Keep verbatim.

The self-application of Axiom 1 ("open contradictions are the engine of motion") is philosophically consistent with the framework's stated epistemology and does not cross into overclaim.

---

## 7. Cross-document consistency

| Check | §5 | §3/§4 | VERDICT | BLOCK_V v2 | Status |
|---|---|---|---|---|---|
| OP1 M2 falsification argument | §5.1 | §3.2 Ax6, §3.4 OP1 | — | — | consistent |
| Three axes A/B/C nomenclature | §5.2.2 | §4.9.3 | §3.1-3.3 | §4.5 intro | consistent |
| CFL violation factor | "750×" | "~380× / ~3800×" | "~380× / ~3800×" | "~380×" | **P1-1 inconsistency** |
| A-2 sub-experiment list | §5.3 (3 items incl. A-2.c) | — | — | v2 §4.5.2 (2 items, A-2.c removed) | **P1-2 inconsistency** |
| A-joint framing | "confirmatory, not best-of" | — | — | v2 §4.5.4 "confirmatory" | consistent |
| IMEX 2×2 Jacobian | §5.3 A-3.b (with BLOCK_V ref) | — | — | v2 §4.5.3 | consistent |
| Phase B gate | §5.4 signposted | — | — | v2 §4.5.6 | consistent |
| Three-stage plan dates | 2026-04-13/20, 2026-07-08, 2027-Q1/Q2 | — | — | — | internally consistent |

---

## 8. Summary of required changes

**P1** (before submission):
- **P1-1**: §5.2.2 (c) — disambiguate "750×" CFL violation; use VERDICT's "≈380× (λ=1) / ≈3800× (λ=10)" or explicitly state which λ the number refers to
- **P1-2**: §5.3 A-2.c — delete or note integration with A-3.c Skorokhod to match BLOCK_V v2; otherwise §5 reintroduces the concept duplication that Review #7 already corrected

**P2** (polish, nice-to-have):
- **P2-1**: §5.1 — add one sentence on one-hot degeneracy of projective limit (`open_problems_followup.md` §A.3 result) to strengthen honesty framing
- **P2-2**: §5.4 — optional tightening of "adds capabilities"
- **P2-3**: §5.5 — 2026-04-20 is tight; ensure any slip is framed as normal variance

**P3** (optional): §5.2.3 footnote about empirical vs. mathematical non-independence.

---

## 9. Bottom line

§5 is the best-calibrated section of the arXiv v1 draft so far. It does the OP-as-program framing correctly; it inherits upstream review fixes; it does not over-promise. Two small inconsistencies (CFL factor, leftover A-2.c) need reconciliation. After those, §5 is submission-ready and actively supports the paper's credibility.

*End of review.*
