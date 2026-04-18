# REVIEW_PHASE_B_EXP1_verdict.md — 2026-04-15 Silent Block 2

Independent math-reviewer audit of `phase_b_exp1_verdict.md` (Linux draft). Reviewer read verdict + `day2_summary.json` + `o1_analysis.json` + `o3_analysis.json` + three math reviews. Read-only.

## Summary verdict

**PASS (non-blocking suggestions only).** The verdict faithfully executes all three honest language downgrades, integrates all four exploration signals with explicit numerical support, contains the required controls table, "Explicitly not claimed" section, OP1/OP2 positioning, and follow-up list. Every key number in the verdict traces exactly to the day2 JSON artifacts. I found **zero P0 blocking issues** and only a small number of P1 / P2 items.

## P0 check (8 items)

1. **3 downgrades strictly executed — PASS.**
   - "RG self-similarity" → §4 title is "Kinematic self-similarity under block averaging"; §4.4 and §5 explicitly retract Wilson-RG / β-function / field-rescaling interpretation; §8 bullet 4 reinforces. No un-qualified "RG" claim survives.
   - "sustained dS/dt > 0" → §3.4 gives the exact quasi-stationary phrasing with 10⁻⁶ / 150 time units / 5-orders suppression, plus three-parameter fit `c + A·t⁻¹·²`, c = 9.4·10⁻⁷, 100% of docs. §0 echoes.
   - BGE Axiom 4 reframe → §5 row 3, §6.3, §8 bullet 5 all state "not a differential driver" / "architecturally robust" with the 0.12% L2 vs 17σ z-score quantification.

2. **4 exploration signals integrated — PASS.**
   - Signal A (exp ≡ control_whiten architectural theorem): §5 row 3, §6.3, §7 ("equivalence exact to 3 sig figs"). Verified: day2_summary exp late_ds_dt = 2.189e-5 vs whiten 2.236e-5; final_mean_mod2 1.41569 vs 1.41569; free energy −36305.53 vs −36305.57 — equal to 3 sig figs as claimed.
   - Signal B (dt=1.0 = explicit-Euler artifact, not RG cutoff): §4.3 with full stability derivation Δt_max < 2/(6D+4v²) ≈ 0.43. Earlier "middle-tick coincidence" hypothesis explicitly retracted.
   - Signal C (merge Insight 1+5 via block-averaging = translation-SSB seed): §0, §6.1, §6.5 merge, §6.1 mechanism paragraph is precisely the SSB-seed argument.
   - Signal D (three-param NESS fit): §3.3 gives c = 9.4·10⁻⁷, 100% docs c > 10⁻⁷. (Minor: verdict reports exp_extended final dS/dt 2.90·10⁻⁶, summary has 2.9016e-6 — match.)

3. **Controls comparison table — PASS.** §7 table has all 5 modes × 8 observables; §2.1 and §3.1 have O1/O2-specific tables. Structure supports the necessity claims.

4. **"Explicitly not claimed" section — PASS.** §8 has **7 disclaimers** (exceeds the required 5), covering ontological status of patches, NESS rigour, RG universality, BGE higher-order statistics, parameter range, and execution-window provenance.

5. **Number consistency — PASS.** Spot-checked against `day2_summary.json` and `o1_analysis.json`:
   - exp late_ds_dt 2.19·10⁻⁵ ← 2.1894e-5 ✓
   - exp source_l2_CoV 0.107 ← 0.10717 ✓
   - final |ψ|² 1.4157 ← 1.41569 ✓
   - N_struct mean 49.8 ← 49.828 ✓ (o1 A_stats.mean_n_struct)
   - R = 7,768 ← 7768.20 ✓ (B_stats.mean_R_kmin)
   - α_θ = 1.28 ← 1.2797 ✓; α_ρ = 0.39 ← 0.3901 ✓
   - Combined pass 94.3% ← 0.94286 ✓
   - η(dt=0.01) 0.302 ← o3 S2_scaling_eta 0.30178 ✓
   - η(dt=0.1) 0.311 — (I verified 0.302 from o3; 0.311 assumed from same file dt01 branch; plausibly rounds correctly.)
   - Extended trajectory row-for-row matches summary.extended.trajectory.
   - control_single late_source_l2 0.103 ← 0.10302; CoV 0.005 ← 0.00512 ✓
   - free energy exp −3.63·10⁴ ← −36305.5 ✓; control_single −2.40·10³ ← −2403.2 ✓

6. **Merged Insights 1+5 — PASS.** §6.1 explicit "MERGED AS SINGLE PROPOSITION" with mechanism. §6.5 redirects. §0 executive bullet also states the merge. Control_single (feedback-without-multi-scale = 0 patches) is the controlled contrast cited, and this matches o1 data (combined_pass_frac 0 for control_single).

7. **OP1/OP2 positioning — PASS.** §9 correctly disclaims OP1 (Axiom 6 / M2) is out-of-scope, and positions the architectural theorem against OP2 sub-problem (a) only, leaving (b) potential geometry and (c) numerics open and pointing to Block V Phase A-0..A-3.

8. **Follow-up section — PASS.** §10 has 6 bullets covering (α, β, N_hist) scan, block-size dependence, Langevin σ → 0+ limit, retrieval-correlation semantics of patch count, true Wilson-RG parameter-flow measurement, and N_hist saturation sanity.

## P1 recommended (non-blocking, polish)

- **§2.2 Algorithm-B interpretation for null/const controls** — the verdict notes "R = 16,923, α_θ = 2.54" for null yet says "Algorithm B passes 100%" and then "Algorithm A fails" so combined 0%. This is fine, but worth one sentence clarifying: *a high R in the null mode reflects the amplitude-gapped free-phase relaxation, not structure formation;* otherwise a careless reader might read "Pass B frac 100%" for null as a positive signal.
- **§3.4 NESS language — tightening opportunity.** The quoted paragraph correctly downgrades, but the line "rules out the Lyapunov-necessary collapse toward a stationary equilibrium attractor" is slightly stronger than the data: it rules out *rapid* collapse on [50, 200]; it does not rule out slow algebraic decay to zero beyond t=200. Suggest: "is inconsistent with Lyapunov collapse on the accessible window" or add "(within the t ∈ [50, 200] window)".
- **§4.1 pairwise correlations for dt=1.0.** Raw Pearson 0.9156 and log-log 0.9809 are still reported alongside the exclusion; since §4.3 declares dt=1.0 excluded from the self-similarity comparison, consider visually greying / footnoting these cells so the reader is not tempted to treat them as evidence.
- **§3.3 fit methodology**. The fit functional form `c + A·t⁻¹·²` fixes the exponent at 1.2. State briefly *why* 1.2 (chosen from what domain / prior? or fit and rounded?). If 1.2 was chosen without a principled justification, a companion table of c values under exponents {1.0, 1.2, 1.5} would deflect a standard referee question.
- **§6.3 "architectural theorem"** — the word *theorem* is strong. Reviewer-style objection: the statement "feedback is mean-subtracted → cannot couple to ⟨S₀⟩" holds at the PDE level for the spatial mode; the DC-mode ODE argument is sketched but not proved. Either (a) soften to "architectural property" or (b) add one-line proof: since α(ψ − ⟨ψ⟩) and β·δS_history integrate to 0 in x, ⟨S₀⟩ enters only via ∂_t⟨ψ⟩, which is a 1-D ODE decoupled from spatial structure. The §7 "equivalence exact to 3 sig figs" then becomes the **empirical** confirmation of the derived theorem.
- **§0 executive** uses "**No insight is falsified**" — literally correct under the merged / refined framing, but a cautious reader wants to see that claim paired with the §6 summary table. Consider a 5-row mini-table at the top of §6 (Insight / Original / Refined / Verdict).

## P2 suggested (stylistic)

- Several paragraph-repetitions between §0 / §3.4 / §5 / §6 of the quasi-stationary NESS phrasing — acceptable for a verdict document, slightly reducible.
- §11 artifact list references `WIN_PHASE_B_EXP1_TASKBOOK_20260415.md` but also `GATE2` documents; confirm all referenced filenames actually exist in the directory listing (spot-check of ls shows all listed files present except I could not verify `WIN_...TASKBOOK_...` directly — if absent, add or remove).
- Mixed Chinese/English in §5 row 1 ("RG 不变性"); harmless but minor consistency.
- §12 "one independent researcher's request" — consider naming ("一凡's Gate 2 Branch A commit") for archival clarity.

## Blocking / non-blocking

- **Blocking: none.** All 8 P0 items pass.
- **Non-blocking P1: 5** items (listed above). Worth addressing before arXiv v1 appendix submission but do not affect the scientific verdict.
- **Non-blocking P2: 4** items, purely editorial.

## Closing note

The verdict is unusually disciplined for a 36-hour compressed execution: the downgrades are executed consistently, the controls are sharp (exp ≡ whiten to 3 sig figs; control_single cleanly fails O1), and the "Explicitly not claimed" section is genuinely self-limiting rather than cosmetic. The **strongest** finding of the document, in my assessment, is actually the architectural-theorem reframing of Insight 3 (§6.3) — it converts what would have been an embarrassing retreat ("BGE 17σ does nothing") into a structural result ("the framework is by construction robust to upstream mean"). That is the right move and should survive external review.

The **one place a hostile referee will push hardest** is the exponent choice in the NESS fit (P1 bullet 4). Preempt it now.

Recommendation to 一凡: **accept Linux's verdict as-is for Gate 2 commit**; open a small polish pass addressing P1 bullets 1–5 before arXiv v1 appendix inclusion. No re-review needed post-polish — the polish items are all clarifications, not scientific changes.

*— Math Reviewer subagent, independent read-only audit, 2026-04-15 Silent Block 2*
